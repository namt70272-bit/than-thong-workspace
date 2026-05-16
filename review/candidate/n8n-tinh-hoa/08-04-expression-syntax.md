# n8n Expression Syntax Guide

Guide for writing and using expressions in n8n workflows.

## Overview

n8n expressions allow you to reference data from previous nodes, perform calculations, and manipulate data dynamically.

## Basic Syntax

### Expression Format

All expressions MUST follow this format:

```
={{ expression_code }}
```

**CRITICAL Rules:**
- ALWAYS use `=` before the double curly braces
- ALWAYS use DOUBLE curly braces `{{` `}}`, never single
- NEVER use emojis or special characters inside node names that are referenced
- NEVER omit the equals sign

**Examples:**
- ✅ CORRECT: `={{ $('Previous Node').item.json.field }}`
- ❌ INCORRECT: `{ $('Node').item.json.field }` (missing `=`, single braces)
- ❌ INCORRECT: `{{ $('Node').item.json.field }}` (missing `=`)
- ❌ INCORRECT: `={{ $('👍 Node').item.json.field }}` (contains emoji)

## Referencing Node Data

### Basic Node Reference

Access data from a specific node:

```javascript
={{ $('Node Name').item.json.fieldName }}
```

**Components:**
- `$('Node Name')`: Reference to the node by its display name
- `.item`: Current item being processed
- `.json`: JSON data of the item
- `.fieldName`: Specific field within the JSON

### Accessing Different Data Levels

**First item:**
```javascript
={{ $('Node Name').first().json.fieldName }}
```

**Last item:**
```javascript
={{ $('Node Name').last().json.fieldName }}
```

**All items:**
```javascript
={{ $('Node Name').all() }}
```

**Specific item by index:**
```javascript
={{ $('Node Name').item(0).json.fieldName }}
```

### Nested Field Access

**Simple nested field:**
```javascript
={{ $('Node Name').item.json.user.email }}
```

**Array access:**
```javascript
={{ $('Node Name').item.json.items[0].name }}
```

**Deep nesting:**
```javascript
={{ $('Node Name').item.json.data.users[0].profile.email }}
```

## Common Expression Patterns

### String Operations

**Concatenation:**
```javascript
="Order #{{ $('Set').item.json.orderId }} processed"
```

**String methods:**
```javascript
={{ $('Node').item.json.text.toLowerCase() }}
={{ $('Node').item.json.text.toUpperCase() }}
={{ $('Node').item.json.text.trim() }}
={{ $('Node').item.json.text.replace('old', 'new') }}
```

### Number Operations

**Arithmetic:**
```javascript
={{ $('Set').item.json.quantity * $('Set').item.json.price }}
={{ $('Node').item.json.total + 100 }}
={{ $('Node').item.json.value / 2 }}
```

**Number formatting:**
```javascript
={{ $('Node').item.json.price.toFixed(2) }}
={{ Math.round($('Node').item.json.value) }}
={{ Math.floor($('Node').item.json.value) }}
```

### Array Operations

**Map:**
```javascript
={{ $('Node').item.json.items.map(item => item.name) }}
```

**Filter:**
```javascript
={{ $('Node').item.json.items.filter(item => item.active) }}
```

**Join:**
```javascript
={{ $('Node').item.json.tags.join(', ') }}
```

**Length:**
```javascript
={{ $('Node').item.json.items.length }}
```

### Object Operations

**JSON stringify:**
```javascript
={{ JSON.stringify($('Node').item.json.userData) }}
```

**JSON parse:**
```javascript
={{ JSON.parse($('Node').item.json.jsonString) }}
```

**Object keys:**
```javascript
={{ Object.keys($('Node').item.json.data) }}
```

**Object values:**
```javascript
={{ Object.values($('Node').item.json.data) }}
```

## Built-in Variables and Functions

### Date and Time

**Current date/time:**
```javascript
={{ $now }}
={{ $now.toISO() }}
={{ $now.toFormat('yyyy-MM-dd') }}
```

**Today (start of day):**
```javascript
={{ $today }}
```

**Timezone:**
```javascript
={{ $timezone }}
```

### Utility Functions

**Generate random string:**
```javascript
={{ $('Node').item.json.id || Math.random().toString(36).substr(2, 9) }}
```

**Conditional (ternary):**
```javascript
={{ $('Node').item.json.count > 10 ? 'high' : 'low' }}
```

**Null coalescing:**
```javascript
={{ $('Node').item.json.field ?? 'default value' }}
```

## Special Contexts

### Credentials

Access stored credentials:

```javascript
={{ $credentials.apiKey }}
={{ $credentials.username }}
```

### Environment Variables

Access environment variables:

```javascript
={{ $env.API_URL }}
={{ $env.DATABASE_NAME }}
```

### Workflow Configuration Node

Reference centralized configuration:

```javascript
={{ $('Workflow Configuration').first().json.apiUrl }}
={{ $('Workflow Configuration').first().json.maxRetries }}
```

## Advanced Patterns

### Complex Conditionals

**If-else logic:**
```javascript
={{
  $('Node').item.json.status === 'active' ?
    'Proceed' :
    $('Node').item.json.status === 'pending' ?
      'Wait' :
      'Error'
}}
```

**Multiple conditions:**
```javascript
={{
  $('Node').item.json.score > 80 && $('Node').item.json.verified
    ? 'approved'
    : 'rejected'
}}
```

### Data Transformation

**Transform object:**
```javascript
={{
  JSON.stringify({
    id: $('HTTP Request').item.json.userId,
    name: $('HTTP Request').item.json.fullName,
    email: $('HTTP Request').item.json.emailAddress
  })
}}
```

**Filter and map:**
```javascript
={{
  $('Node').item.json.users
    .filter(user => user.active)
    .map(user => user.email)
    .join(', ')
}}
```

## Common Mistakes to Avoid

### 1. Missing Equals Sign

❌ WRONG:
```javascript
{{ $('Node').item.json.field }}
```

✅ CORRECT:
```javascript
={{ $('Node').item.json.field }}
```

### 2. Single Curly Braces

❌ WRONG:
```javascript
={ $('Node').item.json.field }
```

✅ CORRECT:
```javascript
={{ $('Node').item.json.field }}
```

### 3. Using Emojis in Node Names

❌ WRONG:
```javascript
={{ $('✅ Validation').item.json.result }}
```

✅ CORRECT:
```javascript
={{ $('Validation').item.json.result }}
```

### 4. Incorrect Data Access Path

❌ WRONG:
```javascript
={{ $('Node').json.field }}  // Missing .item
```

✅ CORRECT:
```javascript
={{ $('Node').item.json.field }}
```

### 5. Not Stringifying Objects/Arrays

When setting object/array values in Set node:

❌ WRONG:
```javascript
value: { name: "John" }  // Direct object
```

✅ CORRECT:
```javascript
value: "={{ JSON.stringify({ name: 'John' }) }}"  // Stringified
```

## Best Practices

1. **Use descriptive node names** - Easier to reference in expressions
2. **Test expressions** - Use the expression editor to verify syntax
3. **Handle null/undefined** - Use null coalescing `??` or optional chaining `?.`
4. **Keep expressions readable** - Break complex logic into multiple nodes
5. **Use Workflow Configuration** - Centralize reusable values
6. **Comment complex expressions** - Add node descriptions explaining logic
7. **Avoid hardcoding** - Use expressions to reference dynamic data
8. **Type safety** - Ensure data types match expected formats

## Expression Editor Tips

- Use the built-in expression editor in n8n UI for testing
- Hover over variables to see available properties
- Use autocomplete (Ctrl+Space) for suggestions
- Check the sample output to verify results
- Test with real data when possible
