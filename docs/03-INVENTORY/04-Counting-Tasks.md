# Counting Tasks

## Overview

Counting Tasks organize audit work by department and storage location. Tasks are auto-generated from the audit scope and assigned to departments for counting.

## Purpose

- Organize counting work by department and storage
- Assign work to departments/users
- Track task progress
- Support concurrent counting by multiple users
- Enable task-based counting workflow

## DocType Definition

### Counting Task DocType (Child Table)

```python
# Counting Task
- parent (Link: Inventory Audit)
- task_name (Data, auto-generated)  # "Rooms Department - Rooms Supply Closet"
- department (Link: Department, required)  # Which department this task is for
- storage_locations (Table: Task Storage Location)  # Which storages to count
- categories (Table: Task Category)  # Which categories (if partial audit)
- assigned_to_department (Link: Department)  # Same as department (for clarity)
- status (Select: Not Started, In Progress, Complete)
- started_by (Link: User)
- started_at (Datetime)
- completed_by (Link: User)
- completed_at (Datetime)
- notes (Text)
```

### Task Storage Location DocType (Child of Counting Task)

```python
# Task Storage Location
- parent (Link: Counting Task)
- parenttype ("Counting Task")
- parentfield ("storage_locations")
- storage_location (Link: Storage Area, required)
```

### Task Category DocType (Child of Counting Task - for partial audits)

```python
# Task Category
- parent (Link: Counting Task)
- parenttype ("Counting Task")
- parentfield ("categories")
- category (Link: Product Category, required)
```

## Key Features

### Auto-Generation
- Tasks auto-generated from audit scope
- Grouped by department and storage
- Categories assigned for partial audits

### Department Assignment
- Each task assigned to a department
- Users count only their assigned tasks
- Department-based access control

### Task Progress Tracking
- Track task status (Not Started, In Progress, Complete)
- Track who started/completed task
- Track completion times

## Implementation Steps

### Step 1: Create Counting Task Child Table
1. Create `Counting Task` child table DocType
2. Add parent link fields
3. Add department field (required)
4. Add status field

### Step 2: Create Child Tables
1. Create `Task Storage Location` child table
2. Create `Task Category` child table
3. Add to Counting Task DocType

### Step 3: Implement Auto-Generation
1. Implement create_counting_tasks() method
2. Group storages by department
3. Create task for each department-storage combination
4. Assign categories for partial audits

### Step 4: Add Progress Tracking
1. Add status field
2. Add started_by/started_at fields
3. Add completed_by/completed_at fields
4. Add notes field

## Dependencies

- **Inventory Audit DocType**: Parent DocType
- **Department DocType**: Department assignments
- **Storage Area DocType**: Storage locations
- **Product Category DocType**: Category filtering

## Usage Examples

### Auto-Generated Tasks
```
Audit Scope:
  - Departments: Kitchen, Beverage
  - Storages: Main Cooler, Dry Storage, Bar Cooler

Generated Tasks:
  - Task 1: Kitchen - Main Cooler
  - Task 2: Kitchen - Dry Storage
  - Task 3: Beverage - Bar Cooler
```

### Task Assignment
```
Task: "Kitchen - Main Cooler"
  - Department: Kitchen
  - Storage: Main Cooler
  - Assigned To: Kitchen Department
  - Status: Not Started
```

### Task Completion
```
Task: "Kitchen - Main Cooler"
  - Status: Complete
  - Started By: John Doe
  - Started At: 2025-01-31 08:00:00
  - Completed By: John Doe
  - Completed At: 2025-01-31 10:30:00
```

## Testing Checklist

- [ ] Auto-generate tasks from audit scope
- [ ] Group tasks by department
- [ ] Assign storage locations to tasks
- [ ] Assign categories for partial audits
- [ ] Update task status
- [ ] Track task progress
- [ ] Complete tasks
- [ ] Verify department assignments

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

