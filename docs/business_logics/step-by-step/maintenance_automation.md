---
description: Complete maintenance management step-by-step guide — planning, triggering, executing, and closing maintenance work
---

# Maintenance Management — Complete Step-by-Step Guide

## Overview

This document covers the full lifecycle of maintenance work in the system: from setting up the planning foundation, through automated generation of work packages via scheduler triggers, to executing and closing the work.

```text
Asset Class
  └─ Maintenance Plan
       └─ Planned Maintenance Activity (PMA)
            ├─ Maintenance Calendar  ──┐
            ├─ Maintenance Interval  ──┼─ Scheduler runs → Work Package created
            └─ Maintenance Condition ──┘
                                           ↓
                                  Maintenance Request (approved)
                                  Work Order (requested)
                                  Work Order Activity (awaiting_resources)
                                           ↓
                         Assign Labor → Allocate → Start Activity → Complete
                                           ↓
                                  Asset returns to active
                                  MR closed_date set
```

---

## Workflow State Reference

### Asset

| State               | Meaning                                                         |
| ------------------- | --------------------------------------------------------------- |
| `acquired`          | Asset is registered but not yet active                          |
| `inspected`         | Asset passed inspection                                         |
| `failed_inspection` | Asset failed inspection                                         |
| `active`            | Asset is live and in use                                        |
| `inactive`          | Asset is stored, not in use                                     |
| `under_maintenance` | Asset is being maintained (set automatically on Start Activity) |
| `under_repair`      | Asset is in internal or vendor repair                           |
| `decommissioned`    | Asset retired from service                                      |
| `disposed`          | Asset permanently removed                                       |

**Asset transitions relevant to maintenance:**

| From                | Action           | To                  |
| ------------------- | ---------------- | ------------------- |
| `active`            | `maintain_asset` | `under_maintenance` |
| `under_maintenance` | `complete`       | `active`            |
| `under_maintenance` | `remove_asset`   | `inactive`          |

### Maintenance Request

| State              | Meaning                                              |
| ------------------ | ---------------------------------------------------- |
| `draft`            | Created manually, not yet submitted                  |
| `pending_approval` | Submitted for review                                 |
| `approved`         | Approved — PM-generated MRs start here automatically |
| `release`          | Released for execution                               |
| `completed`        | Work is done, `closed_date` is set                   |

**Maintenance Request transitions:**

| From               | Action                  | To                 |
| ------------------ | ----------------------- | ------------------ |
| `draft`            | `submit_for_approval`   | `pending_approval` |
| `draft`            | `submit_for_emergency`  | `release`          |
| `pending_approval` | `approve`               | `approved`         |
| `approved`         | `submit_for_resolution` | `release`          |
| `release`          | `complete`              | `completed`        |
| `completed`        | `reopen`                | `release`          |

> **Note:** Maintenance Requests created by the PM scheduler are automatically set to `approved`, bypassing `draft` and `pending_approval`.

> **For Work Order and Work Order Activity workflows, see:** [Work Order Execution Guide](work_order_execution.md)

---

## Part 1 — Setting Up the Planning Foundation

### Step 1.1 — Create an Asset Class

Every maintenance plan targets an asset class. Create one if it does not exist.

```http
POST /api/entity/asset_class/action
{
  "action": "create",
  "data": {
    "name": "Office Desktop Computer",
    "description": "Standard finance department desktop computers",
    "due_date_lead_time": 3
  }
}
```

`due_date_lead_time` controls how many days ahead of the scheduled date the WOA due date is set.

### Step 1.2 — Create a Maintenance Activity

A Maintenance Activity defines the work to be done. It holds child rows for parts, trade, and equipment.

```http
POST /api/entity/maintenance_activity/action
{
  "action": "create",
  "data": {
    "activity_name": "Monthly Computer PM",
    "description": "Clean fans, verify OS updates, check hardware"
  }
}
```

Optionally add child rows:

- `maintenance_parts` — spare parts required
- `maintenance_trade` — trade skill required
- `maintenance_equipment` — tools or equipment required

These are copied into the WOA resource tabs when the work package is created.

### Step 1.3 — Create a Checklist (optional)

```http
POST /api/entity/checklist/action
{
  "action": "create",
  "data": {
    "checklist_name": "Computer PM Checklist",
    "checklist_type": "Preventive Maintenance"
  }
}
```

Add checklist items as `checklist_details` child rows. These are copied to the WOA when the work package is created.

### Step 1.4 — Create a Maintenance Plan

A Maintenance Plan links a maintenance strategy to an asset class.

```http
POST /api/entity/maintenance_plan/action
{
  "action": "create",
  "data": {
    "description": "Finance office computer PM plan",
    "asset_class": "<asset_class_id>"
  }
}
```

### Step 1.5 — Create a Planned Maintenance Activity (PMA)

A PMA links a plan to a specific activity with a schedule type.

```http
POST /api/entity/planned_maintenance_activity/action
{
  "action": "create",
  "data": {
    "maintenance_plan": "<plan_id>",
    "maintenance_activity": "<activity_id>",
    "checklist": "<checklist_id>",
    "maintenance_schedule": "Calendar Based",
    "maintenance_type": "<request_activity_type_id>"
  }
}
```

`maintenance_type` is the ID of a `request_activity_type` record. The `menu` field of that record controls WOA business logic (e.g. `"Maintain Asset"` triggers asset state changes).

`maintenance_schedule` options: `Calendar Based`, `Interval`, `Condition Based`.

---

## Part 2 — Setting Up a Trigger

### Calendar-Based Trigger

Create a `maintenance_calendar` record linked to the PMA.

Required fields:

- `frequency` — Weekly, Monthly, Quarterly, Annually, Day of Week, Day of Month
- `lead_calendar_days` — days before due date to create the work package
- `last_maintenance_date_property` — asset property storing the last maintenance date

**Real life example:** A building's fire extinguishers need annual inspection.

- `frequency`: Annually (365 days)
- `lead_calendar_days`: 30 (create work order 30 days before due date)
- `last_maintenance_date_property`: links to "Last Inspection Date" asset property
- Trigger logic: If (Last Inspection Date + 365 days - 30 days) <= today, create Maintenance Request

```http
POST /api/entity/maintenance_calendar/action
{
  "action": "create",
  "data": {
    "planned_maintenance_activity": "<pma_id>",
    "maintenance_plan": "<plan_id>",
    "maintenance_activity": "<activity_id>",
    "frequency": "Monthly",
    "lead_calendar_days": 3,
    "last_maintenance_date_property": "<property_id>"
  }
}
```

**How it fires:** The scheduler runs daily. For each calendar, it finds all active assets for the plan's asset class. For each asset, it reads the `last_maintenance_date_property` value (a `Date` type property on the asset). If the next due date (last date + frequency days − lead days) is today or earlier, a work package is created.

If `last_maintenance_date_property` is not set or has no value for the asset, the trigger fires immediately.

**Frequency → days mapping:**

| Frequency    | Days |
| ------------ | ---- |
| Weekly       | 7    |
| Monthly      | 30   |
| Quarterly    | 90   |
| Annually     | 365  |
| Day of Week  | 7    |
| Day of Month | 30   |

### Interval-Based Trigger

Create a `maintenance_interval` record.

Required fields:

- `running_interval_property` — property holding the current meter reading (e.g. km driven)
- `last_interval_property` — property holding the meter reading at the last PM
- `interval` — the interval threshold (e.g. 10000 km)
- `lead_interval` — how many units before the threshold to trigger (e.g. 500 km)

**Real life example:** A forklift needs oil change every 500 operating hours.

- `interval`: 500
- `running_interval_property`: links to the forklift's "Operating Hours" asset property
- `last_interval_property`: links to the forklift's "Last Oil Change Hours" property
- `lead_interval`: 48 (hours before deadline to create the Maintenance Request)
- Trigger logic: When (Current Operating Hours - Last Oil Change Hours) >= 500, the system creates a Maintenance Request 48 hours before the 500-hour deadline.

**How it fires:** If `running_value − last_value >= interval − lead_interval`, a work package is created.

### Condition-Based Trigger

Create a `maintenance_condition` record.

Required fields:

- `sensor` — the sensor to read
- `threshold_property` — the asset property holding the threshold value
- `comparison_operator` — `>`, `>=`, `<`, `<=`, `==`, `!=`

**Real life example:** A server room temperature sensor triggers when it gets too hot.

- `sensor`: links to "Server Room Temp" sensor
- `threshold_property`: links to "Max Temperature Threshold" asset property (e.g., 28°C)
- `comparison_operator`: `>=`
- `threshold_value`: 28
- Trigger logic: When latest sensor reading >= 28°C, create emergency Maintenance Request

**How it fires:** The latest `sensor_data` reading is compared to the asset's threshold property value. If the condition is met, a work package is created.

---

## Part 3 — Creating an Asset

Assets must be `active` and belong to the plan's `asset_class` to receive work packages.

```http
POST /api/entity/asset/action
{
  "action": "create",
  "data": {
    "asset_tag": "PC-FIN-001",
    "description": "Finance office desktop",
    "asset_class": "<asset_class_id>",
    "site": "<site_id>",
    "department": "<department_id>",
    "item_type": "Asset Item",
    "workflow_state": "active"
  }
}
```

For calendar triggers, create the `last_maintenance_date_property` asset property value with a past date so the trigger fires immediately in testing:

```http
POST /api/entity/asset_property/action
{
  "action": "create",
  "data": {
    "asset": "<asset_id>",
    "property": "<last_pm_property_id>",
    "property_value": "2026-02-10"
  }
}
```

---

## Part 4 — Triggering PM Generation

### Via Scheduler (production)

The scheduler runs automatically at these times:

| Time    | Trigger                    |
| ------- | -------------------------- |
| `01:00` | Calendar-based generation  |
| `02:00` | Interval-based generation  |
| `03:00` | Condition-based generation |

### Via Manual API (development / testing)

Three test endpoints are available to fire each generator on demand:

```http
POST /api/test/scheduler/calendar-check
POST /api/test/scheduler/interval-check
POST /api/test/scheduler/condition-check
```

These call the same functions as the scheduler — there is no difference in behaviour.

### What gets created

A successful trigger creates one **pre-work package** per qualifying asset:

| Record                | Initial State        | Key Fields                                                                  |
| --------------------- | -------------------- | --------------------------------------------------------------------------- |
| `maintenance_request` | `approved`           | `planned_maintenance_activity`, `asset`, `work_order_activity`              |
| `work_order_activity` | `awaiting_resources` | `work_order = null`, `work_item` (asset), `activity_type`, `work_item_type` |

Then, when the user runs **Submit for Resolution** on the MR, the system creates:

| Record       | Initial State | Key Fields                                          |
| ------------ | ------------- | --------------------------------------------------- |
| `work_order` | `requested`   | `site`, `department`, `due_date`, `work_order_type` |

and links the existing WOA to the newly created Work Order.

---

## Part 5 — Executing the Work

This is the operational flow after a work package is created.

### Step 5.1 — Assign Work Order Labor

```http
POST /api/entity/work_order_labor/action
{
  "action": "create",
  "data": {
    "work_order_activity": "<woa_id>",
    "trade": "<trade_id>",
    "labor": "<labor_id>",
    "lead": true,
    "estimated_hours": 1.5
  }
}
```

### Step 5.2 — Allocate the WOA

`awaiting_resources` → `ready`

```http
POST /api/entity/work_order_activity/workflow
{
  "action": "Allocate",
  "id": "<woa_id>"
}
```

**Validation:** If the WOA is linked to a PMA, allocation checks that labor is assigned. If the PMA's Maintenance Activity has equipment or parts defined, those must also be assigned. If the WOA has no PMA link, only labor is checked.

### Step 5.3 — Start the Activity

`ready` → `in_progress`

```http
POST /api/entity/work_order_activity/workflow
{
  "action": "Start Activity",
  "id": "<woa_id>"
}
```

**Side-effect:** If `work_item_type = "Asset"` and `activity_type` maps to `"Maintain Asset"`, the linked asset is automatically transitioned from `active` → `under_maintenance`.

### Step 5.4 — Put On Hold (optional)

`in_progress` → `on_hold`

```http
POST /api/entity/work_order_activity/workflow
{ "action": "Put On Hold", "id": "<woa_id>" }
```

Resume with:

```http
POST /api/entity/work_order_activity/workflow
{ "action": "Resume", "id": "<woa_id>" }
```

### Step 5.5 — Complete the Activity

`in_progress` → `completed`

```http
POST /api/entity/work_order_activity/workflow
{
  "action": "Complete",
  "id": "<woa_id>"
}
```

**Side-effects (when activity type = "Maintain Asset"):**

- Asset `workflow_state` → `active`
- Asset `need_repair` → `False`
- `maintenance_request.closed_date` → today's date
- If the MR has a `property` linked, the corresponding `asset_property` value is updated to today's date

### Step 5.6 — Close the WOA (optional)

`completed` → `closed`

```http
POST /api/entity/work_order_activity/workflow
{ "action": "Close", "id": "<woa_id>" }
```

**Validation:** Requires activity logs, labor actual hours, and equipment actual hours to all be present.

---

## Part 6 — Closing the Work Order

After all WOAs are completed or closed, progress the Work Order:

```http
POST /api/entity/work_order/workflow
{ "action": "Complete", "id": "<wo_id>" }
```

`in_progress` → `closed`

**Validation:** All linked WOAs must be in `completed` or `closed`.

---

## Full E2E Summary

```text
1.  Create Asset Class
2.  Create Maintenance Activity  (+ optional Parts / Trade / Equipment children)
3.  Create Checklist             (+ Checklist Details children)
4.  Create Maintenance Plan      (link → asset_class)
5.  Create Planned Maintenance Activity (link → plan + activity + checklist)
6.  Create Maintenance Calendar  (link → PMA, set frequency)
7.  Create Property (Date type)  — "Last PM Date"
8.  Update Maintenance Calendar  — set last_maintenance_date_property
9.  Create Asset                 (workflow_state = active, asset_class = plan's class)
10. Create Asset Property        — set last PM date to a past date
11. POST /api/test/scheduler/calendar-check
12. Verify: MR (approved) + WOA (awaiting_resources) created; WOA has no WO yet
13. Workflow: Maintenance Request → Submit for Resolution
14. Verify: WO (requested) created and existing WOA is linked to that WO
15. Create Work Order Labor on WOA
16. Workflow: WOA → Allocate          (awaiting_resources → ready)
17. Workflow: WOA → Start Activity    (ready → in_progress; asset → under_maintenance)
18. Workflow: WOA → Complete          (in_progress → completed; asset → active; MR.closed_date set)
```

---

## Verification

**E2E test command:**

```bash
python backend/tests/test_computer_pm_flow_e2e.py
```

**Expected result:** 34/34 checks pass.

**What it covers:**

- Reference data setup (asset class, activity, checklist, plan, PMA)
- Calendar trigger record creation
- Property creation and asset property linkage
- Server-side calendar scheduler invocation
- Trigger generation (MR + WOA only)
- Submit for Resolution generation (WO and link to existing WOA)
- Initial workflow states on all created records
- Labor assignment
- WOA Allocate → Start Activity → Complete transitions
- Asset state changes (active → under_maintenance → active)
- MR closed_date set on completion

---

## Quick Verification Checklist

After PM generation, check these fields:

| Record                | Field                          | Expected Value                      |
| --------------------- | ------------------------------ | ----------------------------------- |
| `maintenance_request` | `workflow_state`               | `approved`                          |
| `maintenance_request` | `planned_maintenance_activity` | matches PMA                         |
| `maintenance_request` | `asset`                        | matches asset                       |
| `maintenance_request` | `work_order_activity`          | filled                              |
| `work_order_activity` | `workflow_state`               | `awaiting_resources`                |
| `work_order_activity` | `work_order`                   | `null` before Submit for Resolution |
| `work_order_activity` | `work_item`                    | matches asset                       |
| `work_order_activity` | `activity_type`                | matches `maintenance_type` from PMA |

After **Submit for Resolution**:

| Record                | Field            | Expected Value |
| --------------------- | ---------------- | -------------- |
| `work_order`          | `workflow_state` | `requested`    |
| `work_order_activity` | `work_order`     | matches WO     |

After WOA completion:

| Record                | Field            | Expected Value |
| --------------------- | ---------------- | -------------- |
| `work_order_activity` | `workflow_state` | `completed`    |
| `asset`               | `workflow_state` | `active`       |
| `maintenance_request` | `closed_date`    | today          |

---

## Common Errors

| Error                                      | Cause                                                                                   | Fix                                                                                            |
| ------------------------------------------ | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| No MR/WO/WOA created after trigger         | Trigger condition not met (date not past, interval not reached, sensor OK)              | Set asset property value to a past date / set sensor reading above threshold                   |
| `ForeignKeyViolationError` on `department` | `department` value does not exist in DB                                                 | Fetch a real department ID via `GET /api/entity/department/list` before creating assets        |
| `UniqueViolationError` on entity ID        | ID naming counter out of sync with existing rows                                        | Fixed — `NamingService` now resyncs counter against actual table rows                          |
| `Action 'X' not available from state 'Y'`  | Wrong action name sent, or record not in expected state                                 | Check transition table above; send slug (`allocate`) or label (`Allocate`) — both work         |
| `Cannot allocate: missing Labor`           | No Work Order Labor assigned to WOA                                                     | Create a `work_order_labor` child record before calling Allocate                               |
| `Cannot start: no Work Order linked`       | Submit for Resolution was not run yet, so WOA is still pre-resolution                   | Run MR workflow action `Submit for Resolution` before starting WOA                             |
| Asset not moving to `under_maintenance`    | WOA `work_item_type` is not `"Asset"` or `activity_type` menu is not `"Maintain Asset"` | Check PMA `maintenance_type` links to a `request_activity_type` with `menu = "Maintain Asset"` |
| `MR closed_date` not set on Complete       | WOA has no linked `maintenance_request`, or `activity_type` not found                   | Ensure MR was created with correct `work_order_activity` FK                                    |

---

## File Reference

| Responsibility              | File                                                                  |
| --------------------------- | --------------------------------------------------------------------- |
| Calendar trigger logic      | `backend/app/modules/maintenance_mgmt/apis/maintenance_calendar.py`   |
| Interval trigger logic      | `backend/app/modules/maintenance_mgmt/apis/maintenance_interval.py`   |
| Condition trigger logic     | `backend/app/modules/maintenance_mgmt/apis/maintenance_condition.py`  |
| Work package creation       | `backend/app/modules/maintenance_mgmt/apis/maintenance_job_common.py` |
| WOA workflow handler        | `backend/app/modules/work_mgmt/apis/work_order_activity.py`           |
| MR workflow handler         | `backend/app/modules/maintenance_mgmt/apis/maintenance_request.py`    |
| Workflow validation service | `backend/app/services/workflow.py`                                    |
| Manual trigger endpoints    | `backend/app/api/test_scheduler.py`                                   |
| Scheduler dispatcher        | `backend/app/services/scheduler.py`                                   |
| E2E test                    | `backend/tests/test_computer_pm_flow_e2e.py`                          |
