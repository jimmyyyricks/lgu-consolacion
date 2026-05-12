# Procurement Workflow

[Back to Main Manual](../00_EAM_User_Manual.md)

## Purpose

Execute the purchasing process for equipment and materials, including the warehouse structure needed to receive and store them.

## Function Signature

```text
procurement_workflow(purchase_requests) -> procurement_records
```

## Required Input Records

| Entity           | Field         | Value           | Notes             |
| ---------------- | ------------- | --------------- | ----------------- |
| Purchase Request | requestor     | [Employee ID]   | From Employee     |
| Purchase Request | department    | Maintenance     | From Department   |
| Purchase Request | cost_code     | MAINT           | From Cost Code    |
| Purchase Request | item          | SCREW-CONV-001  | From Item         |
| Purchase Request | quantity      | 1               | Purchase quantity |
| Purchase Request | delivery_date | [required date] | When needed       |
| Purchase Request | unit_cost     | [quoted price]  | Supplier price    |

| Purchase Order | purchase_request | [PR ID] | From Purchase Request |
| Purchase Order | vendor | [equipment vendor] | From Vendor |
| Purchase Order | order_date | [current date] | Order placed |

| Purchase Receipt | purchase_order | [PO ID] | From Purchase Order |
| Purchase Receipt | item | SCREW-CONV-001 | From Item |
| Purchase Receipt | quantity_received | 1 | Actual receipt |
| Purchase Receipt | receipt_date | [current date] | Date received |

#### Store

Physical warehouse used to receive and hold materials.

| Field      | Value                     |
| ---------- | ------------------------- |
| store_name | "Surallah Main Warehouse" |
| location   | Site Office               |
| site       | Polomolok                 |

#### Zone

Storage area inside the warehouse.

| Field     | Value                   |
| --------- | ----------------------- |
| zone_name | "Spare Parts Zone"      |
| store     | Surallah Main Warehouse |
| site      | Polomolok               |

#### Bin

Specific storage slot inside a warehouse zone.

| Field      | Value                   |
| ---------- | ----------------------- |
| rack_name  | "A"                     |
| shelf_name | "1"                     |
| bin_name   | "01"                    |
| store      | Surallah Main Warehouse |
| site       | Polomolok               |

## Output Records

- Purchase Request IDs
- Purchase Order IDs
- Purchase Receipt IDs
- Updated inventory quantities
- Store, Zone, and Bin records

## Dependencies

- Phase 1: Setting Up
- Phase 2: Item Acquisition and Procurement
