"""Seed Work Management data from legacy CSV exports."""

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, select, text
from sqlalchemy.exc import SQLAlchemyError


BACKEND_DIR = Path(
    "/home/eamadmin/eam-2.0/eam-2.1-fastapi-vue/backend"
)
CSV_DIR = Path(__file__).parent.parent / "work_mgmt"
ENTITY_DIR = BACKEND_DIR / "app/modules/work_mgmt/entities"

# Load .env from backend directory
env_file = BACKEND_DIR / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import async_session_maker, init_db
from app.core.framework.models.auth import User
from app.modules.asset_management.models.asset import Asset
from app.modules.asset_management.models.equipment import Equipment
from app.modules.asset_management.models.incident import Incident
from app.modules.asset_management.models.location import Location
from app.modules.asset_management.models.position import Position
from app.modules.core_eam.models import CostCode, Department, Labor, Site, Trade
from app.modules.purchasing_stores.models import Item, UnitOfMeasure
from app.modules.work_mgmt.models import (
    WorkOrder,
    WorkOrderActivity,
    WorkOrderActivityLogs,
    WorkOrderEquipment,
    WorkOrderLabor,
    WorkOrderLaborActualHours,
    WorkOrderParts,
)


SYSTEM_HEADERS = {
    "creation",
    "modified",
    "modified_by",
    "owner",
    "docstatus",
    "idx",
    "_user_tags",
    "_comments",
    "_assign",
    "_liked_by",
}

ENTITY_CONFIGS = [
    {"entity": "work_order", "model": WorkOrder, "csv": "tabWork Order.csv"},
    {"entity": "work_order_activity", "model": WorkOrderActivity, "csv": "tabWork Order Activity.csv"},
    {"entity": "work_order_labor", "model": WorkOrderLabor, "csv": "tabWork Order Labor.csv"},
    {"entity": "work_order_equipment", "model": WorkOrderEquipment, "csv": "tabWork Order Equipment.csv"},
    {"entity": "work_order_parts", "model": WorkOrderParts, "csv": "tabWork Order Parts.csv"},
    {"entity": "work_order_activity_logs", "model": WorkOrderActivityLogs, "csv": "tabWork Order Activity Logs.csv"},
    {"entity": "work_order_labor_actual_hours", "model": WorkOrderLaborActualHours, "csv": "tabWork Order Labor Actual Hours.csv"},
]

ENTITY_NAME_BY_TABLE = {
    config["model"].__tablename__: config["entity"]
    for config in ENTITY_CONFIGS
}

MODEL_BY_TABLE = {
    "asset": Asset,
    "bin": None,
    "category_of_failure": None,
    "core_users": User,
    "cost_code": CostCode,
    "department": Department,
    "equipment": Equipment,
    "incident": Incident,
    "item": Item,
    "labor": Labor,
    "location": Location,
    "position": Position,
    "site": Site,
    "trade": Trade,
    "unit_of_measure": UnitOfMeasure,
    "work_order": WorkOrder,
    "work_order_activity": WorkOrderActivity,
    "work_order_labor": WorkOrderLabor,
}


def load_entity_naming() -> dict[str, dict[str, Any]]:
    naming: dict[str, dict[str, Any]] = {}
    for config in ENTITY_CONFIGS:
        entity_path = ENTITY_DIR / f"{config['entity']}.json"
        with entity_path.open("r", encoding="utf-8") as handle:
            entity_definition = json.load(handle)

        pattern = entity_definition.get("naming")
        match = re.search(r"\{(#+)\}", pattern or "")
        naming[config["entity"]] = {
            "pattern": pattern,
            "prefix": pattern[: match.start()] if match else None,
            "width": len(match.group(1)) if match else None,
        }
    return naming


ENTITY_NAMING = load_entity_naming()


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None

    cleaned = value.strip().strip("\"'")
    if not cleaned or cleaned.upper() == "NULL":
        return None
    return cleaned


def parse_legacy_csv(csv_path: Path) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        headers = [header.strip() for header in handle.readline().strip().split(",")]

        for line_number, raw_line in enumerate(handle, start=2):
            stripped = raw_line.strip()
            if not stripped:
                continue

            normalized = stripped
            if normalized.startswith('"') and normalized.endswith('"'):
                normalized = f"'{normalized[1:-1]}'"

            parsed = next(csv.reader([normalized], delimiter=",", quotechar="'"))
            if len(parsed) != len(headers):
                raise ValueError(
                    f"{csv_path.name}:{line_number} expected {len(headers)} columns, got {len(parsed)}"
                )

            rows.append({header: clean_value(value) for header, value in zip(headers, parsed)})

    return rows


def normalize_identifier(value: str | None, entity: str | None) -> str | None:
    cleaned = clean_value(value)
    if not cleaned or not entity:
        return cleaned

    naming = ENTITY_NAMING.get(entity)
    if not naming:
        return cleaned

    prefix = naming.get("prefix")
    width = naming.get("width")
    if not prefix or not width:
        return cleaned

    if cleaned.startswith(prefix):
        suffix = cleaned[len(prefix):]
        if suffix.isdigit():
            return f"{prefix}{suffix.zfill(width)}"

    if cleaned.isdigit():
        return f"{prefix}{cleaned.zfill(width)}"

    return cleaned


def coerce_value(raw_value: str | None, column_type: Any):
    if raw_value is None:
        return None

    if isinstance(column_type, Boolean):
        lowered = raw_value.lower()
        if lowered in {"1", "true", "yes", "y"}:
            return True
        if lowered in {"0", "false", "no", "n"}:
            return False
        return None

    if isinstance(column_type, Integer):
        return int(float(raw_value))

    if isinstance(column_type, Float):
        return float(raw_value)

    if isinstance(column_type, DateTime):
        for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                return datetime.strptime(raw_value, fmt)
            except ValueError:
                continue
        raise ValueError(f"Unsupported datetime: {raw_value}")

    if isinstance(column_type, Date):
        for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
            try:
                return datetime.strptime(raw_value, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Unsupported date: {raw_value}")

    return raw_value


async def load_existing_ids(db, model: Any, id_cache: dict[str, set[str]]) -> set[str]:
    table_name = model.__tablename__
    if table_name not in id_cache:
        result = await db.execute(select(model.id))
        id_cache[table_name] = set(result.scalars().all())
    return id_cache[table_name]


async def load_user_lookup(db, user_cache: dict[str, str]) -> dict[str, str]:
    if user_cache:
        return user_cache

    result = await db.execute(select(User.id, User.email, User.username))
    for user_id, email, username in result.all():
        if user_id:
            user_cache[user_id] = user_id
        if email:
            user_cache[email] = user_id
        if username:
            user_cache[username] = user_id
    return user_cache


async def check_table_id_exists(db, table_name: str, candidate_id: str) -> bool:
    result = await db.execute(
        text(f"SELECT 1 FROM {table_name} WHERE id = :candidate_id LIMIT 1"),
        {"candidate_id": candidate_id},
    )
    return result.first() is not None


async def resolve_foreign_key(
    db,
    raw_value: str | None,
    column: Any,
    id_cache: dict[str, set[str]],
    user_cache: dict[str, str],
    current_table: str,
    current_id: str,
) -> tuple[str | None, bool]:
    cleaned = clean_value(raw_value)
    if cleaned is None:
        return None, False

    foreign_keys = list(column.foreign_keys)
    if not foreign_keys:
        return cleaned, False

    target_table = foreign_keys[0].column.table.name
    if target_table == "core_users":
        users = await load_user_lookup(db, user_cache)
        resolved = users.get(cleaned)
        return resolved, resolved is None

    target_entity = ENTITY_NAME_BY_TABLE.get(target_table)
    candidate = normalize_identifier(cleaned, target_entity) if target_entity else cleaned
    if target_table == current_table and candidate == current_id:
        return candidate, False

    target_model = MODEL_BY_TABLE.get(target_table)
    if target_model is not None:
        existing_ids = await load_existing_ids(db, target_model, id_cache)
        if candidate in existing_ids:
            return candidate, False
        return None, True

    try:
        if await check_table_id_exists(db, target_table, candidate):
            return candidate, False
    except SQLAlchemyError:
        pass

    return None, True


async def seed_entity(config: dict[str, Any], entity_order: int, entity_total: int) -> None:
    entity_name = config["entity"]
    model = config["model"]
    rows = parse_legacy_csv(CSV_DIR / config["csv"])
    valid_columns = {
        column.name: column
        for column in model.__table__.columns
        if column.name not in {"created_at", "updated_at"}
    }

    async with async_session_maker() as db:
        id_cache: dict[str, set[str]] = {}
        user_cache: dict[str, str] = {}
        existing_ids = await load_existing_ids(db, model, id_cache)

        seeded_count = 0
        skipped_count = 0
        failed_count = 0
        unresolved_count = 0

        for row in rows:
            record_id = normalize_identifier(row.get("name"), entity_name)
            if not record_id:
                failed_count += 1
                continue

            if record_id in existing_ids:
                skipped_count += 1
                continue

            payload = {"id": record_id}

            for header, raw_value in row.items():
                if header == "name" or header in SYSTEM_HEADERS:
                    continue

                column = valid_columns.get(header)
                if column is None:
                    continue

                try:
                    if column.foreign_keys:
                        value, unresolved = await resolve_foreign_key(
                            db,
                            raw_value,
                            column,
                            id_cache,
                            user_cache,
                            model.__tablename__,
                            record_id,
                        )
                        if unresolved:
                            unresolved_count += 1
                    else:
                        value = coerce_value(clean_value(raw_value), column.type)
                except Exception as exc:
                    print(f"{entity_name} {record_id}: could not parse {header}: {exc}")
                    value = None
                    failed_count += 1

                payload[header] = value

            try:
                async with db.begin_nested():
                    db.add(model(**payload))
                    await db.flush()
                existing_ids.add(record_id)
                seeded_count += 1
            except SQLAlchemyError as exc:
                failed_count += 1
                print(f"{entity_name} {record_id}: insert failed: {exc}")

        await db.commit()

    print(
        f"[{entity_order}/{entity_total}] {model.__name__}: "
        f"Seeded {seeded_count}, Skipped {skipped_count}, Failed {failed_count}, "
        f"Unresolved FKs nulled {unresolved_count}"
    )


async def seed_work_mgmt() -> None:
    print("Initializing database...")
    await init_db()
    print("Database initialized.")

    print("\nSeeding Work Management entities...")
    total = len(ENTITY_CONFIGS)
    for index, config in enumerate(ENTITY_CONFIGS, start=1):
        await seed_entity(config, index, total)

    print("\nWork Management seeding complete.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_work_mgmt())