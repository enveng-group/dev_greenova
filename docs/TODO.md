# TODO

## Session Handling
- Fix session handling to remember session token and return to the previous state.

## UI Improvements
- Add a home button in the obligation view.

## Data Review
- Review import values for the keys in the obligation register. Investigate why many items are marked as in-progress but nothing is being returned.

## Security
- Investigate the insecure notification for Clough Fortinet.
- Github CodeQL integration
- Github repository rulesets
    - https://github.com/github/ruleset-recipes

## Authorization
- Use groups in authentication as the responsibility values in the obligation register. Map these groups to user profiles.

## Compliance Graphs
- Create three compliance graphs for:
    - PCEMP
    - WA6946
    - MS1180
- Each graph should have its own chart.
- Note: The project name is "SCJV - Pilbara Ports", but the environmental aspects are the primary concern.

## Obligations View
- Map environmental aspects to the obligations view.
- accountability is the username when it is mapped with the relationship "responsibility"
- Ensure that the mapping process is documented for clarity.

## Branding
- Update the application to include the trademarked EnvEng logo.

## Containerization
- Create a Docker container for release.
- Set up a devcontainer for development.

## Version Control
- Set up a local GitLab repository.
- Set up configutation/dotfiles repository

## Development Environment
- Ensure compatibility with FreeBSD on a local laptop.

## Performance Optimization
- Eliminate render-blocking resources:
    - Inline critical CSS/JS
    - Defer non-critical resources
    - Optimize CDN resources loading
- Improve server response time:
    - Target < 660ms for initial response
    - Optimize database queries
- Implement efficient cache policies:
    - Set appropriate cache TTL for static assets
    - Configure browser caching headers
- Reduce JavaScript payload:
    - Minimize unused JavaScript
    - Optimize hyperscript.org dependency
    - Implement code splitting

## Documentation
- markdownlint2
    - https://github.com/github/markdownlint-github?tab=readme-ov-file

## Automation
- helper shell scripts
    - https://github.com/github/training-utils/tree/master
    - https://github.com/github/scripts-to-rule-them-all
- Use other shell script setup.py with setuptools, cmake or makefile or ninja or something else? 
- create .dotfiles repository

is there any opportunity to modularialise/break-down dashboard.html? if so, please provide new file names and paths?

do we need to add anything to settings.py urls.py admin.py apps.py models.py tests.py .env forms.py or views.py or init.py and styles.css and main.js now that we have setup all templates for login/registration
