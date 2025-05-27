# Style Guide

## Colour Guide

To change the colours used within the website, all values which are in this
document must be prefixed by "--greenova" while if they exist in picocss must
be overwritten. When adding a colour, make it clear that it is written for
greenova, under the correct category and list the use cases. When changing a
colour of an existing element / pico variable please list the use case, using
as little custom classes as possible.

### Colour Scheme

**Primary Colours**:

- `--greenova-primary-green: #7FB04F;` (Green - Used for primary buttons,
  headers, and highlights)
- `--greenova-primary-orange: #EC7A32;` (Orange - Used for warnings, alerts,
  and accents)
- `--greenova-primary-blue: #30AEE4;` (Blue - Used for links, informational
  messages, and secondary highlights)

**Secondary Colours**:

- `--greenova-secondary-dark-gray: #58595B;` (Dark Gray - Used for text,
  borders, and backgrounds)
- `--greenova-secondary-olive-green: #526827;` (Olive Green - Used for subtle
  highlights and secondary buttons)
- `--greenova-secondary-rust-orange: #CC6114;` (Rust Orange - Used for critical
  alerts and call-to-action elements)
- `--greenova-secondary-teal-blue: #146890;` (Teal Blue - Used for secondary
  links and informational accents)

Please go to "static/css/dist/utils/colours.css",
"static/css/dist/abstracts/variables.css" and "static/css/dist/variables.css".

## HTMX Indicator Requirements

### Persistent Indicator Element

- The `#htmx-indicator` element is provided by `base.html` and must remain
  outside any htmx swap targets.
- Do **not** include or remove `#htmx-indicator` in any content that may be
  swapped by htmx.
- All `hx-indicator` attributes must reference an element that is always
  present in the DOM.
- If you add new htmx-enhanced forms or components, ensure the indicator is not
  inside a swap target.

#### Example

```html
<!-- Correct: indicator outside swap target -->
<div id="htmx-indicator"></div>
<div id="main-content" hx-target="this">
  <!-- Swapped content here -->
</div>

<!-- Incorrect: indicator inside swap target -->
<div id="main-content" hx-target="this">
  <div id="htmx-indicator"></div>
  <!-- This will be removed on swap! -->
</div>
```

See also: `docs/resources/js/htmx.md` and `base.html` for implementation
details.
