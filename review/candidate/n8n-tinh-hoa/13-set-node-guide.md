# Set Node Configuration Guide - Complete Type Handling

Complete guide for configuring the Set node (`n8n-nodes-base.set`).

## Source
Extracted from official n8n AI Workflow Builder prompts and examples.

---

## Overview

The Set node uses assignments to create or modify data fields. Each assignment has a specific type that determines how the value is formatted and processed.

## Assignment Structure

```json
{
  "id": "unique-id",
  "name": "field_name",
  "value": "field_value",  // Format depends on type
  "type": "string|number|boolean|array|object"
}
```

**CRITICAL**: ALWAYS use "value" field for ALL types. NEVER use type-specific fields like "stringValue", "numberValue", "booleanValue", etc. The field is ALWAYS named "value" regardless of the type.

## Type-Specific Value Formatting

### String Type

**Format**: Direct string value or expression

**Examples**:
- Literal: `"Hello World"`
- Expression: `"={{ $('Previous Node').item.json.message }}"`
- With embedded expressions: `"=Order #{{ $('Set').item.json.orderId }} processed"`

**Use when**: Text data, IDs, names, messages, dates as strings

**Example Assignment**:
```json
{
  "id": "id-1",
  "name": "message",
  "value": "Hello World",
  "type": "string"
}
```

### Number Type

**Format**: Direct numeric value (NOT as a string)

**Examples**:
- Integer: `123`
- Decimal: `45.67`
- Negative: `-100`
- Expression: `"={{ $('HTTP Request').item.json.count }}"`

**CRITICAL**: Use actual numbers, not strings: `123` not `"123"`

**Use when**: Quantities, prices, scores, numeric calculations

**Example Assignment**:
```json
{
  "id": "id-2",
  "name": "price",
  "value": 19.99,
  "type": "number"
}
```

### Boolean Type

**Format**: Direct boolean value (NOT as a string)

**Examples**:
- True: `true`
- False: `false`
- Expression: `"={{ $('IF').item.json.isActive }}"`

**CRITICAL**:
- Use actual booleans, not strings: `true` not `"true"`
- The field name is "value", NOT "booleanValue"

**Use when**: Flags, toggles, yes/no values, active/inactive states

**Example Assignment**:
```json
{
  "id": "id-3",
  "name": "inStock",
  "value": true,
  "type": "boolean"
}
```

### Array Type

**Format**: JSON stringified array

**Examples**:
- Simple array: `"[1, 2, 3]"`
- String array: `"[\"apple\", \"banana\", \"orange\"]"`
- Mixed array: `"[\"item1\", 123, true]"`
- Expression: `"={{ JSON.stringify($('Previous Node').item.json.items) }}"`

**CRITICAL**: Arrays must be JSON stringified

**Use when**: Lists, collections, multiple values

**Example Assignment**:
```json
{
  "id": "id-4",
  "name": "categories",
  "value": "[\"electronics\", \"gadgets\"]",
  "type": "array"
}
```

### Object Type

**Format**: JSON stringified object

**Examples**:
- Simple object: `"{ \"name\": \"John\", \"age\": 30 }"`
- Nested object: `"{ \"user\": { \"id\": 123, \"role\": \"admin\" } }"`
- Expression: `"={{ JSON.stringify($('Set').item.json.userData) }}"`

**CRITICAL**: Objects must be JSON stringified with escaped quotes

**Use when**: Complex data structures, grouped properties

**Example Assignment**:
```json
{
  "id": "id-5",
  "name": "userData",
  "value": "{ \"name\": \"John\", \"email\": \"john@example.com\" }",
  "type": "object"
}
```

## Complete Set Node Parameters Structure

```json
{
  "assignments": {
    "assignments": [
      {
        "id": "id-1",
        "name": "fieldName",
        "value": "fieldValue",
        "type": "string"
      }
    ]
  },
  "options": {
    "includeOtherFields": false  // Set to true to pass through input fields
  }
}
```

## Important Type Selection Rules

### 1. Analyze the requested data type:
- "Set count to 5" → number type with value: `5`
- "Set message to hello" → string type with value: `"hello"`
- "Set active to true" → boolean type with value: `true`
- "Set tags to apple, banana" → array type with value: `"[\"apple\", \"banana\"]"`

### 2. Expression handling:
- All types can use expressions with `"={{ ... }}"`
- For arrays/objects from expressions, use `JSON.stringify()`

### 3. Common mistakes to avoid:
- **WRONG**: Setting number as string: `{ "value": "123", "type": "number" }`
- **CORRECT**: `{ "value": 123, "type": "number" }`
- **WRONG**: Setting boolean as string: `{ "value": "false", "type": "boolean" }`
- **CORRECT**: `{ "value": false, "type": "boolean" }`
- **WRONG**: Using type-specific field names: `{ "booleanValue": true, "type": "boolean" }`
- **CORRECT**: `{ "value": true, "type": "boolean" }`
- **WRONG**: Setting array without stringification: `{ "value": [1,2,3], "type": "array" }`
- **CORRECT**: `{ "value": "[1,2,3]", "type": "array" }`

## Complete Examples

### Example 1: Simple String Assignment

**Requested**: Set message to "Hello World"

**Output**:
```json
{
  "assignments": {
    "assignments": [
      {
        "id": "id-1",
        "name": "message",
        "value": "Hello World",
        "type": "string"
      }
    ]
  },
  "options": {}
}
```

### Example 2: Multiple Type Assignments

**Requested**:
- Set productName to "Widget"
- Set price to 19.99
- Set inStock to true
- Set categories to electronics and gadgets

**Output**:
```json
{
  "assignments": {
    "assignments": [
      {
        "id": "id-1",
        "name": "productName",
        "value": "Widget",
        "type": "string"
      },
      {
        "id": "id-2",
        "name": "price",
        "value": 19.99,
        "type": "number"
      },
      {
        "id": "id-3",
        "name": "inStock",
        "value": true,
        "type": "boolean"
      },
      {
        "id": "id-4",
        "name": "categories",
        "value": "[\"electronics\", \"gadgets\"]",
        "type": "array"
      }
    ]
  },
  "options": {}
}
```

### Example 3: Expression-Based Assignments

**Requested**:
- Set userId from HTTP Request node
- Calculate totalPrice from quantity and unit price

**Output**:
```json
{
  "assignments": {
    "assignments": [
      {
        "id": "id-1",
        "name": "userId",
        "value": "={{ $('HTTP Request').item.json.id }}",
        "type": "string"
      },
      {
        "id": "id-2",
        "name": "totalPrice",
        "value": "={{ $('Set').item.json.quantity * $('Set').item.json.unitPrice }}",
        "type": "number"
      }
    ]
  },
  "options": {}
}
```

### Example 4: Complex Object and Array Creation

**Current Parameters**:
```json
{
  "assignments": {
    "assignments": [
      {
        "id": "existing-1",
        "name": "orderId",
        "value": "12345",
        "type": "string"
      }
    ]
  },
  "options": {}
}
```

**Requested Changes**:
- Keep orderId
- Add customer object with name and email from previous nodes
- Add items array from JSON string
- Set processed timestamp

**Expected Output**:
```json
{
  "assignments": {
    "assignments": [
      {
        "id": "existing-1",
        "name": "orderId",
        "value": "12345",
        "type": "string"
      },
      {
        "id": "id-2",
        "name": "customer",
        "value": "={{ JSON.stringify({ \"name\": $('Form').item.json.customerName, \"email\": $('Form').item.json.customerEmail }) }}",
        "type": "object"
      },
      {
        "id": "id-3",
        "name": "items",
        "value": "={{ $('HTTP Request').item.json.itemsJson }}",
        "type": "array"
      },
      {
        "id": "id-4",
        "name": "processedAt",
        "value": "={{ $now.toISO() }}",
        "type": "string"
      }
    ]
  },
  "options": {}
}
```

## Best Practices

1. **Always specify the correct type** - Don't default to string for everything
2. **Use proper value formats** - Numbers as numbers, booleans as booleans
3. **Stringify arrays and objects** - They must be JSON strings
4. **Use descriptive field names** - Makes data flow easier to understand
5. **Enable includeOtherFields when needed** - To pass through existing data
6. **Use expressions for dynamic values** - Reference previous nodes
7. **Generate unique IDs** - Use a simple pattern like "id-1", "id-2", etc.
