# Design Notes

## Design references
- shadcn/ui dashboard example: https://ui.shadcn.com/examples/dashboard
- shadcn/ui dashboard and sidebar blocks: https://ui.shadcn.com/blocks?category=dashboard

Use these as references for the sidebar, summary cards, and table layout. Keep the project simpler than the full examples and do not copy unrelated features.

## Basic rules
- Light background with dark text
- One main accent color
- Use status labels with both text and color
- Avoid too many animations or gradients
- Make forms easy to read
- Support normal laptop and desktop widths first, then make the layout usable on mobile
- Use consistent spacing and button styles
- Use only normal HTML, CSS, and JavaScript for the first frontend version

## Pages
1. Dashboard
2. Repair Orders
3. New Repair Order form
4. Repair Order Details
5. Spare Parts
6. Customer Status Lookup

## Coding-agent prompt
Create a simple and usable frontend for a student project called FixFlow, a repair-order management app for a small laptop repair shop. Use the provided dashboard references for a sidebar, summary cards, and an orders table, but keep the design simple. Use HTML, CSS, and JavaScript modules with a separate mock service. Include a dashboard, repair orders table with search and status filters, a repair details page, a spare parts table, and a customer status lookup. Use realistic sample data. Do not add unrelated features or a complicated framework.
