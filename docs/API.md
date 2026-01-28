# API Documentation 📡

## Base URL
- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://chainquery-app.onrender.com/api/v1`

## Authentication

ChainQuery AI uses **Hybrid Authentication**:
1. **Guest Access**: No token required. Requests tracked via `session_id`.
2. **User Access**: Requires `Authorization` header with JWT Bearer token.

**Header Format:**
```http
Authorization: Bearer <access_token>
```

---

## Endpoints

### 🔐 Authentication

#### 1. Sign Up
Create a new user account.

- **Endpoint**: `POST /auth/signup`
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "strongpassword123",
    "full_name": "John Doe"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "id": "uuid-string",
    "email": "user@example.com",
    "access_token": "jwt-token-string",
    "token_type": "bearer"
  }
  ```

#### 2. Login
Authenticate and receive an access token.

- **Endpoint**: `POST /auth/login`
- **Content-Type**: `application/x-www-form-urlencoded`
- **Request Body**:
  - `username`: "user@example.com"
  - `password`: "strongpassword123"
- **Response**: `200 OK`
  ```json
  {
    "access_token": "jwt-token-string",
    "token_type": "bearer"
  }
  ```

---

### 🧠 Query Generation

#### 3. Generate SQL
Convert natural language to DuneSQL (Trino).

- **Endpoint**: `POST /generate`
- **Auth**: Optional (Hybrid)
- **Request Body**:
  ```json
  {
    "user_input": "Show me the top 10 NFT sales on Magic Eden yesterday",
    "chain": "solana",
    "session_id": "device-uuid-string"
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "id": "query-uuid",
    "user_input": "Show me the top 10 NFT sales...",
    "sql_output": "SELECT ... FROM ...",
    "error_message": null,
    "chain": "solana",
    "created_at": "2024-03-20T10:00:00Z"
  }
  ```

#### 4. Get History
Retrieve past queries for the current session.

- **Endpoint**: `GET /history`
- **Auth**: Optional
- **Query Parameters**:
  - `session_id`: (Required) The device UUID
  - `limit`: (Optional, default=10)
- **Response**: `200 OK`
  ```json
  [
    {
      "id": "query-uuid",
      "user_input": "...",
      "sql_output": "...",
      "created_at": "..."
    }
  ]
  ```

---

## Error Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Success |
| 400 | Bad Request | Missing fields or invalid input |
| 401 | Unauthorized | Invalid or missing token (for protected routes) |
| 500 | Server Error | Internal failure (AI provider or DB issue) |
