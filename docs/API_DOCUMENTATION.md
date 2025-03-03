
# API Documentation

## Base URL
`/api/v1/`

## Authentication
- Bearer token authentication required for all endpoints
- Token format: `Authorization: Bearer <token>`

## Endpoints

### Obligations

#### GET /obligations
Retrieves list of obligations.

**Parameters:**
- `status` (optional): Filter by status
- `due_date` (optional): Filter by due date

**Response:**
