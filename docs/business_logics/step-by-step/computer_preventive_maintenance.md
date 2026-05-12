# Computer Preventive Maintenance — Step-by-Step Manual

> This document explains a realistic preventive-maintenance flow for a desktop computer using the Maintenance Management module. It covers the planning setup, the trigger configuration, the generated work package, and the execution flow through Work Order Activity completion.

---

## Overview

In this example, you want the system to manage recurring preventive maintenance for an office desktop computer.

The record chain looks like this:

```
Maintenance Activity
    ↓
Maintenance Plan
    ↓
Planned Maintenance Activity
    ↓
Maintenance Calendar / Interval / Condition
    ↓
Maintenance Request + Work Order + Work Order Activity
    ↓
Allocate → Start Activity → Complete
```

In the current implementation:

- A **Planned Maintenance Activity** is the parent definition of the work.
- **Maintenance Calendar**, **Maintenance Interval**, and **Maintenance Condition** act as trigger definitions.
- When a trigger fires, the system creates a **work package**:
  - **Maintenance Request**
  - **Work Order**
  - **Work Order Activity**
- The generated **Work Order Activity** is then executed by maintenance staff.

---

## Real-Life Example

Use this example scenario:

- **Asset**: Finance Office Desktop PC
- **Maintenance Goal**: Monthly preventive maintenance
- **Typical Work**:
  - Clean air vents and keyboard
  - Check disk health
  - Confirm antivirus and operating system updates
  - Verify CPU temperature is normal

---

## Prerequisites

Before you start, make sure:

- A **Site** exists.
- A **Department** exists.
- At least one **Labor** record exists.
- At least one **Trade** record exists.
- A **Request Activity Type** exists for **Maintain Asset**.
- The target **Asset** exists and is linked to the right Site and Department.

If you want the trigger to apply only to a specific kind of computer, create or reuse a dedicated **Asset Class** such as `Desktop Computer`.

---

## Step 1 — Create the Maintenance Activity

Create a **Maintenance Activity** record.

Example values:

- **Activity Name**: `Computer Preventive Maintenance`
- **Description**: `Monthly preventive maintenance for office desktop computers`

This is the reusable definition of the actual work technicians will perform.

---

## Step 2 — Create the Checklist

Create a **Checklist** for the task.

Example values:

- **Checklist Name**: `Computer PM Checklist`
- **Checklist Type**: `Preventive Maintenance`

Then add one or more **Checklist Details** rows.

Example checklist detail items:

- `Clean air vents and confirm OS updates`
- `Check antivirus status`
- `Inspect keyboard, mouse, and cables`
- `Review disk usage and health`

This checklist becomes the operational guide for the technician.

---

## Step 3 — Create the Maintenance Plan

Create a **Maintenance Plan**.

Example values:

- **Description**: `Office computer PM plan`
- **Asset Class**: `Desktop Computer`

The Maintenance Plan defines the scope of assets that the PM setup applies to.

---

## Step 4 — Create the Planned Maintenance Activity

Create a **Planned Maintenance Activity** under the Maintenance Plan.

Example values:

- **Maintenance Plan**: `Office computer PM plan`
- **Maintenance Activity**: `Computer Preventive Maintenance`
- **Checklist**: `Computer PM Checklist`
- **Schedule Type**: `Calendar Based`
- **Maintenance Type**: `Maintain Asset`

This is the main PM definition that the trigger tabs hang off of.

---

## Step 5 — Configure the Trigger

Open the **Planned Maintenance Activity** and use its link tabs.

### Option A — Calendar Trigger

Create a **Maintenance Calendar** row.

Example values:

- **Planned Activity**: your PMA
- **Frequency**: `Monthly`
- **Lead Days**: `3`

This means the system should create the work package before the next due date.

### Option B — Interval Trigger

Create a **Maintenance Interval** row if you want usage-based maintenance.

Example example:

- **Lead Interval**: `20`
- **Interval**: `200`
- **Running Property**: `computer_runtime_hours`
- **Last Property**: `last_pm_runtime_hours`

This means the system creates maintenance when the runtime approaches the next threshold.

### Option C — Condition Trigger

Create a **Maintenance Condition** row if you want sensor-based maintenance.

Example values:

- **Sensor**: CPU temperature sensor for the computer
- **Operator**: `>`
- **Threshold Property**: `cpu_temperature_limit`

This means the system creates maintenance when the live reading crosses the configured limit.

---

## Step 6 — Make Sure the Asset Matches the Plan

Your computer asset must match the PM scope.

Example asset:

- **Asset Tag**: `PC-FIN-001`
- **Description**: `Finance office desktop computer`
- **Asset Class**: `Desktop Computer`
- **Site**: correct site
- **Department**: correct department

If the asset does not match the Maintenance Plan scope, the trigger will not generate the expected work package.

---

## Step 7 — Trigger the PM Work Package

When the configured trigger condition is met, the system creates the work package.

For the computer example, the generated records are:

- **Work Order**
- **Work Order Activity**
- **Maintenance Request**

Expected initial behavior:

- **Maintenance Request** is linked to the PMA and generated WOA.
- **Maintenance Request** starts in **Approved** state.
- **Work Order** starts in **Requested** state.
- **Work Order Activity** starts in **Awaiting Resources** state.

---

## Step 8 — Assign Labor to the Work Order Activity

Before the activity can move forward, assign labor.

Create a **Work Order Labor** row linked to the generated WOA.

Example values:

- **Activity**: generated WOA
- **Trade**: `IT Technician`
- **Labor**: assigned technician
- **Lead**: `Yes`
- **Estimated Hours**: `1.5`

This is the minimum manual step required before allocation in the standard PM execution path.

---

## Step 9 — Allocate the Work Order Activity

Open the generated **Work Order Activity** and click:

- **Allocate**

Expected result:

- WOA moves from `Awaiting Resources` → `Ready`

---

## Step 10 — Start the Work Order Activity

On the same WOA, click:

- **Start Activity**

Expected result:

- WOA moves from `Ready` → `In Progress`
- If the activity type is **Maintain Asset**, the linked Asset moves to **Under Maintenance**

For the computer example, this means the desktop PC is now officially under maintenance.

---

## Step 11 — Complete the Work Order Activity

When the technician has finished the computer PM work, click:

- **Complete**

Expected result:

- WOA moves to **Completed**
- The linked **Maintenance Request** gets `closed_date`
- The linked **Asset** moves back to **Active**

For the computer example, this indicates the desktop PC has finished its preventive-maintenance cycle and is back in service.

---

## What the Full Flow Looks Like

```
[Maintenance Activity: Computer Preventive Maintenance]
    ↓
[Maintenance Plan: Office computer PM plan]
    ↓
[Planned Maintenance Activity]
    ↓
[Maintenance Calendar / Interval / Condition]
    ↓ trigger fires
[Work Order WO-xxxxx]
[Work Order Activity WOACT-xxxxx]
[Maintenance Request MTREQ-xxxxx]
    ↓ assign labor
[Work Order Labor WOLBR-xxxxx]
    ↓ Allocate
[WOA Ready]
    ↓ Start Activity
[WOA In Progress]
[Asset Under Maintenance]
    ↓ Complete
[WOA Completed]
[Maintenance Request closed_date set]
[Asset Active]
```

---

## What to Verify After Completion

| Record | What to Check |
|---|---|
| **Maintenance Activity** | Correct reusable activity exists |
| **Maintenance Plan** | Correct Asset Class is linked |
| **Planned Maintenance Activity** | Correct Activity, Checklist, and Maintenance Type are linked |
| **Maintenance Calendar / Interval / Condition** | Trigger row exists under the PMA |
| **Maintenance Request** | Linked to PMA and WOA, `closed_date` is filled after completion |
| **Work Order** | Exists and is linked to the WOA |
| **Work Order Activity** | Progresses through `Awaiting Resources` → `Ready` → `In Progress` → `Completed` |
| **Asset** | Moves to `under_maintenance` on Start Activity, then back to `active` on Complete |

---

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| No Maintenance Request / Work Order / WOA generated | Asset does not match the Maintenance Plan scope | Confirm the asset uses the same Asset Class targeted by the plan |
| WOA cannot Allocate | No Work Order Labor assigned | Create at least one Work Order Labor row linked to the WOA |
| WOA cannot Start Activity | No Work Order linked | Verify the generated work package includes a Work Order and that the WOA is linked to it |
| Asset does not move to Under Maintenance on Start Activity | Request Activity Type is not configured as `Maintain Asset` | Check the `Request Activity Type` record used by the PMA |
| Asset does not move back to Active on Complete | Activity type is not mapped to `Maintain Asset` behavior | Confirm the WOA `activity_type` points to the correct Request Activity Type |
| Maintenance Request remains open | WOA was not completed | Complete the generated WOA |

---

## Notes on Trigger Types

- **Maintenance Calendar** is best for regular time-based PM, such as monthly desktop cleaning and update verification.
- **Maintenance Interval** is best for usage-based PM, such as runtime-based servicing.
- **Maintenance Condition** is best for threshold-based PM, such as high CPU temperature or abnormal vibration.

All three trigger types ultimately feed the same execution pattern:

- generate work package
- assign resources
- execute WOA
- complete maintenance
