"""Seed Sidebar Ordering - Updates entity metadata and module/entity display order."""

import json
import os
import sys
from pathlib import Path

from sqlalchemy import select, text


BACKEND_DIR = Path(
    "/home/eamadmin/eam-2.0/eam-2.1-fastapi-vue/backend"
)

# Load .env from backend directory
env_file = BACKEND_DIR / ".env"
if env_file.exists():
    from dotenv import load_dotenv
    load_dotenv(env_file)

sys.path.insert(0, str(BACKEND_DIR))

from app.core.database import async_session_maker
from app.core.framework.models.ordering import EntityOrder, ModuleOrder
from app.api.system.meta import _module_order_key


# Canonical sidebar configuration
SIDEBAR_CONFIG = {
    "entities": [
        {"name": "disposed", "label": "Disposed", "module": "asset_management", "group": "Assets", "icon": "trash-2", "in_sidebar": 1},
        {"name": "asset_class", "label": "Asset Class", "module": "asset_management", "group": "Asset Classification", "icon": "layers", "in_sidebar": 1},
        {"name": "asset", "label": "Asset", "module": "asset_management", "group": "Assets", "icon": "box", "in_sidebar": 1},
        {"name": "property", "label": "Property", "module": "asset_management", "group": "Assets", "icon": "list", "in_sidebar": 1},
        {"name": "system_type", "label": "System Type", "module": "asset_management", "group": "Asset Classification", "icon": "folder", "in_sidebar": 1},
        {"name": "system", "label": "System", "module": "asset_management", "group": "Asset Structure", "icon": "cpu", "in_sidebar": 1},
        {"name": "incident", "label": "Incident", "module": "asset_management", "group": "Incidents", "icon": "alert-triangle", "in_sidebar": 1},
        {"name": "location", "label": "Location", "module": "asset_management", "group": "Asset Structure", "icon": "map", "in_sidebar": 1},
        {"name": "location_type", "label": "Location Type", "module": "asset_management", "group": "Asset Classification", "icon": "folder", "in_sidebar": 1},
        {"name": "equipment", "label": "Equipment", "module": "asset_management", "group": "Asset Structure", "icon": "tool", "in_sidebar": 1},
        {"name": "position", "label": "Position", "module": "asset_management", "group": "Asset Structure", "icon": "crosshair", "in_sidebar": 1},
        {"name": "breakdown", "label": "Breakdown", "module": "asset_management", "group": "Incidents", "icon": "alert-circle", "in_sidebar": 1},
        {"name": "maintenance_calendar", "label": "Maintenance Calendar", "module": "maintenance_mgmt", "group": "Maintenance Planning", "icon": "calendar", "in_sidebar": 1},
        {"name": "maintenance_request", "label": "Maintenance Request", "module": "maintenance_mgmt", "group": "Maintenance Requests", "icon": "alert-circle", "in_sidebar": 1},
        {"name": "maintenance_trade", "label": "Maintenance Trade", "module": "maintenance_mgmt", "group": "Maintenance Configuration", "icon": "users", "in_sidebar": 1},
        {"name": "maintenance_condition", "label": "Maintenance Condition", "module": "maintenance_mgmt", "group": "Maintenance Configuration", "icon": "gauge", "in_sidebar": 1},
        {"name": "maintenance_parts", "label": "Maintenance Parts", "module": "maintenance_mgmt", "group": "Maintenance Configuration", "icon": "package", "in_sidebar": 1},
        {"name": "maintenance_plan", "label": "Maintenance Plan", "module": "maintenance_mgmt", "group": "Maintenance Planning", "icon": "clipboard-check", "in_sidebar": 1},
        {"name": "maintenance_order", "label": "Maintenance Order", "module": "maintenance_mgmt", "group": "Maintenance Execution", "icon": "file-text", "in_sidebar": 1},
        {"name": "maintenance_interval", "label": "Maintenance Interval", "module": "maintenance_mgmt", "group": "Maintenance Configuration", "icon": "clock", "in_sidebar": 1},
        {"name": "maintenance_equipment", "label": "Maintenance Equipment", "module": "maintenance_mgmt", "group": "Maintenance Configuration", "icon": "cog", "in_sidebar": 1},
        {"name": "maintenance_activity", "label": "Maintenance Activity", "module": "maintenance_mgmt", "group": "Maintenance Execution", "icon": "wrench", "in_sidebar": 1},
        {"name": "planned_maintenance_activity", "label": "Planned Maint. Activity", "module": "maintenance_mgmt", "group": "Maintenance Planning", "icon": "calendar-check", "in_sidebar": 1},
        {"name": "checklist", "label": "Checklist", "module": "maintenance_mgmt", "group": "Maintenance Execution", "icon": "clipboard-list", "in_sidebar": 1},
        {"name": "sensor", "label": "Sensor", "module": "maintenance_mgmt", "group": "Condition Monitoring", "icon": "activity", "in_sidebar": 1},
        {"name": "sensor_data", "label": "Sensor Data", "module": "maintenance_mgmt", "group": "Condition Monitoring", "icon": "database", "in_sidebar": 1},
        {"name": "service_request", "label": "Service Request", "module": "maintenance_mgmt", "group": "Maintenance Requests", "icon": "clipboard", "in_sidebar": 1},
        {"name": "work_order", "label": "Work Order", "module": "work_mgmt", "group": "Work Orders", "icon": "clipboard", "in_sidebar": 1},
        {"name": "work_order_activity", "label": "Work Order Activity", "module": "work_mgmt", "group": "Work Orders", "icon": "activity", "in_sidebar": 1},
        {"name": "work_order_activity_logs", "label": "Work Order Activity Logs", "module": "work_mgmt", "group": "Work Execution", "icon": "file-text", "in_sidebar": 1},
        {"name": "work_order_checklist", "label": "Work Order Checklist", "module": "work_mgmt", "group": "Work Execution", "icon": "check-square", "in_sidebar": 1},
        {"name": "work_order_equipment", "label": "Work Order Equipment", "module": "work_mgmt", "group": "Work Execution", "icon": "tool", "in_sidebar": 1},
        {"name": "work_order_parts", "label": "Work Order Parts", "module": "work_mgmt", "group": "Work Resources", "icon": "package", "in_sidebar": 1},
        {"name": "work_order_parts_reservation", "label": "Work Order Parts Reservation", "module": "work_mgmt", "group": "Work Resources", "icon": "bookmark", "in_sidebar": 1},
        {"name": "work_order_labor", "label": "Work Order Labor", "module": "work_mgmt", "group": "Work Resources", "icon": "users", "in_sidebar": 1},
        {"name": "category_of_failure", "label": "Category of Failure", "module": "work_mgmt", "group": "Failure Analysis", "icon": "alert-triangle", "in_sidebar": 1},
        {"name": "unit_of_measure", "label": "Unit of Measure", "module": "purchasing_stores", "group": "Item Catalog", "icon": "ruler", "in_sidebar": 1},
        {"name": "item", "label": "Item", "module": "purchasing_stores", "group": "Item Catalog", "icon": "package", "in_sidebar": 1},
        {"name": "item_issue", "label": "Item Issue", "module": "purchasing_stores", "group": "Inventory Operations", "icon": "log-out", "in_sidebar": 1},
        {"name": "item_return", "label": "Item Return", "module": "purchasing_stores", "group": "Inventory Operations", "icon": "log-in", "in_sidebar": 1},
        {"name": "item_class", "label": "Item Class", "module": "purchasing_stores", "group": "Item Catalog", "icon": "layers", "in_sidebar": 1},
        {"name": "purchase_request", "label": "Purchase Request", "module": "purchasing_stores", "group": "Purchasing", "icon": "shopping-cart", "in_sidebar": 1},
        {"name": "purchase_return", "label": "Purchase Return", "module": "purchasing_stores", "group": "Receiving", "icon": "rotate-ccw", "in_sidebar": 1},
        {"name": "purchase_receipt", "label": "Purchase Receipt", "module": "purchasing_stores", "group": "Receiving", "icon": "file-text", "in_sidebar": 1},
        {"name": "transfer_receipt", "label": "Transfer Receipt", "module": "purchasing_stores", "group": "Warehouse Movement", "icon": "check-circle", "in_sidebar": 1},
        {"name": "transfer", "label": "Transfer", "module": "purchasing_stores", "group": "Warehouse Movement", "icon": "repeat", "in_sidebar": 1},
        {"name": "zone", "label": "Zone", "module": "purchasing_stores", "group": "Warehouse Structure", "icon": "map-pin", "in_sidebar": 1},
        {"name": "stock_count", "label": "Stock Count", "module": "purchasing_stores", "group": "Stock Control", "icon": "clipboard-list", "in_sidebar": 1},
        {"name": "stock_ledger_entry", "label": "Stock Ledger Entry", "module": "purchasing_stores", "group": "Stock Control", "icon": "book", "in_sidebar": 1},
        {"name": "store", "label": "Store", "module": "purchasing_stores", "group": "Warehouse Structure", "icon": "home", "in_sidebar": 1},
        {"name": "vendor", "label": "Vendor", "module": "purchasing_stores", "group": "Purchasing", "icon": "truck", "in_sidebar": 1},
        {"name": "currency", "label": "Currency", "module": "purchasing_stores", "group": "Reference Data", "icon": "dollar-sign", "in_sidebar": 1},
        {"name": "request_for_quotation", "label": "Request For Quotation", "module": "purchasing_stores", "group": "Purchasing", "icon": "file-invoice", "in_sidebar": 1},
        {"name": "inventory_adjustment", "label": "Inventory Adjustment", "module": "purchasing_stores", "group": "Inventory Operations", "icon": "sliders", "in_sidebar": 1},
        {"name": "inventory", "label": "Inventory", "module": "purchasing_stores", "group": "Inventory Operations", "icon": "archive", "in_sidebar": 1},
        {"name": "putaway", "label": "Putaway", "module": "purchasing_stores", "group": "Warehouse Movement", "icon": "corner-down-left", "in_sidebar": 1},
        {"name": "inspection", "label": "Inspection", "module": "purchasing_stores", "group": "Stock Control", "icon": "search", "in_sidebar": 1},
        {"name": "bin", "label": "Bin", "module": "purchasing_stores", "group": "Warehouse Structure", "icon": "box", "in_sidebar": 1},
        {"name": "reason_code", "label": "Reason Code", "module": "purchasing_stores", "group": "Reference Data", "icon": "tag", "in_sidebar": 1},
        {"name": "work_schedule", "label": "Work Schedule", "module": "core_eam", "group": "Scheduling", "icon": "calendar-days", "in_sidebar": 1},
        {"name": "labor_availability", "label": "Labor Availability", "module": "core_eam", "group": "Labor", "icon": "calendar-check", "in_sidebar": 1},
        {"name": "labor", "label": "Labor", "module": "core_eam", "group": "Labor", "icon": "wrench", "in_sidebar": 1},
        {"name": "trade_labor", "label": "Trade Labor", "module": "core_eam", "group": "Trades", "icon": "link", "in_sidebar": 1},
        {"name": "trade", "label": "Trade", "module": "core_eam", "group": "Trades", "icon": "hammer", "in_sidebar": 1},
        {"name": "trade_availability", "label": "Trade Availability", "module": "core_eam", "group": "Trades", "icon": "clock", "in_sidebar": 1},
        {"name": "employee", "label": "Employee", "module": "core_eam", "group": "Employees", "icon": "user", "in_sidebar": 1},
        {"name": "employee_site", "label": "Employee Site", "module": "core_eam", "group": "Employees", "icon": "user-check", "in_sidebar": 1},
        {"name": "site", "label": "Site", "module": "core_eam", "group": "Organization Structure", "icon": "map-pin", "in_sidebar": 1},
        {"name": "model", "label": "Model", "module": "core_eam", "group": "System Configuration", "icon": "box", "in_sidebar": 1},
        {"name": "labor_group", "label": "Labor Group", "module": "core_eam", "group": "Labor", "icon": "users-round", "in_sidebar": 1},
        {"name": "holiday", "label": "Holiday", "module": "core_eam", "group": "Scheduling", "icon": "party-popper", "in_sidebar": 1},
        {"name": "cost_code", "label": "Cost Code", "module": "core_eam", "group": "Costing", "icon": "hash", "in_sidebar": 1},
        {"name": "note", "label": "Note", "module": "core_eam", "group": "System", "icon": "sticky-note", "in_sidebar": 1},
        {"name": "account", "label": "Account", "module": "core_eam", "group": "Finance", "icon": "wallet", "in_sidebar": 1},
        {"name": "manufacturer", "label": "Manufacturer", "module": "core_eam", "group": "System Configuration", "icon": "factory", "in_sidebar": 1},
        {"name": "leave_application", "label": "Leave Application", "module": "core_eam", "group": "Scheduling", "icon": "plane-takeoff", "in_sidebar": 1},
        {"name": "leave_type", "label": "Leave Type", "module": "core_eam", "group": "Scheduling", "icon": "palm-tree", "in_sidebar": 1},
        {"name": "request_activity_type", "label": "Request Activity Type", "module": "core_eam", "group": "System Configuration", "icon": "workflow", "in_sidebar": 1},
        {"name": "department", "label": "Department", "module": "core_eam", "group": "Organization Structure", "icon": "users", "in_sidebar": 1},
        {"name": "organization", "label": "Organization", "module": "core_eam", "group": "Organization Structure", "icon": "building-2", "in_sidebar": 1},
        {"name": "contractor", "label": "Contractor", "module": "core_eam", "group": "Costing", "icon": "hard-hat", "in_sidebar": 1},
        {"name": "annual_budget", "label": "Annual Budget", "module": "core_eam", "group": "Finance", "icon": "calendar-range", "in_sidebar": 1},
        {"name": "error_log", "label": "Error Log", "module": "core", "group": "System", "icon": "alert-circle", "in_sidebar": True},
        {"name": "role", "label": "Role", "module": "core", "group": "Authentication", "icon": "shield", "in_sidebar": True},
        {"name": "user", "label": "User", "module": "core", "group": "Authentication", "icon": "users", "in_sidebar": True},
        {"name": "email_log", "label": "Email Log", "module": "core", "group": "System", "icon": "mail", "in_sidebar": True},
        {"name": "scheduled_job_log", "label": "Scheduled Job Log", "module": "core", "group": "System", "icon": "clock", "in_sidebar": True},
    ],
    "navigation": [
        {"key": "asset_management", "label": "Asset Management"},
        {"key": "maintenance_mgmt", "label": "Maintenance Management"},
        {"key": "work_mgmt", "label": "Work Management"},
        {"key": "purchasing_stores", "label": "Procurement"},
        {"key": "core_eam", "label": "Enterprise"},
        {"key": "core", "label": "Core"},
    ]
}


def update_entity_json(entity_config: dict) -> bool:
    """Update entity JSON file with icon, group, and in_sidebar values."""
    entity_name = entity_config["name"]
    module_name = entity_config["module"]
    
    # Build path to entity JSON file
    entity_json_path = BACKEND_DIR / "app" / "modules" / module_name / "entities" / f"{entity_name}.json"
    
    if not entity_json_path.exists():
        print(f"  ⚠️  Entity JSON not found: {entity_json_path}")
        return False
    
    try:
        with open(entity_json_path, 'r') as f:
            entity_data = json.load(f)
        
        # Update metadata fields
        entity_data["icon"] = entity_config["icon"]
        entity_data["group"] = entity_config["group"]
        entity_data["in_sidebar"] = entity_config["in_sidebar"]
        
        with open(entity_json_path, 'w') as f:
            json.dump(entity_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"  ❌ Error updating {entity_name}.json: {e}")
        return False


async def seed_module_order(db) -> tuple[int, int]:
    """Seed module display order based on navigation configuration."""
    created = 0
    skipped = 0
    
    for idx, nav_item in enumerate(SIDEBAR_CONFIG["navigation"]):
        module_key = nav_item["key"]
        module_order_key = _module_order_key(module_key)
        
        existing = await db.execute(
            select(ModuleOrder).where(ModuleOrder.module_name == module_order_key)
        )
        module_order = existing.scalar_one_or_none()
        
        if module_order:
            if module_order.sort_order != idx:
                module_order.sort_order = idx
                created += 1  # Count as update
            else:
                skipped += 1
        else:
            db.add(ModuleOrder(module_name=module_order_key, sort_order=idx))
            created += 1
    
    await db.commit()
    return created, skipped


async def seed_entity_order(db) -> tuple[int, int]:
    """Seed entity display order based on entities configuration."""
    created = 0
    skipped = 0
    
    for idx, entity_config in enumerate(SIDEBAR_CONFIG["entities"]):
        entity_name = entity_config["name"]
        module_name = entity_config["module"]
        module_order_key = _module_order_key(module_name)
        
        existing = await db.execute(
            select(EntityOrder).where(EntityOrder.entity_name == entity_name)
        )
        entity_order = existing.scalar_one_or_none()
        
        if entity_order:
            if entity_order.sort_order != idx or entity_order.module_name != module_order_key:
                entity_order.sort_order = idx
                entity_order.module_name = module_order_key
                created += 1  # Count as update
            else:
                skipped += 1
        else:
            db.add(EntityOrder(
                entity_name=entity_name,
                module_name=module_order_key,
                sort_order=idx
            ))
            created += 1
    
    await db.commit()
    return created, skipped


async def create_ordering_tables_if_not_exist(db) -> None:
    """Create ordering tables if they don't exist."""
    # Check and create core_module_orders table
    await db.execute(text("""
        CREATE TABLE IF NOT EXISTS core_module_orders (
            id TEXT PRIMARY KEY,
            module_name TEXT NOT NULL UNIQUE,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    # Check and create core_entity_orders table
    await db.execute(text("""
        CREATE TABLE IF NOT EXISTS core_entity_orders (
            id TEXT PRIMARY KEY,
            entity_name TEXT NOT NULL UNIQUE,
            module_name TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
    """))
    
    await db.commit()
    print("  ✅ Ordering tables verified/created")


async def seed_sidebar_ordering(update_json_files: bool = True) -> None:
    """
    Update entity JSON files and seed module/entity ordering.

    Args:
        update_json_files: If True, updates entity JSON files with icon/group/in_sidebar
    """
    print("🎨 Updating sidebar ordering...")
    
    # Ensure ordering tables exist
    async with async_session_maker() as db:
        await create_ordering_tables_if_not_exist(db)
    
    # Update entity JSON files
    if update_json_files:
        print("  Updating entity JSON files...")
        json_updated = 0
        json_skipped = 0
        
        for entity_config in SIDEBAR_CONFIG["entities"]:
            if update_entity_json(entity_config):
                json_updated += 1
            else:
                json_skipped += 1
        
        print(f"  ✅ Entity JSON files: +{json_updated} updated, ={json_skipped} skipped")
    
    # Seed module order
    print("  Seeding module order...")
    async with async_session_maker() as db:
        module_created, module_skipped = await seed_module_order(db)
    print(f"  ✅ Module order: +{module_created} updated, ={module_skipped} skipped")
    
    # Seed entity order
    print("  Seeding entity order...")
    async with async_session_maker() as db:
        entity_created, entity_skipped = await seed_entity_order(db)
    print(f"  ✅ Entity order: +{entity_created} updated, ={entity_skipped} skipped")
    
    total_updated = (json_updated if update_json_files else 0) + module_created + entity_created
    total_skipped = (json_skipped if update_json_files else 0) + module_skipped + entity_skipped
    
    print(f"\n🎨 Sidebar ordering complete: +{total_updated} updated, ={total_skipped} skipped\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(seed_sidebar_ordering(update_json_files=True))
