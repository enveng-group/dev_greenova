# CSS Organization Plan

## Template to CSS Class Mapping

### Dashboard Components
- `project_content.html`: `.grid`
- `dashboard/components/project_content.html`, `chart_container.html`: `.chart-container`
- `obligation_list.html`: `.table-container`
- `dashboard.html`: 
    - `.project-selection`
    - `#project-select`
    - `#dashboard-content`
    - `.app-status` (footer)
- `project_content.html`: `#obligations-section`
- `obligation_list.html`: `#obligations-table`

### Chat Widget Components
- `chat_widget.html`:
    - `.chat-widget`
    - `.chat-container`
    - `.chat-header`
    - `.chat-messages`
    - `.chat-form`
    - `.bot-message`
    - `.user-message`

### Global Components
- Multiple templates: `[aria-busy="true"]`, `.htmx-indicator`

## PicoCSS Coverage
- Forms
- Typography
- Basic layouts
- Tables
- Articles/sections
- Alerts
- Headers/footers
- Basic grid system
- Basic containers

## Required Custom CSS
1. Chart Visualization:
     - Canvas dimensions
     - Responsive behaviors

2. HTMX Integration:
     - Loading states
     - Indicators
     - Interaction feedback

3. Custom Layouts:
     - Dashboard grids
     - Chart positioning
     - Widget placements

4. Interactive Elements:
     - Status indicators
     - Loading states
     - Position fixes
     - Content transitions

## Optimization Steps
1. Remove PicoCSS-covered styles
2. Maintain app-specific CSS
3. Use semantic HTML elements
4. Validate remaining classes
5. Test responsive behaviors
6. Verify HTMX integration
