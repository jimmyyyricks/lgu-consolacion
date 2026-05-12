# Item Types Reference Guide

## Overview

Item Types control how items are processed during Purchase Receipt and determine what records are automatically generated. Both the new EAM FastAPI system and the legacy CI EAM system use the same Item Type logic.

## Available Item Types

| Item Type | Description | Creates Asset? | Creates Inventory? | Use Case |
|-----------|-------------|----------------|-------------------|----------|
| **Fixed Asset Item** | Permanent assets that are tracked individually | ✅ Yes | ✅ Yes | Buildings, major equipment, vehicles |
| **Asset Item** | Trackable assets but not fixed assets | ✅ Yes | ✅ Yes | Tools, computers, movable equipment |
| **Inventory Item** | Consumable or stock items | ❌ No | ✅ Yes | Spare parts, supplies, materials |
| **Non Inventory Item** | Items not tracked in inventory | ❌ No | ❌ No | Services, consulting, expenses |
| **Service Item** | Intangible services | ❌ No | ❌ No | Maintenance services, training |

## Processing Logic by Item Type

### Fixed Asset Item
- **Creates**: Inventory + Asset + (optional) Equipment + (optional) Maintenance Request
- **Workflow**: Acquired → Inspect Asset → Install Asset
- **Special**: Automatically goes through inspection and installation workflow
- **Use when**: Item is a permanent asset that needs formal installation

### Asset Item  
- **Creates**: Inventory + Asset + (optional) Equipment + (optional) Maintenance Request
- **Workflow**: Acquired → Putaway (or inspection if required)
- **Special**: Simpler workflow than Fixed Asset
- **Use when**: Item is trackable equipment but doesn't need formal installation

### Inventory Item
- **Creates**: Inventory only + (optional) Equipment
- **Workflow**: No asset workflow
- **Special**: Can create Equipment if marked as equipment
- **Use when**: Consumable items or spare parts that don't need asset tracking

### Non Inventory Item
- **Creates**: Nothing (blocked from receipt processing)
- **Workflow**: N/A
- **Special**: Purchase Receipt will fail with error
- **Use when**: Items that shouldn't generate inventory (expenses, etc.)

### Service Item
- **Creates**: Nothing (blocked from receipt processing)
- **Workflow**: N/A  
- **Special**: Purchase Receipt will fail with error
- **Use when**: Intangible services

## Key Fields That Affect Processing

### Serialization (`is_serialized`)
- **Yes**: Creates individual inventory/asset records for each unit
- **No**: Creates single batch record or updates existing inventory

### Equipment (`is_equipment`)
- **Yes**: Creates Equipment record in addition to other records
- **No**: No Equipment record created

### Inspection Required (`inspection_required`)
- **Yes**: Creates Maintenance Request for inspection
- **No**: No maintenance request, asset goes directly to operational state

## Examples for METPower Polomolok

### Screw Press Conveyor
```
Item Type: Fixed Asset Item
Is Serialized: Yes
Is Equipment: Yes  
Inspection Required: Yes
Result: Creates Inventory + Asset + Equipment + Maintenance Request
```

### Conveyor Belt
```
Item Type: Inventory Item
Is Serialized: No
Is Equipment: Yes
Inspection Required: No
Result: Creates Inventory + Equipment
```

### Motor Oil
```
Item Type: Inventory Item
Is Serialized: No
Is Equipment: No
Inspection Required: No
Result: Creates Inventory only
```

### Maintenance Service
```
Item Type: Service Item
Result: Purchase Receipt blocked (error)
```

## Error Messages

When trying to receive prohibited item types:
- **Service Item**: "Cannot create or update inventory record for Service Item"
- **Non Inventory Item**: "Cannot create or update inventory record for Non Inventory Item"

## Workflow States

### Fixed Asset Item
- Asset: Acquired → Inspect Asset → Install Asset → Active

### Asset Item
- Asset: Acquired → Putaway → Active (or inspection if required)

### Inventory Item
- No asset workflow, only inventory updates
