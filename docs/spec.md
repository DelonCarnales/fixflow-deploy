# FixFlow - Basic Specification

## Problem
Small repair shops can lose track of repair details when they use paper notes or chat messages. FixFlow keeps the main information together.

## MVP requirements

### Repair orders
Each order should have:
- Order number
- Customer name and phone
- Device type and model
- Problem description
- Date received
- Status
- Assigned technician (optional)
- Estimated cost (optional)
- Notes

Allowed statuses:
- Received
- Diagnosing
- Waiting for parts
- Repairing
- Ready for pickup
- Completed
- Cancelled

### Order list
The user can see orders, search by order number/customer/device, and filter by status.

### Order details
The user can open an order, see its details, and change its status. Status changes should be recorded with a date and time.

### Spare parts
The user can view parts, their current stock, and price. For the MVP, adding and editing parts is enough; automatic supplier ordering is not needed.

### Customer status lookup
A customer can enter an order number and see the current repair status plus a short status message. The public page must not show private staff notes or unnecessary customer information.

### Dashboard
Show simple totals: all active orders, orders waiting for parts, ready for pickup, and completed orders.

## Basic validation
- Customer name, device model, and problem description are required.
- Estimated cost cannot be negative.
- Order status must be one of the allowed values.
- Spare-part stock cannot be negative.
- Invalid form input should show a readable error.

## Design direction
Use a simple, clean layout with a left sidebar, readable tables, clear status labels, and ordinary buttons/forms. It should look like a realistic student project, not an over-designed enterprise product.

## Success criteria
A user can create a repair order, find it in the list, change its status, refresh the page, and still see the saved data after SQLite is added. A customer can look up the status with an order number.
