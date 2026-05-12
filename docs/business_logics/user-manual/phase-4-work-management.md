# Phase 4: Work Management

[Back to Main Manual](./00_EAM_User_Manual.md)

---

## Purpose

Use this phase to execute approved maintenance work using the actual work records in the system:

- `Work Order`
- `Work Order Activity`
- `Work Order Labor`
- `Work Order Parts`
- `Work Order Equipment`
- `Work Order Checklist`
- `Work Order Activity Logs`

This phase covers the full execution flow from work preparation to work closure.

By the end of this phase, you will be able to:

- Review a `Work Order`
- Prepare each `Work Order Activity`
- Assign labor, parts, equipment, and checklists
- Start and execute the work
- Record actual work details
- Complete and close both the `Work Order Activity` and the `Work Order`

---

# 📄 1. Review the Work Order

A `Work Order` is created from a `Maintenance Request`.

1. Open the `Work Order`
2. Confirm the main details:

| Field | What to check |
| ----- | ------------- |
| Type | Preventive Maintenance or Corrective Maintenance |
| Description | Matches the requested work |
| Due Date | Correct target date |
| Priority | Correct urgency |
| Site | Correct site |
| Department | Correct department |

3. Open the **Activities** tab
4. Confirm the linked `Work Order Activity` rows are present

> 📌 A `Work Order` cannot move forward if it has no linked `Work Order Activity` records.

---

# 🧩 2. Review Each Work Order Activity

Each `Work Order Activity` represents an individual work step under the `Work Order`.

1. Open one `Work Order Activity`
2. Confirm these details:

| Field | What to check |
| ----- | ------------- |
| Description | Matches the work to be done |
| Work Item Type | Usually `Asset` for equipment work |
| Work Item | Correct asset |
| Activity Type | Correct request or action type |
| Position | Correct equipment position when applicable |
| Site | Correct site |
| Department | Correct department |

3. Review the linked tabs:

- **Labor**
- **Parts**
- **Equipment**
- **Checklists**
- **Activity Logs**
- **Purchase Requests**
- **Transfers**
- **Item Issues**
- **Item Returns**

---

# 👷 3. Add Work Order Labor

1. Open the `Work Order Activity`
2. Go to **Labor**
3. Add the required `Work Order Labor` rows
4. For each row, fill in the needed labor details
5. During execution, record actual labor time in the labor actual-hours rows

## Why this matters

At least one labor row is required before many `Work Order Activity` records can be allocated successfully.

---

# 🔩 4. Add Work Order Parts

1. Open the `Work Order Activity`
2. Go to **Parts**
3. Add the required `Work Order Parts` rows
4. Enter the planned quantity required for each part

## Important rule before closing

If a part row has a required quantity, the issued quantity must be recorded before the `Work Order Activity` can be closed.

> 📌 If parts are needed, continue with **Phase 4.1: Issuing and Returning Items** before attempting closure.

---

# 🛠️ 5. Add Work Order Equipment

1. Open the `Work Order Activity`
2. Go to **Equipment**
3. Add the required `Work Order Equipment` rows
4. Record actual equipment hours during or after execution

## Important rule before closing

If equipment is used, actual equipment hours must be recorded before the `Work Order Activity` can be closed.

---

# ☑️ 6. Add the Work Order Checklist

1. Open the `Work Order Activity`
2. Go to **Checklists**
3. Review the generated or manually added checklist rows
4. Complete the checklist details during work execution

The checklist is the structured record of what was inspected, confirmed, or completed during the job.

---

# 📝 7. Record Work Order Activity Logs

1. Open the `Work Order Activity`
2. Go to **Activity Logs**
3. Add at least one log entry that describes the work performed

## Important rule before closing

A `Work Order Activity` cannot be closed unless it has `Work Order Activity Logs`.

---

# ✅ 8. Allocate the Work Order Activity

When labor, parts, and equipment are ready:

1. Open the `Work Order Activity`
2. Click **Allocate**
3. Confirm the activity moves from **Awaiting Resources** to **Ready**

## Allocation rules

The system checks the activity before allowing allocation:

- `Work Order` must already be approved
- Labor must exist
- If planned parts are required, parts must be present
- If planned equipment is required, equipment must be present

---

# ▶️ 9. Start the Work Order

1. Return to the `Work Order`
2. Confirm all linked `Work Order Activity` rows are in **Ready**
3. Click **Start** on the `Work Order`

## What the system enforces

A `Work Order` can only start when all linked `Work Order Activity` rows are ready.

---

# 🔧 10. Complete the Work Order Activity

1. Open the `Work Order`
2. Open the target `Work Order Activity`
3. Perform the work
4. Click **Complete** when the work itself is done

## What the system updates

When the `Work Order Activity` is completed, the system can also:

- Update the related `Maintenance Request` closed date
- Update linked asset measurements for date-based maintenance follow-up
- Complete installation or removal actions when the activity type is related to asset movement

---

# 🔒 11. Close the Work Order Activity

After completion, close the `Work Order Activity`.

1. Open the completed `Work Order Activity`
2. Confirm the following are finished:

- `Work Order Activity Logs` exist
- Required part issuance is recorded
- Labor actual hours are recorded
- Equipment actual hours are recorded when equipment was used

3. Click **Close**

## Closing rules

The system will block closure if any required logs, issued quantities, labor hours, or equipment hours are missing.

---

# 🏁 12. Complete the Work Order

After all linked `Work Order Activity` rows are completed or closed:

1. Return to the `Work Order`
2. Confirm every linked activity is finished
3. Click **Complete**

A `Work Order` can only be completed when all linked `Work Order Activity` records are already in `Completed` or `Closed`.

---

# 📋 13. Records Created or Updated

This phase creates or updates the following:

- `Work Order`
- `Work Order Activity`
- `Work Order Labor`
- `Work Order Labor Actual Hours`
- `Work Order Parts`
- `Work Order Equipment`
- `Work Order Equipment Actual Hours`
- `Work Order Checklist`
- `Work Order Checklist Detail`
- `Work Order Activity Logs`
- `Maintenance Request`
- `Asset`

---

# 🔗 Dependencies

- Phase 3: Maintenance Management
- Phase 3.1: Emergency Maintenance
- Phase 4.1: Issuing and Returning Items
