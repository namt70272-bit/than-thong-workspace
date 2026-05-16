# IF Node Configuration Guide - Complete Operator Reference

Complete guide for configuring the IF node (`n8n-nodes-base.if`) with all operator types and examples.

## Source
Extracted from official n8n AI Workflow Builder prompts.

---

## Overview

The IF node uses a complex filter structure for conditional logic. Understanding the correct operator format is crucial for proper workflow behavior.

## IF Node Structure

```json
{
  "conditions": {
    "options": {
      "caseSensitive": false,      // For string comparisons
      "leftValue": "",              // Optional default left value
      "typeValidation": "loose"     // "strict" or "loose"
    },
    "conditions": [
      {
        "id": "unique-id",          // Optional, auto-generated
        "leftValue": "={{ $('Node').item.json.field }}",
        "rightValue": "value",      // Can be expression or literal
        "operator": {
          "type": "string|number|boolean|dateTime|array|object",
          "operation": "specific-operation"
        }
      }
    ],
    "combinator": "and"  // "and" or "or"
  }
}
```

## Complete Operator Reference

### String Operators

**exists** - Check if value exists (singleValue: true, no rightValue needed)
```json
{ "type": "string", "operation": "exists" }
```

**notExists** - Check if value doesn't exist (singleValue: true)
```json
{ "type": "string", "operation": "notExists" }
```

**empty** - Check if string is empty (singleValue: true)
```json
{ "type": "string", "operation": "empty" }
```

**notEmpty** - Check if string is not empty (singleValue: true)
```json
{ "type": "string", "operation": "notEmpty" }
```

**equals** - Exact match
```json
{ "type": "string", "operation": "equals" }
```

**notEquals** - Not equal
```json
{ "type": "string", "operation": "notEquals" }
```

**contains** - Contains substring
```json
{ "type": "string", "operation": "contains" }
```

**notContains** - Doesn't contain substring
```json
{ "type": "string", "operation": "notContains" }
```

**startsWith** - Starts with string
```json
{ "type": "string", "operation": "startsWith" }
```

**notStartsWith** - Doesn't start with
```json
{ "type": "string", "operation": "notStartsWith" }
```

**endsWith** - Ends with string
```json
{ "type": "string", "operation": "endsWith" }
```

**notEndsWith** - Doesn't end with
```json
{ "type": "string", "operation": "notEndsWith" }
```

**regex** - Matches regex pattern
```json
{ "type": "string", "operation": "regex" }
```

**notRegex** - Doesn't match regex
```json
{ "type": "string", "operation": "notRegex" }
```

### Number Operators

**exists** - Check if number exists (singleValue: true)
```json
{ "type": "number", "operation": "exists" }
```

**notExists** - Check if number doesn't exist (singleValue: true)
```json
{ "type": "number", "operation": "notExists" }
```

**equals** - Equal to
```json
{ "type": "number", "operation": "equals" }
```

**notEquals** - Not equal to
```json
{ "type": "number", "operation": "notEquals" }
```

**gt** - Greater than
```json
{ "type": "number", "operation": "gt" }
```

**lt** - Less than
```json
{ "type": "number", "operation": "lt" }
```

**gte** - Greater than or equal
```json
{ "type": "number", "operation": "gte" }
```

**lte** - Less than or equal
```json
{ "type": "number", "operation": "lte" }
```

### DateTime Operators

**exists** - Check if date exists (singleValue: true)
```json
{ "type": "dateTime", "operation": "exists" }
```

**notExists** - Check if date doesn't exist (singleValue: true)
```json
{ "type": "dateTime", "operation": "notExists" }
```

**equals** - Same date/time
```json
{ "type": "dateTime", "operation": "equals" }
```

**notEquals** - Different date/time
```json
{ "type": "dateTime", "operation": "notEquals" }
```

**after** - After date
```json
{ "type": "dateTime", "operation": "after" }
```

**before** - Before date
```json
{ "type": "dateTime", "operation": "before" }
```

**afterOrEquals** - After or same date
```json
{ "type": "dateTime", "operation": "afterOrEquals" }
```

**beforeOrEquals** - Before or same date
```json
{ "type": "dateTime", "operation": "beforeOrEquals" }
```

### Boolean Operators

**exists** - Check if boolean exists (singleValue: true)
```json
{ "type": "boolean", "operation": "exists" }
```

**notExists** - Check if boolean doesn't exist (singleValue: true)
```json
{ "type": "boolean", "operation": "notExists" }
```

**true** - Is true (singleValue: true)
```json
{ "type": "boolean", "operation": "true" }
```

**false** - Is false (singleValue: true)
```json
{ "type": "boolean", "operation": "false" }
```

**equals** - Equal to boolean value
```json
{ "type": "boolean", "operation": "equals" }
```

**notEquals** - Not equal to boolean value
```json
{ "type": "boolean", "operation": "notEquals" }
```

### Array Operators

**exists** - Check if array exists (singleValue: true)
```json
{ "type": "array", "operation": "exists" }
```

**notExists** - Check if array doesn't exist (singleValue: true)
```json
{ "type": "array", "operation": "notExists" }
```

**empty** - Array is empty (singleValue: true)
```json
{ "type": "array", "operation": "empty" }
```

**notEmpty** - Array is not empty (singleValue: true)
```json
{ "type": "array", "operation": "notEmpty" }
```

**contains** - Array contains value
```json
{ "type": "array", "operation": "contains" }
```

**notContains** - Array doesn't contain value
```json
{ "type": "array", "operation": "notContains" }
```

**lengthEquals** - Array length equals
```json
{ "type": "array", "operation": "lengthEquals" }
```

**lengthNotEquals** - Array length not equals
```json
{ "type": "array", "operation": "lengthNotEquals" }
```

**lengthGt** - Array length greater than
```json
{ "type": "array", "operation": "lengthGt" }
```

**lengthLt** - Array length less than
```json
{ "type": "array", "operation": "lengthLt" }
```

**lengthGte** - Array length greater or equal
```json
{ "type": "array", "operation": "lengthGte" }
```

**lengthLte** - Array length less or equal
```json
{ "type": "array", "operation": "lengthLte" }
```

### Object Operators

**exists** - Check if object exists (singleValue: true)
```json
{ "type": "object", "operation": "exists" }
```

**notExists** - Check if object doesn't exist (singleValue: true)
```json
{ "type": "object", "operation": "notExists" }
```

**empty** - Object is empty (singleValue: true)
```json
{ "type": "object", "operation": "empty" }
```

**notEmpty** - Object is not empty (singleValue: true)
```json
{ "type": "object", "operation": "notEmpty" }
```

## Important Notes

1. **singleValue operators**: When using exists, notExists, empty, notEmpty, true, or false operators, DO NOT include a rightValue in the condition
2. **Expression values**: Both leftValue and rightValue can be expressions using `={{ ... }}` syntax
3. **Type matching**: The operator type must match the data type you're comparing
4. **Case sensitivity**: Only applies to string comparisons when caseSensitive is true in options
5. **Type validation**: "loose" allows type coercion, "strict" requires exact type matches

## Complete Examples

### Example 1: Simple String Condition

**Request**: Check if order status equals "pending"

**Output**:
```json
{
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "id-1",
        "leftValue": "={{ $('Previous Node').item.json.orderStatus }}",
        "rightValue": "pending",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      }
    ],
    "combinator": "and"
  }
}
```

### Example 2: Check if Field Exists

**Request**: Check if email field exists in the data

**Output**:
```json
{
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "id-1",
        "leftValue": "={{ $('Previous Node').item.json.email }}",
        "operator": {
          "type": "string",
          "operation": "exists"
        }
      }
    ],
    "combinator": "and"
  }
}
```

Note: No rightValue is included because "exists" is a singleValue operator.

### Example 3: Multiple Conditions with AND

**Request**: Check if status is active AND score is 50 or higher

**Output**:
```json
{
  "conditions": {
    "options": {
      "caseSensitive": false,
      "leftValue": "",
      "typeValidation": "loose"
    },
    "conditions": [
      {
        "id": "id-1",
        "leftValue": "={{ $('Set').item.json.status }}",
        "rightValue": "active",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      },
      {
        "id": "id-2",
        "leftValue": "={{ $('Set').item.json.score }}",
        "rightValue": "50",
        "operator": {
          "type": "number",
          "operation": "gte"
        }
      }
    ],
    "combinator": "and"
  }
}
```

### Example 4: Complex Multi-Type Conditions

**Request**: Check if email is not empty AND verified is true AND permissions array contains "write"

**Output**:
```json
{
  "conditions": {
    "options": {
      "caseSensitive": true,
      "leftValue": "",
      "typeValidation": "strict"
    },
    "conditions": [
      {
        "id": "id-1",
        "leftValue": "={{ $('Set').item.json.email }}",
        "operator": {
          "type": "string",
          "operation": "notEmpty"
        }
      },
      {
        "id": "id-2",
        "leftValue": "={{ $('Set').item.json.verified }}",
        "operator": {
          "type": "boolean",
          "operation": "true"
        }
      },
      {
        "id": "id-3",
        "leftValue": "={{ $('Set').item.json.permissions }}",
        "rightValue": "write",
        "operator": {
          "type": "array",
          "operation": "contains"
        }
      }
    ],
    "combinator": "and"
  }
}
```

## Best Practices

1. **Choose the correct operator type** - Match the data type being compared
2. **Use singleValue operators correctly** - Don't add rightValue when not needed
3. **Use expressions for dynamic values** - Reference previous node data
4. **Set appropriate validation mode** - "loose" for flexibility, "strict" for precision
5. **Combine conditions logically** - Use "and" or "or" combinators appropriately
6. **Test edge cases** - Consider empty values, null, undefined
7. **Use descriptive condition IDs** - Makes debugging easier
