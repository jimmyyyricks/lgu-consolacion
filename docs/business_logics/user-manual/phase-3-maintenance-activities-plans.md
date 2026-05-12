# Phase 3: Maintenance Management

[Back to Main Manual](./00_EAM_User_Manual.md)

---

## Purpose

> 🔧 Build preventive maintenance for the **Screw Press Conveyor Assembly** that was procured in Phase 2 and installed in Phase 2.1.

This phase turns the installed asset into a fully managed maintenance asset with measurements, maintenance activities, maintenance plans, planned maintenance activities, and generated `Maintenance Request` records.

By the end of this phase, you will be able to:

- Track asset condition using properties
- Create maintenance activities for the conveyor
- Group those activities into a maintenance plan
- Create planned maintenance activities that auto-generate `Maintenance Request` records
- Process maintenance requests into work orders

---

# 🧱 1. Confirm the Installed Asset

This guide assumes the conveyor has already been purchased in Phase 2 and installed in Phase 2.1.

### Asset Validation

> ✅ Confirm that the asset already has these details before you continue.

| Detail        | Value                           | Why it matters                     |
| ------------- | ------------------------------- | ---------------------------------- |
| Asset Tag     | `SCREW-001`                     | Required asset identifier          |
| Item          | `Screw Press Conveyor Assembly` | The item received in Phase 2       |
| Asset Class   | `Rotating Equipment`            | Used for maintenance grouping      |
| Serial Number | [manufacturer serial]           | Traceability                       |
| Location      | `Waste Water Treatment Area`    | Installed location                 |
| Site          | `Polomolok`                     | Site context for requests          |
| System        | `Screw Press Line A`            | System assigned after installation |
| Position      | `CONV-LINE-A-01`                | Installed position                 |
| Status        | `Active`                        | Ready for maintenance planning     |

> 📌 `asset_tag` must be unique. `item` and `inventory` are already handled by the system. `bypass_process` is off by default.

---

# 📊 2. Confirm the Asset Measurements for the Conveyor

Asset measurements let the system track the condition and usage of the conveyor over time.

> 📌 **Note**: If these measurements were already created in Phase 1 or came from the asset class when the asset was saved, you only need to confirm them here. If not, create them first before continuing.

### Step 2.1: Confirm the Measurements

Go to **Property** → **New** and create or confirm these measurements:

| Property Name                | Data Type | Description                                         |
| ---------------------------- | --------- | --------------------------------------------------- |
| Operating Hours              | Number    | Total running hours since installation              |
| Last Bearing Inspection Date | Date      | Date of the last bearing inspection                 |
| Last Lubrication Hours       | Number    | Operating hours when lubrication was last done      |
| Vibration Level              | Number    | Current vibration reading from inspection or sensor |

### Step 2.2: Set Initial Values on the Asset

Open the installed asset `SCREW-001` and set the initial values:

| Property                     | Value      |
| ---------------------------- | ---------- |
| Operating Hours              | 450        |
| Last Bearing Inspection Date | 2026-01-15 |
| Last Lubrication Hours       | 0          |
| Vibration Level              | 2.1        |

> 💡 These values are the baseline for later maintenance triggers.

---

# 🛠️ 3. Create Maintenance Activities

Create the actual maintenance activities that will be reused in the plan.

### Step 3.1: Monthly Bearing Inspection

1. Go to **Maintenance Activity** → **New**
2. Fill in:
   - **Activity Name**: `Monthly Screw Press Bearing Inspection`
   - **Description**: `Inspect bearings, rollers, alignment, and unusual vibration on the screw press conveyor`

> 📌 If this inspection activity does not already exist, create it before you use it in the maintenance plan.

### Step 3.2: Lubrication Service

1. Go to **Maintenance Activity** → **New**
2. Fill in:
   - **Activity Name**: `Screw Press Lubrication Service`
   - **Description**: `Lubricate bearings, drive components, and moving joints on the conveyor`

> 📌 If this service activity does not already exist, create it before you use it in the maintenance plan.

### Step 3.3: Belt Alignment Check

1. Go to **Maintenance Activity** → **New**
2. Fill in:
   - **Activity Name**: `Screw Press Belt Alignment Check`
   - **Description**: `Check belt tension, alignment, and wear condition`

> 📌 If this corrective activity does not already exist, create it before you use it in the maintenance plan.

---

# 🗂️ 4. Create the Maintenance Plan

The maintenance plan groups the activities for the conveyor asset class.

### Step 4.1: Create Plan

1. Go to **Maintenance Plan** → **New**
2. Fill in:
   - **Description**: `Screw Press Conveyor Comprehensive Maintenance Plan`
   - **Asset Class**: `Rotating Equipment`

> 📌 If you have not created a maintenance plan yet, create it now before adding scheduled activities.

### Step 4.2: Confirm the Plan Scope

This plan is for:

- The installed screw press conveyor asset
- Other assets that share the **Rotating Equipment** class

---

# ⏱️ 5. Create Planned Maintenance Activities

`Planned Maintenance Activity` records connect the plan to the rules that create `Maintenance Request` records.

### Step 5.1: Calendar-Based Inspection Schedule

1. Go to **Planned Maintenance Activity** → **New**
2. Fill in:
   - **Maintenance Plan**: `Screw Press Conveyor Comprehensive Maintenance Plan`
   - **Maintenance Activity**: `Monthly Screw Press Bearing Inspection`
   - **Checklist**: `Screw Press Inspection Checklist`
   - **Maintenance Schedule**: `Calendar Based`
   - **Maintenance Type**: `Preventive Maintenance`
3. In the **Calendars** tab, add:
   - **Frequency**: `Monthly`
   - **Lead Days**: `7`
   - **Last Maintenance Property**: `Last Bearing Inspection Date`

> 📌 If the checklist does not already exist, create it first, then come back and link it here.

### Step 5.2: Interval-Based Lubrication Schedule

1. Go to **Planned Maintenance Activity** → **New**
2. Fill in:
   - **Maintenance Plan**: `Screw Press Conveyor Comprehensive Maintenance Plan`
   - **Maintenance Activity**: `Screw Press Lubrication Service`
   - **Checklist**: `Lubrication Checklist`
   - **Maintenance Schedule**: `Interval Based`
   - **Maintenance Type**: `Preventive Maintenance`
3. In the **Intervals** tab, add:
   - **Lead Interval**: `50`
   - **Interval**: `500`
   - **UoM**: `Hours`
   - **Running Property**: `Operating Hours`
   - **Last Property**: `Last Lubrication Hours`

> 📌 If the lubrication checklist does not already exist, create it first, then link it here.

### Step 5.3: Condition-Based Vibration Schedule

1. Go to **Planned Maintenance Activity** → **New**
2. Fill in:
   - **Maintenance Plan**: `Screw Press Conveyor Comprehensive Maintenance Plan`
   - **Maintenance Activity**: `Screw Press Belt Alignment Check`
   - **Checklist**: `Alignment Checklist`
   - **Maintenance Schedule**: `Condition Based`
   - **Maintenance Type**: `Corrective Maintenance`
3. In the **Conditions** tab, add a sensor or threshold rule for:
   - **Property**: `Vibration Level`
   - **Threshold Value**: `5.0`

> 💡 When the vibration level rises above the threshold, the system should generate a `Maintenance Request` immediately.

> 📌 If the sensor does not already exist, create it first so the condition can read a real measurement.

---

# 📝 6. Process Maintenance Requests

When the system creates a `Maintenance Request` from a planned maintenance activity, that request is linked to a `Work Order Activity`.

### Step 6.1: Review the Approved Request

1. Go to **Maintenance Request**
2. Filter by **Workflow State**: `Approved`
3. Open the request and confirm:
   - Asset = `SCREW-001`
   - Request Type matches the planned maintenance activity
   - Due date is correct
   - The linked `Work Order Activity` is already present

### Step 6.2: Submit for Resolution

1. Click **Submit for Resolution**
2. The request is released for resolution
3. The system creates a **Work Order** and links the `Work Order Activity` to it
4. The request moves forward in the process

> ✅ This means the `Work Order Activity` is now ready to be worked on from inside the `Work Order`.

### Step 6.3: Complete the Work Order Activity

1. Open the **Work Order** first
2. Open the linked `Work Order Activity` from inside the Work Order
3. Complete the work
4. When the `Work Order Activity` is completed, the system:
   - Updates the Maintenance Request closed date
   - Updates date-based asset measurements automatically when one is linked

### Step 6.4: Update Interval Measurements Manually

For interval-based work, update the "Last" measurement yourself:

- After lubrication, set `Last Lubrication Hours` to the current operating hours

> ⚠️ If you do not update the interval measurement, the system will keep creating the same maintenance request.

---

# 📋 7. Records Created or Updated

This phase creates and updates the following records:

- Asset Properties
- Maintenance Activities
- Maintenance Plan
- Planned Maintenance Activities
- Maintenance Requests
- Work Orders
- Work Order Activities
- Updated Asset Property values

---

# 🔗 Dependencies

- Phase 1: Setting Up
- Phase 2: Item Acquisition and Procurement
- Phase 2.1: Asset Installation (Optional)
