# Phase 2.1: Asset Installation (Optional)

[Back to Main Manual](./00_EAM_User_Manual.md)

---

## Purpose

> 🔧 Optional step for procured assets that must be installed or commissioned at a specific position.

Use this phase only when the procured item becomes a physical asset that must be placed into service. The system will create an installation request, release it for resolution, create a work order, and then let you complete the linked `Work Order Activity`.

By the end of this phase, the asset will:

- Be linked to a position
- Carry the correct location and system from that position
- Have an installation record for traceability

# 🧾 1. Validate the Asset Before Installation

The asset must already exist from Phase 2.

### Asset Validation Checklist

> ✅ The asset details below must already be in place before you start installation.

| Field          | Value                           | Why it matters                                         |
| -------------- | ------------------------------- | ------------------------------------------------------ |
| asset_tag      | `SCREW-001`                     | Required, unique asset identifier                      |
| item           | `Screw Press Conveyor Assembly` | The item received in Phase 2                           |
| asset_class    | `Rotating Equipment`            | The class used for planning and follow-up work         |
| serial_number  | [manufacturer serial]           | Used for traceability                                  |
| location       | `Waste Water Treatment Area`    | The current location before installation               |
| site           | `Polomolok`                     | Site where the asset belongs                           |
| system         | `Screw Press Line A`            | The system the asset will belong to after installation |
| position       | `CONV-LINE-A-01`                | The exact installation point                           |
| bypass_process | `false`                         | Standard path for formal approval                      |

> 📌 **Note**: `item` and `inventory` are already set by the system. You do not need to edit them. The installation details become available once the asset moves beyond the `Acquired` stage.

---

# 🏗️ 2. Start the Install Asset Action

1. Open the installed asset record, for example `SCREW-001`.
2. Confirm the asset is ready to be installed.
   - If the asset is still in `Acquired`, run the inspection step first if your process requires it.
3. Click **Actions**.
4. Select **Install Asset**.

### What the system does

- If `bypass_process = false`, the system creates an installation request and a linked `Work Order Activity`.
- If `bypass_process = true`, the system skips the formal request path and creates the installation record directly.

---

# 📝 3. Review the Maintenance Request Path

When the formal path is used:

1. The system creates a `Maintenance Request` for the asset.
2. Change the request to **Submit for Resolution**.
3. The request moves to **Released** and the system creates a **Work Order**.
4. The work order includes the linked `Work Order Activity`.

> 🔗 **Important**: This request is what allows the installation work to move forward. You must release it before you can complete the linked `Work Order Activity`.

---

# 🔨 4. Complete the Work Order Activity

1. Open the **Work Order** created from the request.
2. Open the linked `Work Order Activity` from inside the Work Order.
3. Confirm the following are present:
   - Asset
   - Position
   - Site
   - Department
4. Click **Complete**.

### What happens when you complete the Work Order Activity

- The system creates the installation record.
- The selected position is linked to the asset.
- The asset’s location, system, and position are updated from the selected position.

> ✅ This is the step that places the asset into service.

---

# 📍 5. Confirm the Installed Asset

After completion:

- The asset is linked to its position.
- The asset can now be used in maintenance planning.
- The installation record becomes the reference for future maintenance and location changes.

## Output Records

- Installation request number, when the formal path is used
- Work order number
- Linked `Work Order Activity`
- Installation record
- Updated asset location, system, and position

## Dependencies

- Phase 1: Setting Up
- Phase 2: Item Acquisition and Procurement
