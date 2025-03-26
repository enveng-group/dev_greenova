from typing import List, Tuple

# Status choices for Obligation model
STATUS_NOT_STARTED = 'not started'
STATUS_IN_PROGRESS = 'in progress'
STATUS_COMPLETED = 'completed'
STATUS_OVERDUE = 'overdue'
STATUS_UPCOMING = 'upcoming'

STATUS_CHOICES: List[Tuple[str, str]] = [
    (STATUS_NOT_STARTED, 'Not Started'),
    (STATUS_IN_PROGRESS, 'In Progress'),
    (STATUS_COMPLETED, 'Completed')
]

# Due date periods for filtering
DUE_PERIOD_OVERDUE = 'overdue'
DUE_PERIOD_THIS_WEEK = 'this_week'
DUE_PERIOD_NEXT_WEEK = 'next_week'
DUE_PERIOD_THIS_MONTH = 'this_month'
DUE_PERIOD_NEXT_MONTH = 'next_month'

# Recurring frequency constants
FREQUENCY_DAILY = 'daily'
FREQUENCY_WEEKLY = 'weekly'
FREQUENCY_FORTNIGHTLY = 'fortnightly'
FREQUENCY_MONTHLY = 'monthly'
FREQUENCY_QUARTERLY = 'quarterly'
FREQUENCY_BIANNUAL = 'biannual'
FREQUENCY_ANNUAL = 'annual'

# Alternative terms that should be normalized
FREQUENCY_SEMI_ANNUAL = 'semi-annual'   # should be treated as biannual
FREQUENCY_BI_ANNUALLY = 'bi-annually'   # should be treated as biannual
FREQUENCY_YEARLY = 'yearly'             # should be treated as annual
FREQUENCY_ANNUALLY = 'annually'         # should be treated as annual

# Display names for frequencies (for UI)
FREQUENCY_DISPLAY_NAMES = {
    FREQUENCY_DAILY: 'Daily',
    FREQUENCY_WEEKLY: 'Weekly',
    FREQUENCY_FORTNIGHTLY: 'Fortnightly',
    FREQUENCY_MONTHLY: 'Monthly',
    FREQUENCY_QUARTERLY: 'Quarterly',
    FREQUENCY_BIANNUAL: 'Bi-annual (Twice a year)',
    FREQUENCY_ANNUAL: 'Annual (Once a year)'
}

# Choices for forms and models
FREQUENCY_CHOICES: List[Tuple[str, str]] = [
    (FREQUENCY_DAILY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_DAILY]),
    (FREQUENCY_WEEKLY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_WEEKLY]),
    (FREQUENCY_FORTNIGHTLY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_FORTNIGHTLY]),
    (FREQUENCY_MONTHLY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_MONTHLY]),
    (FREQUENCY_QUARTERLY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_QUARTERLY]),
    (FREQUENCY_BIANNUAL, FREQUENCY_DISPLAY_NAMES[FREQUENCY_BIANNUAL]),
    (FREQUENCY_ANNUAL, FREQUENCY_DISPLAY_NAMES[FREQUENCY_ANNUAL])
]

# Mapping of alternative terms to canonical constants
FREQUENCY_ALIASES = {
    FREQUENCY_SEMI_ANNUAL: FREQUENCY_BIANNUAL,
    FREQUENCY_BI_ANNUALLY: FREQUENCY_BIANNUAL,
    FREQUENCY_YEARLY: FREQUENCY_ANNUAL,
    FREQUENCY_ANNUALLY: FREQUENCY_ANNUAL,
}

# Frequency duration in days (approximate)
FREQUENCY_DAYS = {
    FREQUENCY_DAILY: 1,
    FREQUENCY_WEEKLY: 7,
    FREQUENCY_FORTNIGHTLY: 14,
    FREQUENCY_MONTHLY: 30,  # Approximate
    FREQUENCY_QUARTERLY: 90,  # Approximate
    FREQUENCY_BIANNUAL: 182,  # Approximate
    FREQUENCY_ANNUAL: 365,  # Approximate
}

RESPONSIBILITY_ROLES = [
    ('Project Manager', 'Project Manager'),
    ('Environmental Officer', 'Environmental Officer'),
    ('Site Supervisor', 'Site Supervisor'),
    ('Compliance Manager', 'Compliance Manager'),
    ('Health and Safety Officer', 'Health and Safety Officer'),
    ('Quality Assurance Officer', 'Quality Assurance Officer'),
    ('Operations Manager', 'Operations Manager'),
    ('Maintenance Supervisor', 'Maintenance Supervisor'),
    ('Other', 'Other')
]
