# Frappe to FastAPI Porting Guide

**Purpose:** Practical guide for migrating BLKSHP OS from Frappe Framework to FastAPI
**Audience:** Developers familiar with Frappe, learning FastAPI
**Timeline:** Reference for Phase 2 (after MVP approval)

---

## Overview

This guide shows how to port Frappe Framework code to FastAPI, with side-by-side examples from the BLKSHP OS codebase.

**What You're Porting:**
- ~40-50% of business logic can be directly adapted
- Database schema concepts transfer (with syntax changes)
- Permission rules need redesigning but concepts transfer
- API endpoint patterns similar (different decorators)

**What's New:**
- Async Python patterns (`async`/`await`)
- SQLAlchemy 2.0 ORM (vs Frappe ORM)
- Pydantic for validation (vs Frappe's built-in validation)
- Custom RBAC system (vs Frappe's DocType permissions)

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Database Models](#database-models)
3. [API Endpoints](#api-endpoints)
4. [Validation](#validation)
5. [Permissions](#permissions)
6. [Business Logic](#business-logic)
7. [Queries & Filtering](#queries--filtering)
8. [File Handling](#file-handling)
9. [Background Jobs](#background-jobs)
10. [Testing](#testing)

---

## Project Structure

### Frappe Structure
```
blkshp_os/
├── blkshp_os/
│   ├── products/
│   │   └── doctype/
│   │       └── product/
│   │           ├── product.json      # DocType definition
│   │           ├── product.py        # Controller
│   │           └── product.js        # Form script
│   ├── api/
│   │   ├── inventory.py              # Whitelisted methods
│   │   └── auth.py
│   └── hooks.py                      # App hooks
```

### FastAPI Structure
```
blkshp-platform/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   ├── product.py            # SQLAlchemy models
│   │   │   ├── inventory.py
│   │   │   └── base.py
│   │   ├── schemas/
│   │   │   ├── product.py            # Pydantic schemas
│   │   │   └── inventory.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── products.py       # FastAPI routes
│   │   │   │   ├── inventory.py
│   │   │   │   └── auth.py
│   │   │   └── dependencies.py       # Auth, permissions
│   │   ├── services/
│   │   │   ├── product_service.py    # Business logic
│   │   │   └── rbac_service.py
│   │   ├── core/
│   │   │   ├── config.py             # Settings
│   │   │   ├── database.py           # DB session
│   │   │   └── security.py           # Auth helpers
│   │   └── main.py                   # FastAPI app
│   ├── alembic/                      # Migrations
│   └── tests/
├── frontend/                         # Next.js (separate)
└── docker-compose.yml
```

---

## Database Models

### Frappe: DocType (JSON + Python)

**product.json:**
```json
{
  "doctype": "DocType",
  "name": "Product",
  "fields": [
    {
      "fieldname": "product_code",
      "fieldtype": "Data",
      "label": "Product Code",
      "reqd": 1,
      "unique": 1
    },
    {
      "fieldname": "product_name",
      "fieldtype": "Data",
      "label": "Product Name",
      "reqd": 1
    },
    {
      "fieldname": "category",
      "fieldtype": "Link",
      "options": "Product Category",
      "label": "Category"
    },
    {
      "fieldname": "primary_unit",
      "fieldtype": "Link",
      "options": "Unit of Measure",
      "label": "Primary Unit",
      "reqd": 1
    },
    {
      "fieldname": "valuation_rate",
      "fieldtype": "Currency",
      "label": "Valuation Rate"
    }
  ]
}
```

**product.py (Frappe Controller):**
```python
import frappe
from frappe.model.document import Document

class Product(Document):
    def validate(self):
        """Validation before save"""
        if not self.product_code:
            frappe.throw("Product Code is required")

        # Auto-generate code if not provided
        if not self.product_code:
            self.product_code = self.generate_product_code()

    def before_save(self):
        """Before save hook"""
        self.product_name = self.product_name.strip().title()

    def on_update(self):
        """After save hook"""
        frappe.publish_realtime("product_updated", {"product": self.name})

    def generate_product_code(self):
        """Business logic method"""
        # Get last product code
        last_code = frappe.db.get_value(
            "Product",
            filters={},
            fieldname="product_code",
            order_by="creation desc"
        )
        # Generate new code
        if last_code:
            num = int(last_code.split("-")[1]) + 1
            return f"PROD-{num:05d}"
        return "PROD-00001"
```

### FastAPI: SQLAlchemy 2.0 + Pydantic

**models/product.py (SQLAlchemy):**
```python
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

from app.models.base import Base, TimestampMixin

class Product(Base, TimestampMixin):
    """Product model - SQLAlchemy ORM"""
    __tablename__ = "products"
    __table_args__ = {"schema": "tenant_acme"}  # Multi-tenancy

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Fields
    product_code: Mapped[str] = mapped_column(
        String(50), unique=True, index=True
    )
    product_name: Mapped[str] = mapped_column(String(255))
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("tenant_acme.product_categories.id")
    )
    primary_unit_id: Mapped[int] = mapped_column(
        ForeignKey("tenant_acme.units_of_measure.id")
    )
    valuation_rate: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(15, 2)
    )

    # Relationships
    category: Mapped[Optional["ProductCategory"]] = relationship()
    primary_unit: Mapped["UnitOfMeasure"] = relationship()
    departments: Mapped[list["ProductDepartment"]] = relationship(
        back_populates="product"
    )

    def __repr__(self):
        return f"<Product {self.product_code}: {self.product_name}>"
```

**schemas/product.py (Pydantic):**
```python
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal
from datetime import datetime
from typing import Optional

class ProductBase(BaseModel):
    """Base product schema"""
    product_code: str = Field(min_length=1, max_length=50)
    product_name: str = Field(min_length=1, max_length=255)
    category_id: Optional[int] = None
    primary_unit_id: int
    valuation_rate: Optional[Decimal] = None

    @field_validator('product_name')
    @classmethod
    def title_case_name(cls, v: str) -> str:
        """Validation: title case the name"""
        return v.strip().title()

class ProductCreate(ProductBase):
    """Schema for creating product"""
    pass

class ProductUpdate(BaseModel):
    """Schema for updating product (all optional)"""
    product_code: Optional[str] = None
    product_name: Optional[str] = None
    category_id: Optional[int] = None
    primary_unit_id: Optional[int] = None
    valuation_rate: Optional[Decimal] = None

class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # ORM mode
```

**services/product_service.py (Business Logic):**
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductService:
    """Business logic for products"""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def generate_product_code(self) -> str:
        """Generate next product code"""
        # Get last product code
        result = await self.session.execute(
            select(Product.product_code)
            .order_by(Product.created_at.desc())
            .limit(1)
        )
        last_code = result.scalar_one_or_none()

        if last_code:
            num = int(last_code.split("-")[1]) + 1
            return f"PROD-{num:05d}"
        return "PROD-00001"

    async def create_product(
        self, product_data: ProductCreate
    ) -> Product:
        """Create new product"""
        # Auto-generate code if not provided
        if not product_data.product_code:
            product_data.product_code = await self.generate_product_code()

        # Create product
        product = Product(**product_data.model_dump())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)

        # Emit event (optional - use WebSocket/SSE)
        # await notify_product_update(product.id)

        return product

    async def update_product(
        self, product_id: int, product_data: ProductUpdate
    ) -> Product:
        """Update existing product"""
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalar_one_or_none()

        if not product:
            raise ValueError(f"Product {product_id} not found")

        # Update fields
        for key, value in product_data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        await self.session.commit()
        await self.session.refresh(product)
        return product
```

---

## API Endpoints

### Frappe: @frappe.whitelist()

**api/inventory.py:**
```python
import frappe
from typing import List, Dict, Any

@frappe.whitelist()
def get_product(product_id: str) -> Dict[str, Any]:
    """Get single product"""
    product = frappe.get_doc("Product", product_id)

    # Check permissions
    if not frappe.has_permission("Product", "read", product):
        frappe.throw("No permission", frappe.PermissionError)

    return product.as_dict()

@frappe.whitelist()
def list_products(
    filters: Dict[str, Any] | None = None,
    limit: int = 20,
    offset: int = 0
) -> List[Dict[str, Any]]:
    """List products with filters"""
    products = frappe.get_list(
        "Product",
        filters=filters or {},
        fields=["*"],
        limit_page_length=limit,
        limit_start=offset,
        order_by="product_name asc"
    )
    return products

@frappe.whitelist(methods=["POST"])
def create_product(product_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create new product"""
    # Check permissions
    if not frappe.has_permission("Product", "create"):
        frappe.throw("No permission", frappe.PermissionError)

    # Create product
    product = frappe.get_doc({
        "doctype": "Product",
        **product_data
    })
    product.insert()
    frappe.db.commit()

    return product.as_dict()
```

### FastAPI: @router.get/post/etc

**api/routes/products.py:**
```python
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.api.dependencies import (
    get_db,
    get_current_user,
    require_permission
)
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService
from app.services.rbac_service import RBACService

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """Get single product"""
    # Get product
    result = await session.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check permissions
    rbac = RBACService(session)
    has_permission = await rbac.check_permission(
        user["id"], "products", "read", product_id
    )
    if not has_permission:
        raise HTTPException(status_code=403, detail="Permission denied")

    return product

@router.get("/", response_model=List[ProductResponse])
async def list_products(
    category_id: int | None = Query(None),
    search: str | None = Query(None),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """List products with filters"""
    # Build query
    query = select(Product)

    # Apply filters
    if category_id:
        query = query.where(Product.category_id == category_id)

    if search:
        query = query.where(
            Product.product_name.ilike(f"%{search}%") |
            Product.product_code.ilike(f"%{search}%")
        )

    # Apply permission filtering
    rbac = RBACService(session)
    query = await rbac.filter_query_by_permissions(
        query, user["id"], "products"
    )

    # Apply pagination
    query = query.limit(limit).offset(offset).order_by(Product.product_name)

    # Execute
    result = await session.execute(query)
    products = result.scalars().all()

    return products

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_data: ProductCreate,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(require_permission("products", "create"))
):
    """Create new product"""
    service = ProductService(session)

    try:
        product = await service.create_product(product_data)
        return product
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(require_permission("products", "update"))
):
    """Update existing product"""
    service = ProductService(session)

    try:
        product = await service.update_product(product_id, product_data)
        return product
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    session: AsyncSession = Depends(get_db),
    user: dict = Depends(require_permission("products", "delete"))
):
    """Delete product"""
    result = await session.execute(
        select(Product).where(Product.id == product_id)
    )
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await session.delete(product)
    await session.commit()
```

---

## Validation

### Frappe: validate() method

```python
class Product(Document):
    def validate(self):
        # Required field check
        if not self.product_code:
            frappe.throw("Product Code is required")

        # Custom validation
        if self.valuation_rate and self.valuation_rate < 0:
            frappe.throw("Valuation rate cannot be negative")

        # Unique check
        if frappe.db.exists("Product", {
            "product_code": self.product_code,
            "name": ["!=", self.name]
        }):
            frappe.throw(f"Product code {self.product_code} already exists")

        # Link validation
        if self.category and not frappe.db.exists("Product Category", self.category):
            frappe.throw(f"Category {self.category} does not exist")
```

### FastAPI: Pydantic validators

```python
from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from decimal import Decimal

class ProductCreate(BaseModel):
    product_code: str = Field(min_length=1, max_length=50)
    product_name: str = Field(min_length=1, max_length=255)
    category_id: Optional[int] = None
    valuation_rate: Optional[Decimal] = Field(None, ge=0)

    @field_validator('valuation_rate')
    @classmethod
    def validate_valuation_rate(cls, v: Optional[Decimal]) -> Optional[Decimal]:
        """Ensure valuation rate is not negative"""
        if v is not None and v < 0:
            raise ValueError("Valuation rate cannot be negative")
        return v

    @model_validator(mode='after')
    def validate_product(self):
        """Model-level validation"""
        # Add any cross-field validation here
        return self

# In the route/service, check uniqueness:
async def create_product(product_data: ProductCreate, session: AsyncSession):
    # Check if product code exists
    result = await session.execute(
        select(Product).where(Product.product_code == product_data.product_code)
    )
    if result.scalar_one_or_none():
        raise ValueError(f"Product code {product_data.product_code} already exists")

    # Check if category exists
    if product_data.category_id:
        result = await session.execute(
            select(ProductCategory).where(ProductCategory.id == product_data.category_id)
        )
        if not result.scalar_one_or_none():
            raise ValueError(f"Category {product_data.category_id} does not exist")

    # Create product...
```

---

## Permissions

### Frappe: has_permission()

**Permission rules in product.py:**
```python
def has_permission(doc, ptype, user):
    """Custom permission logic"""
    # Allow if user has Product Manager role
    if "Product Manager" in frappe.get_roles(user):
        return True

    # Check department access
    user_departments = frappe.get_all(
        "Department Access",
        filters={"user": user},
        pluck="department"
    )

    # Check if product is in user's departments
    product_departments = frappe.get_all(
        "Product Department",
        filters={"parent": doc.name},
        pluck="department"
    )

    return bool(set(user_departments) & set(product_departments))
```

### FastAPI: Custom RBAC Service

**services/rbac_service.py:**
```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from typing import Any

from app.models.rbac import Role, Permission, UserRole, DepartmentAccess
from app.models.product import Product

class RBACService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_permission(
        self,
        user_id: str,
        resource: str,
        action: str,
        resource_id: int | None = None,
        context: dict | None = None
    ) -> bool:
        """Check if user has permission"""
        # Get user's roles
        result = await self.session.execute(
            select(UserRole).where(UserRole.user_id == user_id)
        )
        user_roles = result.scalars().all()

        # Get permissions for those roles
        role_ids = [ur.role_id for ur in user_roles]
        result = await self.session.execute(
            select(Permission)
            .join(RolePermission)
            .where(RolePermission.role_id.in_(role_ids))
            .where(Permission.resource == resource)
            .where(Permission.action == action)
        )
        permissions = result.scalars().all()

        if not permissions:
            return False

        # If resource_id provided, check department/company access
        if resource_id:
            return await self._check_resource_access(
                user_id, resource, resource_id, permissions
            )

        return True

    async def _check_resource_access(
        self,
        user_id: str,
        resource: str,
        resource_id: int,
        permissions: list[Permission]
    ) -> bool:
        """Check if user has access to specific resource"""
        # Get user's department access
        result = await self.session.execute(
            select(DepartmentAccess.department_id)
            .where(DepartmentAccess.user_id == user_id)
        )
        user_departments = [row[0] for row in result.all()]

        if resource == "products":
            # Get product's departments
            result = await self.session.execute(
                select(ProductDepartment.department_id)
                .where(ProductDepartment.product_id == resource_id)
            )
            product_departments = [row[0] for row in result.all()]

            # Check overlap
            return bool(set(user_departments) & set(product_departments))

        return True

    async def filter_query_by_permissions(
        self,
        query: Select,
        user_id: str,
        resource: str
    ) -> Select:
        """Apply permission filters to query"""
        # Get user's departments
        result = await self.session.execute(
            select(DepartmentAccess.department_id)
            .where(DepartmentAccess.user_id == user_id)
        )
        user_departments = [row[0] for row in result.all()]

        if resource == "products" and user_departments:
            # Filter products by departments user has access to
            query = query.join(ProductDepartment).where(
                ProductDepartment.department_id.in_(user_departments)
            )

        return query
```

**api/dependencies.py:**
```python
from fastapi import Depends, HTTPException, Header
from clerk_backend_api import Clerk
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.services.rbac_service import RBACService

clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)

async def get_current_user(
    authorization: str = Header(..., alias="Authorization")
) -> dict:
    """Get current user from Clerk token"""
    token = authorization.replace("Bearer ", "")

    try:
        session = await clerk.sessions.verify_session(token)
        return session.user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_permission(resource: str, action: str):
    """Dependency factory for permission checking"""
    async def permission_checker(
        user: dict = Depends(get_current_user),
        session: AsyncSession = Depends(get_db)
    ):
        rbac = RBACService(session)
        has_permission = await rbac.check_permission(
            user["id"], resource, action
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return permission_checker
```

---

## Queries & Filtering

### Frappe: frappe.get_list() / frappe.db.get_all()

```python
# Simple query
products = frappe.get_list(
    "Product",
    filters={"category": "Vegetables"},
    fields=["product_code", "product_name", "valuation_rate"],
    order_by="product_name asc",
    limit_page_length=20
)

# Complex query with joins
products_with_departments = frappe.db.sql("""
    SELECT
        p.product_code,
        p.product_name,
        GROUP_CONCAT(pd.department) as departments
    FROM `tabProduct` p
    LEFT JOIN `tabProduct Department` pd ON pd.parent = p.name
    WHERE p.category = %(category)s
    GROUP BY p.name
    ORDER BY p.product_name
""", {"category": "Vegetables"}, as_dict=True)

# Using ORM with filters
products = frappe.get_all(
    "Product",
    filters=[
        ["category", "=", "Vegetables"],
        ["valuation_rate", ">", 10]
    ],
    or_filters=[
        ["product_name", "like", "%tomato%"],
        ["product_code", "like", "%tomato%"]
    ]
)
```

### FastAPI: SQLAlchemy queries

```python
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload

# Simple query
result = await session.execute(
    select(Product)
    .where(Product.category_id == category_id)
    .order_by(Product.product_name)
    .limit(20)
)
products = result.scalars().all()

# Complex query with joins
result = await session.execute(
    select(
        Product.product_code,
        Product.product_name,
        func.group_concat(ProductDepartment.department_id).label("departments")
    )
    .outerjoin(ProductDepartment)
    .where(Product.category_id == category_id)
    .group_by(Product.id)
    .order_by(Product.product_name)
)
products = result.all()

# Eager loading relationships
result = await session.execute(
    select(Product)
    .options(selectinload(Product.departments))
    .where(Product.category_id == category_id)
)
products = result.scalars().all()

# Multiple filters with AND/OR
result = await session.execute(
    select(Product)
    .where(
        and_(
            Product.category_id == category_id,
            Product.valuation_rate > 10,
            or_(
                Product.product_name.ilike("%tomato%"),
                Product.product_code.ilike("%tomato%")
            )
        )
    )
)
products = result.scalars().all()
```

---

## Background Jobs

### Frappe: frappe.enqueue()

```python
import frappe

def process_inventory_audit(audit_id):
    """Background job to close audit"""
    audit = frappe.get_doc("Inventory Audit", audit_id)
    audit.close_audit()
    frappe.db.commit()

# Enqueue the job
frappe.enqueue(
    process_inventory_audit,
    audit_id="AUDIT-001",
    queue="long",  # short, long, default
    timeout=300,
    is_async=True
)
```

### FastAPI: BullMQ (via arq or similar)

```python
from bullmq import Queue, Worker
import asyncio

# Define queue
inventory_queue = Queue("inventory")

# Enqueue job
async def enqueue_audit_close(audit_id: str):
    await inventory_queue.add(
        "close_audit",
        {"audit_id": audit_id},
        opts={"timeout": 300000}  # 5 minutes
    )

# Worker definition
async def close_audit_job(job):
    """Background job to close audit"""
    audit_id = job.data["audit_id"]

    async with get_async_session() as session:
        service = InventoryAuditService(session)
        await service.close_audit(audit_id)

    return {"status": "completed"}

# Worker
worker = Worker("inventory", close_audit_job)
```

---

## Testing

### Frappe: unittest

```python
import frappe
from frappe.tests.utils import FrappeTestCase

class TestProduct(FrappeTestCase):
    def setUp(self):
        # Create test data
        self.product = frappe.get_doc({
            "doctype": "Product",
            "product_code": "TEST-001",
            "product_name": "Test Product",
            "primary_unit": "Each"
        }).insert()

    def tearDown(self):
        frappe.delete_doc("Product", self.product.name)

    def test_create_product(self):
        self.assertEqual(self.product.product_code, "TEST-001")

    def test_validation(self):
        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc({
                "doctype": "Product",
                "product_name": "Invalid Product"
                # Missing required field: product_code
            }).insert()
```

### FastAPI: pytest + httpx

```python
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.product import Product
from tests.utils import create_test_user, get_test_token

@pytest.mark.asyncio
async def test_create_product(
    async_client: AsyncClient,
    async_session: AsyncSession,
    test_user: dict
):
    """Test product creation"""
    token = await get_test_token(test_user)

    response = await async_client.post(
        "/products/",
        json={
            "product_code": "TEST-001",
            "product_name": "Test Product",
            "primary_unit_id": 1
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["product_code"] == "TEST-001"

    # Verify in database
    result = await async_session.execute(
        select(Product).where(Product.product_code == "TEST-001")
    )
    product = result.scalar_one()
    assert product.product_name == "Test Product"

@pytest.mark.asyncio
async def test_validation_error(
    async_client: AsyncClient,
    test_user: dict
):
    """Test validation errors"""
    token = await get_test_token(test_user)

    response = await async_client.post(
        "/products/",
        json={
            "product_name": "Invalid Product"
            # Missing required field: product_code, primary_unit_id
        },
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 422  # Validation error
    assert "product_code" in response.json()["detail"][0]["loc"]
```

---

## Summary: Key Differences

| Aspect | Frappe | FastAPI |
|--------|--------|---------|
| **Model Definition** | JSON + Python class | SQLAlchemy classes |
| **Validation** | `validate()` method | Pydantic models |
| **API Routes** | `@frappe.whitelist()` | `@router.get/post/etc` |
| **Permissions** | `has_permission()` | Custom RBAC service |
| **Queries** | `frappe.get_list()` | SQLAlchemy select() |
| **Async** | Synchronous | Async/await |
| **Database** | MariaDB (MySQL) | PostgreSQL (recommended) |
| **ORM** | Frappe ORM | SQLAlchemy 2.0 |
| **Jobs** | `frappe.enqueue()` | BullMQ/Celery |
| **Testing** | unittest | pytest |

---

## Porting Checklist

For each Frappe DocType/module, follow these steps:

**1. Database Model:**
- [ ] Create SQLAlchemy model in `models/`
- [ ] Define relationships
- [ ] Create Alembic migration

**2. Validation:**
- [ ] Create Pydantic schemas in `schemas/`
- [ ] Port validation logic to Pydantic validators
- [ ] Add custom validators for business rules

**3. Business Logic:**
- [ ] Create service class in `services/`
- [ ] Port methods from Frappe controller
- [ ] Make async where needed

**4. API Endpoints:**
- [ ] Create router in `api/routes/`
- [ ] Port whitelisted methods to FastAPI routes
- [ ] Add permission dependencies

**5. Permissions:**
- [ ] Define permissions in RBAC system
- [ ] Implement permission checks
- [ ] Add filters to queries

**6. Testing:**
- [ ] Write pytest tests
- [ ] Test all endpoints
- [ ] Test permissions
- [ ] Test business logic

---

*Document Version: 1.0*
*Created: 2025-11-16*
*For: Phase 2 - FastAPI Migration*
