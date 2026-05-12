# Phase 4: Daily Operations

[Back to Main Manual](./00_EAM_User_Manual.md)

## Purpose

Execute day-to-day work management.

## Function Signature

```text
phase4_daily_operations(work_requests) -> work_records
```

## Required Input Records

| Entity              | Field       | Value                 | Notes                    |
| ------------------- | ----------- | --------------------- | ------------------------ |
| Maintenance Request | asset       | SCREW-001             | From Asset               |
| Maintenance Request | requestor   | [Employee ID]         | From Employee            |
| Maintenance Request | description | [problem description] | Issue details            |
| Maintenance Request | priority    | [urgency level]       | Critical/High/Medium/Low |

| Work Order | maintenance_request | [Request ID] | From Maintenance Request |
| Work Order | asset | SCREW-001 | From Asset |
| Work Order | assigned_to | [Employee ID] | From Employee |
| Work Order | scheduled_date | [planned date] | When to work |
| Work Order | status | Scheduled/In Progress/Completed | Current status |

| Labor | work_order | [WO ID] | From Work Order |
| Labor | employee | [Employee ID] | From Employee |
| Labor | actual_hours | [hours worked] | Time spent |
| Labor | work_date | [date] | When performed |

| Item Issue | work_order | [WO ID] | From Work Order |
| Item Issue | item | [Item ID] | From Item |
| Item Issue | quantity_issued | [amount] | Parts used |
| Item Issue | bin_location | [Bin ID] | From Bin |

## Output Records

- Maintenance Request IDs
- Work Order IDs
- Labor records
- Item Issue records
- Updated inventory

## Dependencies

- Phase 3: Maintenance Activities and Plans
- Phase 2.1: Asset Installation (Optional)
- Phase 1: Setting Up
