# JavaScript Analysis and Optimization Plan

## 1. Current Function Usage Mapping

### Global Event Listeners
- `htmx:beforeSwap` - Chart cleanup
- `htmx:afterSettle` - Chart initialization 
- `DOMContentLoaded` - Chatbot initialization

### Dashboard Components
- `initializeChart` function
- `updateObligationsTable` function
- Chart instance management (`chartInstances` Map)

### Chat Widget
- `SimpleChatbot` class and methods
- Toggle functionality
- Message handling

## 2. Optimization Opportunities

### A. Move to HTML5/Django
- Replace JS form handling with Django forms
- Use HTML5 validation attributes
- Move state management to Django session/context

### B. Replace with HTMX
- Convert chart filtering to `hx-trigger` attributes
- Replace `fetch()` calls with `hx-get`
- Add proper HTMX triggers and swap targets

### C. Alternative Libraries
- Consider Alpine.js for state management
- Use HTML dialog element
- Move chat logic to Django where possible

## 3. Required JavaScript Review

### Must Keep
- Chart.js initialization and config
- Complex chart interactions
- Data transformation logic

### Can Remove/Replace
- Debug logging (move to Django)
- Basic form handling
- Simple state management

## 4. Implementation Plan

### Phase 1: Django Migration
1. Move form handling to Django
2. Implement session-based state
3. Use Django messages framework

### Phase 2: HTMX Integration
1. Replace AJAX calls with HTMX
2. Add proper HTMX triggers
3. Implement swap targets

### Phase 3: JavaScript Optimization
1. Lazy load Chart.js
2. Remove redundant functions
3. Optimize chart handling

### Phase 4: Web API Enhancement
1. Use native browser APIs
2. Add progressive enhancement
3. Implement fallbacks

## 5. Final JavaScript Structure

```javascript
// app.js
const chartManager = {
    instances: new Map(),
    
    init(ctx, config) {
        // Chart initialization
    },
    
    cleanup(chartId) {
        // Chart cleanup logic
    }
};

// Essential chart interactions
document.addEventListener('htmx:afterSettle', () => {
    // Chart initialization after HTMX updates
});
```