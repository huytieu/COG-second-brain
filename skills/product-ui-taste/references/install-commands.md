# Install / CLI per system

Reference for product-ui-taste: package-manager install commands for each supported host design system.

## Appendix A - Install / CLI per system

```bash
# House design system - resolve the real API before writing UI.
# Most systems ship a CLI or a docs site; use whichever exists.
#   1. find the closest shipped page/block template
#   2. study its layout skeleton
#   3. read real props for every component (never invent props)

# IBM Carbon
npm install @carbon/react @carbon/styles
# Microsoft Fluent UI React v9
npm install @fluentui/react-components
# Atlassian Atlaskit (per-component + tokens)
npm install @atlaskit/tokens @atlaskit/dynamic-table
# Shopify Polaris
npm install @shopify/polaris
# GitHub Primer React
npm install @primer/react styled-components
# Radix Primitives + shadcn/ui + TanStack Table
npm install @radix-ui/react-dialog @radix-ui/react-toast @tanstack/react-table
npx shadcn@latest add table dialog
# Material Web (Material 3)
npm install @material/web
# Ant Design / Mantine + Mantine React Table
npm install antd
npm install @mantine/core @mantine/form mantine-react-table
```
