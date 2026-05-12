# Maintenance Workflow Tutorial

## Complete Tutorial: Forklift Fleet Preventive Maintenance

> 📌 For the conveyor-based phase-by-phase guide, see [Phase 3: Maintenance Management](../phase-3-maintenance-activities-plans.md).

---

## Chapter 1: Setting Up Asset Classes and Properties

Setting up Asset Classes and Properties allows the system to group similar equipment and track the measurements that trigger maintenance work. For a Forklift Asset, here are the steps to set it up for Preventive Maintenance.

### Step 1.1: Create Forklift Asset Class

First, create an asset class to group all forklifts:

1. Navigate to **Asset Class** in the sidebar
2. Click **New**
3. Fill in:
   - **Name**: `Electric Forklift`
   - **Description**: `Warehouse electric forklifts - 3-ton capacity`
   - **Due Date Lead Time**: `7` (days)

> **Why Lead Time?** This creates work orders 7 days before due dates, giving you time to schedule.

### Step 1.2: Create Asset Properties

Forklifts need tracking properties. Create these:

#### Operating Hours Property

1. Go to **Property** → **New**
2. Fill in:
   - **Property Name**: `Operating Hours`
   - **Data Type**: `Number`
   - **Description**: `Total operating hours since new`

#### Last Oil Change Hours Property

1. Go to **Property** → **New**
2. Fill in:
   - **Property Name**: `Last Oil Change Hours`
   - **Data Type**: `Number`
   - **Description**: `Operating hours at last oil change`

#### Battery Voltage Property

1. Go to **Property** → **New**
2. Fill in:
   - **Property Name**: `Battery Voltage`
   - **Data Type**: `Number`
   - **Description**: `Current battery voltage in volts`

#### Last Safety Inspection Property

1. Go to **Property** → **New**
2. Fill in:
   - **Property Name**: `Last Safety Inspection`
   - **Data Type**: `Date`
   - **Description**: `Date of last monthly safety inspection`

### Step 1.3: Set Asset Property Values

Assume you already have forklifts created. Now set their initial property values:

1. Go to **Asset** → select a forklift (e.g., FLK-001)
2. Go to **Asset Properties** tab
3. Add properties:
   - Operating Hours: `450`
   - Last Oil Change Hours: `0` (new forklift)
   - Battery Voltage: `24.5`
   - Last Safety Inspection: `2026-01-15` (set to past date for testing)

---

## Chapter 2: Setting Up Maintenance Activities

Setting up Maintenance Activities defines the actual work to be performed and serves as templates that include required parts, tools, and procedures. For forklift maintenance, here's how to create the work templates.

### Step 2.1: Create Maintenance Activities

Create three maintenance activities:

#### Monthly Safety Inspection

1. Go to **Maintenance Activity** → **New**
2. Fill in:
   - **Activity Name**: `Monthly Forklift Safety Inspection`
   - **Description**: `Check brakes, lights, horn, safety features, fluid levels`

#### Oil Change Service

1. Go to **Maintenance Activity** → **New**
2. Fill in:
   - **Activity Name**: `Forklift Oil Change`
   - **Description**: `Replace engine oil and filter, check all fluid levels`

#### Battery Replacement

1. Go to **Maintenance Activity** → **New**
2. Fill in:
   - **Activity Name**: `Forklift Battery Replacement`
   - **Description**: `Replace battery when voltage drops below threshold`

### Step 2.2: Add Required Resources (Optional but Recommended)

For each activity, add required parts and tools:

#### Oil Change Parts

1. Open "Forklift Oil Change" activity
2. Go to **Maintenance Parts** tab
3. Add:
   - **Part**: `Engine Oil 5W-30`
   - **Quantity**: `4`
   - **Part**: `Oil Filter`
   - **Quantity**: `1`

#### Oil Change Tools

1. Go to **Maintenance Equipment** tab
2. Add:
   - **Equipment**: `Oil Drain Pan`
   - **Quantity**: `1`
   - **Equipment**: `Filter Wrench`
   - **Quantity**: `1`

---

## Chapter 3: Creating Maintenance Plans

Setting up Maintenance Plans organizes all maintenance activities for a specific asset class, making it easy to manage and report on equipment maintenance. Here's how to create a plan for your forklift fleet.

### Step 3.1: Create Forklift Maintenance Plan

1. Go to **Maintenance Plan** → **New**
2. Fill in:
   - **Description**: `Electric Forklift Comprehensive Maintenance Plan`
   - **Asset Class**: `Electric Forklift`

This plan groups all maintenance activities for forklifts.

---

## Chapter 4: Setting Up Planned Maintenance Activities (PMAs)

Setting up Planned Maintenance Activities links maintenance activities to specific triggers (calendar, interval, or condition-based). This is how the system knows when to automatically create work orders for your forklifts.

### Step 4.1: Create Safety Inspection PMA (Calendar-Based)

1. Go to **Planned Maintenance Activity** → **New**
2. Fill in:
   - **Maintenance Plan**: `Electric Forklift Comprehensive Maintenance Plan`
   - **Maintenance Activity**: `Monthly Forklift Safety Inspection`
   - **Checklist**: `Forklift Safety Checklist` (create one if needed)
   - **Maintenance Schedule**: `Calendar Based`
   - **Maintenance Type**: `Preventive Maintenance`

3. **Create Calendar Trigger**:
   - Go to **Calendars** tab
   - Click **New**
   - Fill in:
     - **Frequency**: `Monthly`
     - **Lead Days**: `7`
     - **Last Maintenance Property**: `Last Safety Inspection`

> **Real Life Logic**: Every month, the system checks if (Last Inspection + 30 days - 7 days) <= today. If yes, creates work order 7 days before due.

### Step 4.2: Create Oil Change PMA (Interval-Based)

1. Go to **Planned Maintenance Activity** → **New**
2. Fill in:
   - **Maintenance Plan**: `Electric Forklift Comprehensive Maintenance Plan`
   - **Maintenance Activity**: `Forklift Oil Change`
   - **Checklist**: `Oil Change Checklist`
   - **Maintenance Schedule**: `Interval Based`
   - **Maintenance Type**: `Preventive Maintenance`

3. **Create Interval Trigger**:
   - Go to **Intervals** tab
   - Click **New**
   - Fill in:
     - **Lead Interval**: `50` (trigger 50 hours before 500-hour mark)
     - **Interval**: `500`
     - **UoM**: `Hours`
     - **Running Property**: `Operating Hours`
     - **Last Property**: `Last Oil Change Hours`

> **Real Life Logic**: When (Current Hours - Last Oil Change Hours) >= 450 (500-50), create work order.

### Step 4.3: Create Battery Replacement PMA (Condition-Based)

1. Go to **Planned Maintenance Activity** → **New**
2. Fill in:
   - **Maintenance Plan**: `Electric Forklift Comprehensive Maintenance Plan`
   - **Maintenance Activity**: `Forklift Battery Replacement`
   - **Checklist**: `Battery Replacement Checklist`
   - **Maintenance Schedule**: `Condition Based`
   - **Maintenance Type**: `Corrective Maintenance`

3. **Create Sensor** (for monitoring):
   - Go to **Sensor** → **New**
   - Fill in:
     - **Sensor Name**: `Forkift Battery Monitor`
     - **Asset**: `FLK-001` (or create one per forklift)
     - **Property**: `Battery Voltage`
     - **Topic**: `warehouse/forklift/battery`
     - **Frequency**: `hourly`

4. **Create Condition Trigger**:
   - Go to **Conditions** tab
   - Click **New**
   - Fill in:
     - **Sensor**: `Forkift Battery Monitor`
     - **Operator**: `<`
     - **Threshold Value**: `24`
     - **Threshold Property**: `Battery Voltage`

> **Real Life Logic**: When battery voltage drops below 24V, immediately create emergency work order.

---

## Chapter 5: Processing Maintenance Requests

When the scheduler creates maintenance requests, they start in "Approved" state with a Work Order Activity already linked. You need to submit these for resolution to create the actual Work Order before work can begin.

### Step 5.1: Review New Maintenance Requests

Each morning, check for new requests created by the scheduler:

1. Go to **Maintenance Request**
2. Filter by **Workflow State**: `Approved`
3. Review new requests - these were automatically created by the triggers

### Step 5.2: Submit for Resolution (Creates Work Order)

For each approved request:

1. **Review Details**:
   - Click on the request
   - Check asset, due date, priority
   - Review linked checklist and required parts/tools

2. **Submit for Resolution**:
   - Click **Submit for Resolution** button
   - System creates a Work Order and links it to the existing Work Order Activity
   - Maintenance Request state changes to `release`

> **Important**: The scheduler only creates the Maintenance Request (approved) and Work Order Activity (awaiting_resources). You must run "Submit for Resolution" to create the actual Work Order.

> **For detailed Work Order procedures, see:** [Work Order User Manual](work-order-management-guide.md)

### Step 5.3: Asset Property Updates (Automated + Manual)

When Work Order Activities are completed, the system automatically updates some asset properties:

#### Automatic Updates (System Handles)

- **Date Properties**: If the Maintenance Request has a `property` field set, the system automatically updates that asset property to today's date when the Work Order Activity is completed.
  - Example: "Last Safety Inspection" automatically set to today's date

#### Manual Updates Required (User Must Handle)

- **Interval Properties**: For interval-based maintenance, you must manually update the counter values:
  - After oil change: Set "Last Oil Change Hours" to current operating hours
  - After any interval-based work: Update the corresponding "Last" property

> **Why Manual Updates Matter**: The automated scheduler calculates triggers based on the difference between "Running" and "Last" interval properties. If you don't update "Last Oil Change Hours", the system will keep creating oil change requests.

> **For detailed Work Order execution procedures, see:** [Work Order User Manual](work-order-management-guide.md)

---

## Conclusion

You now have a complete preventive maintenance system for your forklift fleet. The system will:

- Automatically create work orders based on time, usage, or conditions
- Track all maintenance history and costs
- Keep your fleet in safe operating condition
- Provide data for continuous improvement

Remember: **The system is only as good as the data you put in.** Keep asset properties updated and follow the workflows consistently.

---

## Quick Reference

### Key Numbers for Forklifts

- **Safety Inspection**: Every 30 days, 7-day lead time
- **Oil Change**: Every 500 hours, 50-hour lead time
- **Battery Voltage**: Replace below 24V (immediate)

### Daily Checklist

- [ ] Review new Maintenance Requests (Approved state)
- [ ] Submit for Resolution to create Work Orders
- [ ] Update asset properties after work completion
- [ ] Check for emergency condition triggers

---

**For detailed Work Order procedures, see:** [Work Order User Manual](work-order-management-guide.md)
