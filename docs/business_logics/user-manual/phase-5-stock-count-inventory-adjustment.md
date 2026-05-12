# Phase 5: Stock Count and Inventory Adjustment

[Back to Main Manual](./00_EAM_User_Manual.md)

---

## Purpose

Use this phase to verify actual stock in the warehouse and reconcile any variance through an `Inventory Adjustment`.

This phase uses the actual inventory-control records in the system:

- `Stock Count`
- `Stock Count Line`
- `Inventory Adjustment`
- `Inventory Adjustment Line`

By the end of this phase, you will be able to:

- Prepare a `Stock Count`
- Generate or add `Stock Count Line` rows
- Capture counted quantities
- Review variances
- Create an `Inventory Adjustment`
- Post the `Inventory Adjustment` to update inventory quantities

---

# 📋 1. Create the Stock Count Header

1. Go to **Stock Count** → **New**
2. Fill in the header:

| Field | Value | Notes |
| ----- | ----- | ----- |
| Store | `Surallah Main Warehouse` | Required |
| Site | `Polomolok` | Fetched from the store |
| Method | `Guided` or `Blind` | Counting method |
| Basis | `Full`, `ABC`, or `Selection` | Counting scope |
| ABC Code | `A`, `B`, or `C` | Required only when Basis = `ABC` |
| Freeze Policy | `None`, `Freeze`, or `Warn` | Controls inventory handling during the count |

---

# 🔍 2. Generate or Add Stock Count Lines

## Option A: Full or ABC count

1. Save the `Stock Count`
2. Click **Find Stock Count Lines**

## What the system does

The system creates `Stock Count Line` rows based on the selected basis:

- **Full** → all matching inventory in the selected store
- **ABC** → only inventory for items in the selected ABC class
- **Selection** → no automatic lines; the user adds lines manually

The system also excludes:

- Inventory already tied to another `Stock Count` that is still in progress
- Inventory already marked as frozen
- Duplicate lines for the same stock count, item, bin, and zone

## Option B: Manual selection

If **Basis = Selection**:

1. Add `Stock Count Line` rows manually
2. Fill in the item and storage details you want to count

---

# 📸 3. Start the Stock Count

Before the team begins counting:

1. Confirm the `Stock Count` has lines
2. Click **Start Stock Count**

## What the system does

When the count starts, the system:

- Captures `snapshot_at`
- Applies the selected freeze policy to the linked `Inventory` records

## Freeze policy behavior

- **None** → no warning or freeze is applied
- **Warn** → inventory is flagged with a warning during the count
- **Freeze** → inventory is locked during the count

> 📌 A `Stock Count` cannot start unless it already has at least one `Stock Count Line`.

---

# 🧮 4. Enter Counted Quantities

1. Open each `Stock Count Line`
2. Enter the `Counted Qty`

## What the system calculates automatically

As the counted quantity is saved, the system calculates:

- `Variance Qty`
- `Variance Value`

Key line fields:

| Field | Meaning |
| ----- | ------- |
| Snapshot Qty | Quantity captured from inventory when the line was created |
| Counted Qty | Physical quantity counted by the user |
| Variance Qty | Difference between snapshot and counted quantity |
| Variance Value | Financial value of the variance |
| Variance Reason | Optional reason code |
| Is Reconciled | Set by the system after approval |

---

# ✅ 5. Approve the Stock Count

After all lines are counted and reviewed:

1. Open the `Stock Count`
2. Review the variance lines
3. Click **Approve**

## What the system checks before approval

The system will block approval if the result would create negative inventory on any line.

## What the system does on approval

When approval succeeds, the system:

- Creates one `Inventory Adjustment`
- Creates `Inventory Adjustment Line` rows for the variance lines
- Marks all `Stock Count Line` rows as reconciled
- Clears any freeze or warning flags on the linked `Inventory` records

> 📌 If all counted quantities match the snapshot exactly, the stock count can still be approved even though no variance adjustment lines are needed.

---

# 📄 6. Review the Inventory Adjustment

After approval:

1. Open the linked `Inventory Adjustment`
2. Review the header:

| Field | What to check |
| ----- | ------------- |
| Source Stock Count | Linked stock count |
| Reference DocType | `Inventory` |
| Location | Store location |
| Store | Correct store |
| Site | Correct site |
| Remarks | Auto-generated stock count reference |

3. Review the `Inventory Adjustment Line` rows

Important line fields:

| Field | Meaning |
| ----- | ------- |
| Inventory | Existing inventory record, if one already exists |
| Item | The adjusted item |
| Asset Tag | Asset reference when applicable |
| Serial Nos | Serial reference when applicable |
| Bin | Bin location |
| Zone | Zone location |
| UoM | Unit of measure |
| Current Qty | Snapshot quantity |
| Adjustment Qty | Variance quantity to post |
| Current Rate | Current unit cost |
| Delta Value | Financial value of the adjustment |

---

# 📤 7. Submit the Inventory Adjustment

1. Open the `Inventory Adjustment`
2. Confirm it has at least one line
3. Click **Submit**

A header with no lines cannot be submitted.

---

# 🧾 8. Post the Inventory Adjustment

1. Open the submitted `Inventory Adjustment`
2. Click **Post**

## What the system does on posting

For each `Inventory Adjustment Line`, the system will:

- Update an existing `Inventory` record when one already exists, or
- Create a new `Inventory` record when the line has no linked inventory record

The system also:

- Prevents posting if the final quantity would become negative
- Clears freeze and warning flags on the adjusted inventory
- Stamps the `posting_datetime`
- Recalculates the total on-hand quantity on the linked `Item`

---

# 🏁 9. Complete the Stock Count

After the related `Inventory Adjustment` has been reviewed and posted:

1. Return to the `Stock Count`
2. Click **Complete**

This closes the stock count cycle for that batch of counted lines.

---

# 📋 10. Records Created or Updated

This phase creates or updates the following:

- `Stock Count`
- `Stock Count Line`
- `Inventory Adjustment`
- `Inventory Adjustment Line`
- `Inventory`
- `Item`

---

# 🔗 Dependencies

- Phase 1: Setting Up
- Phase 2: Item Acquisition and Procurement
- Phase 4.1: Issuing and Returning Items
