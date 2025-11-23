# BLKSHP OS Authentication API

## Overview

BLKSHP OS provides JWT-based authentication for single-page applications (SPAs) consuming the REST APIs. This allows stateless, secure authentication suitable for modern web and mobile applications.

**Base Path:** `/api/method/blkshp_os.api.auth.`

**Token Types:**
- **Access Token** - Short-lived (1 hour) token for API requests
- **Refresh Token** - Long-lived (30 days) token for obtaining new access tokens

---

## Quick Start

### 1. Configure JWT Secret

Add to your `site_config.json`:

```json
{
  "jwt_secret": "your-secure-random-secret-key-here"
}
```

**Generate a secure secret:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Login

```javascript
const response = await fetch('/api/method/blkshp_os.api.auth.login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'user@example.com',
    password: 'password123'
  })
});

const data = await response.json();
const { access_token, refresh_token } = data.message;

// Store tokens securely
localStorage.setItem('access_token', access_token);
localStorage.setItem('refresh_token', refresh_token);
```

### 3. Make Authenticated Requests

```javascript
const response = await fetch('/api/method/blkshp_os.api.inventory.list_inventory_balances', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${access_token}`,
    'Content-Type': 'application/json',
  }
});
```

### 4. Refresh Expired Tokens

```javascript
const response = await fetch('/api/method/blkshp_os.api.auth.refresh', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    refresh_token: refresh_token
  })
});

const data = await response.json();
const { access_token: new_access_token } = data.message;

localStorage.setItem('access_token', new_access_token);
```

---

## API Endpoints

### Login

Authenticate user and receive JWT tokens.

**Endpoint:** `login`

**Method:** POST

**Access:** Guest (no authentication required)

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "message": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
      "email": "user@example.com",
      "full_name": "John Doe",
      "user_image": "/files/user.jpg",
      "companies": ["ACME", "HOTEL-1"],
      "roles": ["Inventory Manager", "Procurement User"]
    }
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "exc_type": "AuthenticationError",
  "message": "Invalid username or password"
}
```

---

### Refresh Token

Obtain a new access token using a refresh token.

**Endpoint:** `refresh`

**Method:** POST

**Access:** Guest (no authentication required)

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "message": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "exc_type": "AuthenticationError",
  "message": "Token has expired"
}
```

---

### Get Profile

Get authenticated user's comprehensive profile.

**Endpoint:** `profile`

**Method:** GET

**Access:** Authenticated (requires access token)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "message": {
    "user": {
      "email": "user@example.com",
      "full_name": "John Doe",
      "user_image": "/files/user.jpg",
      "companies": ["ACME"],
      "roles": ["Inventory Manager"]
    },
    "subscription": {
      "company": "ACME",
      "plan": {
        "plan_code": "STANDARD",
        "plan_name": "Standard Tier",
        "billing_frequency": "Monthly"
      },
      "modules": [
        {"key": "products", "label": "Products", "is_enabled": true},
        {"key": "inventory", "label": "Inventory", "is_enabled": true}
      ],
      "features": {
        "products.bulk_operations": true,
        "inventory.audit_workflows": true
      }
    },
    "permissions": {
      "departments": ["KITCHEN-ACME", "BAR-ACME"],
      "flags": {
        "can_read": true,
        "can_write": true,
        "can_create": false
      }
    }
  }
}
```

---

### Verify Token

Verify a JWT token and inspect its payload.

**Endpoint:** `verify_token`

**Method:** POST

**Access:** Guest (no authentication required)

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK - Valid Token):**
```json
{
  "message": {
    "valid": true,
    "payload": {
      "user": "user@example.com",
      "type": "access",
      "exp": 1700000000,
      "iat": 1699996400,
      "companies": ["ACME"],
      "roles": ["Inventory Manager"],
      "full_name": "John Doe"
    },
    "error": null
  }
}
```

**Response (200 OK - Invalid Token):**
```json
{
  "message": {
    "valid": false,
    "payload": null,
    "error": "Token has expired"
  }
}
```

---

### Token Info

Get information about a token (for debugging).

**Endpoint:** `token_info`

**Method:** POST

**Access:** Guest (no authentication required)

**Request Body:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "message": {
    "user": "user@example.com",
    "type": "access",
    "exp": 1700000000,
    "iat": 1699996400,
    "expires_in_seconds": 3600,
    "expires_in_minutes": 60,
    "is_expired": false
  }
}
```

---

### Logout

Logout and invalidate tokens.

**Endpoint:** `logout`

**Method:** POST

**Access:** Guest (no authentication required)

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response:**
```json
{
  "message": {
    "success": true,
    "message": "Logged out successfully. Please discard your tokens."
  }
}
```

**Note:** Since JWT tokens are stateless, logout primarily signals the client to discard tokens. In a production implementation, you may want to maintain a token blacklist.

---

## Authentication Flow

### Initial Authentication

```
Client                          Server
  |                               |
  |-- POST /api/auth/login ------>|
  |   {username, password}        |
  |                               |
  |<-- 200 OK -------------------|
  |   {access_token,              |
  |    refresh_token, user}       |
  |                               |
```

### Making Authenticated Requests

```
Client                          Server
  |                               |
  |-- GET /api/inventory -------->|
  |   Authorization: Bearer token |
  |                               |
  |<-- 200 OK -------------------|
  |   {data}                      |
  |                               |
```

### Refreshing Expired Tokens

```
Client                          Server
  |                               |
  |-- POST /api/auth/refresh ---->|
  |   {refresh_token}             |
  |                               |
  |<-- 200 OK -------------------|
  |   {access_token}              |
  |                               |
```

---

## Token Structure

### Access Token Payload

```json
{
  "user": "user@example.com",
  "exp": 1700000000,
  "iat": 1699996400,
  "type": "access",
  "companies": ["ACME", "HOTEL-1"],
  "roles": ["Inventory Manager"],
  "full_name": "John Doe"
}
```

### Refresh Token Payload

```json
{
  "user": "user@example.com",
  "exp": 1702588400,
  "iat": 1699996400,
  "type": "refresh"
}
```

**Token Claims:**
- `user` - User email
- `exp` - Expiration timestamp (Unix epoch)
- `iat` - Issued at timestamp (Unix epoch)
- `type` - Token type ("access" or "refresh")
- `companies` - User's accessible companies (access token only)
- `roles` - User's roles (access token only)
- `full_name` - User's full name (access token only)

---

## Client Implementation Examples

### React/Next.js

```typescript
// auth.ts
import axios from 'axios';

const API_BASE = '/api/method/blkshp_os.api.auth';

export async function login(username: string, password: string) {
  const response = await axios.post(`${API_BASE}.login`, {
    username,
    password
  });

  const { access_token, refresh_token, user } = response.data.message;

  // Store tokens
  localStorage.setItem('access_token', access_token);
  localStorage.setItem('refresh_token', refresh_token);
  localStorage.setItem('user', JSON.stringify(user));

  return { access_token, refresh_token, user };
}

export async function refreshToken() {
  const refresh_token = localStorage.getItem('refresh_token');

  const response = await axios.post(`${API_BASE}.refresh`, {
    refresh_token
  });

  const { access_token } = response.data.message;
  localStorage.setItem('access_token', access_token);

  return access_token;
}

export async function getProfile() {
  const access_token = localStorage.getItem('access_token');

  const response = await axios.get(`${API_BASE}.profile`, {
    headers: {
      'Authorization': `Bearer ${access_token}`
    }
  });

  return response.data.message;
}

export function logout() {
  const refresh_token = localStorage.getItem('refresh_token');

  // Call logout endpoint (optional)
  axios.post(`${API_BASE}.logout`, { refresh_token }).catch(() => {});

  // Clear local storage
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
}
```

### Axios Interceptor for Auto-Refresh

```typescript
import axios from 'axios';

// Add request interceptor to attach access token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Add response interceptor to handle token refresh
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and haven't retried yet
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        // Attempt to refresh token
        const newAccessToken = await refreshToken();

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return axios(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        logout();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);
```

---

## Security Best Practices

### Token Storage

**Browser/SPA:**
- **Access Token**: Store in memory (React state/context) or sessionStorage
- **Refresh Token**: Store in httpOnly cookie (most secure) or localStorage
- **Never** store in plain cookies or expose to XSS

**Mobile Apps:**
- Use secure storage (Keychain on iOS, Keystore on Android)

### Token Expiry

- **Access tokens**: Short-lived (1 hour default) - limits exposure if compromised
- **Refresh tokens**: Long-lived (30 days default) - reduces login frequency
- Implement automatic token refresh before expiry

### HTTPS Only

- **Always** use HTTPS in production
- JWT tokens are bearer tokens - anyone with the token can use it
- HTTPS prevents token interception

### Token Rotation

- Generate new refresh token on each refresh (token rotation)
- Invalidate old refresh token
- Limits damage from stolen refresh tokens

### CORS Configuration

Configure CORS to only allow your SPA domain:

```python
# site_config.json
{
  "allow_cors": "*",  # Development only!
  "cors_origins": ["https://app.blkshp.com"]  # Production
}
```

### Rate Limiting

Implement rate limiting on login endpoint to prevent brute force:

```python
# site_config.json
{
  "rate_limit": {
    "limit": 5,
    "window": 60  # 5 requests per minute
  }
}
```

---

## Troubleshooting

### "JWT secret not configured"

**Solution:** Add `jwt_secret` to `site_config.json`:

```json
{
  "jwt_secret": "your-secure-secret-here"
}
```

Restart the site after adding.

### "Token has expired"

**Solution:** Use the refresh token to get a new access token:

```javascript
const response = await fetch('/api/method/blkshp_os.api.auth.refresh', {
  method: 'POST',
  body: JSON.stringify({ refresh_token })
});
```

### "Invalid token"

**Possible causes:**
- Token was tampered with
- Wrong JWT secret on server
- Token format is incorrect

**Solution:** Re-authenticate and get new tokens.

### "User is disabled"

**Solution:** Contact administrator to enable the user account.

### CORS Errors

**Solution:** Configure CORS in `site_config.json`:

```json
{
  "allow_cors": "*"
}
```

Or for production, specify allowed origins:

```json
{
  "cors_origins": ["https://app.blkshp.com"]
}
```

---

## Related Documentation

- [Inventory API Reference](/docs/API-INVENTORY.md)
- [Finance API Reference](/docs/API-FINANCE.md)
- [User Profile Service](/docs/CORE-PLATFORM-README.md)
- [Development Guide](/docs/DEVELOPMENT-GUIDE.md)

---

## Changelog

### Version 1.0 (2025-11-16)
- Initial release
- JWT-based authentication
- Login, refresh, profile endpoints
- Token verification and debugging endpoints
- Comprehensive documentation and examples

---

**Last Updated:** 2025-11-16
**Version:** 1.0
