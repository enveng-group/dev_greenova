# Greenova Technical Documentation Guidelines

When generating technical documentation for the Greenova project, follow these
guidelines.

## Documentation Types and Standards

### GitHub Markdown (.md)

- Use GitHub Flavored Markdown for general documentation
- Structure documents with clear heading hierarchy (H1 > H2 > H3)
- Use fenced code blocks with language identifiers (```python)
- Properly format tables using pipe syntax for better readability
- Use emphasis (bold/italic) sparingly and consistently

### Python Documentation (.py and .rst)

- Follow PEP 257 for docstrings in Python code
- Use NumPy style docstring format for consistency
- For .rst files, follow strict reStructuredText syntax
- Include type hints in documentation using PEP 484 conventions
- Document parameters, return values, exceptions, and examples

## Document Structure

### README Files

- Include clear project title and concise description
- Provide installation instructions with code examples
- List dependencies with version requirements
- Include basic usage examples
- Add contributing guidelines and license information

### API Documentation

- Document each endpoint with HTTP method, URL, parameters, and response format
- Include authentication requirements
- Provide request and response examples
- Document error codes and messages

### User Guides

- Start with an introduction and purpose
- Include step-by-step instructions with screenshots
- Use numbered lists for sequential procedures
- Use bullet points for options or features
- Include troubleshooting section for common issues

## IEEE Referencing Style

### In-text Citations

- Use sequential numbering system in square brackets \[1\]
- For multiple references, use comma separation \[1\], \[2\], \[3\] or ranges \[1\]-\[3\]
- Place citation number before punctuation
- Example: "Django provides robust security features \[4\]."

### Reference List

- Format book references as: \[n\] A. Author, B. Author, "Title of Book,"
  Edition. City, State/Country: Publisher, Year, pp. pages.

- Format article references as: \[n\] A. Author, B. Author, "Title of Article,"
  Title of Journal, vol. #, no. #, pp. pages, Month Year, DOI.

- Format website references as: \[n\] A. Author, "Title of Page," Website Name,
  Date Published. \[Online\]. Available: URL \[Accessed: Date\].

- Format technical report references as: \[n\] A. Author, "Title of Report,"
  Organization, City, State/Country, Report No., Month Year.

### Example Reference List

```
## References

[1] Django Software Foundation, "Django Documentation," Django Project, 2023. [Online]. Available: https://docs.djangoproject.com/ [Accessed: Oct. 15, 2023].

[2] A. Holovaty and J. Kaplan-Moss, "The Definitive Guide to Django: Web Development Done Right," 2nd ed. Berkeley, CA: Apress, 2009.

[3] M. Smith and P. Johnson, "Environmental Compliance Tracking Systems: A Review," Journal of Environmental Management, vol. 45, no. 2, pp. 112-125, Apr. 2022, doi:10.1234/jem.2022.045.
```

## Formatting and Style

### General Rules

- Use sentence case for headings
- Keep paragraphs concise (3-5 sentences)
- Use active voice rather than passive
- Define acronyms at first use
- Include alt text for all images
- Maintain consistent terminology throughout

### Code Examples

- Always specify the language for syntax highlighting
- Provide context before code blocks
- Keep examples minimal but complete
- Add comments to explain complex parts
- Use proper indentation and formatting

### Diagrams and Visuals

- Use SVG format when possible for diagrams
- Include captions for all figures
- Reference all figures in text
- Use consistent visual style across diagrams
- Add descriptive alt text for accessibility

## Accessibility

- Ensure proper heading hierarchy (H1 > H2 > H3)
- Add alt text to all images
- Use descriptive link text
- Provide text alternatives for multimedia content
- Use sufficient color contrast

## Quality Checks

- Run spelling and grammar check
- Validate all links
- Verify code examples actually work
- Check rendering in GitHub interface
- Review for technical accuracy

## File Organization

- Group related documentation files together
- Use consistent naming conventions (kebab-case)
- Keep documentation close to relevant code
- Maintain a centralized index for all documentation
- Use relative links between documentation files
