# Block skeletons

Reference for product-ui-taste: worked reference implementations for the three block contracts most often gotten wrong.

### 12.A Block Library (reference implementations)
Full component implementations live in the host system, not duplicated here: reach them via your host system's template/skeleton command or its docs (Appendix B). Three high-value skeletons are worked below because they encode the contracts most often gotten wrong; treat them as the canonical shape, adapt to the host system.

**Block 1 - Index + detail-drawer (frame-first):**
```tsx
// Budget the frame first: nav 256 | table flex | inspector 380
<AppShell sideNav={<SideNav>{/* nav */}</SideNav>} contentPadding={0}>
  <Layout>
    <LayoutContent>
      <ToolbarTableFilter /* search + status/priority filters + overflow (cap 5) */ />
      {/* applied-filter chips row + Clear all (Section 7.F) */}
      <Table
        plugins={[useTableStickyColumns, useTableColumnResize /*, pagination */]}
        /* selection persists by row id across page/sort/filter (Section 7.E) */
      />
      {/* pagination footer; three empty states + ErrorState wired per Section 6 */}
    </LayoutContent>
    <LayoutPanel width={380} resizable={{minSizePx: 320, maxSizePx: 480}} hasDivider isScrollable>
      {selected ? <DetailFields item={selected} /> : <EmptyState title="Nothing selected" />}
    </LayoutPanel>
  </Layout>
</AppShell>
// Below ~1024px: LayoutPanel overlays Content; SideNav becomes MobileNav.
```

**Block 2 - Table scroll + sticky header + frozen column (the CSS contract a system's hooks satisfy):**
```css
/* ONE wrapper owns both scroll axes; page body never scrolls sideways (Section 4). */
.table-scroll { overflow: auto; max-block-size: 70vh; }            /* bounded height => sticky works */
.table-scroll thead th { position: sticky; inset-block-start: 0; z-index: 20; }
/* Frozen first column: sticky + offset + z + SOLID THEME-TOKEN bg + shadow divider, never border */
.col-frozen {
  position: sticky; inset-inline-start: 0; z-index: 10;
  background: var(--color-surface);                 /* must also cover hover/selected rows */
  box-shadow: inset -1px 0 0 var(--color-border);   /* not border-right (double-renders on scroll) */
}
```

**Block 3 - Truncation contract (single-line + multi-line):**
```css
.cell { min-inline-size: 0; }                        /* required on EVERY flex ancestor or ellipsis no-ops */
.cell .text { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.clamp {                                             /* all four props; NO padding on this node */
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
```

