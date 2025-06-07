<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [API Documentation](#api-documentation)
  - [Base URL](#base-url)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
    - [Obligations](#obligations)
      - [GET /obligations](#get-obligations)
    - [Protobuf Endpoints](#protobuf-endpoints)
      - [GET /protobuf/api/projects/](#get-protobufapiprojects)
      - [GET /protobuf/api/projects/<project_id>/](#get-protobufapiprojectsproject_id)
      - [GET /protobuf/api/projects/<project_id>/obligations/](#get-protobufapiprojectsproject_idobligations)
      - [GET /protobuf/api/charts/<chart_id>/](#get-protobufapichartschart_id)
    - [Client Integration Notes](#client-integration-notes)

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

### Protobuf Endpoints

#### GET /protobuf/api/projects/

Returns all projects in Protocol Buffer (protobuf) binary format.

- **Response Content-Type:** application/x-protobuf
- **Response Body:** Serialized ProjectCollection message (see projects.proto)
- **Usage:**
  - Frontend/clients should use protobuf.js or a compatible library to parse the binary response.

#### GET /protobuf/api/projects/<project_id>/

Returns a single project in protobuf format.

- **Response Content-Type:** application/x-protobuf
- **Response Body:** Serialized ProjectProto message

#### GET /protobuf/api/projects/<project_id>/obligations/

Returns all obligations for a project in protobuf format.

- **Response Content-Type:** application/x-protobuf
- **Response Body:** Serialized ObligationList message (see greenova_data.proto)

#### GET /protobuf/api/charts/<chart_id>/

Returns chart data in protobuf format.

- **Response Content-Type:** application/x-protobuf
- **Response Body:** Serialized ChartData message

### Client Integration Notes

- To consume these endpoints, use a Protocol Buffer parser (e.g., protobuf.js for JavaScript/TypeScript frontends).
- Example (JavaScript):

  ```js
  // Fetch binary protobuf data
  fetch('/protobuf/api/projects/1/obligations/')
    .then(res => res.arrayBuffer())
    .then(buffer => {
      // Use protobuf.js to decode
      const root = await protobuf.load('greenova_data.proto');
      const ObligationList = root.lookupType('greenova.core.ObligationList');
      const message = ObligationList.decode(new Uint8Array(buffer));
      // Now you can use message.obligations
    });
  ```

- Prefer protobuf over JSON for new API/data exchange for efficiency and type safety.
