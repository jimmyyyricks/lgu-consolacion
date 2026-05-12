# Item Issue & Item Return — Step-by-Step

## Overview

This is the normal operational flow for issuing parts/equipment to a Work Order Activity, then returning unused items back to inventory.

```text
Maintenance Request / Work Order
  → Work Order Activity
  → Work Order Parts or Work Order Equipment
  → Item Issue
  → Item Return
```

The important system effects are:

- `work_order_parts.quantity_issued` increases on issue
- `work_order_parts.quantity_returned` increases on return
- `inventory.actual_inv` and `inventory.available_inv` go down on issue
- `inventory.actual_inv` and `inventory.available_inv` go up on return
- `item.actual_qty_on_hand` and `item.available_capacity` follow the same movement
- Equipment issue/return also updates custodian and asset state

---

## Step 1 — Create the Work Order path

Create or progress the upstream records until you have:

- a **Work Order**
- a **Work Order Activity** linked to that Work Order

The Work Order Activity is the anchor used by:

- `work_order_parts`
- `work_order_equipment`
- `item_issue`
- `item_return`

---

## Step 2 — Add required resources to the Work Order Activity

### For parts issue

Create one or more **Work Order Parts** records linked to the same `work_order_activity`.

Important fields:

- `item`
- `quantity_required`
- `quantity_issued` starts at `0`
- `quantity_returned` starts at `0`

### For equipment issue

Create one or more **Work Order Equipment** records linked to the same `work_order_activity`.

Important fields:

- `equipment`
- the equipment should be linked to an `inventory` record if it will be returned through the equipment return flow

---

## Step 3 — Create the Item Issue record

Create an **Item Issue** in state `Requested`.

Important fields:

- `issue_type`
  - `WO Parts Issue`
  - `WO Equipment Issue`
- `issue_to`
- `work_order_activity`

Then add one or more **Item Issue Line** rows.

### For parts

Each line should contain:

- `work_order_parts`
- `inventory`
- `quantity_issued`

### For equipment

Each line should contain:

- `work_order_equipment`
- `inventory`
- `quantity_issued`

---

## Step 4 — Run **Issue Item**

Trigger workflow action:

- `Requested` → `Issue_Item` → `Issued`

### System validations

The action fails if:

- there are no item issue lines
- any line has `quantity_issued <= 0`
- any line has no `inventory`
- inventory does not have enough `actual_inv`
- inventory does not have enough `available_inv`
- `WO Parts Issue` line has no `work_order_parts`
- `WO Equipment Issue` line has no `work_order_equipment`

### System updates

#### For WO Parts Issue

Per line:

- `work_order_parts.quantity_issued += quantity_issued`
- `inventory.actual_inv -= quantity_issued`
- `inventory.available_inv -= quantity_issued`
- `item.actual_qty_on_hand -= quantity_issued`
- `item.available_capacity -= quantity_issued`

#### For WO Equipment Issue

Per line:

- equipment `custodian = item_issue.issue_to`
- linked asset moves to active/in-use state by workflow side effect
- `inventory.actual_inv -= quantity_issued`
- `inventory.available_inv -= quantity_issued`
- `item.actual_qty_on_hand -= quantity_issued`
- `item.available_capacity -= quantity_issued`

### User-facing result

The backend now returns readable messages such as:

- `Item Pump Seal qty 2 has been issued to Work Order Parts WOP-00012. Qty issued is now 2.`
- `Item Pump Seal qty 2 has been deducted from inventory INV-00045. Remaining actual inventory: 18, available inventory: 18.`
- `Equipment Portable Welder has been issued to EMP-0003. Custodian updated successfully.`

---

## Step 5 — Use or complete the Work Order Activity

Once issue is done, the Work Order Activity can continue through its normal workflow.

Typical expectation:

- parts/equipment are now considered assigned/used for the activity
- `quantity_issued` on Work Order Parts reflects what was actually released from stores

---

## Step 6 — Create the Item Return record

Create an **Item Return** in state `Received`.

Important fields:

- `return_type`
  - `WO Parts Return`
  - `WO Equipment Return`
- `work_order_activity`

Then add one or more **Item Return Line** rows.

### For parts return

Each line should contain:

- `work_order_parts`
- `inventory` if known
- `quantity_returned`

### For equipment return

Each line should contain:

- `work_order_equipment`
- `quantity_returned`

---

## Step 7 — Run **Return Item**

Trigger workflow action:

- `Received` → `Return_Item` → `Returned`

### System validations

The action fails if:

- Item Return is not in `Received`
- there are no item return lines
- any line has `quantity_returned <= 0`
- a `putaway` already exists for `source_data_parts_return = line.id`
- parts return quantity is greater than `work_order_parts.quantity_issued`
- equipment return line has no `work_order_equipment`
- equipment has no linked inventory to receive the return

### System updates

#### For WO Parts Return

Per line:

- create `putaway` with `putaway_type = "Item Return"`
- `work_order_parts.quantity_returned += quantity_returned`
- `work_order_parts.quantity_issued -= quantity_returned`
- `inventory.actual_inv += quantity_returned`
- `inventory.available_inv += quantity_returned`
- `item.actual_qty_on_hand += quantity_returned`
- `item.available_capacity += quantity_returned`

#### For WO Equipment Return

Per line:

- create `putaway` using inventory store/bin/zone/serial data
- clear equipment `custodian`
- linked asset moves back to inactive/putaway state by workflow side effect
- `inventory.actual_inv += quantity_returned`
- `inventory.available_inv += quantity_returned`
- `item.actual_qty_on_hand += quantity_returned`
- `item.available_capacity += quantity_returned`

### User-facing result

The backend now returns readable messages such as:

- `Item Pump Seal qty 1 has been returned from Work Order Parts WOP-00012. Qty returned is now 1 and qty issued is now 1.`
- `Item Pump Seal qty 1 has been added back to inventory INV-00045. Current actual inventory: 19, available inventory: 19.`
- `Equipment Portable Welder qty 1 has been returned. Custodian cleared and putaway created successfully.`

---

## Step 8 — Complete the records

After operational processing:

- `Item Issue`: `Issued` → `Complete` → `Closed`
- `Item Return`: `Returned` → `Complete` → `Closed`

These completion actions do not add extra business logic. They just close the records.

---

## Quick Verification Checklist

After a full issue + return simulation, verify:

- **Work Order Parts**
  - `quantity_issued` increased on issue
  - `quantity_returned` increased on return
  - `quantity_issued` decreased back correctly after return

- **Inventory**
  - qty decreased on issue
  - qty increased on return

- **Item**
  - `actual_qty_on_hand` decreased on issue
  - `actual_qty_on_hand` increased on return

- **Equipment**
  - `custodian` set on issue
  - `custodian` cleared on return

- **Asset**
  - asset becomes active/in-use on equipment issue
  - asset becomes inactive/putaway on equipment return

---

## Common Errors

| Error                                                    | Meaning                                |
| -------------------------------------------------------- | -------------------------------------- |
| `no Item Issue Lines found`                              | You tried to issue without child rows  |
| `insufficient actual inventory`                          | Physical stock is too low              |
| `insufficient available inventory`                       | Available stock is too low             |
| `work_order_equipment is required`                       | Equipment issue line is incomplete     |
| `cannot return qty ... because only ... has been issued` | User is returning more than was issued |
| `Putaway record already exists`                          | Same return line was already processed |
| `Expected state: Received`                               | Item Return workflow state is wrong    |

---

## Bottom Line

Use **Item Issue** to reduce inventory and push quantities into the Work Order resource records.

Use **Item Return** to create the putaway trail and restore inventory correctly.

If the messages are shown to the user, they are now human-readable enough to explain:

- what item/equipment moved
- how much moved
- what record was updated
- what the resulting quantity is

---

## Verification

- **Command:** `PYTHONPATH=backend python backend/tests/test_item_issue_return_e2e.py`
- **Status:** 61/61 passed
- **What it covers:**
  - Item Issue validations: no lines, >0 qty, inventory availability, required links for parts/equipment
  - Item Issue effects: inventory/item deductions, WO Parts qty_issued updates, equipment custodian update
  - Item Return validations: correct workflow state, no lines, duplicate putaway guard, >0 qty, over-return blocked, required links/inventory
  - Item Return effects: inventory/item restoration, WO Parts qty_returned/qty_issued updates, equipment custodian cleared, asset inactive on return
  - HTTP integration smoke: metadata fields, Issue_Item guard with no lines, options filtering
