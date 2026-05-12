# Phase 3.1: Emergency Maintenance

[Back to Main Manual](./00_EAM_User_Manual.md)

---

## Purpose

Use this phase when an asset fails unexpectedly and the work cannot wait for the normal preventive maintenance flow.

This phase starts with a `Maintenance Request` marked as **Emergency**. The system then creates a `Work Order` and a linked `Work Order Activity` immediately when the request is moved using **Submit for Emergency**.

By the end of this phase, you will have:

- An emergency `Maintenance Request`
- A `Work Order` for urgent execution
- A linked `Work Order Activity`
- A clear path to continue into Phase 4: Work Management

---

# 🚨 1. Create the Emergency Maintenance Request

Use the installed conveyor example from the earlier phases.

1. Go to **Maintenance Request** → **New**
2. Fill in the request using the failed asset, for example:

| Field | Value | Why it matters |
| ----- | ----- | -------------- |
| Requestor | [responsible employee] | Person reporting the failure |
| Requested Date | [today] | The date the emergency was reported |
| Description | `Emergency conveyor shutdown at Screw Press Line A` | Main issue summary |
| Priority | `Emergency` | Required for emergency processing |
| Asset | `SCREW-001` | The failed asset |
| Request Type | `Corrective Maintenance` or the matching emergency activity type | Defines the type of work |
| Location | `Waste Water Treatment Area` | Where the issue happened |
| Site | `Polomolok` | Site reference |
| Department | `Production` | Department reference |
| Position | `CONV-LINE-A-01` | Exact equipment position |
| Due Date | [today] | Emergency work is due immediately |

> 📌 `Priority` must be **Emergency** before you use **Submit for Emergency**.

---

# ⚡ 2. Move the Request with Submit for Emergency

1. Save the `Maintenance Request`
2. Click **Submit for Emergency**

## What the system does

When you use **Submit for Emergency**, the system immediately creates:

- A `Work Order`
- A linked `Work Order Activity`

The emergency path is different from the normal preventive path:

- It does **not** wait for the standard approval-and-release sequence
- It creates the `Work Order` immediately
- It creates the `Work Order Activity` immediately
- Resource tabs start empty and must be filled by the user

---

# 📄 3. Review the Emergency Work Order

After the emergency submission:

1. Open the generated `Work Order`
2. Confirm these values:

| Field | Expected Value |
| ----- | -------------- |
| Priority | `Emergency` |
| Type | Usually `Corrective Maintenance` |
| Site | `Polomolok` |
| Department | `Production` |
| Due Date | [today] |

3. Open the linked `Work Order Activity` from the `Work Order`
4. Confirm that it is linked to the correct asset and location

> 📌 Unlike preventive work, the emergency path does not automatically bring in planned checklist, parts, labor, or equipment from a maintenance plan.

---

# 🧰 4. Add the Required Emergency Resources

Before the `Work Order Activity` can move to **Ready**, add the resources needed for the repair.

## Minimum requirement

The emergency path still requires at least `Work Order Labor` before allocation can continue.

1. Open the `Work Order Activity`
2. Add at least one row in **Work Order Labor**
3. Add `Work Order Parts` if spare parts are needed
4. Add `Work Order Equipment` if tools or support equipment are needed
5. Add a `Work Order Checklist` if you want inspection or sign-off steps recorded

---

# ✅ 5. Prepare the Work Order Activity for Execution

1. In the `Work Order Activity`, click **Allocate**
2. Confirm the record moves to **Ready**
3. Return to the `Work Order`
4. Approve the `Work Order` if it is still in **Requested**
5. Click **Start** on the `Work Order`

## What happens next

- The `Work Order` moves to **In Progress**
- The linked `Work Order Activity` can begin execution
- The work now continues under Phase 4: Work Management

---

# 📋 6. Records Created

This phase creates or updates the following:

- `Maintenance Request`
- `Work Order`
- `Work Order Activity`
- Optional `Work Order Labor`
- Optional `Work Order Parts`
- Optional `Work Order Equipment`
- Optional `Work Order Checklist`

---

# 🔗 Dependencies

- Phase 1: Setting Up
- Phase 2: Item Acquisition and Procurement
- Phase 2.1: Asset Installation (Optional)
- Phase 3: Maintenance Management
