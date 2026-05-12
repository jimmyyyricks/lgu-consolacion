# Work Order Execution Guide

## Work Order Workflow

### Work Order states

| State                | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| `draft`              | Initial state when WO is created (usually from MR resolution)  |
| `scheduled`          | Work is scheduled with dates and assigned resources             |
| `in_progress`        | Work is actively underway                                      |
| `completed`          | Work done — all WOAs completed                                 |
| `closed`             | Fully closed after all logs and actuals are recorded           |

### Work Order transitions

| From          | Action              | To            | Side-effects                                      |
| ------------- | ------------------- | ------------- | ------------------------------------------------- |
| `draft`       | `Schedule`          | `scheduled`   | Sets planned dates, assigns resources             |
| `scheduled`   | `Start Work`        | `in_progress` | Enables WOA-level work to begin                   |
| `in_progress` | `Complete`          | `completed`   | Requires all WOAs to be completed first           |
| `completed`   | `Close`             | `closed`      | Requires logs, actuals, and final documentation   |
| `completed`   | `Reopen`            | `in_progress` | Allows reopening if work needs to resume          |

## Work Order Activity Workflow

### Work Order Activity states

| State                | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| `awaiting_resources` | Created by MR approval; waiting for labor/parts/equipment      |
| `ready`              | Resources allocated; ready to start                            |
| `in_progress`        | Work is actively underway                                      |
| `on_hold`            | Work paused                                                    |
| `completed`          | Work done — asset state updated, MR closed_date set          |
| `closed`             | Fully closed after all logs and actuals are recorded           |

### Work Order Activity transitions

| From                 | Action           | To            | Side-effects                                                                   |
| -------------------- | ---------------- | ------------- | ------------------------------------------------------------------------------ |
| `awaiting_resources` | `Allocate`       | `ready`       | Validates labor (and equipment/parts if PMA-linked) are assigned               |
| `ready`              | `Start Activity` | `in_progress` | Moves linked asset to `under_maintenance` (if activity type is Maintain Asset) |
| `in_progress`        | `Put On Hold`    | `on_hold`     | —                                                                              |
| `on_hold`            | `Resume`         | `in_progress` | —                                                                              |
| `in_progress`        | `Complete`       | `completed`   | Sets asset back to `active`; sets `maintenance_request.closed_date`            |
| `completed`          | `Reopen`         | `in_progress` | —                                                                              |
| `completed`          | `Close`          | `closed`      | Requires activity logs, labor actuals, equipment actuals                       |

> **Important:** Workflow actions accept both human labels (`"Start Activity"`) and slugs (`"start_activity"`). The system normalises them automatically.

## Real Life Examples

### Work Order Example
A building has three HVAC units that need annual inspection:

1. **Work Order Created**: "Annual HVAC Inspection" (draft)
2. **Schedule**: Assign to maintenance team for next week, schedule 8 hours (scheduled)
3. **Start Work**: Begin inspections (in_progress)
4. **Complete**: All three units inspected, WO completed (completed)
5. **Close**: Final reports filed, time sheets submitted (closed)

### Work Order Activity Example
One HVAC unit needs filter replacement:

1. **WOA Created**: "Replace HVAC Unit 1 Filters" (awaiting_resources)
2. **Allocate**: Assign technician and bring filters (ready)
3. **Start Activity**: Technician begins replacement (in_progress)
4. **Complete**: Filters replaced, unit tested (completed)
5. **Close**: Technician logs time, parts used (closed)

## Key Relationships

- **Work Order** contains one or more **Work Order Activities**
- **Work Order Activity** is created when **Maintenance Request** is approved
- **Work Order Activity** completion can trigger **Maintenance Request** closure
- **Asset state** changes during WOA execution (active → under_maintenance → active)
