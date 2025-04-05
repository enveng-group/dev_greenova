# Greenova Bug Report Generation Guidelines

This prompt helps you generate comprehensive bug reports for the Greenova
environmental management application. Follow this structured approach to ensure
all necessary information is included.

## Bug Report Structure

### Title and Summary

- Create a concise title following the format: `bug: [brief description]`
- Write a clear 1-2 sentence summary explaining the core issue

### Environment Details

- Django Version: 4.1.13
- Python Version: 3.9.21
- Frontend Technologies: PicoCSS, django-hyperscript, django-htmx
- Browser and version (if applicable)
- Device type and operating system

### Reproduction Steps

1. Start with initial state/prerequisites
2. Provide numbered, specific steps to reproduce
3. Include exact inputs, clicks, and actions
4. Describe expected behavior
5. Describe actual behavior
6. Include error messages and traceback if available

### Technical Context

Specify which component of the Greenova system is affected:

- Django model/view affected
- URL path where issue occurs
- Template type and file involved (Jinja2 .jinja file or DTL .html file)
- Template rendering issues (Jinja2 or DTL specific)
- Database interaction issues
- Form handling problems
- Authentication/permission issues

### Impact Assessment

- Severity (Critical/High/Medium/Low)
- User impact description
- Functionality affected
- Data integrity concerns
- Accessibility implications (WCAG 2.1 AA standards)

### Debugging Information

- Console logs (if relevant)
- Django debug output
- Database query issues
- Network request problems
- How to access the traceback information:
  1. When the error occurs, examine Django's error page
  2. Look for the "Traceback" section
  3. Switch to copy-and-paste view
  4. Copy the entire trace report

### Screenshots and Visual Evidence

- Instructions for attaching relevant screenshots
- Annotate screenshots to highlight the issue
- Include before/after images if applicable

### Potential Solutions

- Initial analysis of possible cause
- Suggested investigation approach
- Reference to similar issues if known
- Code areas that likely need inspection

## Example Bug Report
