# BLKSHP OS

**A unified inventory management and cost control platform for hospitality operations.**

**Version:** 0.0.1  
**Architecture:** Frappe Desk-Only Application  
**License:** MIT

---

## What is BLKSHP OS?

BLKSHP OS is a comprehensive business operating system for hospitality companies (restaurants, bars, catering operations) built on the Frappe Framework. It provides:

- ✅ **Unified Product Management** - Single system for all product types
- ✅ **Department-Based Organization** - Flexible segmentation and permissions
- ✅ **2D Inventory Tracking** - Product + Department inventory model
- ✅ **Role-Based Permissions** - 70+ granular permissions
- ✅ **API-First Design** - RESTful APIs for all functionality
- ✅ **Modular Architecture** - Domain-based organization

---

## Quick Start

### Installation

```bash
cd /path/to/frappe-bench

# Get the app
bench get-app https://github.com/your-org/blkshp_os --branch main

# Install on your site
bench --site mysite.local install-app blkshp_os

# Start the server
bench start
```

### First Steps

1. **Access your site:** `http://localhost:8000`
2. **Find the BLKSHP OS workspace** in Frappe Desk
3. **Create test data:** `bench --site mysite.local execute blkshp_os.scripts.setup_test_data.setup_all`
4. **Explore the documentation:** See `docs/README.md`

---

## Documentation

📚 **[Complete Documentation → docs/README.md](docs/README.md)**

### Quick Links

- **[Getting Started](docs/README.md#quick-start)** - 5-minute setup guide
- **[First-Time Setup](docs/README.md#first-time-setup)** - Detailed installation
- **[Development Guide](docs/DEVELOPMENT-GUIDE.md)** - Development roadmap
- **[Architecture](docs/00-ARCHITECTURE/)** - Architecture documentation
- **[Testing Guide](docs/TESTING-GUIDE.md)** - Testing practices
- **[API Reference](docs/API-REFERENCE.md)** - API documentation

### Domain Documentation

- **[Departments](docs/02-DEPARTMENTS/)** - ✅ Complete
- **[Permissions](docs/11-PERMISSIONS/)** - ✅ Complete
- **[Products](docs/01-PRODUCTS/)** - ⏳ Next Priority
- **[Inventory](docs/03-INVENTORY/)** - Planned
- **[Procurement](docs/04-PROCUREMENT/)** - Planned
- **[Other Domains](docs/)** - See docs/ directory

---

## Current Status

### Completed (Phase 1)

- ✅ **Departments Domain** - Department management and segmentation
- ✅ **Permissions Domain** - Role-based and department-based permissions
- ✅ **API Layer** - 20 whitelisted API endpoints
- ✅ **Fixtures** - Custom fields and standard roles
- ✅ **Test Coverage** - Comprehensive unit tests

### Next Steps (Phase 2)

- ⏳ **Products Domain** - Unified product management
- ⏳ **Inventory Domain** - Inventory tracking and audits
- ⏳ **Procurement Domain** - Vendor management and ordering

### Key Features

**Implemented:**
- 4 DocTypes (Department, Department Permission, Product Department, Role Permission)
- 5 Custom Fields (User and Role extensions)
- 70+ Permission definitions across 11 categories
- 8 Standard Roles with permissions
- 20 API Endpoints (7 Department, 13 Role/Permission)
- Client-side enhancements for User and Role forms

---

## Development

### Prerequisites

- Python 3.10+
- Node.js 18+
- Frappe Framework v14+
- MariaDB/PostgreSQL

### Setup for Development

```bash
# Navigate to bench
cd /path/to/frappe-bench

# Install app on site
bench --site mysite.local install-app blkshp_os

# Enable developer mode
bench --site mysite.local set-config developer_mode 1

# Build assets
bench build --app blkshp_os

# Run tests
bench --site mysite.local run-tests --app blkshp_os
```

### Code Quality

This app uses pre-commit hooks for code quality:

```bash
cd apps/blkshp_os

# Install pre-commit
pip install pre-commit

# Set up hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

**Tools configured:**
- **ruff** - Python linting and formatting
- **pyupgrade** - Python syntax modernization
- **eslint** - JavaScript linting
- **prettier** - JavaScript/JSON formatting

### Project Structure

```
blkshp_os/
├── blkshp_os/              # Main Python package
│   ├── api/                # API endpoints
│   ├── departments/        # Departments domain
│   ├── permissions/        # Permissions domain
│   ├── [other domains]/    # Future domains
│   ├── config/             # Desk configuration
│   ├── public/             # Static assets
│   └── hooks.py            # App configuration
├── docs/                   # Documentation
├── fixtures/               # Fixtures (custom fields, roles)
├── scripts/                # Utility scripts
└── pyproject.toml          # Python package config
```

---

## Contributing

### Before Contributing

1. Read the [Development Guide](docs/DEVELOPMENT-GUIDE.md)
2. Review the [Architecture Documentation](docs/00-ARCHITECTURE/)
3. Check the [Git Workflow](docs/GIT-WORKFLOW.md)
4. Understand the [Testing Guide](docs/TESTING-GUIDE.md)

### Development Process

1. Create a feature branch
2. Make your changes
3. Write tests
4. Run tests: `bench --site mysite.local run-tests --app blkshp_os`
5. Format code: `pre-commit run --all-files`
6. Update documentation
7. Submit pull request

### Code Standards

- Follow Frappe framework conventions
- Write comprehensive tests
- Document all public APIs
- Use type hints in Python code
- Follow the established patterns in the codebase

---

## Testing

### Run All Tests

```bash
bench --site mysite.local run-tests --app blkshp_os
```

### Run Domain-Specific Tests

```bash
# Departments domain
bench --site mysite.local run-tests --app blkshp_os --module blkshp_os.departments

# Permissions domain
bench --site mysite.local run-tests --app blkshp_os --module blkshp_os.permissions
```

### Run Specific Test File

```bash
bench --site mysite.local run-tests --app blkshp_os --module blkshp_os.departments.doctype.department.test_department
```

See [Testing Guide](docs/TESTING-GUIDE.md) for comprehensive testing documentation.

---

## Architecture

BLKSHP OS uses a **Frappe Desk-only architecture**:

- **Backend:** Python (DocTypes, API endpoints, business logic)
- **Frontend:** Frappe's built-in Desk UI
- **Database:** MariaDB/PostgreSQL
- **Framework:** Frappe Framework v14+
- **Organization:** Domain-based modules

**Key Architectural Decisions:**

1. **Desk-Only** - No separate frontend (can add later if needed)
2. **Domain-Based** - Code organized by business domain
3. **Department-Centric** - Department-based permissions and organization
4. **2D Inventory** - Product + Department (not storage location)
5. **Hub-and-Spoke Units** - All quantities in primary count unit

See [Architecture Documentation](docs/00-ARCHITECTURE/) for details.

---

## Support & Resources

### Documentation

- **Main Documentation:** [docs/README.md](docs/README.md)
- **Development Guide:** [docs/DEVELOPMENT-GUIDE.md](docs/DEVELOPMENT-GUIDE.md)
- **API Reference:** [docs/API-REFERENCE.md](docs/API-REFERENCE.md)
- **Architecture:** [docs/00-ARCHITECTURE/](docs/00-ARCHITECTURE/)

### Getting Help

- Check the [Testing Guide](docs/TESTING-GUIDE.md) troubleshooting section
- Review domain-specific implementation summaries
- Check test files for usage examples
- See error logs: `bench --site mysite.local logs`

### Community

- **Framework:** [Frappe Framework Docs](https://frappeframework.com/docs)
- **Forum:** [Frappe Community Forum](https://discuss.frappe.io/)

---

## License

MIT

---

**For complete documentation, see [docs/README.md](docs/README.md)**
