# Phase 2: Item Acquisition and Procurement

[Back to Main Manual](./00_EAM_User_Manual.md)

---

## Purpose

> 📦 Define items and acquire them through the purchase process.
>
> This phase creates the item catalog and uses Purchase Requests to automatically generate Inventory and Asset records when items are received.

By the end of this phase, items will be properly defined and acquired so that:

- Purchase Requests can be created for needed items
- Items are received and automatically become inventory/asset records
- Assets are ready for installation and maintenance
- Inventory is properly tracked for consumption

> ⚠️ This phase follows the automated flow: Item Definition → Purchase Request → Purchase Receipt → Auto-Generated Inventory & Assets

---

### Function Signature

```text
phase2_item_acquisition_procurement(item_definitions, purchase_requests) -> acquired_items
```

---

# 📦 1. Item Catalog Setup

Defines the materials and equipment that can be purchased and managed.

### Item Class

> 📦 Category that groups similar items together for management and reporting.

| Field              | Value                     |
| ------------------ | ------------------------- |
| item_class_name    | Equipment                 |
| description        | Equipment and spare parts |
| item_class_type    | Inventory Item            |
| asset_class        | Rotating Equipment        |
| parent_item_class  | [optional parent class]   |
| default_uom        | Nos                       |
| valuation_method   | FIFO                      |
| account            | [linked account]          |
| inventory_tracking | Yes                       |
| is_serialized      | Yes                       |
| is_active          | Yes                       |

> 📝 **Reminder**: Create a separate Item Class for each other item group found in the site.

### Item

> 🧰 Individual item that can be purchased and automatically converted to inventory/asset records.
>
> **Item Type** controls what gets created during Purchase Receipt processing. [See Item Types Reference](./references/item-types-reference.md)

| Field                        | Value                                                                     |
| ---------------------------- | ------------------------------------------------------------------------- |
| item_name                    | Screw Press Conveyor Assembly                                             |
| description                  | Complete screw press conveyor assembly for the Polomolok waste water line |
| item_class                   | Equipment                                                                 |
| item_type                    | Fixed Asset Item                                                          |
| expense_account              | [linked account]                                                          |
| inventory_adjustment_account | [linked account]                                                          |
| primary_vendor               | WAMGROUP                                                                  |
| asset_class                  | Rotating Equipment                                                        |
| uom                          | Nos                                                                       |
| actual_qty_on_hand           | 0                                                                         |
| available_capacity           | 1                                                                         |
| unit_cost                    | [purchase price]                                                          |
| reserved_capacity            | 0                                                                         |
| is_serialized                | Yes                                                                       |
| inspection_required          | Yes                                                                       |
| is_equipment                 | Yes                                                                       |

> 💡 **Why Fixed Asset Item?**
>
> - Creates Asset record for lifecycle tracking
> - Creates Equipment record for maintenance planning
> - Creates Maintenance Request for inspection
> - Goes through formal installation workflow
>
> 📊 **Quantity Tracking**: `actual_qty_on_hand` is the **sum of all inventory quantities** across all locations for this item. An item can have multiple inventory records at different sites/locations.
>
> 🔒 **System-Managed Field**: `actual_qty_on_hand` starts at 0 and is **automatically updated** by the system during Purchase Receipt processing - not manually editable.

### Spare Parts Items

> 🔩 Common spare parts used for conveyor maintenance.

> 📝 **Best Practice**: Create separate Item Classes for different item types (e.g., "Spare Parts - Non-Serialized", "Consumables") instead of overriding Item Class defaults at the Item level. This provides cleaner data modeling and avoids confusion.

| Field          | Value                                     |
| -------------- | ----------------------------------------- |
| item_name      | Conveyor Belt                             |
| description    | Replacement belt for screw press conveyor |
| item_class     | Spare Parts - Non-Serialized              |
| item_type      | Inventory Item                            |
| primary_vendor | WAMGROUP                                  |
| uom            | Mtr                                       |
| is_serialized  | No                                        |
| is_equipment   | Yes                                       |

> 💡 **Why Inventory Item?**
>
> - Creates Inventory record for stock tracking
> - Creates Equipment record for maintenance use
> - No Asset record (consumable/replacement part)

| Field          | Value                                  |
| -------------- | -------------------------------------- |
| item_name      | Bearings Set                           |
| description    | High-speed bearings for conveyor motor |
| item_class     | Spare Parts - Non-Serialized           |
| item_type      | Inventory Item                         |
| primary_vendor | WAMGROUP                               |
| uom            | Set                                    |
| is_serialized  | No                                     |
| is_equipment   | Yes                                    |

> 💡 **Why Inventory Item?**
>
> - Creates Inventory record for stock tracking
> - Creates Equipment record for maintenance use
> - No Asset record (spare part)

| Field          | Value                               |
| -------------- | ----------------------------------- |
| item_name      | Motor Oil                           |
| description    | Lubricating oil for conveyor motors |
| item_class     | Consumables                         |
| item_type      | Inventory Item                      |
| primary_vendor | [oil supplier]                      |
| uom            | Ltr                                 |
| is_serialized  | No                                  |
| is_equipment   | No                                  |

> 💡 **Why Inventory Item?**
>
> - Creates Inventory record for stock tracking
> - No Equipment record (consumable fluid)
> - No Asset record (consumable)

> 📝 **TLDR**: For additional items, create appropriate Item Classes first, then follow the same table pattern. Change only: item_name, description, uom, primary_vendor, item_class, is_serialized, is_equipment, and item_type as appropriate.

---

# 🛒 2. Purchase Request Process

Request items for purchase through the automated procurement workflow.

## 📊 Purchase Request Flow Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Create PR     │ →  │   Add PR Lines   │ →  │ Submit PR       │
│  (Draft State)  │    │  (Items & Qty)   │    │ (Start Workflow)│
└─────────────────┘    └──────────────────┘    └─────────────────┘
          │                       │                       │
          ▼                       ▼                       ▼
    ┌─────────────┐        ┌──────────────┐        ┌─────────────┐
    │ PR Details  │        │ Line Details │        │ Workflow    │
    │ - Requestor │        │ - Item       │        │ States      │
    │ - Site      │        │ - Quantity   │        │ Actions     │
    │ - Department│        │ - Cost       │        │ Approvals   │
    └─────────────┘        └──────────────┘        └─────────────┘
```

## 🔄 Purchase Request Workflow

### Purchase Request States & Transitions

| Current State        | Action                  | Next State       | Who Can Act |
| -------------------- | ----------------------- | ---------------- | ----------- |
| **Draft**            | Submit for Review       | Pending Review   | Requestor   |
| **Pending Review**   | Submit for Approval     | Pending Approval | Reviewer    |
| **Pending Approval** | Approve                 | Approved         | Approver    |
| **Pending Approval** | Reject Purchase Request | Rejected         | Approver    |
| **Approved**         | Complete                | Closed           | Requestor   |
| **Rejected**         | Revise Purchase Request | Draft            | Requestor   |

### Purchase Request Line States & Transitions

| Current State          | Action                  | Next State         | Trigger          |
| ---------------------- | ----------------------- | ------------------ | ---------------- |
| **Draft**              | Submit for Approval     | Pending Approval   | PR Approval      |
| **Pending Approval**   | Approve                 | Approved           | Line Approval    |
| **Pending Approval**   | Reject                  | Rejected           | Line Rejection   |
| **Approved**           | Receive Partial Items   | Partially Received | Partial Receipt  |
| **Approved**           | Receive All Items       | Fully Received     | Complete Receipt |
| **Partially Received** | Receive Remaining Items | Fully Received     | Final Receipt    |
| **Fully Received**     | Complete                | Complete           | Process Complete |

---

## 📋 Purchase Request Documents

### Purchase Request

> 📋 Formal request to purchase items needed for operations.

| Field          | Value                                                |
| -------------- | ---------------------------------------------------- |
| date_requested | [current date]                                       |
| requestor      | [employee from Phase 1]                              |
| pr_description | Purchase screw press conveyor for Polomolok          |
| due_date       | [required delivery date]                             |
| site           | Polomolok                                            |
| department     | Maintenance                                          |
| workflow_state | Draft → Pending Review → Pending Approval → Approved |

### Purchase Request Line

> 📝 Individual line items within the purchase request.

| Field             | Value                                                          |
| ----------------- | -------------------------------------------------------------- |
| item              | Screw Press Conveyor Assembly                                  |
| item_description  | Complete screw press conveyor assembly                         |
| vendor            | WAMGROUP                                                       |
| unit_cost         | [quoted price]                                                 |
| unit_of_measure   | Nos                                                            |
| qty_required      | 1                                                              |
| total_line_amount | [auto-calculated]                                              |
| account_code      | [linked account]                                               |
| date_required     | [required delivery date]                                       |
| workflow_state    | Draft → Pending Approval → Approved → Partially/fully Received |

> 💡 **Workflow Note**: Purchase Request Lines follow their own workflow but are triggered by the parent Purchase Request approval. |

---

# 📥 3. Purchase Receipt & Auto-Generation

When items are received, the system automatically creates Inventory and Asset records.

### Purchase Receipt

> ✅ Document confirming items have been received and processed.

| Field                 | Value                         |
| --------------------- | ----------------------------- |
| purchase_request_line | [PR Line from above]          |
| item                  | Screw Press Conveyor Assembly |
| quantity_received     | 1                             |
| date_received         | [actual receipt date]         |
| receiving_location    | Waste Water Treatment Area    |
| site                  | Polomolok                     |
| department            | Maintenance                   |
| generated_inventory   | [auto-set after processing]   |

> 💡 **Automated Process**: When "Confirm Receipt" is clicked, the system automatically creates Inventory, Asset, Equipment, and Maintenance Request records based on Item Type and settings.

> ⏩ **Fast Forward**: For the next PR line, repeat the same Purchase Receipt steps. Only the item, quantity, and serial numbers change.

## 🖱️ UI Instructions for Purchase Receipt Processing

### Step-by-Step Process:

1. **Navigate to Purchase Request**
   - Go to approved Purchase Request (e.g., PR-00001)
   - The **Lines child table** appears below the main form

2. **Access PR Line Form**
   - In the Lines table, **click on any line** to open its form page
   - **Click the "Actions" button** in the form page

3. **Confirm Receipt**
   - Select **"Confirm Receipt"** from the action menu
   - The system will process the receipt automatically

### 🔢 Serial Number Processing (for Serialized Items)

If `is_serialized: true` on the Item:

1. **Single Modal**: One modal appears with input fields for each received unit
2. **Variable Fields**: Number of input fields matches the quantity being received
3. **Enter Serial Numbers**: Type manufacturer serial number for each unit
4. **Automatic Assignment**: Serial numbers populate both Inventory and Asset records

### 📋 Processing Results

After "Confirm Receipt" completes:

- **Inventory records** created/updated automatically
- **Asset records** created for Asset Items
- **Equipment records** created if `is_equipment: true`
- **Maintenance Request** created if `inspection_required: true`
- **Item quantities** updated automatically

---

# 🏭 4. Auto-Generated Records

These records are created automatically during Purchase Receipt processing - **NOT manual creation**.

### Inventory (Auto-Generated)

> 📦 Stock record created automatically when items are received.
>
> 📊 **Location-Based Tracking**: Each inventory record represents stock at a specific location. The Item's `actual_qty_on_hand` is the sum of all inventory `actual_inv` quantities across all locations.

| Field            | Value                         |
| ---------------- | ----------------------------- |
| transaction_type | Add                           |
| date             | [receipt date]                |
| site             | Polomolok                     |
| location         | Waste Water Treatment Area    |
| store_location   | Surallah Main Warehouse       |
| bin_location     | [assigned bin]                |
| item             | Screw Press Conveyor Assembly |
| asset_tag        | SCREW-001                     |
| unit_of_measure  | Nos                           |
| base_unit_cost   | [from PR line]                |
| actual_inv       | 1                             |
| available_inv    | 1                             |

> 💡 **Multiple Locations**: The same item can have multiple inventory records at different sites/locations. Each receipt creates or updates inventory at that specific location.

### Asset (Auto-Generated)

> 🔧 Equipment record created automatically for Asset Items.

| Field             | Value                         |
| ----------------- | ----------------------------- |
| asset_name        | Screw Press Conveyor-001      |
| item              | Screw Press Conveyor Assembly |
| asset_tag         | SCREW-001                     |
| serial_number     | [manufacturer serial]         |
| asset_class       | Rotating Equipment            |
| position          | CONV-LINE-A-01                |
| department        | Maintenance                   |
| installation_date | [receipt date]                |
| status            | Acquired                      |
| warranty_expiry   | [warranty end date]           |

> ✅ **Asset Class Validation**: Matches "Rotating Equipment" created in Phase 1, ensuring consistency across the system.

### Asset Property (Auto-Generated)

> 🔗 Links custom properties to the auto-generated asset.

| Field           | Value                    |
| --------------- | ------------------------ |
| asset           | Screw Press Conveyor-001 |
| property        | Capacity                 |
| property_value  | 50                       |
| unit_of_measure | tons/hour                |
| property_type   | Numeric                  |

---

## Output Records

> ✅ This phase creates the following records:

- 1 Item Class: **Equipment**
- 4 Item master records:
  - **Screw Press Conveyor Assembly** — `Fixed Asset Item`, `is_serialized: true`, `is_equipment: true`
  - **Conveyor Belt** — `Inventory Item`, `is_serialized: false`, `is_equipment: true`
  - **Bearings Set** — `Inventory Item`, `is_serialized: false`, `is_equipment: true`
  - **Motor Oil** — `Inventory Item`, `is_serialized: false`, `is_equipment: false`
- 1 Purchase Request and 1 Purchase Request Line for the conveyor acquisition flow
- 1 Purchase Receipt for the received quantity
- 1 Inventory record for the conveyor example when `quantity_received = 1`
- 1 Asset record for the conveyor example when the Item Type is `Fixed Asset Item`
- 1 Asset Property record linked to the auto-generated conveyor asset
- Inventory-only records for items like **Motor Oil**
- Inventory + Equipment records for items like **Conveyor Belt** and **Bearings Set**

> 🔗 **Reference Values Carried Forward from Phase 1**:
>
> - **Asset Class**: Rotating Equipment
> - **Manufacturer**: WAMGROUP
> - **Model**: Screw Press Conveyor Model S Series
> - **Unit of Measure**: Nos
> - **Position**: CONV-LINE-A-01

> 📌 **Expected Sample Count**:
>
> - **Screw Press Conveyor Assembly**: 1 Purchase Request, 1 Purchase Request Line, 1 Purchase Receipt, 1 Inventory, 1 Asset, 1 Asset Property
> - **Conveyor Belt**: 1 Item, 1 Inventory, 1 Equipment record
> - **Bearings Set**: 1 Item, 1 Inventory, 1 Equipment record
> - **Motor Oil**: 1 Item, 1 Inventory only
>
> If `is_serialized: true` and quantity is greater than 1, the system creates one Inventory and one Asset per received unit.

---

# 🔑 Key Takeaways

- **Item Class → Item** → defines catalog structure
- **Purchase Request → Purchase Receipt** → acquisition workflow
- **Purchase Receipt → Auto-Generate** → Inventory + Assets automatically
- **No manual creation** of Inventory, Asset, or Equipment records
- **Item Type controls** what gets generated (Asset Item = creates Asset)

---

# ⚠️ Completion Rule

Before moving to Phase 2.1, ensure:

- All Item Classes and Items are defined with correct Item Types
- Purchase Request workflow is understood
- Purchase Receipt process creates records automatically
- You can successfully:
  - Create Item ✔
  - Create Purchase Request ✔
  - Process Purchase Receipt and see auto-generated records ✔

If those work, your system is ready for optional Asset Installation in Phase 2.1.
