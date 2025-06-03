<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [API Documentation](#api-documentation)
  - [Base URL](#base-url)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
    - [Obligations](#obligations)
      - [GET /obligations](#get-obligations)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

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
