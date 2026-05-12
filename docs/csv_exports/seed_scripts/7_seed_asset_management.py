"""Seed Asset Management data from legacy CSV exports."""

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
CSV_DIR = Path(__file__).parent.parent / "asset_management"
ENTITY_DIR = BACKEND_DIR / "app/modules/asset_management/entities"

# Load .env from backend directory
env_file = BACKEND_DIR / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import async_session_maker, init_db
from app.core.framework.models.auth import User
from app.modules.asset_management.models import (
    Asset,
    AssetClass,
    AssetClassProperty,
    AssetPosition,
    AssetProperty,
    Equipment,
    Location,
    LocationType,
    Position,
    PositionRelation,
    Property,
    PropertyType,
    System,
    SystemType,
)
from app.modules.core_eam.models import Department, Employee, Model, Site
from app.modules.purchasing_stores.models import Inventory, PurchaseRequestLine, UnitOfMeasure


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
    {
        "entity": "location_type",
        "model": LocationType,
        "csv": "tabLocation Type.csv",
        "aliases": {"location_type_name": "name"},
    },
    {
        "entity": "system_type",
        "model": SystemType,
        "csv": "tabSystem Type.csv",
        "aliases": {"system_type_name": "name"},
    },
    {
        "entity": "property_type",
        "model": PropertyType,
        "csv": "tabProperty Type.csv",
        "aliases": {"property_type_name": "name"},
    },
    {
        "entity": "asset_class",
        "model": AssetClass,
        "csv": "tabAsset Class.csv",
        "aliases": {"class_name": "name", "parent_asset_class_id": "parent_asset_class"},
        "skip_headers": {"manual", "available_capacity", "equipment", "is_asset_item", "available_equip_capacity"},
    },
    {
        "entity": "location",
        "model": Location,
        "csv": "tabLocation.csv",
        "aliases": {"name1": "name"},
        "skip_headers": {"store", "lft", "rgt", "is_group", "old_parent"},
    },
    {
        "entity": "property",
        "model": Property,
        "csv": "tabProperty.csv",
        "aliases": {"property_name": "name"},
        "skip_headers": {"unit_of_measure_name", "property_type_name"},
    },
    {
        "entity": "system",
        "model": System,
        "csv": "tabSystem.csv",
        "aliases": {"name1": "name", "parent_system_id": "parent_system"},
        "skip_headers": {"system_type_name"},
    },
    {
        "entity": "asset_class_property",
        "model": AssetClassProperty,
        "csv": "tabAsset Class Property.csv",
        "skip_headers": {"asset_class_name", "property_name", "uom_short_name", "property_type"},
    },
    {
        "entity": "position",
        "model": Position,
        "csv": "tabPosition.csv",
        "aliases": {"current_asset_id": "current_asset"},
        "skip_headers": {"asset_class_name", "location_name", "system_name"},
    },
    {
        "entity": "asset",
        "model": Asset,
        "csv": "tabAsset.csv",
        "skip_headers": {"manufacturer", "manufacturer_name", "manual", "asset_class_name"},
    },
    {
        "entity": "equipment",
        "model": Equipment,
        "csv": "tabEquipment.csv",
        "skip_headers": {"asset", "asset_description", "item_description", "equipment_group_name", "location_name"},
    },
    {
        "entity": "asset_position",
        "model": AssetPosition,
        "csv": "tabAsset Position.csv",
        "skip_headers": {"position_name", "asset_name"},
    },
    {
        "entity": "asset_property",
        "model": AssetProperty,
        "csv": "tabAsset Property.csv",
        "skip_headers": {"asset_name", "property_name", "uom_short_name"},
    },
    {
        "entity": "position_relation",
        "model": PositionRelation,
        "csv": "tabPosition Relation.csv",
    },
]

ENTITY_NAME_BY_TABLE = {
    config["model"].__tablename__: config["entity"]
    for config in ENTITY_CONFIGS
}

MODEL_BY_TABLE = {
    "asset": Asset,
    "asset_class": AssetClass,
    "department": Department,
    "employee": Employee,
    "inventory": Inventory,
    "location": Location,
    "location_type": LocationType,
    "model": Model,
    "position": Position,
    "property": Property,
    "property_type": PropertyType,
    "purchase_request_line": PurchaseRequestLine,
    "site": Site,
    "system": System,
    "system_type": SystemType,
    "unit_of_measure": UnitOfMeasure,
    "core_users": User,
}

RAW_ROWS = {
    config["entity"]: []
    for config in ENTITY_CONFIGS
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


for config in ENTITY_CONFIGS:
    RAW_ROWS[config["entity"]] = parse_legacy_csv(CSV_DIR / config["csv"])


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
    allow_pending_self_ref: bool = False,
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
    if target_table == current_table and allow_pending_self_ref:
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


def build_payload(config: dict[str, Any], row: dict[str, str | None], valid_columns: dict[str, Any], record_id: str) -> dict[str, Any]:
    aliases = config.get("aliases", {})
    skip_headers = config.get("skip_headers", set())
    payload: dict[str, Any] = {"id": record_id}

    for header, raw_value in row.items():
        if header == "name" or header in SYSTEM_HEADERS or header in skip_headers:
            continue

        field_name = aliases.get(header, header)
        if field_name.endswith("_id") and field_name[:-3] in valid_columns:
            field_name = field_name[:-3]
        column = valid_columns.get(field_name)
        if column is None:
            continue

        payload[field_name] = raw_value

    return payload


async def seed_entity(config: dict[str, Any], entity_order: int, entity_total: int) -> None:
    entity_name = config["entity"]
    model = config["model"]
    rows = RAW_ROWS[entity_name]
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

            payload = build_payload(config, row, valid_columns, record_id)

            for field_name, raw_value in list(payload.items()):
                if field_name == "id":
                    continue
                column = valid_columns[field_name]

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


async def backfill_self_reference(entity_name: str, model: Any, field_name: str) -> int:
    rows = RAW_ROWS[entity_name]
    raw_by_id = {
        normalize_identifier(row.get("name"), entity_name): row
        for row in rows
        if normalize_identifier(row.get("name"), entity_name)
    }

    async with async_session_maker() as db:
        updated_count = 0
        result = await db.execute(select(model))
        docs = result.scalars().all()
        existing_ids = {doc.id for doc in docs}

        for doc in docs:
            raw_row = raw_by_id.get(doc.id)
            if raw_row is None:
                continue

            raw_value = raw_row.get(field_name)
            target_value = normalize_identifier(raw_value, entity_name)
            if not target_value or target_value not in existing_ids:
                continue
            if getattr(doc, field_name) == target_value:
                continue

            setattr(doc, field_name, target_value)
            updated_count += 1

        await db.commit()

    print(f"Backfilled {entity_name}.{field_name}: {updated_count}")
    return updated_count


async def backfill_position_current_asset() -> int:
    rows = RAW_ROWS["position"]
    raw_by_id = {
        normalize_identifier(row.get("name"), "position"): row
        for row in rows
        if normalize_identifier(row.get("name"), "position")
    }

    async with async_session_maker() as db:
        updated_count = 0
        asset_ids = await load_existing_ids(db, Asset, {})
        result = await db.execute(select(Position))
        docs = result.scalars().all()

        for doc in docs:
            raw_row = raw_by_id.get(doc.id)
            if raw_row is None:
                continue
            target_value = normalize_identifier(raw_row.get("current_asset_id"), "asset")
            if not target_value or target_value not in asset_ids:
                continue
            if doc.current_asset == target_value:
                continue

            doc.current_asset = target_value
            updated_count += 1

        await db.commit()

    print(f"Backfilled position.current_asset: {updated_count}")
    return updated_count


async def seed_asset_management() -> None:
    print("Initializing database...")
    await init_db()
    print("Database initialized.")

    print("\nSeeding Asset Management entities...")
    total = len(ENTITY_CONFIGS)
    for index, config in enumerate(ENTITY_CONFIGS, start=1):
        await seed_entity(config, index, total)

    print("\nBackfilling self-references and circular links...")
    await backfill_self_reference("asset_class", AssetClass, "parent_asset_class")
    await backfill_self_reference("location", Location, "parent_location")
    await backfill_self_reference("system", System, "parent_system")
    await backfill_position_current_asset()

    print("\nAsset Management seeding complete.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_asset_management())