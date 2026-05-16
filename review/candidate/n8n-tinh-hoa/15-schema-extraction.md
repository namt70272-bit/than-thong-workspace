# Schema Extraction and Understanding

This document explains how to extract, analyze, and understand data schemas for generating accurate n8n Code node scripts.

## Source
Inspired by: n8n's `useDataSchema.ts` and AskAI component schema extraction logic

---

## Overview

**Schema extraction is the foundation of context-aware code generation.**

Without understanding the input data structure, generated code will:
- ❌ Use wrong field names → undefined values
- ❌ Make incorrect assumptions → runtime errors
- ❌ Miss nested structures → incomplete transformations

With proper schema extraction, generated code will:
- ✅ Use exact field names from actual data
- ✅ Handle nested structures correctly
- ✅ Access arrays and objects properly

---

## What is a Schema?

A **schema** is a structural description of data that shows:
- Field names
- Data types (string, number, boolean, object, array)
- Nesting levels
- Whether fields are arrays or single values

**Example Data**:
```json
{
  "user": {
    "id": 123,
    "name": "Alice",
    "emails": ["alice@work.com", "alice@personal.com"],
    "active": true
  }
}
```

**Extracted Schema**:
```
user (object)
  ├─ id (number)
  ├─ name (string)
  ├─ emails (array of strings)
  └─ active (boolean)
```

---

## Schema Extraction from Different Sources

### 1. From JSON Sample Data

**Most common scenario**: User provides sample JSON

**Example**:
```json
{
  "orders": [
    {
      "orderId": 101,
      "customer": {
        "name": "Alice",
        "email": "alice@example.com"
      },
      "items": [
        { "product": "Widget", "quantity": 2, "price": 15.99 }
      ],
      "total": 31.98
    }
  ]
}
```

**Extracted Schema**:
```
Root object:
  orders (array of objects)
    [0] (object)
      ├─ orderId (number)
      ├─ customer (object)
      │   ├─ name (string)
      │   └─ email (string)
      ├─ items (array of objects)
      │   [0] (object)
      │       ├─ product (string)
      │       ├─ quantity (number)
      │       └─ price (number)
      └─ total (number)
```

**Key Findings**:
- Root has "orders" field (array)
- Each order is an object
- Customer is nested object
- Items is nested array
- Numeric fields: orderId, quantity, price, total

---

### 2. From n8n Execution Data

**n8n format**: Data is wrapped in `items` array with `json` property

**Example**:
```json
[
  {
    "json": {
      "userId": 42,
      "username": "alice_smith",
      "profile": {
        "bio": "Software developer",
        "location": "San Francisco"
      }
    }
  }
]
```

**Extracted Schema (n8n-aware)**:
```
items[0].json:
  ├─ userId (number)
  ├─ username (string)
  └─ profile (object)
      ├─ bio (string)
      └─ location (string)
```

**Access Pattern**:
```javascript
item.json.userId         // 42
item.json.username       // "alice_smith"
item.json.profile.bio    // "Software developer"
```

---

### 3. From API Documentation

**Scenario**: User provides API endpoint documentation

**Example Documentation**:
```
GET /api/users

Response:
{
  "data": {
    "users": [
      {
        "id": integer,
        "email": string,
        "created_at": timestamp,
        "metadata": {
          "last_login": timestamp,
          "login_count": integer
        }
      }
    ]
  },
  "total": integer
}
```

**Extracted Schema**:
```
data (object)
  ├─ users (array of objects)
  │   [0]:
  │     ├─ id (integer)
  │     ├─ email (string)
  │     ├─ created_at (timestamp)
  │     └─ metadata (object)
  │         ├─ last_login (timestamp)
  │         └─ login_count (integer)
  └─ total (integer)
```

---

### 4. From Partial/Incomplete Data

**Scenario**: User provides incomplete sample or description

**Example User Input**:
"The data has a list of products, each with a name, price, and tags array"

**Inferred Schema**:
```
products (array of objects) [INFERRED]
  [0]:
    ├─ name (string) [INFERRED]
    ├─ price (number) [INFERRED]
    └─ tags (array of strings) [INFERRED]
```

**Note**: Mark inferred fields and ask user to confirm

---

## Schema Analysis Checklist

When analyzing schema, identify:

### 1. Root Structure
- [ ] Is root an object or array?
- [ ] What are the top-level field names?

### 2. Data Types
- [ ] Which fields are strings, numbers, booleans?
- [ ] Which fields are objects (nested structures)?
- [ ] Which fields are arrays?

### 3. Nesting Levels
- [ ] How deep is the nesting?
- [ ] Are there arrays within objects within arrays?

### 4. Array Elements
- [ ] If field is array, what type are elements?
- [ ] Array of primitives (strings, numbers)?
- [ ] Array of objects?

### 5. Nullable Fields
- [ ] Which fields might be null/undefined?
- [ ] Which fields are always present?

---

## Common Schema Patterns

### Pattern 1: Simple Flat Object

**Example**:
```json
{
  "name": "Alice",
  "age": 30,
  "email": "alice@example.com"
}
```

**Schema**:
```
name (string)
age (number)
email (string)
```

**Access**:
```javascript
item.json.name
item.json.age
item.json.email
```

---

### Pattern 2: Nested Object

**Example**:
```json
{
  "user": {
    "profile": {
      "name": "Alice",
      "contact": {
        "email": "alice@example.com"
      }
    }
  }
}
```

**Schema**:
```
user (object)
  └─ profile (object)
      ├─ name (string)
      └─ contact (object)
          └─ email (string)
```

**Access**:
```javascript
item.json.user.profile.name
item.json.user.profile.contact.email
```

---

### Pattern 3: Array of Primitives

**Example**:
```json
{
  "tags": ["javascript", "nodejs", "automation"]
}
```

**Schema**:
```
tags (array of strings)
```

**Access**:
```javascript
item.json.tags           // ["javascript", "nodejs", "automation"]
item.json.tags[0]        // "javascript"
item.json.tags.length    // 3
```

---

### Pattern 4: Array of Objects

**Example**:
```json
{
  "products": [
    { "id": 1, "name": "Widget", "price": 9.99 },
    { "id": 2, "name": "Gadget", "price": 19.99 }
  ]
}
```

**Schema**:
```
products (array of objects)
  [0]:
    ├─ id (number)
    ├─ name (string)
    └─ price (number)
```

**Access**:
```javascript
item.json.products              // Array
item.json.products[0]           // { id: 1, name: "Widget", price: 9.99 }
item.json.products[0].name      // "Widget"
item.json.products.length       // 2
```

---

### Pattern 5: Mixed Nested Structure

**Example**:
```json
{
  "order": {
    "id": 101,
    "customer": {
      "name": "Alice",
      "emails": ["alice@work.com", "alice@home.com"]
    },
    "items": [
      { "product": "Widget", "qty": 2 }
    ]
  }
}
```

**Schema**:
```
order (object)
  ├─ id (number)
  ├─ customer (object)
  │   ├─ name (string)
  │   └─ emails (array of strings)
  └─ items (array of objects)
      [0]:
        ├─ product (string)
        └─ qty (number)
```

**Access**:
```javascript
item.json.order.id                      // 101
item.json.order.customer.name           // "Alice"
item.json.order.customer.emails[0]      // "alice@work.com"
item.json.order.items[0].product        // "Widget"
```

---

## Schema Communication Format

When discussing schema with user or in code comments, use this format:

### Compact Format (for simple schemas)
```
fieldName (type) - description
```

**Example**:
```
userId (number) - unique user identifier
email (string) - user's email address
isActive (boolean) - account status
tags (array) - list of tags
```

### Tree Format (for nested schemas)
```
root
  ├─ field1 (type)
  └─ field2 (object)
      ├─ subfield1 (type)
      └─ subfield2 (array)
```

### JavaScript Comment Format (in generated code)
```javascript
// Input schema:
// {
//   "user": {
//     "name": string,
//     "email": string,
//     "orders": [{ "id": number, "total": number }]
//   }
// }
```

---

## Questions to Ask When Schema is Unclear

If user provides incomplete information, ask:

### About Structure
- "What is the root structure of your data - is it an object or array?"
- "Can you provide a sample of the actual data?"

### About Field Names
- "What is the exact field name for [concept]?" (e.g., "for the user ID")
- "Are the field names in camelCase, snake_case, or another format?"

### About Nesting
- "Is [field] nested inside another object?"
- "What is the full path to access [field]?"

### About Arrays
- "Is [field] an array or a single value?"
- "If it's an array, what type are the elements?"

### About Types
- "Is [field] a string or a number?"
- "Is [field] always present or can it be null/undefined?"

---

## Schema Extraction Workflow

### Step 1: Request Schema/Sample Data

If not provided, ask:
"Could you provide a sample of the input data or describe its structure?"

### Step 2: Analyze Structure

Extract:
- Root structure (object/array)
- Top-level fields
- Nested structures
- Array fields and their element types

### Step 3: Confirm Understanding

Summarize back to user:
"Based on the data, I see:
- A 'users' array at the root
- Each user has: id (number), name (string), email (string)
- Users have a nested 'orders' array
Is this correct?"

### Step 4: Generate Access Patterns

Document how to access each field:
```javascript
// Root array access
item.json.users[i].name

// Nested object access
item.json.users[i].profile.bio

// Nested array access
item.json.users[i].orders[j].total
```

---

## Common Schema Pitfalls

### ❌ Pitfall 1: Assuming Field Names

**Wrong**:
```javascript
// Assuming field is called "id"
item.json.id
```

**Right**:
```javascript
// Schema shows field is called "userId"
item.json.userId
```

### ❌ Pitfall 2: Ignoring n8n Wrapper

**Wrong**:
```javascript
// Assuming data is directly accessible
items[0].name
```

**Right**:
```javascript
// Data is wrapped in "json" property
items[0].json.name
```

### ❌ Pitfall 3: Missing Nesting Level

**Wrong**:
```javascript
// Missing intermediate "profile" object
item.json.name
```

**Right**:
```javascript
// Correct path through "profile"
item.json.profile.name
```

### ❌ Pitfall 4: Confusing Array with Object

**Wrong**:
```javascript
// Treating array as single object
item.json.users.name
```

**Right**:
```javascript
// Accessing array elements
item.json.users[0].name
// or iterating
item.json.users.map(user => user.name)
```

---

## Schema-Driven Code Generation

Once schema is understood, generate code that:

1. **Uses exact field names** from schema
2. **Handles nesting** correctly
3. **Iterates arrays** when needed
4. **Checks for null/undefined** on optional fields

**Example**:

**Schema**:
```
user (object)
  ├─ id (number, required)
  ├─ profile (object, optional)
  │   └─ name (string)
  └─ emails (array of strings)
```

**Generated Code**:
```javascript
return items.map(item => ({
  json: {
    userId: item.json.user.id,
    name: item.json.user.profile?.name || 'Unknown',
    primaryEmail: item.json.user.emails?.[0] || 'no-email@example.com'
  }
}));
```

**Note**:
- Uses `user.id` (exact field name)
- Uses optional chaining (`?.`) for optional `profile`
- Provides default for missing email
- Accesses first element of emails array

---

## Summary

**Key Principles**:
1. **Always extract schema before generating code**
2. **Use exact field names from actual data**
3. **Understand nesting levels and array structures**
4. **Document access patterns in code comments**
5. **Confirm schema understanding with user**

**Remember**: Accurate schema extraction is the difference between code that "might work" and code that "definitely works".
