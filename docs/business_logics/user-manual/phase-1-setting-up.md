# Phase 1: Setting Up

[Back to Main Manual](./00_EAM_User_Manual.md)

---

## Purpose

> 🧱 Set up the foundation for the rest of the EAM process.
>
> This phase creates the company structure, the main site, and the first operational records needed before you can move on to procurement, assets, and maintenance.

By the end of this phase, all required master data will be in place so that:

- Procurement can run without missing references
- Assets can be created and installed
- Maintenance can be configured
- Work orders can be executed

> ⚠️ If Phase 1 is incomplete, later phases will fail due to missing dependencies.

---

### Function Signature

```text
phase1_setting_up() -> foundation_records
```

---

# 🧱 1. Organization & Financial Foundation

Defines who you are and how costs are tracked.

### Organization

> 🏢 The top-level company record.

| Field               | Value                     |
| ------------------- | ------------------------- |
| organization_name   | "METPower"                |
| legal_name          | [your legal company name] |
| organizational_code | "METPOWER"                |
| is_active           | Yes                       |

### Cost Code

> 💰 Shared accounting code used by operational records.

| Field       | Value        |
| ----------- | ------------ |
| code        | "M003C00011" |
| description | Global       |

### Site

> 📍 Main operating site under the organization.

| Field        | Value       |
| ------------ | ----------- |
| site_name    | "Polomolok" |
| organization | METPower    |
| cost_code    | M003C00011  |

### Department

> 👥 Team or business unit assigned to a site.

| Field             | Value         |
| ----------------- | ------------- |
| department_name   | "Maintenance" |
| department_code   | "MAINT-P"     |
| site              | Polomolok     |
| default_cost_code | M003C00011    |

### Location Type

> 🏷️ Predefined label that describes what kind of place a location is.

| Field | Value  |
| ----- | ------ |
| name  | "Zone" |

### Location

> 🗺️ A specific place of work inside the site.
>
> Example: a treatment area, office, or workshop. For this manual, use the waste water processing area where the screw press conveyor is installed.

| Field           | Value                                                                           |
| --------------- | ------------------------------------------------------------------------------- |
| name            | "Waste Water Treatment Area"                                                    |
| description     | "Operating area for the screw press conveyor and related waste water equipment" |
| location_type   | Zone                                                                            |
| parent_location | [optional parent location]                                                      |
| site            | Polomolok                                                                       |
| latitude        | [optional latitude]                                                             |
| longitude       | [optional longitude]                                                            |
| address         | [optional address]                                                              |

### Asset Class

> 🧰 Grouping used to classify assets and positions.

| Field              | Value                                          |
| ------------------ | ---------------------------------------------- |
| name               | "Rotating Equipment"                           |
| description        | "Motors, pumps, conveyors, rotating machinery" |
| class_icon         | [optional image]                               |
| due_date_lead_time | 7                                              |
| parent_asset_class | [optional parent class]                        |

### Asset Class Property

> 🔗 Links a property to an asset class, setting default values for all assets of that class.

| Field           | Value              |
| --------------- | ------------------ |
| asset_class     | Rotating Equipment |
| property        | Capacity           |
| unit_of_measure | Nos                |
| default_value   | [optional value]   |

### System Type

> 🧩 Simple label used to group systems.

| Field | Value                |
| ----- | -------------------- |
| name  | "Waste Water System" |

### System

> ⚙️ A system groups related positions under a location.

| Field         | Value                                                     |
| ------------- | --------------------------------------------------------- |
| name          | "Screw Press Line A"                                      |
| description   | "Primary screw press conveyor line at the Polomolok site" |
| system_type   | Waste Water System                                        |
| parent_system | [optional parent system]                                  |
| location      | Waste Water Treatment Area                                |
| site          | Polomolok                                                 |

### Position

> 📌 A physical placeholder where an asset can be installed.

| Field         | Value                           |
| ------------- | ------------------------------- |
| position_tag  | "CONV-LINE-A-01"                |
| description   | "Screw Press Conveyor Position" |
| asset_class   | Rotating Equipment              |
| system        | Screw Press Line A              |
| location      | Waste Water Treatment Area      |
| attach_img    | [optional image]                |
| current_asset | [optional current asset]        |

### Employee

> 👤 Staff record used for assignment and approvals.

| Field         | Value                    |
| ------------- | ------------------------ |
| user          | [optional user account]  |
| employee_name | [Name]                   |
| position      | "Maintenance Supervisor" |

### Vendor

> 🧰 Supplier or service provider record.

| Field       | Value              |
| ----------- | ------------------ |
| vendor_name | [Equipment vendor] |

### Account

> 🧾 Finance account used for tracking costs.

| Field        | Value          |
| ------------ | -------------- |
| account_code | [account code] |
| account_name | [account name] |
| account_type | Equipment      |

### Currency

> 💱 Currency used for costs and purchases.

| Field | Value |
| ----- | ----- |
| code  | PHP   |

### Manufacturer

> 🏭 Brand owner of the screw press conveyor.

| Field        | Value            |
| ------------ | ---------------- |
| company_name | WAMGROUP         |
| email        | [optional email] |

### Model

> 🛠️ Specific product model for the conveyor.

| Field        | Value                                 |
| ------------ | ------------------------------------- |
| name         | "Screw Press Conveyor Model S Series" |
| manufacturer | WAMGROUP                              |

### Unit of Measure

> 📏 Measurement used for items and inventory.

| Field      | Value |
| ---------- | ----- |
| name       | Nos   |
| short_name | nos   |

### Property Type

> 🧪 Type of custom property value.

| Field | Value   |
| ----- | ------- |
| name  | Numeric |

### Property

> 🧩 Custom property that can be attached to assets or classes.

| Field           | Value                                        |
| --------------- | -------------------------------------------- |
| name            | Capacity                                     |
| description     | Maximum throughput for the conveyor assembly |
| unit_of_measure | Nos                                          |
| property_type   | Numeric                                      |
| system          | false                                        |
| inactive        | false                                        |

### Asset Property

> 🔗 Links a property to a specific asset.

| Field           | Value            |
| --------------- | ---------------- |
| asset           | [linked asset]   |
| property        | Capacity         |
| property_value  | [optional value] |
| unit_of_measure | Nos              |
| property_type   | Numeric          |

### Labor Group

> 👷 Group of labor roles used for maintenance work.

| Field            | Value            |
| ---------------- | ---------------- |
| labor_group_name | Maintenance Team |

### Labor

> 🧑‍🔧 Work record linked to an employee.

| Field    | Value            |
| -------- | ---------------- |
| employee | [employee]       |
| group    | Maintenance Team |

### Trade

> 🔩 Skill area used for labor planning.

| Field | Value    |
| ----- | -------- |
| name  | Mechanic |

## Output Records

> ✅ This phase creates the following records:

- 1 Organization: **METPower**
- 1 Account for equipment and cost tracking
- 1 Currency: **PHP**
- 1 Site: **Polomolok**
- 1 Location Type and 1 Location for the site structure
- 1 Department and 1 Cost Code: **M003C00011**
- 1 Asset Class: **Rotating Equipment**
- 1 Asset Class Property: **Capacity** for **Rotating Equipment**
- 1 Manufacturer: **WAMGROUP**
- 1 Model: **Screw Press Conveyor Model S Series**
- 1 Unit of Measure: **Nos**
- 1 Property Type: **Numeric** and 1 Property: **Capacity**
- 1 Employee, 1 Labor, and 1 Trade record for the **Mechanic** example
- 1 System Type, 1 System: **Screw Press Line A**, and 1 Position: **CONV-LINE-A-01**
- 1 Labor Group

> 🔗 **Continuity Note**: Phase 2 uses the same reference values created here, especially **Rotating Equipment**, **WAMGROUP**, **Nos**, **Screw Press Conveyor Model S Series**, and **CONV-LINE-A-01**.

---

# 🔑 Key Takeaways

- **Site > Location** → defines physical structure
- **System > Position** → defines equipment structure
- **Labor abstracts employees for work execution**
- **Property system enables flexibility**
- **Foundation for Item Acquisition and Procurement in Phase 2**

---

# ⚠️ Completion Rule

Before moving to Phase 2, ensure:

- All dropdowns are selectable (no missing references)
- You can create:
  - Employee ✔
  - Position ✔
  - Organization ✔

If those work, your system is ready for Item Acquisition and Procurement.
