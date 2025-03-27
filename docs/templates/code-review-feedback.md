# Code Review Feedback for PR: Technical Documentation Updates

Hi @Channing88,

Thank you for your continued interest in contributing to the Greenova project.
I appreciate your attempt to address the feedback from the previous code review
by submitting updated files.

## Summary of Changes

After reviewing your updated PR, I notice that you've primarily renamed the
files rather than addressing the content issues highlighted in the previous
review:

- Renamed files to `MAKEFILE.md` and `SETUP_PY.md`
- Made minimal changes to the content structure
- Did not significantly improve the technical content quality

## Comparison Between Submissions and Project Standards

To help you understand the expected documentation standards for our project,
I've taken the initiative to rewrite these documents myself. I'm merging these
improved versions into the project to keep our documentation progress moving
forward. Let me highlight some differences that will help you with future
contributions:

### Documentation Structure & Organization

**Your submission:**

- Used inconsistent heading levels
- Lacked clear section organization
- Mixed technical aspects with personal reflections without clear separation

**Project standard:**

- Uses consistent heading hierarchy (H1 > H2 > H3)
- Organizes content in a logical flow from overview to specific details
- Separates reference information from implementation guidance

### Technical Content Depth

**Your submission:**

- `SETUP_PY.md` listed fields with minimal explanation ("Key Fields" section)
- `MAKEFILE.md` provided general statements without technical specifications
- Missing concrete examples of implementation

**Project standard:**

- Provides comprehensive explanations of concepts
- Includes practical code examples with syntax highlighting
- Explains the "why" behind technical decisions
- Uses tables to organize parameter information for better readability

### Formatting & Professional Writing

**Your submission:**

- Contained several spelling and grammar issues ("libralies", "whrite",
  "peroform")
- Inconsistent punctuation and capitalization
- Links provided without context or proper citation

**Project standard:**

- Uses proper technical terminology
- Follows consistent formatting throughout
- Includes properly formatted IEEE-style citations
- Structures content with appropriate Markdown formatting elements

### Concrete Examples

**Your SETUP_PY.md:**

```
# Key Fields

- **name** : The name of the pakage.
- **Version** : The current version.
```

**Project standard:**

```
| Parameter                | Description                                   | Example                                |
| ------------------------ | --------------------------------------------- | -------------------------------------- |
| `name`                   | Package name as it will appear on PyPI        | `"greenova"`                           |
| `version`                | Package version following semantic versioning | `"0.1.0"`                              |
```

## Learning Resources

To help you improve future contributions, I recommend:

1. **Review our documentation standards** in
   `.github/prompts/technical-writing.prompt.md`
2. **Study the merged documents** at:
   - `/workspaces/greenova/docs/resources/makefile.md`
   - `/workspaces/greenova/docs/resources/py/setuptools/setup-py.md`
3. **Follow the IEEE citation style** for technical references
4. **Use a grammar checking tool** like Grammarly or LanguageTool to catch
   basic errors

## Moving Forward

I appreciate your willingness to contribute and hope this feedback helps you
understand our project's documentation standards. Technical documentation is
critical for project sustainability, which is why we maintain high standards.

Please feel free to:

- Ask questions about specific aspects of the documentation you find
  challenging
- Submit smaller, focused PRs that target specific documentation sections
- Request a documentation mentor if you'd like more guidance

Thank you again for your efforts. I look forward to your future contributions
to the Greenova project.