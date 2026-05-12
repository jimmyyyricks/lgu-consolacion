"""Seed Purchasing and Stores data from legacy CSV exports."""

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
CSV_DIR = Path(__file__).parent.parent / "purchasing_stores"
ENTITY_DIR = BACKEND_DIR / "app/modules/purchasing_stores/entities"

# Load .env from backend directory
env_file = BACKEND_DIR / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import async_session_maker, init_db
from app.core.framework.models.auth import User
from app.modules.asset_management.models.location import Location
from app.modules.core_eam.models import Account, CostCode, Department, Employee, Labor, Site
from app.modules.purchasing_stores.models import (
    Bin,
    Currency,
    Inventory,
    InventoryAdjustment,
    InventoryAdjustmentLine,
    Item,
    ItemClass,
    ItemIssue,
    ItemIssueLine,
    ItemReturn,
    ItemReturnLine,
    PurchaseReceipt,
    PurchaseRequest,
    PurchaseRequestLine,
    StockCount,
    StockCountLine,
    Store,
    Transfer,
    UnitOfMeasure,
    Vendor,
    Zone,
)
from app.modules.work_mgmt.models import WorkOrderActivity
from app.modules.maintenance_mgmt.models import MaintenanceRequest


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


def load_item_issue_rows(_: dict[str, Any]) -> list[dict[str, str | None]]:
    header_rows = parse_legacy_csv(CSV_DIR / "tabItem Issue.csv")
    part_rows = parse_legacy_csv(CSV_DIR / "tabParts Issue.csv")
    rows_by_id: dict[str, dict[str, str | None]] = {}

    for row in header_rows:
        record_id = clean_value(row.get("name"))
        if record_id:
            rows_by_id[record_id] = dict(row)

    for row in part_rows:
        record_id = clean_value(row.get("name"))
        if not record_id:
            continue

        if record_id not in rows_by_id:
            merged = {"name": record_id}
            rows_by_id[record_id] = merged
        else:
            merged = rows_by_id[record_id]

        for field_name in (
            "issue_type",
            "work_order_activity",
            "site",
            "department",
            "cost_code",
            "date_issued",
            "workflow_state",
        ):
            if not merged.get(field_name) and row.get(field_name):
                merged[field_name] = row[field_name]

    return list(rows_by_id.values())


def load_item_issue_line_rows(_: dict[str, Any]) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []
    for row in parse_legacy_csv(CSV_DIR / "tabParts Issue.csv"):
        line_row = dict(row)
        line_row["item_issue"] = row.get("name")
        rows.append(line_row)
    return rows


def load_item_return_line_rows(_: dict[str, Any]) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []
    for row in parse_legacy_csv(CSV_DIR / "tabParts Return.csv"):
        line_row = dict(row)
        line_row["item_return"] = row.get("name")
        rows.append(line_row)
    return rows


def stock_count_reference(value: str | None) -> str | None:
    cleaned = clean_value(value)
    if not cleaned:
        return cleaned
    return re.sub(r"^SKC-", "SC-", cleaned)


ENTITY_CONFIGS = [
    {"entity": "currency", "model": Currency, "csv": "tabCurrency.csv"},
    {
        "entity": "unit_of_measure",
        "model": UnitOfMeasure,
        "csv": "tabUnit Of Measure.csv",
        "aliases": {"uom_name": "name"},
    },
    {"entity": "vendor", "model": Vendor, "csv": "tabVendor.csv"},
    {"entity": "store", "model": Store, "csv": "tabStore.csv"},
    {"entity": "zone", "model": Zone, "csv": "tabZone.csv"},
    {"entity": "bin", "model": Bin, "csv": "tabBin.csv"},
    {
        "entity": "item_class",
        "model": ItemClass,
        "csv": "tabItem Class.csv",
        "aliases": {"is_serialiazed": "is_serialized"},
    },
    {"entity": "item", "model": Item, "csv": "tabItem.csv"},
    {"entity": "inventory", "model": Inventory, "csv": "tabInventory.csv"},
    {"entity": "stock_count", "model": StockCount, "csv": "tabStock Count.csv"},
    {
        "entity": "stock_count_line",
        "model": StockCountLine,
        "csv": "tabStock Count Line.csv",
        "value_transforms": {"stock_count": stock_count_reference},
    },
    {
        "entity": "inventory_adjustment",
        "model": InventoryAdjustment,
        "csv": "tabInventory Adjustment.csv",
    },
    {
        "entity": "inventory_adjustment_line",
        "model": InventoryAdjustmentLine,
        "csv": "tabInventory Adjustment Line.csv",
    },
    {
        "entity": "item_issue",
        "model": ItemIssue,
        "csv": "tabItem Issue.csv",
        "rows_loader": load_item_issue_rows,
    },
    {
        "entity": "item_issue_line",
        "model": ItemIssueLine,
        "csv": "tabParts Issue.csv",
        "rows_loader": load_item_issue_line_rows,
        "id_mode": "generated",
    },
    {"entity": "item_return", "model": ItemReturn, "csv": "tabParts Return.csv"},
    {
        "entity": "item_return_line",
        "model": ItemReturnLine,
        "csv": "tabParts Return.csv",
        "rows_loader": load_item_return_line_rows,
        "id_mode": "generated",
    },
    {"entity": "purchase_request", "model": PurchaseRequest, "csv": "tabPurchase Request.csv"},
    {
        "entity": "purchase_request_line",
        "model": PurchaseRequestLine,
        "csv": "tabPurchase Request Line.csv",
    },
    {"entity": "purchase_receipt", "model": PurchaseReceipt, "csv": "tabPurchase Receipt.csv"},
    {"entity": "transfer", "model": Transfer, "csv": "tabTransfer.csv"},
]

ENTITY_NAME_BY_TABLE = {
    config["model"].__tablename__: config["entity"]
    for config in ENTITY_CONFIGS
}

MODEL_BY_TABLE = {
    "account": Account,
    "bin": Bin,
    "cost_code": CostCode,
    "core_users": User,
    "currency": Currency,
    "department": Department,
    "employee": Employee,
    "inventory": Inventory,
    "inventory_adjustment": InventoryAdjustment,
    "item": Item,
    "item_class": ItemClass,
    "item_issue": ItemIssue,
    "item_return": ItemReturn,
    "labor": Labor,
    "location": Location,
    "purchase_request": PurchaseRequest,
    "purchase_request_line": PurchaseRequestLine,
    "site": Site,
    "stock_count": StockCount,
    "stock_count_line": StockCountLine,
    "store": Store,
    "transfer": Transfer,
    "unit_of_measure": UnitOfMeasure,
    "vendor": Vendor,
    "maintenance_request": MaintenanceRequest,
    "work_order_activity": WorkOrderActivity,
    "zone": Zone,
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


def generate_identifier(entity: str, counter: int) -> str:
    naming = ENTITY_NAMING[entity]
    return f"{naming['prefix']}{str(counter).zfill(naming['width'])}"


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


def get_rows_for_config(config: dict[str, Any]) -> list[dict[str, str | None]]:
    row_loader = config.get("rows_loader")
    if row_loader:
        return row_loader(config)
    return parse_legacy_csv(CSV_DIR / config["csv"])


def should_backfill(current_value: Any, new_value: Any) -> bool:
    if new_value is None:
        return False
    if current_value is None:
        return True
    if isinstance(current_value, str) and not current_value.strip():
        return True
    return False


async def update_existing_record(
    db: Any,
    model: Any,
    record_id: str,
    payload: dict[str, Any],
) -> bool:
    record = await db.get(model, record_id)
    if record is None:
        return False

    updated = False
    for field_name, value in payload.items():
        if field_name == "id" or not should_backfill(getattr(record, field_name), value):
            continue
        setattr(record, field_name, value)
        updated = True

    if updated:
        await db.flush()

    return updated


async def seed_entity(config: dict[str, Any], entity_order: int, entity_total: int) -> None:
    entity_name = config["entity"]
    model = config["model"]
    aliases = config.get("aliases", {})
    value_transforms = config.get("value_transforms", {})
    rows = get_rows_for_config(config)
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
        updated_count = 0
        skipped_count = 0
        failed_count = 0
        unresolved_count = 0

        for row_index, row in enumerate(rows, start=1):
            if config.get("id_mode") == "generated":
                record_id = generate_identifier(entity_name, row_index)
            else:
                record_id = normalize_identifier(row.get("name"), entity_name)

            if not record_id:
                failed_count += 1
                continue

            payload = {"id": record_id}

            for header, raw_value in row.items():
                if header == "name" or header in SYSTEM_HEADERS:
                    continue

                field_name = aliases.get(header, header)
                column = valid_columns.get(field_name)
                if column is None:
                    continue

                transformed_value = raw_value
                if field_name in value_transforms:
                    transformed_value = value_transforms[field_name](raw_value)

                try:
                    if column.foreign_keys:
                        value, unresolved = await resolve_foreign_key(
                            db,
                            transformed_value,
                            column,
                            id_cache,
                            user_cache,
                        )
                        if unresolved:
                            unresolved_count += 1
                    else:
                        value = coerce_value(clean_value(transformed_value), column.type)
                except Exception as exc:
                    print(f"{entity_name} {record_id}: could not parse {field_name}: {exc}")
                    value = None
                    failed_count += 1

                payload[field_name] = value

            if record_id in existing_ids:
                try:
                    async with db.begin_nested():
                        updated = await update_existing_record(db, model, record_id, payload)
                    if updated:
                        updated_count += 1
                    else:
                        skipped_count += 1
                except SQLAlchemyError as exc:
                    failed_count += 1
                    print(f"{entity_name} {record_id}: update failed: {exc}")
                continue

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
        f"Seeded {seeded_count}, Updated {updated_count}, Skipped {skipped_count}, Failed {failed_count}, "
        f"Unresolved FKs nulled {unresolved_count}"
    )


RELATIONSHIP_CHECKS = [
    ("purchase_request_line", "purchase_request", "purchase_request"),
    ("purchase_receipt", "purchase_request_line", "purchase_request_line"),
    ("item_issue_line", "item_issue", "item_issue"),
    ("item_return_line", "item_return", "item_return"),
    ("stock_count_line", "stock_count", "stock_count"),
    ("inventory_adjustment_line", "inventory_adjustment", "inventory_adjustment"),
]


async def validate_parent_child_links() -> None:
    async with async_session_maker() as db:
        print("\nParent-child validation:")
        for child_table, field_name, parent_table in RELATIONSHIP_CHECKS:
            result = await db.execute(
                text(
                    f"""
                    SELECT
                        COUNT(*) AS total,
                        SUM(CASE WHEN child.{field_name} IS NULL THEN 1 ELSE 0 END) AS missing_fk,
                        SUM(
                            CASE
                                WHEN child.{field_name} IS NOT NULL AND parent.id IS NULL THEN 1
                                ELSE 0
                            END
                        ) AS orphan_fk
                    FROM {child_table} AS child
                    LEFT JOIN {parent_table} AS parent ON parent.id = child.{field_name}
                    """
                )
            )
            total, missing_fk, orphan_fk = result.one()
            print(
                f"- {child_table}.{field_name}: total={total}, "
                f"missing_fk={missing_fk or 0}, orphan_fk={orphan_fk or 0}"
            )


async def seed_purchasing_stores() -> None:
    print("Initializing database...")
    try:
        await init_db()
        print("Database initialized.")
    except Exception as exc:
        print(f"Database initialization skipped: {exc}")

    print("\nSeeding Purchasing and Stores entities...")
    total = len(ENTITY_CONFIGS)
    for index, config in enumerate(ENTITY_CONFIGS, start=1):
        await seed_entity(config, index, total)

    await validate_parent_child_links()

    print("\nPurchasing and Stores seeding complete.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(seed_purchasing_stores())