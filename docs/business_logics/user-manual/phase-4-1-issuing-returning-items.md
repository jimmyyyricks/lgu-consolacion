# Phase 4.1: Issuing and Returning Items

[Back to Main Manual](./00_EAM_User_Manual.md)

---

## Purpose

Use this phase when a `Work Order Activity` needs parts or equipment to be issued, and when unused items or borrowed equipment must be returned.

This phase uses the actual inventory transaction records in the system:

- `Item Issue`
- `Item Issue Line`
- `Item Return`
- `Item Return Line`
- `Putaway`

By the end of this phase, you will be able to:

- Issue parts to a `Work Order Activity`
- Issue equipment to a `Work Order Activity`
- Return unused parts
- Return borrowed equipment
- Keep inventory quantities accurate

---

# 📦 1. Issue Parts for a Work Order Activity

Use this when the mechanic is ready to consume parts during work.

1. Open the target `Work Order Activity`
2. Review the **Parts** tab
3. Confirm the required rows already exist in `Work Order Parts`
4. Go to **Item Issue** → **New**
5. Fill in the header:

| Field | Value |
| ----- | ----- |
| Issue Type | `WO Parts Issue` |
| Issue To | [responsible employee] |
| Date Issued | [today] |
| Work Order Activity | [linked activity] |

6. Add one or more `Item Issue Line` rows
7. For each row, fill in:

| Field | Value |
| ----- | ----- |
| Inventory | [selected inventory record] |
| Work Order Parts | [matching `Work Order Parts` row] |
| Quantity Issued | [actual issued quantity] |

8. Click **Issue Item**

## What the system does

When the issue is successful, the system:

- Increases `quantity_issued` on the linked `Work Order Parts`
- Reduces `actual_inv` and `available_inv` on the selected `Inventory`
- Reduces `actual_qty_on_hand` and `available_capacity` on the linked `Item`

> 📌 The issue will fail if there are no lines, if the quantity is zero, or if the selected inventory does not have enough stock.

---

# 🛠️ 2. Issue Equipment for a Work Order Activity

Use this when the work needs a tracked equipment item.

1. Go to **Item Issue** → **New**
2. Fill in the header:

| Field | Value |
| ----- | ----- |
| Issue Type | `WO Equipment Issue` |
| Issue To | [custodian / employee] |
| Date Issued | [today] |
| Work Order Activity | [linked activity] |

3. Add one or more `Item Issue Line` rows
4. For each row, fill in:

| Field | Value |
| ----- | ----- |
| Inventory | [equipment inventory record] |
| Work Order Equipment | [matching `Work Order Equipment` row] |
| Quantity Issued | `1` or the actual quantity |

5. Click **Issue Item**

## What the system does

When equipment is issued, the system:

- Updates the related `Equipment` custodian
- Updates the related `Asset` status when applicable
- Reduces the selected inventory quantity
- Reduces the linked item quantity

---

# ↩️ 3. Return Unused Parts

Use this when parts were issued but not fully consumed.

1. Go to **Item Return** → **New**
2. Fill in the header:

| Field | Value |
| ----- | ----- |
| Return Type | `WO Parts Return` |
| Returned By | [employee] |
| Date Returned | [today] |
| Work Order Activity | [linked activity] |

3. Add one or more `Item Return Line` rows
4. For each row, fill in:

| Field | Value |
| ----- | ----- |
| Work Order Parts | [matching part row] |
| Inventory | [original inventory record, if available] |
| Quantity Returned | [actual returned quantity] |

5. Click **Return Item**

## What the system does

When a parts return is successful, the system:

- Creates a `Putaway` record
- Increases `quantity_returned` on `Work Order Parts`
- Decreases the remaining `quantity_issued` on `Work Order Parts`
- Restores inventory quantity
- Restores item quantity

> 📌 The return will fail if the quantity being returned is greater than the quantity already issued.

---

# 🔁 4. Return Equipment

Use this when borrowed equipment is no longer needed.

1. Go to **Item Return** → **New**
2. Fill in the header:

| Field | Value |
| ----- | ----- |
| Return Type | `WO Equipment Return` |
| Returned By | [employee] |
| Date Returned | [today] |
| Work Order Activity | [linked activity] |

3. Add one or more `Item Return Line` rows
4. For each row, fill in:

| Field | Value |
| ----- | ----- |
| Work Order Equipment | [matching equipment row] |
| Quantity Returned | [actual quantity] |

5. Click **Return Item**

## What the system does

When the equipment return is successful, the system:

- Creates a `Putaway` record
- Clears the equipment custodian
- Returns the related asset to `Inactive` when applicable
- Restores inventory quantity

---

# ✅ 5. Complete the Inventory Transactions

After the issue or return is processed:

1. Open the `Item Issue` or `Item Return` record
2. Review the resulting lines and quantities
3. Click **Complete** when the transaction is finished

This moves the transaction to its final closed state.

---

# 📋 6. Records Created or Updated

This phase creates or updates the following:

- `Item Issue`
- `Item Issue Line`
- `Item Return`
- `Item Return Line`
- `Putaway`
- `Work Order Parts`
- `Work Order Equipment`
- `Inventory`
- `Item`
- `Equipment`
- `Asset`

---

# 🔗 Dependencies

- Phase 4: Work Management
- Phase 2: Item Acquisition and Procurement
- Phase 1: Setting Up
