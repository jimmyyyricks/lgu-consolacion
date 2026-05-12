"""Seed Core EAM data from legacy CSV exports."""

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from sqlalchemy import Boolean, Date, Float, Integer, select
from sqlalchemy.exc import SQLAlchemyError


BACKEND_DIR = Path(
    "/home/eamadmin/eam-2.0/eam-2.1-fastapi-vue/backend"
)
CSV_DIR = Path(__file__).parent.parent / "core_eam"
ENTITY_DIR = BACKEND_DIR / "app/modules/core_eam/entities"

# Load .env from backend directory
env_file = BACKEND_DIR / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import async_session_maker, init_db
from app.core.framework.models.auth import User
from app.modules.asset_management.models.location import Location
from app.modules.core_eam.models import (
    Account,
    Contractor,
    CostCode,
    Department,
    Employee,
    EmployeeSite,
    Labor,
    LaborAvailability,
    LaborAvailabilityDetails,
    LaborGroup,
    Manufacturer,
    Model,
    Organization,
    RequestActivityType,
    Site,
    Trade,
    TradeLabor,
    WorkSchedule,
    WorkScheduleDetails,
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
    {"entity": "organization", "model": Organization, "csv": "tabOrganization.csv"},
    {"entity": "manufacturer", "model": Manufacturer, "csv": "tabManufacturer.csv"},
    {"entity": "request_activity_type", "model": RequestActivityType, "csv": "tabRequest Activity Type.csv"},
    {"entity": "trade", "model": Trade, "csv": "tabTrade.csv"},
    {"entity": "account", "model": Account, "csv": "tabAccount.csv"},
    {"entity": "employee", "model": Employee, "csv": "tabEmployee.csv"},
    {"entity": "site", "model": Site, "csv": "tabSite.csv"},
    {"entity": "cost_code", "model": CostCode, "csv": "tabCost Code.csv"},
    {"entity": "department", "model": Department, "csv": "tabDepartment.csv"},
    {"entity": "employee_site", "model": EmployeeSite, "csv": "tabEmployee Site.csv"},
    {"entity": "labor", "model": Labor, "csv": "tabLabor.csv"},
    {"entity": "labor_availability", "model": LaborAvailability, "csv": "tabLabor Availability.csv"},
    {"entity": "labor_availability_details", "model": LaborAvailabilityDetails, "csv": "tabLabor Availability Details.csv"},
    {"entity": "model", "model": Model, "csv": "tabModel.csv", "aliases": {"name1": "model_name"}},
    {"entity": "trade_labor", "model": TradeLabor, "csv": "tabTrade Labor.csv"},
    {"entity": "work_schedule", "model": WorkSchedule, "csv": "tabWork Schedule.csv"},
    {"entity": "work_schedule_details", "model": WorkScheduleDetails, "csv": "tabWork Schedule Details.csv"},
]

MODEL_BY_TABLE = {
    "account": Account,
    "contractor": Contractor,
    "core_users": User,
    "cost_code": CostCode,
    "department": Department,
    "employee": Employee,
    "employee_site": EmployeeSite,
    "labor": Labor,
    "labor_availability": LaborAvailability,
    "labor_availability_details": LaborAvailabilityDetails,
    "labor_group": LaborGroup,
    "location": Location,
    "manufacturer": Manufacturer,
    "model": Model,
    "organization": Organization,
    "request_activity_type": RequestActivityType,
    "site": Site,
    "trade": Trade,
    "trade_labor": TradeLabor,
    "work_schedule": WorkSchedule,
    "work_schedule_details": WorkScheduleDetails,
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
ENTITY_BY_TABLE = {
    config["model"].__tablename__: config["entity"]
    for config in ENTITY_CONFIGS
}


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

            rows.append(
                {header: clean_value(value) for header, value in zip(headers, parsed)}
            )

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

    exact_match = re.fullmatch(rf"{re.escape(prefix)}(\d+)", cleaned)
    if exact_match:
        return f"{prefix}{exact_match.group(1).zfill(width)}"

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
        return int(raw_value)

    if isinstance(column_type, Float):
        return float(raw_value)

    if isinstance(column_type, Date):
        return datetime.strptime(raw_value, "%Y-%m-%d").date()

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


async def resolve_foreign_key(
    db,
    raw_value: str | None,
    column: Any,
    id_cache: dict[str, set[str]],
    user_cache: dict[str, str],
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
        return users.get(cleaned), users.get(cleaned) is None

    target_model = MODEL_BY_TABLE.get(target_table)
    if target_model is None:
        return cleaned, False

    target_entity = ENTITY_BY_TABLE.get(target_table)
    normalized = normalize_identifier(cleaned, target_entity)
    existing_ids = await load_existing_ids(db, target_model, id_cache)
    if normalized in existing_ids:
        return normalized, False

    return None, True


async def seed_entity(config: dict[str, Any], entity_order: int, entity_total: int) -> None:
    entity_name = config["entity"]
    model = config["model"]
    csv_path = CSV_DIR / config["csv"]
    aliases = config.get("aliases", {})
    rows = parse_legacy_csv(csv_path)
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

                field_name = aliases.get(header, header)
                column = valid_columns.get(field_name)
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
                        )
                        if unresolved:
                            unresolved_count += 1
                    else:
                        value = coerce_value(clean_value(raw_value), column.type)
                except Exception as exc:
                    print(f"{entity_name} {record_id}: could not parse {field_name}: {exc}")
                    value = None
                    failed_count += 1

                payload[field_name] = value

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


async def seed_core_eam() -> None:
    """Seed all available Core EAM entities from legacy CSV files."""
    print("Initializing database...")
    await init_db()
    print("Database initialized.")

    print("\nSeeding Core EAM entities...")
    total = len(ENTITY_CONFIGS)
    for index, config in enumerate(ENTITY_CONFIGS, start=1):
        await seed_entity(config, index, total)

    print("\nCore EAM seeding complete.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_core_eam())
