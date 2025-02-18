Here is a  schema for the table in the worksheet labeled OR(2):

1. **Columns**:
   - **Project_Name**: Unique identifier for each project.
   - **Primary_Environmental_Mechanism**: Refers to the primary environmental mechanism.
   - **Procedure**: Describes the procedure.
   - **Environmental_Aspect**: Indicates the environmental aspect.
   - **Obligation_Number**: Represents the obligation number.
   - **Obligation**: Describes the obligation.
   - **Accountability**: Indicates who is accountable.
   - **Responsibility**: Indicates who is responsible.
   - **ProjectPhase**: Specifies the project phase.
   - **Action_DueDate**: Specifies the due date.
   - **Close_Out_Date**: Indicates the close-out date.
   - **Status**: Indicates the current status (e.g., Overdue, Completed, In Progress, Not Started).
   - **Supporting_Information**: Provides supporting information.
   - **General_Comments**: General comments about the obligation.
   - **Compliance_Comments**: Comments related to compliance.
   - **NonConformance_Comments**: Comments related to non-conformance.
   - **Evidence**: Provides evidence.
   - **PersonEmail**: Email of the person responsible.
   - **Recurring_Obligation**: Indicates if the obligation is recurring.
   - **Recurring_Frequency**: Specifies the frequency of the recurring obligation.
   - **Recurring_Status**: Indicates the status of the recurring obligation.
   - **Recurring_Forcasted_Date**: Specifies the forecasted date for the recurring obligation.
   - **Inspection**: Indicates if the obligation is tracked using inspections.
   - **Inspection_Frequency**: Specifies the frequency of inspections.
   - **Site_or_Desktop**: Indicates if the inspection is site-based or desktop-based.
   - **New_Control_Action_Required**: Indicates if a new control or action is required.
   - **Obligation_Type**: Specifies the type of obligation.
   - **Gap_Analysis**: Provides notes for gap analysis.
   - **Notes_for_Gap_Analysis**: Additional notes for gap analysis.

2. **Relationships**:
To establish the relationships in the new table, you can follow these steps:

   - **Identify Primary Keys**: Ensure that each row in your table has a unique identifier. The `Obligation_Number` serves as the primary key.

   - **Define Foreign Keys**: Determine which columns will act as foreign keys to link to other tables. For example, `Accountability` and `Responsibility` could link to tables containing details about accountable and responsible parties.

   - **Create Relationships**:
     - **One-to-Many Relationship**: If one obligation can have multiple related records in another table (e.g., multiple actions or updates), you can establish a one-to-many relationship. Use the primary key from the obligations table as a foreign key in the related table.
     - **Many-to-Many Relationship**: If multiple obligations can be related to multiple entities (e.g., multiple obligations linked to multiple projects), you might need a junction table. This table will have foreign keys from both related tables to establish the many-to-many relationship.

   - **Ensure Data Integrity**: Use constraints to maintain data integrity. For example, ensure that foreign keys always reference valid primary keys in the related tables.

   - **Implement Referential Integrity**: Use database management system (DBMS) features to enforce referential integrity. This ensures that relationships between tables remain consistent.

3. **Components**:
   - The table includes various plans and approvals such as Construction Environmental Management Plan, Cultural Heritage Management Plan, Flora Management Plan, Fauna Management Plan, etc.
   - It also references several acts and regulations like the Biodiversity Conservation Act 2016, Rights in Water and Irrigation Act 1914, and others.
   - The status column tracks the progress of each obligation.

4. **Columns**:

The purpose of each column in the table:

   - **Project_Name**: This is a unique identifier for each project. It ensures that each project can be distinctly identified.
   - **Primary_Environmental_Mechanism**: Refers to the primary environmental mechanism associated with the project. It provides context on the environmental procedures related to the project.
   - **Procedure**: Describes the procedure. This column provides details about what the procedure entails.
   - **Environmental_Aspect**: Indicates the environmental aspect. It specifies the aspect of the environment that the procedure or obligation relates to.
   - **Obligation_Number**: Represents the obligation number. It is a descriptive identifier that helps in easily referencing the obligation.
   - **Obligation**: Describes the obligation. This column provides details about what the obligation entails.
   - **Accountability**: Indicates who is accountable for the obligation. It specifies the entity or individual responsible for ensuring that the obligation is met.
   - **Responsibility**: Indicates who is responsible for the obligation. This column specifies the entity or individual tasked with carrying out the obligation.
   - **ProjectPhase**: Specifies the project phase. It indicates the phase of the project that the obligation relates to.
   - **Action_DueDate**: Specifies the due date for the obligation. It helps in tracking deadlines and ensuring timely completion of obligations.
   - **Close_Out_Date**: Indicates the close-out date for the obligation. It helps in tracking when the obligation was completed.
   - **Status**: Indicates the current status of the obligation (e.g., Overdue, Completed, In Progress, Not Started). This column helps in monitoring the progress of each obligation.
   - **Supporting_Information**: Provides supporting information. This column includes additional information that supports the obligation.
   - **General_Comments**: General comments about the obligation. This column includes any general comments or notes about the obligation.
   - **Compliance_Comments**: Comments related to compliance. This column includes any comments or notes related to compliance with relevant laws, regulations, or standards.
   - **NonConformance_Comments**: Comments related to non-conformance. This column includes any comments or notes related to non-conformance with relevant laws, regulations, or standards.
   - **Evidence**: Provides evidence. This column includes any evidence that supports the obligation.
   - **PersonEmail**: Email of the person responsible. This column includes the email address of the person responsible for the obligation.
   - **Recurring_Obligation**: Indicates if the obligation is recurring. This column specifies if the obligation is a recurring obligation.
   - **Recurring_Frequency**: Specifies the frequency of the recurring obligation. This column indicates how often the obligation recurs.
   - **Recurring_Status**: Indicates the status of the recurring obligation. This column specifies the current status of the recurring obligation.
   - **Recurring_Forcasted_Date**: Specifies the forecasted date for the recurring obligation. This column indicates the forecasted date for the next occurrence of the recurring obligation.
   - **Inspection**: Indicates if the obligation is tracked using inspections. This column specifies if the obligation is tracked using inspections.
   - **Inspection_Frequency**: Specifies the frequency of inspections. This column indicates how often inspections are conducted.
   - **Site_or_Desktop**: Indicates if the inspection is site-based or desktop-based. This column specifies if the inspection is conducted on-site or as a desktop review.
   - **New_Control_Action_Required**: Indicates if a new control or action is required. This column specifies if a new control or action is required for the obligation.
   - **Obligation_Type**: Specifies the type of obligation. This column indicates the type of obligation.
   - **Gap_Analysis**: Provides notes for gap analysis. This column includes any notes or comments related to gap analysis.
   - **Notes_for_Gap_Analysis**: Additional notes for gap analysis. This column includes any additional notes or comments related to gap analysis.

-- Create the obligations table
CREATE TABLE Obligations (
    obligation__number INT PRIMARY KEY,
    project__name VARCHAR(255),
    primary__environmental__mechanism TEXT,
    procedure TEXT,
    environmental__aspect TEXT,
    obligation TEXT,
    accountability INT,
    responsibility INT,
    project_phase TEXT,
    action__due_date DATE,
    close__out__date DATE,
    status VARCHAR(50),
    supporting__information TEXT,
    general__comments TEXT,
    compliance__comments TEXT,
    non_conformance__comments TEXT,
    evidence TEXT,
    person_email TEXT,
    recurring__obligation BOOLEAN,
    recurring__frequency VARCHAR(50),
    recurring__status VARCHAR(50),
    recurring__forcasted__date DATE,
    inspection BOOLEAN,
    inspection__frequency VARCHAR(50),
    site_or__desktop VARCHAR(50),
    new__control__action_required BOOLEAN,
    obligation_type VARCHAR(50),
    gap__analysis TEXT,
    notes_for__gap__analysis TEXT,
    covered_in_which_inspection_checklist TEXT
);

-- Create the accountability table
CREATE TABLE Accountability (
    accountability_id INT PRIMARY KEY,
    accountability_name VARCHAR(255)
);

-- Create the responsibility table
CREATE TABLE Responsibility (
    responsibility_id INT PRIMARY KEY,
    responsibility_name VARCHAR(255)
);

-- Establish foreign key relationships
ALTER TABLE Obligations
ADD CONSTRAINT FK_Accountability
FOREIGN KEY (accountability) REFERENCES Accountability(accountability_id);

ALTER TABLE Obligations
ADD CONSTRAINT FK_Responsibility
FOREIGN KEY (responsibility) REFERENCES Responsibility(responsibility_id);

);

-- Create the accountability table
CREATE TABLE Accountability (
    accountability_id INT PRIMARY KEY,
    accountability_name VARCHAR(255)
);

-- Create the responsibility table
CREATE TABLE Responsibility (
    responsibility_id INT PRIMARY KEY,
    responsibility_name VARCHAR(255)
);

-- Establish foreign key relationships
ALTER TABLE Obligations
ADD CONSTRAINT FK_Accountability
FOREIGN KEY (Accountability) REFERENCES Accountability(accountability_id);

ALTER TABLE Obligations
ADD CONSTRAINT FK_Responsibility
FOREIGN KEY (Responsibility) REFERENCES Responsibility(responsibility_id);
```

6. **One-to-many Relationships**:

To create a one-to-many relationship in SQLite, you need to define a foreign key in the child table that references the primary key in the parent table. Here's a step-by-step guide on how to do this:

   - **Create the Parent Table**: This table will contain the primary key that will be referenced by the child table. For example, let's create a table called `Accountability` with a primary key `accountability_id`.

```sql
CREATE TABLE Accountability (
    accountability_id INTEGER PRIMARY KEY,
    accountability_name TEXT
);
```

   - **Create the Child Table**: This table will contain a foreign key that references the primary key in the parent table. For example, let's create a table called `Obligations` with a foreign key `Accountability` that references `accountability_id` in the `Accountability` table.

```sql
CREATE TABLE Obligations (
    Obligation_Number INTEGER PRIMARY KEY,
    Project_Name VARCHAR(255),
    Primary_Environmental_Mechanism TEXT,
    Procedure TEXT,
    Environmental_Aspect TEXT,
    Obligation TEXT,
    Accountability INTEGER,
    Responsibility INTEGER,
    ProjectPhase TEXT,
    Action_DueDate TEXT,
    Close_Out_Date TEXT,
    Status TEXT,
    Supporting_Information TEXT,
    General_Comments TEXT,
    Compliance_Comments TEXT,
    NonConformance_Comments TEXT,
    Evidence TEXT,
    PersonEmail TEXT,
    Recurring_Obligation BOOLEAN,
    Recurring_Frequency TEXT,
    Recurring_Status TEXT,
    Recurring_Forcasted_Date TEXT,
    Inspection BOOLEAN,
    Inspection_Frequency TEXT,
    Site_or_Desktop TEXT,
    New_Control_Action_Required BOOLEAN,
    Obligation_Type TEXT,
    Gap_Analysis TEXT,
    Notes_for_Gap_Analysis TEXT,
    FOREIGN KEY (Accountability) REFERENCES Accountability(accountability_id)
);
```

   - **Enable Foreign Key Support**: SQLite requires foreign key support to be explicitly enabled. You can do this by executing the following command:

```sql
PRAGMA foreign_keys = ON;
```

   - **Insert Data**: Now you can insert data into the tables, ensuring that the foreign key in the child table references a valid primary key in the parent table.

```sql
-- Insert data into the Accountability table
INSERT INTO Accountability (accountability_id, accountability_name) VALUES (1, 'John Doe');

-- Insert data into the Obligations table
INSERT INTO Obligations (Obligation_Number, Project_Name, Primary_Environmental_Mechanism, Procedure, Environmental_Aspect, Obligation, Accountability, Responsibility, ProjectPhase, Action_DueDate, Close_Out_Date, Status, Supporting_Information, General_Comments, Compliance_Comments, NonConformance_Comments, Evidence, PersonEmail, Recurring_Obligation, Recurring_Frequency, Recurring_Status, Recurring_Forcasted_Date, Inspection, Inspection_Frequency, Site_or_Desktop, New_Control_Action_Required, Obligation_Type, Gap_Analysis, Notes_for_Gap_Analysis)
VALUES (1, 'Project 1', 'Mechanism 1', 'Procedure 1', 'Aspect 1', 'Obligation 1', 1, 2, 'Phase 1', '2025-01-18', '2025-01-19', 'In Progress', 'Supporting Info', 'General Comments', 'Compliance Comments', 'NonConformance Comments', 'Evidence', 'email@example.com', 1, 'Monthly', 'In Progress', '2025-02-18', 1, 'Monthly', 'Site', 1, 'Type 1', 'Gap Analysis', 'Notes for Gap Analysis');
```

By following these steps, you can create a one-to-many relationship in SQLite, ensuring that each record in the child table (`Obligations`) references a valid record in the parent table (`Accountability`). This helps maintain data integrity and ensures that the relationships between tables remain consistent.

7. **Many-to-many junction table schemas**:

To create schemas for all possible junction tables that establish many-to-many relationships based on the file, we need to identify the tables that might have many-to-many relationships. Here are some potential many-to-many relationships and their corresponding junction tables:

   - **Obligations and Projects**: An obligation can be associated with multiple projects, and a project can have multiple obligations.
   - **Obligations and Plans**: An obligation can be associated with multiple plans, and a plan can have multiple obligations.
   - **Obligations and Regulations**: An obligation can be associated with multiple regulations, and a regulation can have multiple obligations.

Here are the schemas for the junction tables:

   - **Obligations and Projects**:
```sql
CREATE TABLE ObligationProjects (
    obligation_id INTEGER,
    project_id INTEGER,
    PRIMARY KEY (obligation_id, project_id),
    FOREIGN KEY (obligation_id) REFERENCES Obligations(Obligation_Number),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);
```

   - **Obligations and Plans**:
```sql
CREATE TABLE ObligationPlans (
    obligation_id INTEGER,
    plan_id INTEGER,
    PRIMARY KEY (obligation_id, plan_id),
    FOREIGN KEY (obligation_id) REFERENCES Obligations(Obligation_Number),
    FOREIGN KEY (plan_id) REFERENCES Plans(plan_id)
);
```

- **Obligations and Regulations**:
```sql
CREATE TABLE ObligationRegulations (
    obligation_id INTEGER,
    regulation_id INTEGER,
    PRIMARY KEY (obligation_id, regulation_id),
    FOREIGN KEY (obligation_id) REFERENCES Obligations(Obligation_Number),
    FOREIGN KEY (regulation_id) REFERENCES Regulations(regulation_id)
);
```

To complete the schema, you would also need to define the `Projects`, `Plans`, and `Regulations` tables:

```sql
-- Create the Projects table
CREATE TABLE Projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT,
    project_description TEXT
);

-- Create the Plans table
CREATE TABLE Plans (
    plan_id INTEGER PRIMARY KEY,
    plan_name TEXT,
    plan_description TEXT
);

-- Create the Regulations table
CREATE TABLE Regulations (
    regulation_id INTEGER PRIMARY KEY,
    regulation_name TEXT,
    regulation_description TEXT
);
```

By creating these junction tables, you can establish many-to-many relationships between the `Obligations` table and the `Projects`, `Plans`, and `Regulations` tables. This allows you to link multiple obligations to multiple projects, plans, and regulations, ensuring data integrity and consistency through foreign key constraints.

Here is how you can create a database table view for the OR(2) demonstrating the 14 days lookahead of obligations in SQLite:

1. **Create the Obligations Table**:
```sql
CREATE TABLE Obligations (
    Obligation_Number INTEGER PRIMARY KEY,
    Project_Name VARCHAR(255),
    Primary_Environmental_Mechanism TEXT,
    Procedure TEXT,
    Environmental_Aspect TEXT,
    Obligation TEXT,
    Accountability INTEGER,
    Responsibility INTEGER,
    ProjectPhase TEXT,
    Action_DueDate DATE,
    Close_Out_Date DATE,
    Status VARCHAR(50),
    Supporting_Information TEXT,
    General_Comments TEXT,
    Compliance_Comments TEXT,
    NonConformance_Comments TEXT,
    Evidence TEXT,
    PersonEmail TEXT,
    Recurring_Obligation BOOLEAN,
    Recurring_Frequency VARCHAR(50),
    Recurring_Status VARCHAR(50),
    Recurring_Forcasted_Date DATE,
    Inspection BOOLEAN,
    Inspection_Frequency VARCHAR(50),
    Site_or_Desktop VARCHAR(50),
    New_Control_Action_Required BOOLEAN,
    Obligation_Type VARCHAR(50),
    Gap_Analysis TEXT,
    Notes_for_Gap_Analysis TEXT,
    FOREIGN KEY (Accountability) REFERENCES Accountability(accountability_id),
    FOREIGN KEY (Responsibility) REFERENCES Responsibility(responsibility_id)
);
```

2. **Create the Accountability Table**:
```sql
CREATE TABLE Accountability (
    accountability_id INTEGER PRIMARY KEY,
    accountability_name TEXT
);
```

3. **Create the Responsibility Table**:
```sql
CREATE TABLE Responsibility (
    responsibility_id INTEGER PRIMARY KEY,
    responsibility_name TEXT
);
```

4. **Enable Foreign Key Support**:
```sql
PRAGMA foreign_keys = ON;
```

5. **Insert Data**:
```sql
-- Insert data into the Accountability table
INSERT INTO Accountability (accountability_id, accountability_name) VALUES (1, 'John Doe');

-- Insert data into the Responsibility table
INSERT INTO Responsibility (responsibility_id, responsibility_name) VALUES (2, 'Jane Smith');

-- Insert data into the Obligations table
INSERT INTO Obligations (Obligation_Number, Project_Name, Primary_Environmental_Mechanism, Procedure, Environmental_Aspect, Obligation, Accountability, Responsibility, ProjectPhase, Action_DueDate, Close_Out_Date, Status, Supporting_Information, General_Comments, Compliance_Comments, NonConformance_Comments, Evidence, PersonEmail, Recurring_Obligation, Recurring_Frequency, Recurring_Status, Recurring_Forcasted_Date, Inspection, Inspection_Frequency, Site_or_Desktop, New_Control_Action_Required, Obligation_Type, Gap_Analysis, Notes_for_Gap_Analysis)
VALUES (1, 'Project 1', 'Mechanism 1', 'Procedure 1', 'Aspect 1', 'Obligation 1', 1, 2, 'Phase 1', '2025-01-18', '2025-01-19', 'In Progress', 'Supporting Info', 'General Comments', 'Compliance Comments', 'NonConformance Comments', 'Evidence', 'email@example.com', 1, 'Monthly', 'In Progress', '2025-02-18', 1, 'Monthly', 'Site', 1, 'Type 1', 'Gap Analysis', 'Notes for Gap Analysis');
```

6. **Create the 14 Days Lookahead View**:
```sql
CREATE VIEW FourteenDaysLookahead AS
SELECT 
    Obligation_Number,
    Project_Name,
    Primary_Environmental_Mechanism,
    Procedure,
    Environmental_Aspect,
    Obligation,
    Accountability,
    Responsibility,
    ProjectPhase,
    Action_DueDate,
    Close_Out_Date,
    Status,
    Supporting_Information,
    General_Comments,
    Compliance_Comments,
    NonConformance_Comments,
    Evidence,
    PersonEmail,
    Recurring_Obligation,
    Recurring_Frequency,
    Recurring_Status,
    Recurring_Forcasted_Date,
    Inspection,
    Inspection_Frequency,
    Site_or_Desktop,
    New_Control_Action_Required,
    Obligation_Type,
    Gap_Analysis,
    Notes_for_Gap_Analysis
FROM Obligations
WHERE Action_DueDate BETWEEN DATE('now') AND DATE('now', '+14 days');
```

This view will display all obligations that have an action due date within the next 14 days. By following these steps, you can create a database table view for the OR(2) demonstrating the 14 days lookahead of obligations in SQLite.

Handling recurring obligations in the new schema involves adding specific columns to track the recurrence details and ensuring that the database can manage and query these recurring obligations effectively. Here’s how you can do it:

1. **Add Columns for Recurrence Details**:
   - **Recurring_Obligation**: A boolean column to indicate if the obligation is recurring.
   - **Recurring_Frequency**: A text column to specify the frequency of the recurring obligation (e.g., Daily, Weekly, Monthly).
   - **Recurring_Status**: A text column to indicate the current status of the recurring obligation.
   - **Recurring_Forecasted_Date**: A date column to specify the forecasted date for the next occurrence of the recurring obligation.

2. **Modify the Obligations Table**:
```sql
CREATE TABLE Obligations (
    Obligation_Number INTEGER PRIMARY KEY,
    Project_Name VARCHAR(255),
    Primary_Environmental_Mechanism TEXT,
    Procedure TEXT,
    Environmental_Aspect TEXT,
    Obligation TEXT,
    Accountability INTEGER,
    Responsibility INTEGER,
    ProjectPhase TEXT,
    Action_DueDate DATE,
    Close_Out_Date DATE,
    Status VARCHAR(50),
    Supporting_Information TEXT,
    General_Comments TEXT,
    Compliance_Comments TEXT,
    NonConformance_Comments TEXT,
    Evidence TEXT,
    PersonEmail TEXT,
    Recurring_Obligation BOOLEAN,
    Recurring_Frequency VARCHAR(50),
    Recurring_Status VARCHAR(50),
    Recurring_Forecasted_Date DATE,
    Inspection BOOLEAN,
    Inspection_Frequency VARCHAR(50),
    Site_or_Desktop VARCHAR(50),
    New_Control_Action_Required BOOLEAN,
    Obligation_Type VARCHAR(50),
    Gap_Analysis TEXT,
    Notes_for_Gap_Analysis TEXT,
    FOREIGN KEY (Accountability) REFERENCES Accountability(accountability_id),
    FOREIGN KEY (Responsibility) REFERENCES Responsibility(responsibility_id)
);
```

3. **Insert Data with Recurrence Details**:
```sql
-- Insert data into the Obligations table with recurrence details
INSERT INTO Obligations (Obligation_Number, Project_Name, Primary_Environmental_Mechanism, Procedure, Environmental_Aspect, Obligation, Accountability, Responsibility, ProjectPhase, Action_DueDate, Close_Out_Date, Status, Supporting_Information, General_Comments, Compliance_Comments, NonConformance_Comments, Evidence, PersonEmail, Recurring_Obligation, Recurring_Frequency, Recurring_Status, Recurring_Forecasted_Date, Inspection, Inspection_Frequency, Site_or_Desktop, New_Control_Action_Required, Obligation_Type, Gap_Analysis, Notes_for_Gap_Analysis)
VALUES (1, 'Project 1', 'Mechanism 1', 'Procedure 1', 'Aspect 1', 'Obligation 1', 1, 2, 'Phase 1', '2025-01-18', '2025-01-19', 'In Progress', 'Supporting Info', 'General Comments', 'Compliance Comments', 'NonConformance Comments', 'Evidence', 'email@example.com', 1, 'Monthly', 'In Progress', '2025-02-18', 1, 'Monthly', 'Site', 1, 'Type 1', 'Gap Analysis', 'Notes for Gap Analysis');
```

4. **Create a View for Recurring Obligations**:
```sql
CREATE VIEW RecurringObligations AS
SELECT 
    Obligation_Number,
    Project_Name,
    Primary_Environmental_Mechanism,
    Procedure,
    Environmental_Aspect,
    Obligation,
    Accountability,
    Responsibility,
    ProjectPhase,
    Action_DueDate,
    Close_Out_Date,
    Status,
    Supporting_Information,
    General_Comments,
    Compliance_Comments,
    NonConformance_Comments,
    Evidence,
    PersonEmail,
    Recurring_Obligation,
    Recurring_Frequency,
    Recurring_Status,
    Recurring_Forecasted_Date,
    Inspection,
    Inspection_Frequency,
    Site_or_Desktop,
    New_Control_Action_Required,
    Obligation_Type,
    Gap_Analysis,
    Notes_for_Gap_Analysis
FROM Obligations
WHERE Recurring_Obligation = 1;
```

This view will display all recurring obligations, allowing you to easily manage and track them. By following these steps, you can effectively handle recurring obligations in the new schema, ensuring that all relevant details are captured and managed efficiently. 

To update recurring obligations in the database, you can follow these steps:

1. **Identify the Recurring Obligations**: First, identify the obligations that are recurring. These will have the `Recurring_Obligation` column set to `TRUE`.

2. **Calculate the Next Due Date**: For each recurring obligation, calculate the next due date based on the `Recurring_Frequency`. This could be daily, weekly, monthly, etc.

3. **Update the Recurring Status**: Update the `Recurring_Status` column to reflect the current status of the recurring obligation.

4. **Insert or Update Records**: Depending on your schema, you may need to insert a new record for each recurrence or update the existing record with the new due date and status.

Here is an example SQL script to update recurring obligations in SQLite:

```sql
-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Update the recurring obligations
UPDATE Obligations
SET 
    Recurring_Status = 'In Progress',
    Recurring_Forecasted_Date = DATE(Recurring_Forecasted_Date, Recurring_Frequency)
WHERE 
    Recurring_Obligation = 1
    AND Recurring_Forecasted_Date <= DATE('now');

-- Insert new records for recurring obligations if needed
INSERT INTO Obligations (
    Obligation_Number, Project_Name, Primary_Environmental_Mechanism, Procedure, Environmental_Aspect, Obligation, Accountability, Responsibility, ProjectPhase, Action_DueDate, Close_Out_Date, Status, Supporting_Information, General_Comments, Compliance_Comments, NonConformance_Comments, Evidence, PersonEmail, Recurring_Obligation, Recurring_Frequency, Recurring_Status, Recurring_Forecasted_Date, Inspection, Inspection_Frequency, Site_or_Desktop, New_Control_Action_Required, Obligation_Type, Gap_Analysis, Notes_for_Gap_Analysis
)
SELECT 
    Obligation_Number, Project_Name, Primary_Environmental_Mechanism, Procedure, Environmental_Aspect, Obligation, Accountability, Responsibility, ProjectPhase, DATE(Action_DueDate, Recurring_Frequency), Close_Out_Date, 'In Progress', Supporting_Information, General_Comments, Compliance_Comments, NonConformance_Comments, Evidence, PersonEmail, Recurring_Obligation, Recurring_Frequency, 'In Progress', DATE(Recurring_Forecasted_Date, Recurring_Frequency), Inspection, Inspection_Frequency, Site_or_Desktop, New_Control_Action_Required, Obligation_Type, Gap_Analysis, Notes_for_Gap_Analysis
FROM 
    Obligations
WHERE 
    Recurring_Obligation = 1
    AND Recurring_Forecasted_Date <= DATE('now');
```

This script does the following:
- Enables foreign key support in SQLite.
- Updates the `Recurring_Status` and `Recurring_Forecasted_Date` for obligations that are due.
- Inserts new records for recurring obligations with the updated due date and status.

By following these steps, you can effectively manage and update recurring obligations in your database.

Here is how you can create a database table view for the OR(2) demonstrating the overdue obligations in SQLite:

1. **Create the Obligations Table**:
```sql
CREATE TABLE Obligations (
    Obligation_Number INTEGER PRIMARY KEY,
    Project_Name VARCHAR(255),
    Primary_Environmental_Mechanism TEXT,
    Procedure TEXT,
    Environmental_Aspect TEXT,
    Obligation TEXT,
    Accountability INTEGER,
    Responsibility INTEGER,
    ProjectPhase TEXT,
    Action_DueDate DATE,
    Close_Out_Date DATE,
    Status VARCHAR(50),
    Supporting_Information TEXT,
    General_Comments TEXT,
    Compliance_Comments TEXT,
    NonConformance_Comments TEXT,
    Evidence TEXT,
    PersonEmail TEXT,
    Recurring_Obligation BOOLEAN,
    Recurring_Frequency VARCHAR(50),
    Recurring_Status VARCHAR(50),
    Recurring_Forecasted_Date DATE,
    Inspection BOOLEAN,
    Inspection_Frequency VARCHAR(50),
    Site_or_Desktop VARCHAR(50),
    New_Control_Action_Required BOOLEAN,
    Obligation_Type VARCHAR(50),
    Gap_Analysis TEXT,
    Notes_for_Gap_Analysis TEXT,
    FOREIGN KEY (Accountability) REFERENCES Accountability(accountability_id),
    FOREIGN KEY (Responsibility) REFERENCES Responsibility(responsibility_id)
);
```

2. **Create the Accountability Table**:
```sql
CREATE TABLE Accountability (
    accountability_id INTEGER PRIMARY KEY,
    accountability_name TEXT
);
```

3. **Create the Responsibility Table**:
```sql
CREATE TABLE Responsibility (
    responsibility_id INTEGER PRIMARY KEY,
    responsibility_name TEXT
);
```

4. **Enable Foreign Key Support**:
```sql
PRAGMA foreign_keys = ON;
```

5. **Insert Data**:
```sql
-- Insert data into the Accountability table
INSERT INTO Accountability (accountability_id, accountability_name) VALUES (1, 'John Doe');

-- Insert data into the Responsibility table
INSERT INTO Responsibility (responsibility_id, responsibility_name) VALUES (2, 'Jane Smith');

-- Insert data into the Obligations table
INSERT INTO Obligations (Obligation_Number, Project_Name, Primary_Environmental_Mechanism, Procedure, Environmental_Aspect, Obligation, Accountability, Responsibility, ProjectPhase, Action_DueDate, Close_Out_Date, Status, Supporting_Information, General_Comments, Compliance_Comments, NonConformance_Comments, Evidence, PersonEmail, Recurring_Obligation, Recurring_Frequency, Recurring_Status, Recurring_Forecasted_Date, Inspection, Inspection_Frequency, Site_or_Desktop, New_Control_Action_Required, Obligation_Type, Gap_Analysis, Notes_for_Gap_Analysis)
VALUES (1, 'Project 1', 'Mechanism 1', 'Procedure 1', 'Aspect 1', 'Obligation 1', 1, 2, 'Phase 1', '2025-01-18', '2025-01-19', 'Overdue', 'Supporting Info', 'General Comments', 'Compliance Comments', 'NonConformance Comments', 'Evidence', 'email@example.com', 1, 'Monthly', 'In Progress', '2025-02-18', 1, 'Monthly', 'Site', 1, 'Type 1', 'Gap Analysis', 'Notes for Gap Analysis');
```

6. **Create the Overdue Obligations View**:
```sql
CREATE VIEW OverdueObligations AS
SELECT 
    Obligation_Number,
    Project_Name,
    Primary_Environmental_Mechanism,
    Procedure,
    Environmental_Aspect,
    Obligation,
    Accountability,
    Responsibility,
    ProjectPhase,
    Action_DueDate,
    Close_Out_Date,
    Status,
    Supporting_Information,
    General_Comments,
    Compliance_Comments,
    NonConformance_Comments,
    Evidence,
    PersonEmail,
    Recurring_Obligation,
    Recurring_Frequency,
    Recurring_Status,
    Recurring_Forecasted_Date,
    Inspection,
    Inspection_Frequency,
    Site_or_Desktop,
    New_Control_Action_Required,
    Obligation_Type,
    Gap_Analysis,
    Notes_for_Gap_Analysis
FROM Obligations
WHERE Status = 'Overdue';
```

This view will display all obligations that are currently overdue. By following these steps, you can create a database table view for the OR(2) demonstrating the overdue obligations in SQLite.

To automate the update of overdue obligations in your database, you can create a scheduled task or a script that runs periodically to check for obligations that are past their due date and update their status accordingly. Here’s how you can do it in SQLite:

1. **Create a Script to Update Overdue Obligations**:
   - This script will check for obligations where the `Action_DueDate` is past the current date and update their status to "Overdue".

```sql
-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- Update the status of overdue obligations
UPDATE Obligations
SET Status = 'Overdue'
WHERE Action_DueDate < DATE('now')
AND Status != 'Completed';
```

2. **Schedule the Script to Run Periodically**:
   - Depending on your operating system, you can use a task scheduler to run this script at regular intervals (e.g., daily).

**On Windows**:
- You can use Task Scheduler to run the script daily.
  1. Open Task Scheduler.
  2. Create a new task.
  3. Set the trigger to run daily.
  4. Set the action to run a program and specify the path to your SQLite script or a batch file that runs the script.

**On Linux**:
- You can use cron jobs to schedule the script.
  1. Open the crontab file by running `crontab -e`.
  2. Add a new cron job to run the script daily. For example, to run the script at midnight every day, add the following line:
     ```sh
     0 0 * * * sqlite3 /path/to/your/database.db < /path/to/your/script.sql
     ```

3. **Example of a Batch File (Windows)**:
   - Create a batch file (e.g., `update_overdue_obligations.bat`) with the following content:
     ```bat
     @echo off
     sqlite3 "C:\path\to\your\database.db" < "C:\path\to\your\script.sql"
     ```

4. **Example of a Shell Script (Linux)**:
   - Create a shell script (e.g., `update_overdue_obligations.sh`) with the following content:
     ```sh
     #!/bin/bash
     sqlite3 /path/to/your/database.db < /path/to/your/script.sql
     ```

By following these steps, you can automate the update of overdue obligations in your database. The script will run periodically, checking for obligations that are past their due date and updating their status to "Overdue". This ensures that your database remains up-to-date without manual intervention.

I attempted to clean up the OR(2) worksheet from the **[Port Project Management .xlsx](https://envenggroup-my.sharepoint.com/personal/agallo_enveng-group_com_au/Documents/Microsoft%20Copilot%20Chat%20Files/Port%20Project%20Management%20.xlsx?web=1&EntityRepresentationId=1015aa5e-e654-43c5-9704-b5a041056d11)** file and generate a CSV file for you to use as an import into SQLite. However, I encountered an issue with the worksheet name not being found. 

**Getting ready to import CSV into SQLite**
Ensure that the worksheet name is correctly identified and then clean up the data accordingly. Here is the structure and columns based on the information provided:

1. **Columns**:
   - **Project_Name**
   - **Primary_Environmental_Mechanism**
   - **Procedure**
   - **Environmental_Aspect**
   - **Obligation_Number**
   - **Obligation**
   - **Accountability**
   - **Responsibility**
   - **ProjectPhase**
   - **Action_DueDate**
   - **Close_Out_Date**
   - **Status**
   - **Supporting_Information**
   - **General_Comments**
   - **Compliance_Comments**
   - **NonConformance_Comments**
   - **Evidence**
   - **PersonEmail**
   - **Recurring_Obligation**
   - **Recurring_Frequency**
   - **Recurring_Status**
   - **Recurring_Forecasted_Date**
   - **Inspection**
   - **Inspection_Frequency**
   - **Site_or_Desktop**
   - **New_Control_Action_Required**
   - **Obligation_Type**
   - **Gap_Analysis**
   - **Notes_for_Gap_Analysis**

I will now attempt to generate the cleaned CSV file again. Please hold on for a moment.

```python
import pandas as pd

# Load the OR(2) worksheet from the 'Port Project Management .xlsx' file
file_path = 'Port Project Management .xlsx'
sheet_name = 'OR(2)'

# Read the worksheet into a DataFrame
df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')

# Clean up the DataFrame and label the columns correctly
df.columns = [
    'Project_Name', 'Primary_Environmental_Mechanism', 'Procedure', 'Environmental_Aspect',
    'Obligation_Number', 'Obligation', 'Accountability', 'Responsibility', 'ProjectPhase',
    'Action_DueDate', 'Close_Out_Date', 'Status', 'Supporting_Information', 'General_Comments',
    'Compliance_Comments', 'NonConformance_Comments', 'Evidence', 'PersonEmail',
    'Recurring_Obligation', 'Recurring_Frequency', 'Recurring_Status', 'Recurring_Forecasted_Date',
    'Inspection', 'Inspection_Frequency', 'Site_or_Desktop', 'New_Control_Action_Required',
    'Obligation_Type', 'Gap_Analysis', 'Notes_for_Gap_Analysis'
]

# Clean up the data (e.g., remove any leading/trailing whitespace)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Save the cleaned DataFrame to a CSV file
output_csv_path = 'OR2_cleaned.csv'
df.to_csv(output_csv_path, index=False)

output_csv_path
```

```csv
Project_Name,Primary_Environmental_Mechanism,Procedure,Environmental_Aspect,Obligation_Number,Obligation,Accountability,Responsibility,ProjectPhase,Action_DueDate,Close_Out_Date,Status,Supporting_Information,General_Comments,Compliance_Comments,NonConformance_Comments,Evidence,PersonEmail,Recurring_Obligation,Recurring_Frequency,Recurring_Status,Recurring_Forecasted_Date,Inspection,Inspection_Frequency,Site_or_Desktop,New_Control_Action_Required,Obligation_Type,Gap_Analysis,Notes_for_Gap_Analysis
"Project 1","Mechanism 1","Procedure 1","Aspect 1",1,"Obligation 1",1,2,"Phase 1","2025-01-18","2025-01-19","In Progress","Supporting Info","General Comments","Compliance Comments","NonConformance Comments","Evidence","email@example.com",1,"Monthly","In Progress","2025-02-18",1,"Monthly","Site",1,"Type 1","Gap Analysis","Notes for Gap Analysis"
```

**Cleaning CSV for Import**

```python
import pandas as pd

# Load the OR(2) data from the CSV file
file_path = 'Port Project Management (Portside OR (2)).csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Clean up the DataFrame and label the columns correctly
df.columns = [
    'Project_Name', 'Primary_Environmental_Mechanism', 'Procedure', 'Environmental_Aspect',
    'Obligation_Number', 'Obligation', 'Accountability', 'Responsibility', 'ProjectPhase',
    'Action_DueDate', 'Close_Out_Date', 'Status', 'Supporting_Information', 'General_Comments',
    'Compliance_Comments', 'NonConformance_Comments', 'Evidence', 'PersonEmail',
    'Recurring_Obligation', 'Recurring_Frequency', 'Recurring_Status', 'Recurring_Forecasted_Date',
    'Inspection', 'Inspection_Frequency', 'Site_or_Desktop', 'New_Control_Action_Required',
    'Obligation_Type', 'Gap_Analysis', 'Notes_for_Gap_Analysis'
]

# Clean up the data (e.g., remove any leading/trailing whitespace)
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Save the cleaned DataFrame to a new CSV file
output_csv_path = 'OR2_cleaned.csv'
df.to_csv(output_csv_path, index=False)

output_csv_path
```
### Structure of the Form

1. **Header**:
   - Title: "Obligation Register"
   - Navigation Links: Home, Create New Obligation, View Obligations, etc.

2. **Form Sections**:
   - **Create New Obligation**:
     - Input fields for all necessary columns (e.g., Project Name, Primary Environmental Mechanism, Procedure, Environmental Aspect, Obligation Number, Obligation, Accountability, Responsibility, Project Phase, Action Due Date, Close Out Date, Status, Supporting Information, General Comments, Compliance Comments, NonConformance Comments, Evidence, Person Email, Recurring Obligation, Recurring Frequency, Recurring Status, Recurring Forecasted Date, Inspection, Inspection Frequency, Site or Desktop, New Control Action Required, Obligation Type, Gap Analysis, Notes for Gap Analysis).
     - Submit button to create a new obligation.

   - **Update Obligation**:
     - Input fields pre-filled with existing data for the selected obligation.
     - Update button to save changes.

   - **Delete Obligation**:
     - Confirmation dialog to confirm deletion.
     - Delete button to remove the obligation.

   - **View Obligations**:
     - Table or list view displaying all obligations with options to edit or delete each entry.

### Components

1. **Input Fields**:
   - **Text Fields**:
     - **Project Name**: A text input field where users can enter the name of the project.
     - **Procedure**: A text input field for users to describe the procedure related to the obligation.
     - **Environmental Aspect**: A text input field for users to specify the environmental aspect.
   - **Date Pickers**:
     - **Action Due Date**: A date picker allowing users to select the due date for the obligation.
     - **Close Out Date**: A date picker for users to select the date when the obligation was closed out.
   - **Dropdowns**:
     - **Status**: A dropdown menu with predefined options such as "Overdue", "Completed", "In Progress", and "Not Started".
     - **Recurring Frequency**: A dropdown menu with options like "Daily", "Weekly", "Monthly", and "Yearly".
   - **Checkboxes**:
     - **Recurring Obligation**: A checkbox to indicate whether the obligation is recurring.
     - **Inspection**: A checkbox to indicate if the obligation is tracked using inspections.
   - **Text Areas**:
     - **General Comments**: A larger text area for users to enter any general comments about the obligation.
     - **Compliance Comments**: A text area for users to add comments related to compliance.
     - **NonConformance Comments**: A text area for users to add comments related to non-conformance.

2. **Buttons**:
   - **Submit Button**:
     - **Create New Obligation**: A button labeled "Create" to submit the form and create a new obligation.
   - **Update Button**:
     - **Save Changes**: A button labeled "Update" to save changes made to an existing obligation.
   - **Delete Button**:
     - **Remove Obligation**: A button labeled "Delete" to remove an obligation. This should be accompanied by a confirmation dialog to prevent accidental deletions.
   - **Navigation Buttons/Links**:
     - **Home**: A button or link to navigate back to the home page or main view of the obligation register.
     - **Create New Obligation**: A button or link to navigate to the form for creating a new obligation.
     - **View Obligations**: A button or link to navigate to the list or table view of all obligations.

3. **Table/List View**:
   - Display all obligations in a tabular or list format.
   - Include columns for key information (e.g., Obligation Number, Project Name, Status).
   - Action buttons or links for editing and deleting each obligation.

4. **Confirmation Dialogs**:
   - For delete operations, include a confirmation dialog to prevent accidental deletions.

### UI/UX Layout Suggestions

1. **User-Friendly Design**:
   - Keep the design clean and simple.
   - Use clear labels and placeholders for input fields.
   - Group related fields together for better organization.

2. **Responsive Layout**:
   - Ensure the form is responsive and works well on different devices (e.g., desktops, tablets, smartphones).

3. **Validation and Error Handling**:
   - Include form validation to ensure all required fields are filled out correctly.
   - Display error messages for invalid input or missing required fields.

4. **Accessibility**:
   - Ensure the form is accessible to all users, including those with disabilities.
   - Use appropriate ARIA labels and roles for better screen reader support.

5. **Feedback and Confirmation**:
   - Provide feedback to users after they perform an action (e.g., "Obligation created successfully", "Changes saved", "Obligation deleted").
   - Use modals or toast notifications for feedback messages.

By following these guidelines, you can create a user-friendly form that allows end-users to perform CRUD operations on the OR(2) database obligation register without needing to know SQL.

**Charts**

Here is a comprehensive plan for creating a business intelligence interactive experience for end-users to visualize, interact, filter, sort, analyze, review, and take action on the OR(2) database obligation register:

### Types of Charts and Visualizations

1. **Bar Charts**:
   - **Obligations by Status**: Display the count of obligations in different statuses (e.g., Overdue, Completed, In Progress, Not Started).
   - **Obligations by Project Phase**: Show the number of obligations in each project phase.

2. **Line Charts**:
   - **Obligation Trends Over Time**: Show the trend of obligations over time, including the number of obligations created, completed, and overdue.

3. **Pie Charts**:
   - **Obligations by Accountability**: Display the distribution of obligations by accountable parties.
   - **Obligations by Responsibility**: Show the distribution of obligations by responsible parties.

4. **Gantt Charts**:
   - **Obligation Timeline**: Visualize the timeline of obligations, including start dates, due dates, and completion dates.

5. **Heatmaps**:
   - **Obligation Density**: Show the density of obligations across different projects or phases.

6. **Interactive Dashboards**:
   - **Overview Dashboard**: Provide a high-level overview of obligations, including key metrics, charts, and visualizations.
   - **Detailed Analysis Dashboard**: Allow users to drill down into specific obligations, filter by various criteria, and view detailed information.

### Interactive Elements

1. **Filters**:
   - **Date Range Filter**: Allow users to filter obligations by date range (e.g., last 7 days, last 30 days, custom date range).
   - **Status Filter**: Enable users to filter obligations by status (e.g., Overdue, Completed, In Progress, Not Started).
   - **Project Phase Filter**: Allow users to filter obligations by project phase.
   - **Accountability and Responsibility Filters**: Enable users to filter obligations by accountable and responsible parties.

2. **Sorting Options**:
   - **Sort by Due Date**: Allow users to sort obligations by due date (ascending or descending).
   - **Sort by Status**: Enable users to sort obligations by status.
   - **Sort by Project Phase**: Allow users to sort obligations by project phase.

3. **Interactive Elements**:
   - **Hover Tooltips**: Provide additional information when users hover over chart elements (e.g., obligation details, due dates, status).
   - **Clickable Elements**: Allow users to click on chart elements to view more detailed information or navigate to related views.
   - **Drill-Down Capabilities**: Enable users to drill down into specific data points for more detailed analysis.

4. **Notifications and Alerts**:
   - **14-Day Lookahead Notifications**: Notify users of obligations due in the next 14 days through visual alerts or notifications.
   - **Overdue Obligation Alerts**: Highlight overdue obligations with visual indicators (e.g., red color, alert icons) and send notifications to relevant users.

5. **Actionable Elements**:
   - **Edit and Update Buttons**: Provide buttons for users with access to edit and update obligations directly from the dashboard.
   - **Delete Buttons**: Allow authorized users to delete obligations with confirmation dialogs to prevent accidental deletions.
   - **Add New Obligation**: Provide a button to add new obligations, opening a form for data entry.

### UI/UX Layout Suggestions

1. **User-Friendly Design**:
   - Keep the design clean and simple, with a focus on usability.
   - Use clear labels and intuitive icons for interactive elements.
   - Group related visualizations and filters together for better organization.

2. **Responsive Layout**:
   - Ensure the dashboard is responsive and works well on different devices (e.g., desktops, tablets, smartphones).

3. **Accessibility**:
   - Ensure the dashboard is accessible to all users, including those with disabilities.
   - Use appropriate ARIA labels and roles for better screen reader support.

4. **Feedback and Confirmation**:
   - Provide feedback to users after they perform an action (e.g., "Obligation updated successfully", "Obligation deleted").
   - Use modals or toast notifications for feedback messages.

By following these guidelines, you can create a visually engaging and interactive business intelligence experience for end-users to analyze and manage the OR(2) database obligation register.

**Dashboard**

Here is a suggested layout for an interactive dashboard that allows end-users to visualize, interact, filter, sort, analyze, review, and take action on the OR(2) database obligation register:

### Interactive Dashboard Layout

#### 1. Header
- **Title**: "Obligation Register Dashboard"
- **Navigation Links**: Home, Create New Obligation, View Obligations, Reports, Settings, Help

#### 2. Overview Section
- **Key Metrics**: Display key metrics at the top of the dashboard for quick insights. Metrics can include:
  - Total Obligations
  - Obligations Due in Next 14 Days
  - Overdue Obligations
  - Completed Obligations
  - Obligations In Progress

#### 3. Filters and Sorting Options
- **Filters**: Place filters on the left side or top of the dashboard to allow users to filter data by:
  - Date Range (e.g., last 7 days, last 30 days, custom date range)
  - Status (e.g., Overdue, Completed, In Progress, Not Started)
  - Project Phase
  - Accountability
  - Responsibility
- **Sorting Options**: Provide sorting options next to the filters to allow users to sort data by:
  - Due Date (ascending or descending)
  - Status
  - Project Phase

#### 4. Visualizations
- **Bar Charts**:
  - Obligations by Status: Display the count of obligations in different statuses.
  - Obligations by Project Phase: Show the number of obligations in each project phase.
- **Line Charts**:
  - Obligation Trends Over Time: Show the trend of obligations over time, including the number of obligations created, completed, and overdue.
- **Pie Charts**:
  - Obligations by Accountability: Display the distribution of obligations by accountable parties.
  - Obligations by Responsibility: Show the distribution of obligations by responsible parties.
- **Gantt Charts**:
  - Obligation Timeline: Visualize the timeline of obligations, including start dates, due dates, and completion dates.
- **Heatmaps**:
  - Obligation Density: Show the density of obligations across different projects or phases.

#### 5. Interactive Elements
- **Hover Tooltips**: Provide additional information when users hover over chart elements (e.g., obligation details, due dates, status).
- **Clickable Elements**: Allow users to click on chart elements to view more detailed information or navigate to related views.
- **Drill-Down Capabilities**: Enable users to drill down into specific data points for more detailed analysis.

#### 6. Notifications and Alerts
- **14-Day Lookahead Notifications**: Display visual alerts or notifications for obligations due in the next 14 days.
- **Overdue Obligation Alerts**: Highlight overdue obligations with visual indicators (e.g., red color, alert icons) and send notifications to relevant users.

#### 7. Actionable Elements
- **Edit and Update Buttons**: Provide buttons for users with access to edit and update obligations directly from the dashboard.
- **Delete Buttons**: Allow authorized users to delete obligations with confirmation dialogs to prevent accidental deletions.
- **Add New Obligation**: Provide a button to add new obligations, opening a form for data entry.

#### 8. Detailed Analysis Section
- **Obligation Details**: Display detailed information about selected obligations, including all relevant fields (e.g., Project Name, Procedure, Environmental Aspect, Accountability, Responsibility, Action Due Date, Status, Comments).
- **Comments and Attachments**: Allow users to add comments and attach files related to specific obligations.

#### 9. Footer
- **Footer Links**: Include links to additional resources, support, and contact information.

By following this layout, you can create a visually engaging and interactive dashboard that allows end-users to effectively analyze and manage the OR(2) database obligation register.