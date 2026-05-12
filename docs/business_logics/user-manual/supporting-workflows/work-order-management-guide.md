# Work Order Management Guide

> **Scope:** Forklift fleet maintenance — from work order creation through closure.

---

## Table of Contents

- [Work Order Creation](#work-order-creation)
- [Workflow States](#workflow-states)
- [Work Order Activities](#work-order-activities)
- [Labor Management](#labor-management)
- [Parts Management](#parts-management)
- [Equipment Management](#equipment-management)
- [Checklists](#checklists)
- [Daily Workflow](#daily-workflow)
- [Troubleshooting](#troubleshooting)

---

## Work Order Creation

Work Orders are the execution engine of the maintenance system. They transform a Maintenance Request into schedulable, trackable work — with assigned mechanics, allocated parts, and a full audit trail. Without a Work Order, maintenance cannot be formally planned, costed, or closed out.

Work Orders are created from a **Maintenance Request** via one of two paths:

| Path      | Action                | Result                                                           |
| --------- | --------------------- | ---------------------------------------------------------------- |
| Standard  | Submit for Resolution | WO created; type set automatically (e.g. Preventive Maintenance) |
| Emergency | Submit for Emergency  | WO created with type = Emergency, high priority                  |

The system automatically sets the Work Order type based on the originating Maintenance Request. For scheduled work, this will be **Preventive Maintenance**. For emergency submissions, the type is locked to **Emergency** and the WO is flagged for immediate processing.

> ⚠️ A Maintenance Request **cannot** use _Submit for Emergency_ if it already has a linked Work Order Activity. This prevents duplicate emergency WOs for the same job.

---

## Workflow States

Understanding the state machine is critical to avoiding blocked work. Both the Work Order (WO) and its child Work Order Activities (WOAs) have their own states, and they are interdependent — you cannot advance one without the other being in the correct state.

### Work Order (WO) States

```
Requested → Approved → In Progress → Closed
```

| State       | Description                   | Available Actions                  |
| ----------- | ----------------------------- | ---------------------------------- |
| Requested   | Created, pending review       | Approve, Edit, Delete              |
| Approved    | Reviewed, ready for execution | Start (requires all WOAs in Ready) |
| In Progress | Work is active                | Complete, monitor activities       |
| Closed      | All work finalized            | Reopen if needed                   |

### Work Order Activity (WOA) States

```
Awaiting Resources → Ready → In Progress → Completed → Closed
                                  ↕
                               On Hold
```

| State              | Description                                      |
| ------------------ | ------------------------------------------------ |
| Awaiting Resources | Created, not yet resourced                       |
| Ready              | All resources allocated; waiting for WO to start |
| In Progress        | Work actively being performed                    |
| On Hold            | Temporarily paused                               |
| Completed          | Work done, pending review                        |
| Closed             | Finalized                                        |

### State Dependencies

The WO and WOA states are tightly coupled. The system enforces these rules and will block transitions that violate them.

| Transition        | Requirement                                                             |
| ----------------- | ----------------------------------------------------------------------- |
| WO → Approved     | Manual approval by authorized user                                      |
| WOA → Ready       | WO must be Approved; all required resources allocated                   |
| WO → In Progress  | **All WOAs must be in Ready state**                                     |
| WOA → In Progress | Cascades automatically from WO Start — cannot be triggered individually |
| WO → Closed       | **All WOAs must be Completed or Closed**                                |

**What happens when you start a WO:**

- All linked WOAs move to **In Progress** simultaneously
- The forklift is set to **Under Maintenance** — it becomes unavailable for other work orders

**What happens when you complete a WOA:**

- The forklift returns to **Active** state — available for operations and future maintenance
- The linked Maintenance Request is stamped with a `closed_date`
- Forklift properties are automatically updated (e.g. last service date), which recalculates the next maintenance trigger

---

## Work Order Activities

Work Order Activities break a Work Order down into individual maintenance tasks. Each activity has its own resource requirements, time tracking, and checklist — giving you granular visibility into what is being done, by whom, and at what cost. Without activities, there is no way to allocate resources or track work at the task level.

### Reviewing Work Order Activities

Work Order Activities are automatically created and linked when a Maintenance Request is submitted for resolution. You do not need to create them manually in most cases. To review them:

1. Navigate to the **Work Order** record
2. Go to the **Work Order Activities** tab
3. Select an activity to view its details, resources, and checklist

### Allocating Resources (Awaiting Resources → Ready)

Once a WOA exists, it starts in **Awaiting Resources**. Before work can begin, all required resources must be assigned. This step is mandatory — it is what signals to the system that mechanics, parts, and tools are confirmed and ready.

1. Navigate to the **Work Order Activity** record
2. Assign the required Labor, Parts, and Equipment (see respective sections below)
3. Click **Allocate**
4. The WOA moves to **Ready**

The validation rules differ by activity type:

**Planned Maintenance** — required if defined on the Maintenance Activity template:

- **Labor** — at least one certified mechanic must be assigned
- **Parts** — e.g. hydraulic fluid, oil filters, batteries
- **Equipment** — e.g. lifts, diagnostic tools, calibration equipment

**Emergency** — streamlined validation to allow faster response:

- **Labor** — at least one certified mechanic is required
- **Parts / Equipment** — optional, based on the repair type

> ⚠️ The Allocate button will fail if any required resource is missing. The system will not allow a WOA to move to Ready until all constraints are satisfied.

---

## Labor Management

Proper labor management ensures that only certified, available mechanics are assigned to forklift work — and that actual time spent is accurately captured for cost reporting and productivity analysis. Without this, you cannot track who performed the work, how long it took, or whether it stayed within budget.

### Assigning Labor to a Work Order Activity

1. Navigate to the **Work Order** → **Work Order Activities** tab
2. Select the relevant activity
3. Go to the **Work Order Labor** tab
4. Click **Add Row**
5. Fill in the following:

| Field           | Description                                                                      |
| --------------- | -------------------------------------------------------------------------------- |
| Trade           | The mechanic's trade (e.g. Forklift Mechanic, Electrician)                       |
| Labor           | The specific mechanic — filtered to those with the selected trade at the WO site |
| Lead            | Check this if the mechanic is the lead for this activity                         |
| Estimated Hours | Planned hours for this task                                                      |

> The Labor field only shows mechanics with the selected trade who are available at the work order's site. This prevents cross-site assignment errors.

### Recording Actual Hours

Time tracking is how the system calculates the difference between planned and actual labor — feeding into cost reports and mechanic productivity dashboards. Log actual hours as work progresses, not after the fact.

1. Navigate to **Work Order Labor** → **Actual Hours** tab
2. Click **Add Row**
3. Fill in:

| Field            | Description                                 |
| ---------------- | ------------------------------------------- |
| Start DateTime   | When the mechanic actually started the task |
| End DateTime     | When the mechanic actually finished         |
| Total Hours Used | Calculated automatically                    |

**Validation rules:**

- Start must be before End
- Entries cannot overlap for the same mechanic
- The time entry must fall within the work order period

> ⚠️ Overlapping time entries for the same mechanic will be rejected. This prevents duplicate time recording for the same person.

---

## Parts Management

Parts management ensures the right components are available before work begins, and that inventory levels stay accurate as parts are consumed and returned. Skipping this step can cause maintenance delays and inaccurate stock counts.

### Adding a Parts Requirement

This step records what parts are needed for the activity. It does **not** yet affect inventory — it is a planning step only.

1. Navigate to **Work Order Activity** → **Work Order Parts** tab
2. Click **Add Row**
3. Fill in:

| Field             | Description                                                   |
| ----------------- | ------------------------------------------------------------- |
| Item              | The required part (e.g. Hydraulic Fluid, Oil Filter, Battery) |
| Quantity Required | Amount needed for this task                                   |
| Date Required     | When the parts need to be on hand                             |

### Issuing Parts

Issuing parts is the step that actually deducts from inventory. Do this when the mechanic is ready to use the parts.

1. In the **Work Order Parts** record, click **Actions → Issue Parts**
2. The system creates an Item Issue transaction
3. Inventory is immediately reduced

> ⚠️ Issue Parts will fail if the inventory count at the required location is zero. Check stock levels before scheduling the work. If parts are unavailable, contact procurement for an emergency order or check if alternative parts are permitted.

### Returning Unused Parts

If not all parts are consumed, return them promptly to keep inventory accurate and available for other work orders.

1. Navigate to **Work Order Parts** → **Actions → Return Parts**
2. Enter the quantity to return
3. The system creates an Item Return transaction and restores inventory

---

## Equipment Management

Equipment management tracks which tools and machinery are needed for each activity, and logs how long they are actually used. This data feeds into equipment maintenance scheduling and depreciation calculations — ensuring your tools stay calibrated and available.

### Adding an Equipment Requirement

This step records equipment needs for planning purposes. It does **not** yet affect equipment availability.

1. Navigate to **Work Order Activity** → **Work Order Equipment** tab
2. Click **Add Row**
3. Fill in:

| Field           | Description                                                         |
| --------------- | ------------------------------------------------------------------- |
| Equipment       | The required tool or machine (must be flagged `is_equipment: true`) |
| Estimated Hours | Planned usage time                                                  |
| Start DateTime  | When the equipment is needed                                        |

> Only items marked as equipment (`is_equipment: true`) appear in the selector. Parts and consumables are excluded from this list.

### Logging Actual Equipment Usage

Actual usage hours are used to track equipment wear, schedule preventive maintenance on the tools themselves, and calculate depreciation.

1. Navigate to **Work Order Equipment** → **Actual Hours** tab
2. Click **Add Row**
3. Fill in:

| Field            | Description                           |
| ---------------- | ------------------------------------- |
| Start DateTime   | When equipment usage actually started |
| End DateTime     | When equipment usage ended            |
| Total Hours Used | Calculated automatically              |

**Validation rules:**

- Start must be before End
- Entries cannot overlap for the same equipment item
- The entry must fall within the work order period

---

## Checklists

Checklists enforce consistency and quality across forklift maintenance tasks. They provide a documented, step-by-step verification that work was performed correctly — and create an audit trail for compliance and safety reviews. Every planned maintenance activity should have a checklist completed before the WO is closed.

### Adding a Checklist to an Activity

1. Navigate to **Work Order Activity** → **Work Order Checklist** tab
2. Click **Add Row**
3. Fill in:

| Field           | Description                                            |
| --------------- | ------------------------------------------------------ |
| Checklist       | Select the appropriate template for this type of work  |
| Inspector       | Assign the person responsible for quality verification |
| Inspection Date | Schedule when the inspection should take place         |

The system automatically loads all checklist items from the selected template.

### Completing Checklist Items

1. Navigate to **Work Order Checklist** → **Checklist Details** tab
2. For each item, set:

| Field   | Description                                    |
| ------- | ---------------------------------------------- |
| Status  | Completed, Failed, or In Progress              |
| Remarks | Notes about the inspection or any issues found |

3. Save after each item

### Checklist Completion Rules

- All **required items** must be marked Completed before the WO can close
- **Failed items** must have documented remediation actions
- The Inspector must have appropriate permissions to submit

> ⚠️ A Work Order **cannot be closed** while any checklist item is in **Failed** status. Address all failures and document the corrective action before attempting to complete the WO.

---

## Troubleshooting

### WO Won't Start

**Symptom:** Start button is disabled or returns an error.

**Cause:** One or more WOAs are not in Ready state.

**Fix:**

1. Open the **Work Order Activities** tab
2. Identify any WOA still in **Awaiting Resources**
3. Allocate the missing resource (labor, parts, or equipment)
4. Click **Allocate** on the WOA — once it reaches Ready, retry starting the WO

---

### Allocation Fails

**Symptom:** Clicking Allocate returns an error.

**Possible causes:**

- Parts inventory is insufficient at the required location
- The selected mechanic is not available during the work period
- The required equipment is currently under maintenance

**Fix:**

1. Check parts stock levels across all locations
2. Reschedule the work or assign an alternative mechanic with the same trade
3. Substitute equipment or wait until the current job using it is closed

---

### Parts Can't Be Issued

**Symptom:** Issue Parts action fails.

**Possible causes:**

- Inventory at the required location is zero
- Parts are already reserved or consumed by another work order
- The part is stocked at a different location

**Fix:**

1. Check inventory across all warehouse locations
2. Contact procurement for an emergency order if needed
3. Confirm whether alternative parts within spec are permitted

---

### Forklift State Conflict

**Symptom:** Cannot start work on the forklift — asset is unavailable.

**Cause:** The forklift is already in **Under Maintenance** state, assigned to a different work order.

**Fix:**

1. Look up the forklift record and check its current WO assignment
2. Coordinate with the owner of the active WO before proceeding
3. Do not force a state change — verify the forklift is safe and clear before starting new work

all steps validated
