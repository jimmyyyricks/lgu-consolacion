# EAM User Manual

---

## Understanding EAM Through a Real Example

An Enterprise Asset Management (EAM) system helps organizations track and manage physical equipment throughout its entire lifecycle — from purchase to disposal.

To understand how this works, let’s follow a real example:

> **METPower** needs to acquire, install, and maintain a **screw press conveyor**.

This single piece of equipment will interact with every part of the system:

- It must be **purchased** (Procurement)
- It becomes a tracked **asset** (Asset Management)
- It requires **maintenance** (Maintenance Management)
- It consumes **spare parts** (Inventory Management)
- It is serviced through **work orders** (Work Management)

This manual walks you through setting up the system and managing this equipment step-by-step.

---

# 📘 Table of Contents

---

## 1. Implementation Phases

| Phase         | Description                                                                                        | Link                                                          |
| ------------- | -------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **Phase 1**   | **Setting Up** – Define all foundational master data                                               | [View Details](./phase-1-setting-up.md)                       |
| **Phase 2**   | **Item Acquisition and Procurement** – Define, purchase, and receive items                         | [View Details](./phase-2-item-acquisition-procurement.md)     |
| **Phase 2.1** | **Asset Installation (Optional)** – Install procured assets that need commissioning                | [View Details](./phase-2-1-asset-installation.md)             |
| **Phase 3**   | **Maintenance Management** – Define maintenance activities, plans, schedules, and request triggers | [View Details](./phase-3-maintenance-activities-plans.md)     |
| **Phase 3.1** | **Emergency Maintenance** – Handle emergency `Maintenance Request` records and urgent work         | [View Details](./phase-3-1-emergency-maintenance.md)          |
| **Phase 4**   | **Work Management** – Execute `Work Order` and `Work Order Activity` records                       | [View Details](./phase-4-work-management.md)                  |
| **Phase 4.1** | **Issuing and Returning Items** – Issue parts and equipment, then return unused materials          | [View Details](./phase-4-1-issuing-returning-items.md)        |
| **Phase 5**   | **Stock Count and Inventory Adjustment** – Count stock and post inventory reconciliation           | [View Details](./phase-5-stock-count-inventory-adjustment.md) |

---

## 1.1 Overall Process Flow

```text
Phase 1: Setting Up
        ↓
Phase 2: Item Acquisition and Procurement
        ↓
Phase 2.1: Asset Installation (Optional)
        ↓
Phase 3: Maintenance Management
        ↓
Phase 3.1: Emergency Maintenance
        ↓
Phase 4: Work Management
        ↓
Phase 4.1: Issuing and Returning Items
        ↓
Phase 5: Stock Count and Inventory Adjustment
```

### Process Meaning

- **Phase 1** creates the master data
- **Phase 2** brings items into the system
- **Phase 2.1** places fixed assets into service
- **Phase 3** sets up preventive maintenance
- **Phase 3.1** handles urgent breakdown work
- **Phase 4** executes work using `Work Order` and `Work Order Activity`
- **Phase 4.1** controls part and equipment movement during work
- **Phase 5** reconciles stock and corrects inventory balances

---

## 2. Quick Reference Guides

| Topic                     | Description                            | Link                                                |
| ------------------------- | -------------------------------------- | --------------------------------------------------- |
| **Item Types Reference**  | How Item Types affect processing       | [View Guide](./references/item-types-reference.md)  |
| **System Reference Data** | Pre-loaded and required system records | [View Guide](./references/system-reference-data.md) |
| **Daily Operations**      | Common tasks and workflows             | [View Section](#daily-operations-guide)             |
| **Role-Based Access**     | Responsibilities per user role         | [View Section](#role-based-access)                  |
| **Integration Points**    | How modules interact across the system | [View Section](#integration-points)                 |

---

## 3. Module-Specific Guides

| Module                            | Purpose                                           | Link                                                                |
| --------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------- |
| **Installing Asset**              | Asset activation and placement                    | [View Guide](./phase-2-1-asset-installation.md)                     |
| **Maintenance Management**        | Maintenance planning and execution                | [View Guide](./phase-3-maintenance-activities-plans.md)             |
| **Emergency Maintenance**         | Emergency `Maintenance Request` workflow          | [View Guide](./phase-3-1-emergency-maintenance.md)                  |
| **Work Management**               | `Work Order` and `Work Order Activity` execution  | [View Guide](./phase-4-work-management.md)                          |
| **Issuing and Returning Items**   | Item issue, return, and putaway flow              | [View Guide](./phase-4-1-issuing-returning-items.md)                |
| **Stock Count and Adjustment**    | Stock reconciliation and posting                  | [View Guide](./phase-5-stock-count-inventory-adjustment.md)         |
| **Maintenance Workflow Tutorial** | Forklift example for preventive maintenance setup | [View Guide](./supporting-workflows/maintenance-workflow-guide.md)  |
| **Procurement Workflow**          | Purchase request, order, and receipt flow         | [View Guide](./supporting-workflows/procurement-workflow.md)        |
| **Work Order Management**         | Supporting walkthrough for work execution         | [View Guide](./supporting-workflows/work-order-management-guide.md) |
| **Item Issue & Return**           | Inventory movement and tracking                   | [View Guide](./step-by-step/item_issue_item_return.md)              |

---

## 4. Getting Started

| Step  | Action                                                                            | Resources                 |
| ----- | --------------------------------------------------------------------------------- | ------------------------- |
| **1** | Review System Reference Data                                                      | Pre-configured data       |
| **2** | Complete **Phase 1: Setting Up**                                                  | Foundation setup          |
| **3** | Continue through Phases **2**, **2.1**, **3**, **3.1**, **4**, **4.1**, and **5** | Official phase guides     |
| **4** | Configure user roles and permissions                                              | System Admin              |
| **5** | Train users based on role                                                         | Training materials        |
| **6** | Begin daily operations                                                            | Work and inventory guides |

---

# ⚡ Quick Reference

| Task                     | Navigation                | Notes                         |
| ------------------------ | ------------------------- | ----------------------------- |
| **New Equipment**        | Purchase Request → New    | Always start with PR          |
| **Asset Registration**   | Asset → New               | Requires Item + Position      |
| **Maintenance Planning** | Maintenance Plan → New    | Define intervals and triggers |
| **Breakdown Repair**     | Maintenance Request → New | Use for emergency issues      |
| **Parts Issue**          | Item Issue → New          | Link to work order            |

---

# 👥 Role-Based Access

### Maintenance Technician

- Execute assigned work orders
- Record work progress and hours
- Request parts
- Report additional issues

---

### Maintenance Supervisor

- Plan and schedule work
- Assign technicians
- Approve requests
- Monitor maintenance compliance

---

### Production Manager

- Report equipment issues
- Submit maintenance requests
- Monitor equipment availability

---

### Warehouse Keeper

- Issue and receive inventory
- Manage stock levels
- Perform cycle counts

---

### Purchasing Staff

- Process purchase requests
- Manage vendors
- Track purchase orders and deliveries

---

# 🔗 Integration Points

## Data Flow

- Master data (Phase 1) feeds all processes
- Procurement updates inventory and enables asset creation
- Asset installation links items → assets → positions
- Maintenance consumes labor, parts, and equipment
- Financial data tracks all costs

---

## Process Integration

- Maintenance plans trigger work orders
- Work orders consume inventory and labor
- Inventory levels affect procurement decisions
- Asset performance influences maintenance strategy

---

# 🛠️ Daily Operations Guide

---

## For Maintenance Technicians

- Check assigned work orders daily
- Record actual work and time spent
- Report issues found during work
- Request materials if needed

---

## For Maintenance Planners

- Review pending work orders
- Schedule jobs based on priority
- Assign labor and resources
- Track preventive maintenance compliance

---

## For Purchasing Staff

- Process incoming purchase requests
- Create and send purchase orders
- Track delivery status
- Coordinate with vendors

---

## For Storekeepers

- Issue materials to work orders
- Receive incoming stock
- Maintain accurate inventory
- Perform stock counts

---

# 📋 Common Tasks

| Task                | Where to Go               | Key Steps                       |
| ------------------- | ------------------------- | ------------------------------- |
| Request Maintenance | Maintenance Request → New | Select asset, describe issue    |
| View Work Orders    | Work Order → List         | Filter by technician/date       |
| Order Parts         | Purchase Request → New    | Select item, quantity           |
| Update Inventory    | Inventory → Item          | Adjust stock or review movement |
| Create Asset        | Asset → New               | Link item + position            |

---

# 🧯 Troubleshooting

---

### Can't Find an Item

- Ensure item is created in Item Master
- Check Item Class
- Verify permissions

---

### Work Order Won’t Close

- Ensure all activities are completed
- Record actual labor hours
- Confirm parts issued/returned

---

### Inventory Incorrect

- Review recent transactions
- Check pending receipts/issues
- Perform stock count

---

### Purchase Request Stuck

- Check approval workflow
- Verify required fields
- Confirm budget/cost code

---

# 🧭 System Navigation Tips

---

### Finding Records

- Use global search
- Apply filters (site, date, status)
- Bookmark frequently used pages

---

### Keyboard Shortcuts

- `Ctrl + /` → Search
- `Ctrl + N` → New record
- `Ctrl + S` → Save
- `Esc` → Cancel

---

### Mobile Usage

- Accessible via tablet/mobile
- Useful for field technicians
- Sync required after offline work

---

# 🆘 Getting Help

---

### Within the System

- Use Help icon per field
- Access User Guide
- Check System Status

---

### Support Contacts

- **System Admin** → Access & setup
- **Manager** → Workflow questions
- **IT Help Desk** → Technical issues

---

### Training Resources

- Built-in guides
- Video tutorials
- Internal documentation

---

# ✅ Implementation Checklist

---

## Phase 1: Setting Up

- [ ] All master data created (see Phase 1)
- [ ] No missing references in dropdowns
- [ ] Sample Item, Employee, Position created successfully

---

## Phase 2: Item Acquisition and Procurement

- [ ] Items fully defined
- [ ] Asset Classes finalized
- [ ] Purchase Request workflow tested
- [ ] Inventory updates correctly

---

## Phase 2.1: Asset Installation (Optional)

- [ ] Assets registered
- [ ] Linked to positions
- [ ] Activated and tracked

---

## Phase 3: Maintenance Management

- [ ] Maintenance activities created
- [ ] Maintenance plans created
- [ ] Planned maintenance activities configured
- [ ] Request triggers reviewed

---

## Phase 3.1: Emergency Maintenance

- [ ] Emergency `Maintenance Request` tested
- [ ] `Submit for Emergency` workflow verified
- [ ] Emergency `Work Order` and `Work Order Activity` created successfully

---

## Phase 4: Work Management

- [ ] `Work Order` approval and start flow tested
- [ ] `Work Order Activity` allocation completed
- [ ] Labor, parts, equipment, checklist, and logs recorded
- [ ] `Work Order` closure validated

---

## Phase 4.1: Issuing and Returning Items

- [ ] `Item Issue` tested for parts
- [ ] `Item Issue` tested for equipment
- [ ] `Item Return` tested for parts
- [ ] `Item Return` tested for equipment

---

## Phase 5: Stock Count and Inventory Adjustment

- [ ] `Stock Count` lines generated or entered manually
- [ ] Counted quantities and variances reviewed
- [ ] `Inventory Adjustment` created from approved count
- [ ] `Inventory Adjustment` submitted and posted successfully

---

## Completed Checklist Items

- [ ] Supporting workflow guides moved to the separate workflow folder
- [ ] Official phase guides reviewed in sequence

---

# 🔑 Final Note

> A successful EAM implementation depends on **strong Phase 1 setup**.

If your foundation is correct:

- All modules will connect seamlessly
- Users will experience fewer errors
- Scaling the system becomes easier

---

## 🚀 Next Step

Proceed to:

👉 **Phase 1: Setting Up**
and complete all foundational records before continuing.

---
