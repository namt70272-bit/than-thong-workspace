---
name: n8n-code-creator
description: Generate JavaScript code for n8n Code nodes based on input data structure and transformation requirements. Handles data extraction, filtering, transformation, calculation, and business logic processing. Replicates the official n8n "Ask AI" feature.
---

# n8n Code Creator

## Overview

This skill provides expert-level n8n Code node development capabilities, replicating the official "Ask AI" feature. Generate production-ready JavaScript code based on actual input data structures and transformation requirements.

## What This Skill Does

**Core Capability**: Generate JavaScript code for n8n Code nodes by analyzing input data schema and understanding transformation requirements.

**Unlike generic code generators**, this skill:
- ✅ Analyzes **actual input data structure** from parent nodes
- ✅ Understands **n8n's data format** (items array with `json` property)
- ✅ Generates **context-aware code** that works with real data
- ✅ Follows **n8n best practices** (error handling, type safety)

## When to Use This Skill

Use this skill when:
- ✅ User provides input data structure (JSON, schema, or sample data)
- ✅ Task involves data processing in n8n workflows
- ✅ User mentions "Code node", "JavaScript", or data transformation
- ✅ Request includes data extraction, filtering, transformation, or calculation
- ✅ User says "generate code to..." with data context

## Core Principles

### 1. Schema-First Generation

**Always start with understanding the input data structure.**

```javascript
// BAD: Generic code without knowing input structure
return items.map(item => ({
  json: {
    name: item.json.name,  // What if structure is different?
    email: item.json.email
  }
}));

// GOOD: Code based on actual schema
// Input schema: { "user": { "fullName": "...", "contact": { "email": "..." } } }
return items.map(item => ({
  json: {
    name: item.json.user.fullName,
    email: item.json.user.contact.email
  }
}));
```

### 2. n8n Data Format

**All n8n Code node code works with `items` array.**

Standard format:
```javascript
// Input
items = [
  { json: { /* your data */ } },
  { json: { /* your data */ } }
];

// Output (MUST return same format)
return [
  { json: { /* transformed data */ } }
];
```

### 3. Context-Aware Processing

**Use actual field names and structure from input schema.**

- ✅ If schema has `userId`, use `userId` (not `id` or `user_id`)
- ✅ If schema has nested `data.items[]`, access via `item.json.data.items`
- ✅ Handle types correctly (numbers vs strings, arrays vs objects)

## Workflow Generation Process

### Step 1: Analyze Input Schema

**What**: Understand the structure of data from parent nodes

**How**: Request sample data or schema if not provided

**Example**:
```
User provides: { "orders": [{ "id": 1, "amount": 150 }] }
Analysis: Root has "orders" array, each order has id (number), amount (number)
Access: item.json.orders[i].amount
```

### Step 2: Understand Transformation Requirement

**What**: Clarify what the user wants to do

**Categories**:
1. **Extract**: Get specific fields
2. **Filter**: Keep only matching items
3. **Transform**: Restructure format
4. **Calculate**: Compute values
5. **Parse**: Extract patterns (emails, URLs)

### Step 3: Generate Code

**Pattern**:
```javascript
return items.map(item => ({
  json: {
    // Transformation here
  }
}));
```

**Always include**:
- Null/undefined checks with optional chaining (`?.`)
- Default values (`|| 'default'`)
- Comments for complex logic

### Step 4: Validate

**Check**:
- ✅ Returns correct n8n format `[{ json: ... }]`
- ✅ Uses actual field names from schema
- ✅ Handles edge cases (empty arrays, null values)

## Common Patterns

### Pattern 1: Field Extraction

**Use case**: Extract specific fields from complex structure

**Template**:
```javascript
return items.map(item => ({
  json: {
    field1: item.json.path?.to?.field1 || 'default',
    field2: item.json.path?.to?.field2
  }
}));
```

### Pattern 2: Filtering

**Use case**: Keep only items matching condition

**Template**:
```javascript
return items.filter(item => {
  return item.json.field operator value;
});
```

### Pattern 3: Data Transformation

**Use case**: Restructure data format

**Template**:
```javascript
return items.map(item => {
  const transformed = /* Transform logic */;
  return { json: transformed };
});
```

### Pattern 4: Aggregation

**Use case**: Calculate aggregate values (sum, average, count)

**Template**:
```javascript
const result = items.reduce((acc, item) => {
  return acc + item.json.numberField;
}, 0);
return [{ json: { result } }];
```

### Pattern 5: String Processing

**Use case**: Extract patterns (emails, URLs) or manipulate text

**Template**:
```javascript
return items.map(item => {
  const text = item.json.textField;
  const pattern = /regex-here/g;
  const matches = text.match(pattern) || [];
  return { json: { matches } };
});
```

### Pattern 6: Nested Array Processing

**Use case**: Flatten or process arrays inside items

**Template**:
```javascript
return items.flatMap(item => {
  return item.json.arrayField.map(element => ({
    json: {
      parent: item.json.parentField,
      ...element
    }
  }));
});
```

**Note**: See `references/code-patterns.md` for 40+ detailed patterns covering all scenarios.

## Critical Rules - ALWAYS FOLLOW

### 1. Always Return n8n Format

**CRITICAL**: Code node MUST return array of items with `json` property

✅ **Correct**:
```javascript
return [{ json: { result: "value" } }];
```

❌ **Wrong**:
```javascript
return { result: "value" };  // Missing array wrapper
return [{ result: "value" }];  // Missing json property
```

### 2. Use Actual Field Names from Schema

✅ **Correct**: Use exact field names from input schema
❌ **Wrong**: Assume field names will be undefined

### 3. Handle Null/Undefined Values

✅ **Correct**:
```javascript
email: item.json.user?.contact?.email || 'no-email@example.com'
```

❌ **Wrong**:
```javascript
email: item.json.user.contact.email  // Crashes if null!
```

### 4. Preserve Item Structure When Filtering

✅ **Correct**:
```javascript
return items.filter(item => item.json.amount > 1000);
```

❌ **Wrong**:
```javascript
return items.filter(...).map(item => item.json);  // Lost wrapper!
```

### 5. Single Item Output Needs Array Wrapper

✅ **Correct**:
```javascript
const total = items.reduce((sum, item) => sum + item.json.amount, 0);
return [{ json: { total } }];  // Array wrapper
```

❌ **Wrong**:
```javascript
return { json: { total } };  // Missing array!
```

## When to Load Reference Files

**For understanding input schema**:
- `references/schema-extraction.md` - Schema extraction and analysis guide

**For code patterns**:
- `references/code-patterns.md` - 40+ transformation patterns library

**For prompt construction**:
- `assets/templates/prompt-templates.md` - Templates for clarifying requirements

**For best practices**:
- `references/best-practices.md` - Error handling, performance, type safety

## Output Format

### 1. Confirm Understanding

Briefly confirm the understood requirements:
- Input data structure (key fields)
- Transformation requirement
- Expected output

### 2. Provide Complete Code

```javascript
// Clear comments explaining logic
return items.map(item => ({
  json: {
    // Transformed data
  }
}));
```

### 3. Explain Key Points (if complex)

- Assumptions made
- Edge cases handled
- How to test with sample data

## Example Generation

**User Request**: "Extract user names and emails from this data"

**Input Schema**:
```json
{
  "users": [
    {
      "profile": {
        "fullName": "Alice Smith",
        "contact": {
          "emailAddress": "alice@example.com"
        }
      }
    }
  ]
}
```

**Response Format**:

"Generate code to extract names and emails from the nested user structure:

```javascript
return items.flatMap(item => {
  // Handle the users array inside each item
  return item.json.users.map(user => ({
    json: {
      name: user.profile?.fullName || 'Unknown',
      email: user.profile?.contact?.emailAddress || 'no-email@example.com'
    }
  }));
});
```

**Key points**:
- Uses `flatMap` to handle nested users array
- Optional chaining (`?.`) prevents errors if fields missing
- Provides default values for missing data
- Returns one item per user"

## Common Mistakes to Avoid

❌ **Mistake 1**: Forgetting array wrapper
```javascript
return { json: { result } };  // WRONG
return [{ json: { result } }];  // RIGHT
```

❌ **Mistake 2**: Assuming field names
```javascript
item.json.id  // WRONG if schema has "userId"
item.json.userId  // RIGHT - uses actual field name
```

❌ **Mistake 3**: No null checks
```javascript
item.json.user.profile.name  // WRONG - crashes if null
item.json.user?.profile?.name || 'Unknown'  // RIGHT
```

❌ **Mistake 4**: Incorrect aggregation return
```javascript
const sum = items.reduce(...);
return sum;  // WRONG
return [{ json: { total: sum } }];  // RIGHT
```

❌ **Mistake 5**: Losing item wrapper in filter
```javascript
return items.filter(...).map(item => item.json);  // WRONG
return items.filter(...);  // RIGHT
```

## Quick Checklist

Before providing code:

- [ ] Analyzed input schema (exact field names and structure)
- [ ] Confirmed transformation requirement
- [ ] Code returns `[{ json: ... }]` format
- [ ] Used actual field names from schema
- [ ] Added null/undefined checks with `?.` or defaults
- [ ] Included comments for complex operations
- [ ] Handles edge cases (empty arrays, missing fields)

## For Complex Scenarios

**Nested Arrays**: See `references/code-patterns.md` section "Array Operations"
**Date Handling**: See "Date and Time" patterns
**Regex Patterns**: See "String Processing" section
**Error Handling**: See `references/best-practices.md`
**Performance**: See "Performance" section in best practices

---

## Resources

### references/
Detailed guides to load as needed:

- `schema-extraction.md` - Understanding input data structure
- `code-patterns.md` - 40+ transformation patterns library (9 categories)
- `prompt-templates.md` - Question templates for clarifying requirements
- `best-practices.md` - Error handling, performance optimization, type safety

Load these references when dealing with complex transformations or unfamiliar patterns.
