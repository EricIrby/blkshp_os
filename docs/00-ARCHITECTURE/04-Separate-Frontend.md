# Separate Frontend Architecture (Future Reference)

**Status:** Not Currently Implemented - For Future Use  
**Current Architecture:** Desk-Only (See `01-App-Structure.md`)  
**Last Updated:** November 8, 2025

---

## ⚠️ Important Note

This document describes how to build a Frappe app with a **separate frontend** (Vue/React/SPA) when/if that becomes necessary in the future.

**BLKSHP OS currently uses a Desk-only architecture** and does not implement the patterns described here. This guide is preserved for future reference if requirements change.

### When to Use This Guide

Consider implementing a separate frontend when:
- Customer-facing portals are required
- Mobile-first experience is critical
- Modern SPA performance is needed
- Highly customized UI/UX is required
- External user access (non-employees) is needed
- Real-time collaborative features are essential

### Current Implementation

For the **current** BLKSHP OS architecture, see:
- `01-App-Structure.md` - Desk-only application structure
- `docs/README.md` - Project overview and setup
- Domain-specific documentation

---

# Frappe App Architecture Guide: Separate Frontend + Backend

> **Complete reference for building Frappe apps with a modern separate frontend (Vue/React) while maintaining backend DocTypes manageable in Frappe Desk**
> 
> Based on the architecture of Frappe Helpdesk, Frappe CRM, and other modern Frappe applications

---

## Table of Contents

1. [Overview](#overview)
2. [Complete File Structure](#complete-file-structure)
3. [Directory Explanations](#directory-explanations)
4. [Critical Configuration Files](#critical-configuration-files)
5. [Development Workflow](#development-workflow)
6. [Production Build & Deployment](#production-build--deployment)
7. [API Integration](#api-integration)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

---

## Overview

This architecture allows you to:

- ✅ Manage **system settings and DocTypes** via the standard Frappe Desk interface
- ✅ Build a **modern, separate frontend** using Vue 3, React, or any framework
- ✅ Use **Vite** for fast development with hot module replacement
- ✅ Maintain **complete control** over frontend UI/UX
- ✅ Leverage **Frappe's REST API** for backend communication
- ✅ Deploy as a **single integrated application**

### Access Points

- **Frappe Desk (Backend)**: `http://yoursite.com/app`
- **Your Frontend (SPA)**: `http://yoursite.com/your-app-route`
- **Development Frontend**: `http://yoursite.test:8080/your-app-route`

---

## Complete File Structure

```
frappe-bench/
├── apps/
│   └── your_app/                              # Your custom Frappe app
│       ├── MANIFEST.in                        # Python package manifest
│       ├── README.md                          # App documentation
│       ├── license.txt                        # License file
│       ├── requirements.txt                   # Python dependencies
│       ├── setup.py                           # Python package setup
│       ├── pyproject.toml                     # Modern Python package config (or setup.cfg)
│       │
│       ├── your_app/                          # Main Python package (same name as app)
│       │   ├── __init__.py                    # Package initialization
│       │   ├── hooks.py                       # ⭐ CRITICAL: App configuration & routing
│       │   ├── modules.txt                    # List of modules (one per line)
│       │   ├── patches.txt                    # Database migration patches
│       │   │
│       │   ├── config/                        # Desk configuration
│       │   │   ├── __init__.py
│       │   │   ├── desktop.py                 # Desk workspace icons
│       │   │   └── docs.py                    # Documentation links (optional)
│       │   │
│       │   ├── your_app/                      # Default module (auto-created)
│       │   │   └── __init__.py
│       │   │
│       │   ├── [module_name]/                 # Your custom modules (e.g., "settings", "core", "entities")
│       │   │   ├── __init__.py
│       │   │   │
│       │   │   └── doctype/                   # Backend DocTypes (manageable in Desk)
│       │   │       ├── your_settings/         # Example: System Settings DocType
│       │   │       │   ├── __init__.py
│       │   │       │   ├── your_settings.py   # Python controller
│       │   │       │   ├── your_settings.json # DocType metadata
│       │   │       │   ├── your_settings.js   # Form script (optional)
│       │   │       │   └── test_your_settings.py  # Unit tests (optional)
│       │   │       │
│       │   │       └── your_entity/           # Example: Business entity DocType
│       │   │           ├── __init__.py
│       │   │           ├── your_entity.py
│       │   │           ├── your_entity.json
│       │   │           └── your_entity.js
│       │   │
│       │   ├── api/                           # Custom API endpoints (optional but recommended)
│       │   │   ├── __init__.py
│       │   │   └── v1/
│       │   │       ├── __init__.py
│       │   │       └── endpoints.py           # Whitelisted API methods
│       │   │
│       │   ├── public/                        # Static assets (served by nginx in production)
│       │   │   ├── css/
│       │   │   ├── js/
│       │   │   └── images/
│       │   │
│       │   ├── templates/                     # Jinja templates (for portal pages, emails, etc.)
│       │   │   ├── __init__.py
│       │   │   ├── includes/                  # Reusable template parts
│       │   │   ├── pages/                     # Full page templates
│       │   │   └── emails/                    # Email templates
│       │   │
│       │   └── www/                           # ⭐ Production build output directory
│       │       ├── frontend/                  # Built frontend files (output from Vite build)
│       │       │   ├── index.html             # Main HTML file (with Jinja)
│       │       │   ├── assets/                # Built JS/CSS assets
│       │       │   │   ├── index-[hash].js
│       │       │   │   ├── index-[hash].css
│       │       │   │   └── vendor-[hash].js
│       │       │   └── favicon.ico
│       │       │
│       │       └── frontend.py                # Optional: Python controller for /frontend route
│       │
│       └── frontend/                          # ⭐ SEPARATE FRONTEND SOURCE (like helpdesk/desk)
│           ├── .gitignore                     # Frontend-specific gitignore
│           ├── package.json                   # Node dependencies & scripts
│           ├── yarn.lock                      # or package-lock.json
│           ├── vite.config.js                 # ⭐ Vite configuration
│           ├── index.html                     # Dev HTML template
│           ├── proxyOptions.js                # ⭐ Dev server proxy configuration
│           ├── .env.example                   # Environment variables template
│           │
│           ├── src/                           # Source code
│           │   ├── main.js                    # Application entry point
│           │   ├── App.vue                    # Root Vue component
│           │   ├── router.js                  # Vue Router configuration
│           │   │
│           │   ├── components/                # Reusable components
│           │   │   ├── common/
│           │   │   └── layout/
│           │   │
│           │   ├── views/                     # Page/route components
│           │   │   ├── Home.vue
│           │   │   ├── Settings.vue
│           │   │   └── Dashboard.vue
│           │   │
│           │   ├── stores/                    # State management (Pinia/Vuex)
│           │   │   └── auth.js
│           │   │
│           │   ├── composables/               # Vue composables (reusable logic)
│           │   │   └── useFrappeAPI.js
│           │   │
│           │   ├── utils/                     # Utility functions
│           │   │   ├── frappe-client.js       # ⭐ Frappe API wrapper
│           │   │   └── helpers.js
│           │   │
│           │   └── assets/                    # Frontend assets (images, styles)
│           │       ├── styles/
│           │       │   └── main.css
│           │       └── images/
│           │
│           └── public/                        # Static assets (copied as-is)
│               └── favicon.ico
│
└── sites/
    └── yoursite.test/
        └── site_config.json                   # Site-specific configuration
```

---

## Directory Explanations

### Root Level Files

#### `setup.py`
Python package setup file. Defines how your app is installed as a Python package.

```python
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="your_app",
    version="0.0.1",
    description="Your app description",
    author="Your Name",
    author_email="your@email.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
```

#### `pyproject.toml` (Modern alternative to setup.py)
```toml
[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"

[project]
name = "your_app"
authors = [{name = "Your Name", email = "your@email.com"}]
dynamic = ["version", "description"]
readme = "README.md"

[project.urls]
Home = "https://github.com/yourusername/your_app"
```

#### `MANIFEST.in`
Specifies which non-Python files to include in the package.

```
include MANIFEST.in
include requirements.txt
include *.json
include *.md
include *.py
include *.txt
recursive-include your_app *.css
recursive-include your_app *.csv
recursive-include your_app *.html
recursive-include your_app *.ico
recursive-include your_app *.js
recursive-include your_app *.json
recursive-include your_app *.md
recursive-include your_app *.png
recursive-include your_app *.py
recursive-include your_app *.svg
recursive-include your_app *.txt
recursive-exclude your_app *.pyc
```

### Backend Python Package (`your_app/`)

This directory contains all your Frappe backend code.

#### `modules.txt`
Lists all modules in your app (one per line). Each module groups related DocTypes.

```
Your App
Settings
Entities
Reports
```

#### `config/desktop.py`
Defines workspace icons shown in Frappe Desk.

```python
from frappe import _

def get_data():
    return [
        {
            "module_name": "Your App",
            "category": "Modules",
            "label": _("Your App"),
            "color": "blue",
            "icon": "octicon octicon-file-directory",
            "type": "module",
            "description": "Your app description"
        }
    ]
```

#### DocTypes Directory Structure
Each DocType lives in `your_app/[module_name]/doctype/[doctype_name]/`

**Files in a DocType folder:**
- `__init__.py` - Makes it a Python package
- `[doctype_name].py` - Python controller (business logic)
- `[doctype_name].json` - Metadata (fields, permissions, etc.)
- `[doctype_name].js` - Client-side form scripts (optional)
- `test_[doctype_name].py` - Unit tests (optional)

### Frontend Directory (`frontend/`)

This is your **separate frontend application**—completely independent source code that builds to the `www/` directory.

#### Why Separate?
- Uses modern build tools (Vite)
- Hot Module Replacement during development
- Component-based architecture
- Separate dependency management
- Can use any frontend framework (Vue, React, Svelte, etc.)

#### Source Code (`src/`)
All your frontend source code lives here. This is what you edit during development.

#### Output Directory (`../your_app/www/frontend/`)
When you run `yarn build`, Vite compiles your `src/` code and outputs production-ready files to this directory.

---

## Critical Configuration Files

### 1. `your_app/hooks.py` ⭐

This is the **most important file** for integrating your separate frontend with Frappe.

```python
from frappe import __version__ as frappe_version

# App Metadata
app_name = "your_app"
app_title = "Your App"
app_publisher = "Your Company"
app_description = "Your application description"
app_icon = "octicon octicon-file-directory"
app_color = "blue"
app_email = "contact@yourcompany.com"
app_license = "MIT"

# App version
app_version = "0.0.1"

# Required apps (dependencies)
# required_apps = ["frappe"]

# ============================================================================
# ROUTING: Map frontend routes to the built app
# ============================================================================

# Route your SPA - this tells Frappe where to serve your frontend
website_route_rules = [
    {
        "from_route": "/your-app/<path:app_path>", 
        "to_route": "frontend"
    },
]

# Alternative: Catch-all routing for SPA
# update_website_context = []

# ============================================================================
# PERMISSIONS & SECURITY
# ============================================================================

# Role-based permissions
# permission_query_conditions = {
#     "Your DocType": "your_app.permissions.get_permission_query_conditions",
# }

# has_permission = {
#     "Your DocType": "your_app.permissions.has_permission",
# }

# ============================================================================
# SCHEDULED TASKS
# ============================================================================

# Scheduled tasks (cron jobs)
# scheduler_events = {
#     "daily": [
#         "your_app.tasks.daily"
#     ],
#     "hourly": [
#         "your_app.tasks.hourly"
#     ],
# }

# ============================================================================
# API & WHITELISTED METHODS
# ============================================================================

# Custom API endpoints are defined in the files themselves using @frappe.whitelist()
# Example: your_app/api/v1/endpoints.py

# ============================================================================
# DOCUMENT EVENTS
# ============================================================================

# Document Events hooks
# doc_events = {
#     "*": {
#         "on_update": "method",
#         "on_cancel": "method",
#         "on_trash": "method"
#     }
# }

# ============================================================================
# JINJA CUSTOMIZATION
# ============================================================================

# Jinja template helpers
# jinja = {
#     "methods": "your_app.utils.jinja_methods",
#     "filters": "your_app.utils.jinja_filters"
# }

# ============================================================================
# FRAPPE DESK CUSTOMIZATION
# ============================================================================

# Override or extend standard Desk pages
# override_doctype_class = {
#     "ToDo": "custom_app.overrides.CustomToDo"
# }

# Extend standard pages
# extend_bootinfo = "your_app.boot.boot_session"

# ============================================================================
# FIXTURES (Demo/Seed Data)
# ============================================================================

# Fixtures for import/export
# fixtures = [
#     {"dt": "Custom Field", "filters": [["name", "in", ["custom_field_1", "custom_field_2"]]]},
#     {"dt": "Property Setter", "filters": [["doc_type", "=", "Your DocType"]]},
# ]

# ============================================================================
# WEBSITE / PORTAL SETTINGS
# ============================================================================

# Website settings
# website_context = {
#     "favicon": "/assets/your_app/images/favicon.png",
#     "splash_image": "/assets/your_app/images/splash.png"
# }

# Portal menu items
# portal_menu_items = [
#     {"title": "Dashboard", "route": "/your-app/dashboard", "role": "Customer"},
# ]

# ============================================================================
# INSTALLATION HOOKS
# ============================================================================

# before_install = "your_app.setup.install.before_install"
# after_install = "your_app.setup.install.after_install"
# after_sync = "your_app.setup.install.after_sync"

# ============================================================================
# DEVELOPMENT SETTINGS
# ============================================================================

# For development: Allow all CORS (remove in production!)
# This is useful when your Vite dev server runs on a different port
# allow_cors = "*"

# In production, you might want to specify allowed origins:
# allow_cors = ["https://yourdomain.com"]
```

### 2. `frontend/vite.config.js` ⭐

```javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import proxyOptions from './proxyOptions'

export default defineConfig({
  plugins: [vue()],
  
  server: {
    port: 8080,
    proxy: proxyOptions.proxyOptions,
    // Host configuration - allows access from yoursite.test domain
    host: true,
  },
  
  build: {
    // ⭐ CRITICAL: Output to Frappe's www directory
    outDir: '../your_app/www/frontend',
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      output: {
        // Optional: Customize chunk naming
        manualChunks: {
          'vendor': ['vue', 'vue-router'],
        }
      }
    }
  },
  
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  
  // Important for Frappe UI library compatibility
  optimizeDeps: {
    include: [
      'frappe-ui > feather-icons',
      'frappe-ui > sortablejs'
    ]
  }
})
```

### 3. `frontend/proxyOptions.js` ⭐

This file configures the dev server to proxy API requests to your Frappe backend.

```javascript
// Read the webserver port from Frappe's configuration
const common_site_config = require('../../../sites/common_site_config.json');
const { webserver_port } = common_site_config;

export default {
  proxyOptions: {
    // Proxy API and asset requests to Frappe backend
    '^/(app|api|assets|files|private)': {
      target: `http://localhost:${webserver_port}`,
      ws: true,  // Enable WebSocket proxying (for realtime)
      router: function (req) {
        // Multi-site support: route to correct site based on hostname
        const site_name = req.headers.host.split(':')[0];
        return `http://${site_name}:${webserver_port}`;
      }
    }
  }
}
```

### 4. `frontend/package.json`

```json
{
  "name": "your-app-frontend",
  "version": "0.0.1",
  "private": true,
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src --ext .vue,.js"
  },
  "dependencies": {
    "vue": "^3.3.0",
    "vue-router": "^4.2.0",
    "frappe-ui": "^0.1.0",
    "pinia": "^2.1.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.5.0",
    "vite": "^5.0.0",
    "eslint": "^8.0.0",
    "eslint-plugin-vue": "^9.0.0"
  }
}
```

### 5. `your_app/www/frontend/index.html` ⭐

This is the **production entry point**. It includes Jinja templating for Frappe integration.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title or "Your App" }}</title>
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/assets/your_app/images/favicon.ico">
    
    <!-- In production, these will be replaced by Vite's built assets -->
    {% if not in_dev_mode %}
    <!-- Vite injects the built asset links here during build -->
    <script type="module" crossorigin src="/assets/your_app/frontend/assets/index-[hash].js"></script>
    <link rel="stylesheet" href="/assets/your_app/frontend/assets/index-[hash].css">
    {% endif %}
</head>
<body>
    <div id="app"></div>
    
    <!-- Provide CSRF token to frontend -->
    <script>
        window.csrf_token = "{{ frappe.session.csrf_token }}";
        window.site_name = "{{ frappe.local.site }}";
    </script>
    
    <!-- In development mode, Vite dev server handles loading -->
</body>
</html>
```

### 6. `your_app/www/frontend.py` (Optional)

Python controller for the `/frontend` route. Useful for authentication checks.

```python
import frappe

def get_context(context):
    """
    This method is called when /frontend route is accessed.
    You can add authentication checks, context data, etc.
    """
    context.no_cache = 1
    
    # Optional: Require login
    # if frappe.session.user == "Guest":
    #     frappe.throw("Please login to continue", frappe.PermissionError)
    
    # Add custom context
    context.user = frappe.session.user
    context.in_dev_mode = frappe.conf.developer_mode
    
    return context
```

### 7. `sites/yoursite.test/site_config.json`

Development configuration to prevent CSRF errors with Vite dev server.

```json
{
  "db_name": "your_database",
  "db_password": "your_password",
  "developer_mode": 1,
  "ignore_csrf": 1,
  "disable_website_cache": 1
}
```

**⚠️ SECURITY WARNING**: Remove `ignore_csrf` in production!

---

## Development Workflow

### Initial Setup

1. **Create your Frappe app**
   ```bash
   cd frappe-bench
   bench new-app your_app
   ```

2. **Install on a site**
   ```bash
   bench --site yoursite.test install-app your_app
   ```

3. **Set up the frontend directory**
   ```bash
   cd apps/your_app
   mkdir frontend
   cd frontend
   
   # Initialize with Vite + Vue
   npm create vite@latest . -- --template vue
   
   # Or use a Frappe-specific starter
   npx degit NagariaHussain/doppio_frappeui_starter .
   ```

4. **Install frontend dependencies**
   ```bash
   yarn install
   # or: npm install
   ```

5. **Configure hooks.py** (as shown above)

6. **Add site config for development**
   Edit `sites/yoursite.test/site_config.json` and add:
   ```json
   {
     "ignore_csrf": 1
   }
   ```

### Daily Development

**Terminal 1: Start Frappe Backend**
```bash
cd frappe-bench
bench start
```
This runs on `http://yoursite.test:8000`

**Terminal 2: Start Frontend Dev Server**
```bash
cd frappe-bench/apps/your_app/frontend
yarn dev
# or with specific host: yarn dev --host yoursite.test
```
This runs on `http://yoursite.test:8080`

### Access Points During Development

- **Frappe Desk**: `http://yoursite.test:8000/app`
- **Your Frontend (Dev Server)**: `http://yoursite.test:8080/frontend`
- **API Endpoint**: `http://yoursite.test:8000/api/resource/Your DocType`

### Hot Reload

- **Backend changes**: Frappe auto-reloads when you modify Python files
- **Frontend changes**: Vite provides instant hot module replacement (HMR)

---

## Production Build & Deployment

### 1. Build the Frontend

```bash
cd frappe-bench/apps/your_app/frontend
yarn build
```

This command:
- Compiles and optimizes your source code
- Minifies JavaScript and CSS
- Generates hashed filenames for cache-busting
- Outputs everything to `your_app/www/frontend/`

### 2. Update index.html Asset References

After building, you need to update `www/frontend/index.html` with the correct asset paths:

```html
<!-- Update these paths with actual hash values from build output -->
<script type="module" crossorigin src="/assets/your_app/frontend/assets/index-abc123.js"></script>
<link rel="stylesheet" href="/assets/your_app/frontend/assets/index-xyz789.css">
```

**Tip**: You can automate this with a post-build script.

### 3. Build Frappe Assets

```bash
cd frappe-bench
bench build --app your_app
```

### 4. Clear Cache & Restart

```bash
bench --site yoursite.com clear-cache
bench restart
```

### 5. Access in Production

- **Frontend**: `http://yoursite.com/frontend`
- **Desk**: `http://yoursite.com/app`

### Production Deployment Checklist

- [ ] Remove `ignore_csrf: 1` from `site_config.json`
- [ ] Set `allow_cors` appropriately in `hooks.py` (or remove it)
- [ ] Build frontend: `yarn build`
- [ ] Update asset paths in `www/frontend/index.html`
- [ ] Build Frappe assets: `bench build`
- [ ] Clear cache: `bench clear-cache`
- [ ] Restart: `bench restart`
- [ ] Configure nginx (if not using Frappe Cloud)
- [ ] Enable SSL/HTTPS
- [ ] Test authentication flow
- [ ] Test API endpoints

---

## API Integration

### Frontend API Client

Create a reusable API client in `frontend/src/utils/frappe-client.js`:

```javascript
class FrappeAPI {
  constructor() {
    this.baseURL = window.location.origin;
    this.csrf_token = window.csrf_token;
  }

  async call(method, args = {}) {
    const url = `${this.baseURL}/api/method/${method}`;
    
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': this.csrf_token,
      },
      body: JSON.stringify(args),
    });

    if (!response.ok) {
      throw new Error(`API call failed: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (data.exc) {
      throw new Error(data.exc);
    }

    return data.message;
  }

  async getDoc(doctype, name) {
    return this.call('frappe.client.get', {
      doctype,
      name,
    });
  }

  async getList(doctype, fields = ['name'], filters = {}, limit = 20) {
    return this.call('frappe.client.get_list', {
      doctype,
      fields,
      filters,
      limit_page_length: limit,
    });
  }

  async insert(doc) {
    return this.call('frappe.client.insert', { doc });
  }

  async setValue(doctype, name, fieldname, value) {
    return this.call('frappe.client.set_value', {
      doctype,
      name,
      fieldname,
      value,
    });
  }

  async delete(doctype, name) {
    return this.call('frappe.client.delete', {
      doctype,
      name,
    });
  }
}

export const frappeAPI = new FrappeAPI();
```

### Using the API Client in Components

```vue
<template>
  <div>
    <h1>My Entities</h1>
    <ul>
      <li v-for="entity in entities" :key="entity.name">
        {{ entity.name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { frappeAPI } from '@/utils/frappe-client';

const entities = ref([]);

onMounted(async () => {
  try {
    entities.value = await frappeAPI.getList('Your Entity', ['name', 'title']);
  } catch (error) {
    console.error('Failed to load entities:', error);
  }
});
</script>
```

### Custom Whitelisted Methods

In `your_app/api/v1/endpoints.py`:

```python
import frappe

@frappe.whitelist()
def get_dashboard_data():
    """
    Custom API endpoint accessible at:
    POST /api/method/your_app.api.v1.endpoints.get_dashboard_data
    """
    user = frappe.session.user
    
    # Your custom logic
    data = {
        "total_entities": frappe.db.count("Your Entity"),
        "user_entities": frappe.db.count("Your Entity", {"owner": user}),
    }
    
    return data

@frappe.whitelist()
def create_custom_entity(title, description):
    """
    Create entity with custom logic
    """
    doc = frappe.get_doc({
        "doctype": "Your Entity",
        "title": title,
        "description": description,
    })
    doc.insert()
    frappe.db.commit()
    
    return doc.as_dict()
```

Call from frontend:

```javascript
const data = await frappeAPI.call('your_app.api.v1.endpoints.get_dashboard_data');
```

---

## Best Practices

### 1. Directory Organization

✅ **Do:**
- Keep backend code in `your_app/` (Python package)
- Keep frontend code in `frontend/` (separate source)
- Use modules to organize related DocTypes
- Group API endpoints in `api/` directory

❌ **Don't:**
- Mix frontend source code with build output
- Put business logic in frontend
- Store sensitive data in frontend code

### 2. State Management

✅ **Do:**
- Use Pinia or Vuex for global state
- Cache frequently accessed data
- Implement optimistic updates where appropriate

❌ **Don't:**
- Fetch same data multiple times
- Store everything in global state
- Ignore loading and error states

### 3. Authentication

✅ **Do:**
- Rely on Frappe's session management
- Check `frappe.session.user` on backend
- Handle "Guest" user appropriately
- Use CSRF tokens for all mutations

❌ **Don't:**
- Store passwords in frontend
- Implement custom authentication
- Bypass Frappe's permission system

### 4. Performance

✅ **Do:**
- Lazy-load routes and components
- Use Vite's code-splitting
- Implement pagination for large lists
- Optimize images and assets

❌ **Don't:**
- Load all data at once
- Import entire libraries when you need one function
- Ignore bundle size

### 5. Development

✅ **Do:**
- Use `bench start` for backend
- Use Vite dev server for frontend HMR
- Write unit tests for business logic
- Document your API endpoints

❌ **Don't:**
- Build frontend for every small change
- Commit `node_modules/` or `www/frontend/assets/`
- Skip error handling

### 6. Version Control

**`.gitignore` for app root:**
```gitignore
# Python
*.pyc
__pycache__/
*.egg-info/

# Frontend build output
your_app/www/frontend/assets/
your_app/www/frontend/*.js
your_app/www/frontend/*.css

# But keep index.html
!your_app/www/frontend/index.html

# Node modules
frontend/node_modules/
frontend/.vite/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

---

## Troubleshooting

### Problem: CSRF Token Errors in Development

**Error:** `CSRF Token Missing` or `Invalid CSRF Token`

**Solution:**
Add to `sites/yoursite.test/site_config.json`:
```json
{
  "ignore_csrf": 1
}
```

**⚠️ Important:** Remove this in production!

### Problem: 404 on Frontend Route

**Error:** Accessing `/frontend` returns 404

**Solutions:**
1. Check `hooks.py` has `website_route_rules` configured
2. Restart bench: `bench restart`
3. Clear cache: `bench --site yoursite.test clear-cache`
4. Verify `www/frontend/index.html` exists

### Problem: Vite Dev Server Can't Proxy to Frappe

**Error:** Proxy errors or "Connection refused"

**Solutions:**
1. Ensure `bench start` is running
2. Check `proxyOptions.js` has correct port
3. Verify `common_site_config.json` exists
4. Check your `/etc/hosts` file includes site mapping

### Problem: Assets Not Loading in Production

**Error:** Blank page or 404 on JS/CSS files

**Solutions:**
1. Rebuild frontend: `cd frontend && yarn build`
2. Update asset paths in `www/frontend/index.html`
3. Build Frappe assets: `bench build --app your_app`
4. Clear cache: `bench clear-cache`
5. Check nginx configuration (if applicable)

### Problem: Changes Not Reflecting

**For Backend Changes:**
```bash
bench restart
bench --site yoursite.test clear-cache
```

**For Frontend Changes:**
- If dev server is running: Should auto-reload
- If not: Rebuild with `yarn build`

### Problem: Module Import Errors

**Error:** `ModuleNotFoundError` or `Cannot find module`

**Solutions:**

For Python:
```bash
cd frappe-bench
bench restart
```

For JavaScript:
```bash
cd apps/your_app/frontend
rm -rf node_modules package-lock.json
yarn install
```

### Problem: API Calls Failing

**Error:** 403, 401, or CORS errors

**Solutions:**
1. Check user is logged in: `frappe.session.user != "Guest"`
2. Verify method is `@frappe.whitelist()` decorated
3. Check permissions on DocType
4. Include CSRF token in requests
5. Verify `allow_cors` setting in `hooks.py` (dev only)

### Problem: Realtime/WebSocket Not Working

**Solutions:**
1. Ensure `socketio_port` is set in `common_site_config.json`
2. Check proxy configuration includes `ws: true`
3. Verify Frappe realtime service is running (`bench start` starts it)

---

## Additional Resources

### Official Documentation
- [Frappe Framework Docs](https://frappeframework.com/docs)
- [Frappe API Reference](https://frappeframework.com/docs/user/en/api)
- [Vite Documentation](https://vitejs.dev/)

### Example Apps Using This Architecture
- [Frappe Helpdesk](https://github.com/frappe/helpdesk) - Support ticket system
- [Frappe CRM](https://github.com/frappe/crm) - Customer relationship management
- [Frappe HRMS](https://github.com/frappe/hrms) - HR management system

### Tools & Libraries
- [Frappe UI](https://github.com/frappe/frappe-ui) - Vue component library for Frappe apps
- [Doppio](https://github.com/NagariaHussain/doppio) - CLI tool for setting up SPAs in Frappe apps
- [frappe-react-sdk](https://github.com/nikkothari22/frappe-react-sdk) - React hooks for Frappe

---

## Appendix: File Checklist

Use this checklist to verify your app structure:

### Backend Structure
- [ ] `setup.py` or `pyproject.toml` exists
- [ ] `MANIFEST.in` includes all necessary file types
- [ ] `your_app/hooks.py` has `website_route_rules` configured
- [ ] `your_app/modules.txt` lists all modules
- [ ] `your_app/config/desktop.py` defines Desk icons
- [ ] DocTypes are in `your_app/[module]/doctype/[doctype_name]/`
- [ ] API endpoints in `your_app/api/` use `@frappe.whitelist()`
- [ ] `your_app/www/frontend/index.html` exists with Jinja template

### Frontend Structure
- [ ] `frontend/package.json` exists with correct scripts
- [ ] `frontend/vite.config.js` has `outDir: '../your_app/www/frontend'`
- [ ] `frontend/proxyOptions.js` configured correctly
- [ ] `frontend/src/main.js` is the entry point
- [ ] `frontend/src/router.js` defines routes
- [ ] API client utility exists (e.g., `frappe-client.js`)
- [ ] `.gitignore` excludes `node_modules/` and build output

### Configuration
- [ ] `sites/yoursite.test/site_config.json` has dev settings
- [ ] `hooks.py` routing points to correct `www/` directory
- [ ] CSRF token is passed to frontend
- [ ] Proxy configuration matches Frappe port

### Development Workflow
- [ ] Can run `bench start` successfully
- [ ] Can run `yarn dev` in frontend directory
- [ ] Frontend dev server proxies to Frappe backend
- [ ] Changes hot-reload in development
- [ ] Can access Desk at `/app`
- [ ] Can access frontend at configured route

### Production Build
- [ ] `yarn build` completes without errors
- [ ] Build outputs to `www/frontend/`
- [ ] Asset paths in `index.html` are correct
- [ ] `bench build` completes successfully
- [ ] Production site serves frontend correctly
- [ ] No CSRF errors in production
- [ ] API calls work in production

---

**Last Updated:** November 2025  
**Compatible with:** Frappe Framework v15+  
**Example Apps:** Frappe Helpdesk, Frappe CRM

For issues or questions, refer to the [Frappe Forum](https://discuss.frappe.io/)