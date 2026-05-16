# HTTP Request Node Configuration Guide

Complete guide for configuring the HTTP Request node (`n8n-nodes-base.httpRequest`).

## Source
Extracted from: `packages/@n8n/ai-workflow-builder.ee/src/chains/prompts/node-types/http-request.ts`

---

## Common Parameters

- **url**: The endpoint URL (can use expressions)
- **method**: GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS
- **authentication**: Type of auth (none, genericCredentialType, etc.)
- **sendHeaders**: Boolean to enable custom headers
- **headerParameters**: Array of header key-value pairs
- **sendBody**: Boolean to enable request body (for POST/PUT/PATCH)
- **bodyParameters**: Array of body parameters or raw body content
- **contentType**: json, form, raw, etc.
- **options**: Additional options like timeout, proxy, etc.

## Header Structure

```json
{
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "Header-Name",
        "value": "Header Value or {{ expression }}"
      }
    ]
  }
}
```

## Body Structure (JSON)

```json
{
  "sendBody": true,
  "contentType": "json",
  "bodyParameters": {
    "parameters": [
      {
        "name": "fieldName",
        "value": "fieldValue or {{ expression }}"
      }
    ]
  }
}
```

## Authentication Options

- **none**: No authentication
- **genericCredentialType**: Use stored credentials
- **predefinedCredentialType**: Use specific credential type
- Can also set custom auth headers

## Common Patterns

### 1. Adding API Key Header

- Enable sendHeaders
- Add header with name "X-API-Key" or "Authorization"

```json
{
  "method": "GET",
  "url": "https://api.example.com/data",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "X-API-Key",
        "value": "={{ $credentials.apiKey }}"
      }
    ]
  }
}
```

### 2. Setting Request Body

- Enable sendBody
- Set contentType (usually "json")
- Add parameters to bodyParameters.parameters array

```json
{
  "method": "POST",
  "url": "https://api.example.com/users",
  "sendBody": true,
  "contentType": "json",
  "bodyParameters": {
    "parameters": [
      {
        "name": "name",
        "value": "John Doe"
      },
      {
        "name": "email",
        "value": "john@example.com"
      }
    ]
  }
}
```

### 3. Dynamic URLs

Can use expressions to build URLs dynamically:

```json
{
  "url": "=https://api.example.com/{{ $('Set').item.json.endpoint }}"
}
```

Can reference previous node data:

```json
{
  "url": "=https://api.example.com/users/{{ $('Previous Node').item.json.userId }}"
}
```

### 4. Query Parameters

Can be part of URL or set in options.queryParameters:

```json
{
  "url": "https://api.example.com/search?q=test&limit=10"
}
```

Or:

```json
{
  "url": "https://api.example.com/search",
  "options": {
    "queryParameters": {
      "parameters": [
        {
          "name": "q",
          "value": "test"
        },
        {
          "name": "limit",
          "value": "10"
        }
      ]
    }
  }
}
```

## Complete Example

### Current Parameters:
```json
{
  "method": "GET",
  "url": "https://api.example.com/data"
}
```

### Requested Changes:
- Change to POST method
- Add API key header
- Add JSON body with user ID and status

### Expected Output:
```json
{
  "method": "POST",
  "url": "https://api.example.com/data",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {
        "name": "X-API-Key",
        "value": "={{ $credentials.apiKey }}"
      },
      {
        "name": "Content-Type",
        "value": "application/json"
      }
    ]
  },
  "sendBody": true,
  "contentType": "json",
  "bodyParameters": {
    "parameters": [
      {
        "name": "userId",
        "value": "={{ $('Previous Node').item.json.id }}"
      },
      {
        "name": "status",
        "value": "active"
      }
    ]
  },
  "options": {}
}
```

## Common Mistakes to Avoid

1. **Forgetting to enable sendHeaders or sendBody** - These boolean flags must be true
2. **Wrong content type** - Ensure contentType matches the actual body format
3. **Missing authentication** - Set appropriate authentication method
4. **Hardcoding sensitive data** - Use credentials or environment variables
5. **Not handling errors** - Use error workflows or retry settings
