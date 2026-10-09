# CarScope — Brand & UI Guidelines

## 1. Brand name
**CarScope** (capital C and S, no space).
- Product label: **CarScope**
- Tagline: **Explore cars. Compare smarter.**
- Descriptive subtitle: **Interactive Vehicle Data Analytics**
- Never use “official market valuation” or imply affiliation with a vehicle brand.
- Tone: clear, analytical, modern, trustworthy, student-friendly. Avoid hype and exaggerated claims.
- Branding Rule: Do not place car icons or pictures next to the CarScope title or section headers. Keep branding clean, text-based, and minimal.

## 2. Visual direction
Build a clean, light, modern analytics workspace. The emphasis is readable dark typography, bright white card surfaces, ocean blue accents, crisp graphs, and clear comparisons.

Design keywords: **clean, light, precise, readable, spacious, modern**.
- Primary UI: light off-white canvas with bright white surfaces, subtle light grey borders, and ocean blue accents.
- Charts: crisp, high contrast on white background, no 3D or dark futuristic gradients.
- Content hierarchy: strong page title, short intro, KPI row, primary plot, secondary analysis.
- Avoid car photos, car icons next to headers, saturated neon, tiny charts, crowded cards, dark futuristic themes, and ornamental animations.

## 3. Colors
| Token | Hex | Use |
|---|---|---|
| `background` | `#FAFAFA` | App canvas |
| `sidebar` | `#F1F5F9` | Sidebar/navigation |
| `surface` | `#FFFFFF` | Cards and panels |
| `surface_elevated` | `#FFFFFF` | Hover/active panels |
| `border` | `#E2E8F0` | Dividers, panel outlines |
| `text_primary` | `#0F172A` | Main text (deep slate) |
| `text_secondary` | `#475569` | Labels and descriptions |
| `primary` | `#0284C7` | Primary actions, focused selections, key chart series |
| `secondary` | `#6366F1` | Secondary chart series |
| `positive` | `#10B981` | Positive change, success |
| `warning` | `#F59E0B` | Caution and quality warnings |
| `danger` | `#EF4444` | Validation errors, destructive actions |

Follow accessible contrast rules; don't encode meaning by color alone. Do not represent arbitrary increases as positive or decreases as negative: context matters (e.g., higher price isn't automatically good).

## 4. Chart palette
For multiple categories, cycle through readable colors:
`#0284C7`, `#6366F1`, `#10B981`, `#F59E0B`, `#EF4444`, `#8B5CF6`, `#06B6D4`, `#84CC16`.
- Use primary ocean blue for the most important metric, muted tones elsewhere.
- Use Seaborn/Matplotlib plot backgrounds matching white `#FFFFFF` surface with dark text/tick overrides.
- Reference/grid lines: subtle light grey (`#E2E8F0`), never overpower data.
- Avoid rainbow colormaps, especially for continuous numerical variables.
- For correlation heatmaps, use a clean blue color palette centered at zero and display a labeled colorbar.
- Provide legend/category labels where colors distinguish groups; limit simultaneous category colors.

## 5. Typography
- Interface heading: **Inter**, with `system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif` fallback.
- Body: Inter/system sans.
- Numbers and tabular data: tabular numerals where feasible.
- Code snippets: `ui-monospace, SFMono-Regular, Consolas, monospace`.

Suggested desktop scale:
- Main title: 30–34 px, 700 weight.
- Section title: 20–24 px, 650–700 weight.
- Card KPI: 26–32 px, 700 weight.
- Body: 14–16 px, comfortable line height.
- Caption / axis labels: 12–13 px minimum whenever feasible.

## 6. Layout and spacing
- Wide dashboard layout in Streamlit via `st.set_page_config(layout="wide", page_title="CarScope")`.
- Sidebar: upload and navigation at top, filters grouped beneath, reset filters clearly visible.
- Use a consistent 8 px spacing rhythm; typical card padding 20–24 px.
- Use rounded corners 10–12 px; low-contrast borders (`#E2E8F0`); subtle light shadows (`0 1px 3px rgba(0,0,0,0.05)`).
- Desktop KPI row: 3–5 balanced cards depending on width.
- Charts: preferably 2-column when readable, full width for complex scatterplots/tables/heatmaps.
- Keep content within reasonable line lengths and leave sufficient breathing room.
- Narrow screens: stack charts and metrics, avoid horizontal cutoff where possible.

## 7. UI components
### Sidebar
- CarScope brand + short subtitle (no car icon).
- CSV upload card and active dataset details.
- Clear page navigation and global filters.
- Each filter has readable label, units when needed, and reset behavior.

### KPI cards
- White card surface, light border, dark readable number, concise label.
- Examples: “Total Vehicles”, “Median Price”, “Unique Makes”, “Average Mileage”.

### Buttons
- Primary: ocean blue background, white readable text (`#FFFFFF`), used for meaningful actions.
- Secondary: bordered light surface.
- Destructive/reset: distinct but not alarmist.

### Data tables
- Light surface with subtle row dividers and dark text.
- Consistent currency, distance, number formats.
- Sortability and export where useful.

### Chart containers
- Short title, optional one-line subtitle explaining aggregation/sample.
- Chart itself on white background, readable dark axes, units, legend if needed.

## 8. Data visualization ethics
- Zero-baseline for bar charts.
- Distinguish mean versus median clearly.
- Do not claim causality from a correlation or regression line.
- Don't hide outliers silently.
- Display counts when comparing group averages.
- Use comparable units and consistent scales when comparing cars.

## 9. Accessibility
- High contrast text (`#0F172A` on `#FFFFFF` / `#FAFAFA`).
- Readable focus states and interactive control labels.
- Charts should have plain-English descriptions or adjacent accessible summaries.
- Never convey information only with color or an icon.

## 10. Streamlit implementation notes
- Use `.streamlit/config.toml` with `backgroundColor = "#FAFAFA"`, `secondaryBackgroundColor = "#F1F5F9"`, `primaryColor = "#0284C7"`, `textColor = "#0F172A"`.
- Use targeted CSS in `src/ui.py` to enforce light mode surfaces on `.stApp`, `section[data-testid="stSidebar"]`, `header[data-testid="stHeader"]`, `.kpi-card`, `.stExpander`, dropdowns, and text inputs with `!important`.
