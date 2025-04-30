#!/usr/bin/fish

# GitHub issue creation script for Greenova
# This script automates the creation of standardized issues

# --- Configuration ---
set repo_owner enveng-group
set repo_name dev_greenova
set repo_url "https://github.com/$repo_owner/$repo_name"

# --- Issue Details ---
set issue_title "task: Coordinate project logo design process"

# --- Issue Body ---
# Create a temporary file for the issue body
set body_file (mktemp)

# Write the issue body
echo "## Description

Manage the process for designing a project logo based on user interest. Collect submissions and facilitate voting/selection as per the note in \`notes.txt\`.

### Current Status

No official logo exists for the project. This affects:
- Repository presence
- Documentation appearance
- Overall project branding
- User recognition and trust

### Process Workflow

\`\`\`mermaid
flowchart TD
    A[Start Logo Design Process] --> B[Create Design Brief]
    B --> C[Open Call for Submissions]
    C --> D[Collect Logo Submissions]
    D --> E{Enough Submissions?}
    E -->|No| C
    E -->|Yes| F[Initial Screening]
    F --> G[Community Voting Round]
    G --> H{Clear Winner?}
    H -->|No| I[Final Committee Review]
    H -->|Yes| J[Winner Selection]
    I --> J
    J --> K[Prepare Logo Package]
    K --> L[Implement Logo]
    L --> M[Update Project Assets]
    M --> N[End Process]

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style J fill:#9f9,stroke:#333,stroke-width:2px
    style N fill:#999,stroke:#333,stroke-width:2px
\`\`\`

### Logo Requirements ERD

\`\`\`mermaid
erDiagram
    LogoSubmission ||--o{ FileVersion : contains
    LogoSubmission {
        int id PK
        string designer_name
        string design_concept
        datetime submitted_at
        string status
        boolean meets_requirements
        int vote_count
    }
    FileVersion {
        int id PK
        int submission_id FK
        string file_path
        string file_format
        string color_space
        int dimensions
        datetime uploaded_at
    }
    LogoRequirements ||--o{ LogoSubmission : validates
    LogoRequirements {
        string size_specs
        string color_specs
        string format_specs
        string usage_guidelines
        boolean allow_variations
    }
    CommunityVote ||--o{ LogoSubmission : rates
    CommunityVote {
        int id PK
        int submission_id FK
        int user_id FK
        int rating
        string feedback
        datetime voted_at
    }
\`\`\`

### Implementation Plan

\`\`\`pseudocode
FUNCTION CoordinateLogoDesign()
    // Phase 1: Setup
    CREATE design_brief
        INCLUDE project_description
        INCLUDE design_requirements
        INCLUDE submission_guidelines
        INCLUDE timeline

    SETUP submission_system
        CONFIGURE file_upload
        DEFINE acceptance_criteria
        CREATE submission_form

    // Phase 2: Collection
    OPEN_SUBMISSIONS:
        WHILE submission_period_active DO
            COLLECT new_submission
            VALIDATE submission_requirements
            IF valid THEN
                STORE submission
                NOTIFY confirmation
            ELSE
                REQUEST revision
            ENDIF
        END WHILE

    // Phase 3: Voting
    SETUP voting_system
        DEFINE voting_criteria
        SET voting_period
        CONFIGURE vote_tracking

    CONDUCT_VOTING:
        FOR EACH submission IN valid_submissions
            DISPLAY submission
            COLLECT_VOTES until voting_period_ends
            CALCULATE vote_metrics
        END FOR

    // Phase 4: Selection
    SELECT_WINNER:
        SORT submissions BY vote_count DESC
        IF clear_winner THEN
            ANNOUNCE winner
        ELSE
            CONDUCT committee_review
            SELECT final_winner
        ENDIF

    // Phase 5: Implementation
    IMPLEMENT_LOGO:
        PREPARE logo_package
        UPDATE project_assets
        DOCUMENT usage_guidelines
        NOTIFY community

    ARCHIVE_PROCESS:
        STORE all_submissions
        DOCUMENT decision_process
        SAVE voting_results
END FUNCTION

FUNCTION ValidateSubmission(submission)
    CHECK file_formats
    VERIFY dimensions
    VALIDATE color_spaces
    ENSURE meets_guidelines
    RETURN is_valid
END FUNCTION

FUNCTION PrepareLogoPackage(winning_submission)
    GENERATE:
        - SVG vector version
        - PNG versions (multiple sizes)
        - Favicon version
        - Social media versions
        - Dark/light variations

    CREATE style_guide:
        - Color codes
        - Minimum sizes
        - Spacing requirements
        - Usage examples

    PACKAGE_FILES:
        ZIP all_versions
        INCLUDE usage_documentation
END FUNCTION
\`\`\`

### Key Requirements

1. Design Brief:
   - Must reflect environmental focus
   - Clean, modern aesthetic
   - Scalable for various uses
   - Appropriate for professional context

2. Technical Specifications:
   - Vector format (SVG)
   - Multiple size variants
   - Color and monochrome versions
   - Web and print compatible

3. Submission Requirements:
   - Original work only
   - Full rights transfer
   - Source files included
   - Design rationale documented

4. Selection Process:
   - Community voting (60% weight)
   - Technical review (20% weight)
   - Committee decision (20% weight)

### Affected Areas

1. Repository Assets:
   - README.md header
   - Documentation headers
   - Social preview image

2. Web Presence:
   - Favicon
   - Header graphics
   - Footer elements

3. Documentation:
   - PDF templates
   - Presentation templates
   - Email signatures

### Acceptance Criteria

- [ ] Design brief created and approved
- [ ] Submission system configured
- [ ] Collection process documented
- [ ] Voting system implemented
- [ ] Selection criteria defined
- [ ] Logo package specifications documented
- [ ] Implementation plan prepared
- [ ] Usage guidelines drafted

### Project Fields
- Status: Standardize
- Priority: P4
- Size: S
- Effort: 2" >$body_file

# --- Labels ---
set labels "task,design,planning,priority-low,help wanted,good first issue"

# --- Function to create labels if they don't exist ---
function ensure_label
    set label_name $argv[1]
    set color $argv[2]
    set description $argv[3]

    # Check if label exists
    if not gh label list --repo "$repo_owner/$repo_name" --json name | grep -q "\"name\": \"$label_name\""
        echo "Creating label: $label_name"
        gh label create "$label_name" --color "$color" --description "$description" --repo "$repo_owner/$repo_name" || true
    end
end

# Create labels if they don't exist
ensure_label task 0e8a16 "Task to be completed"
ensure_label design d4c5f9 "Design-related changes"
ensure_label planning 84b6eb "Planning and organization"
ensure_label priority-low c5def5 "Low priority issues"
ensure_label "help wanted" 008672 "Extra attention is needed"
ensure_label "good first issue" 7057ff "Good for newcomers"

# Create initial issue first without labels
echo "Creating issue without labels"
set issue_create_output (gh issue create \
    --repo "$repo_owner/$repo_name" \
    --title "$issue_title" \
    --body-file "$body_file")

# Extract issue URL and number
set issue_url (echo $issue_create_output | grep -Eo 'https://github.com/[^[:space:]]+' || echo '')
set issue_number (echo $issue_url | grep -Eo '/[0-9]+$' | tr -d '/' || echo '')

if test -z "$issue_url"
    echo "Error: Failed to create issue or capture URL" >&2
    exit 1
end

if test -z "$issue_number"
    echo "Error: Failed to extract issue number from URL: $issue_url" >&2
    exit 1
end

echo "Issue created successfully: $issue_url"
echo "Issue number: $issue_number"

# Clean up the temporary file
rm -f "$body_file"

# Add labels one by one
echo "Adding labels to issue #$issue_number"
for label in (string split "," $labels)
    gh issue edit "$issue_number" --repo "$repo_owner/$repo_name" --add-label "$label" || echo "Failed to add $label label"
end

# Add the issue to the project and get the item ID
set item_id (gh project item-add 8 --owner "$repo_owner" --url "$issue_url" --format json | jq -r '.id')

# Check if we got the item ID
if test -z "$item_id"; or test "$item_id" = null
    echo "Error: Failed to add issue to project or retrieve item ID." >&2
    set item_id (gh project item-list 8 --owner "$repo_owner" --format json | jq -r --arg url "$issue_url" '.items[] | select(.content.url == $url) | .id' | head -n 1)
    if test -z "$item_id"; or test "$item_id" = null
        echo "Error: Could not find item ID for issue $issue_url in project 8." >&2
        exit 1
    else
        echo "Found existing item ID: $item_id"
    end
end

echo "Issue added to project with Item ID: $item_id"

# Fetch Project ID
set project_id (gh project list --owner "$repo_owner" --format json | jq -r '.projects[] | select(.number == 8) | .id')
if test -z "$project_id"; or test "$project_id" = null
    echo "Error: Could not find Project ID for project number 8." >&2
    exit 1
end

echo "Found Project ID: $project_id"

# Set the custom fields
set -l status_field_id PVTSSF_lAHOCchfJ84A3c00zgslf0U
set -l priority_field_id PVTSSF_lAHOCchfJ84A3c00zgslf9E
set -l size_field_id PVTSSF_lAHOCchfJ84A3c00zgslf9I
set -l effort_field_id PVTF_lAHOCchfJ84A3c00zgslf9M

gh project item-edit --id "$item_id" --project-id "$project_id" \
    --field-id "$status_field_id" --single-select-option-id 47fc9ee4 # Standardize

gh project item-edit --id "$item_id" --project-id "$project_id" \
    --field-id "$priority_field_id" --single-select-option-id 98236657 # P4

gh project item-edit --id "$item_id" --project-id "$project_id" \
    --field-id "$size_field_id" --single-select-option-id d3982a83 # S

gh project item-edit --id "$item_id" --project-id "$project_id" \
    --field-id "$effort_field_id" --number 2

echo "Script finished."
