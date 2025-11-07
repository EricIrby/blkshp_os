# Frappe Framework Guide

## What is Frappe Framework?

Frappe Framework is a full-stack, metadata-driven web framework written in Python (backend) and JavaScript (frontend). It provides:

- **DocType System**: Define data models declaratively (no SQL migrations needed)
- **Desk UI**: Automatic form, list, report, and dashboard views
- **Permission System**: Field-level and document-level permissions
- **Workflow Engine**: State machine for document approval workflows
- **Print Format Builder**: Customizable PDF generation
- **Email Integration**: Built-in email sending and receiving
- **API Framework**: RESTful APIs for all DocTypes
- **Background Jobs**: Task queue system for async operations
- **File Management**: Document storage and versioning

## Installation & Setup

### Installing Frappe Bench

```bash
# Install Frappe Bench (recommended)
curl -o install.py https://install.erpnext.com
python3 install.py
```

### Creating a New Site

```bash
# Create new site
bench new-site blkshp.local
```

### Installing Your Custom App

```bash
# Install your custom app
bench get-app blkshp-product-platform
bench --site blkshp.local install-app blkshp-product-platform
```

### Starting Development Server

```bash
# Start development server
bench start
```

## Key Frappe Concepts

### DocTypes

DocTypes are the core data models in Frappe. They define:
- Fields and field types
- Relationships (Link, Table)
- Validation rules
- Permissions
- Form layouts

### Modules

Modules organize related DocTypes and functionality:
- Each module has its own directory
- Contains DocTypes, pages, reports, and custom scripts
- Can be packaged as separate apps

### Permissions

Frappe provides granular permission control:
- Role-based permissions
- Document-level permissions
- Field-level permissions
- User-level overrides

### Workflows

Workflows define document state machines:
- States (Draft, Submitted, Approved, etc.)
- Transitions between states
- Actions on state change
- Permissions per state

### APIs

All DocTypes automatically expose REST APIs:
- GET, POST, PUT, DELETE methods
- Filtering and pagination
- Authentication via API keys or sessions

## Development Workflow

1. **Create DocType**: Define data model in Frappe UI or JSON
2. **Add Fields**: Define fields with types and properties
3. **Set Permissions**: Configure role-based access
4. **Customize Forms**: Adjust form layouts and behavior
5. **Add Scripts**: Python server scripts and JavaScript client scripts
6. **Create Reports**: Build custom reports and dashboards
7. **Test**: Test functionality and permissions
8. **Deploy**: Migrate changes to production

## Best Practices

- **Use DocTypes**: Always use DocTypes instead of raw database tables
- **Leverage Built-ins**: Use Frappe's built-in features (permissions, workflows, etc.)
- **Follow Naming**: Use clear, descriptive names for DocTypes and fields
- **Version Control**: Keep JSON definitions in version control
- **Test Permissions**: Always test with different user roles
- **Optimize Queries**: Use database indexes and efficient queries

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 2

