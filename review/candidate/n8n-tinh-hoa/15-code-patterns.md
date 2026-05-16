# n8n Code Patterns Library

Comprehensive collection of code patterns for n8n Code nodes, covering all common data transformation scenarios.

## Overview

This library provides battle-tested patterns for:
- Data extraction
- Filtering and selection
- Transformation and restructuring
- Aggregation and calculation
- String processing
- Date/time handling
- Business logic

Each pattern includes:
- Template code
- Real-world example
- Input/output samples
- Common variations

---

## Pattern Categories

1. Field Extraction
2. Filtering
3. Data Transformation
4. Aggregation
5. Array Operations
6. String Processing
7. Date and Time
8. Conditional Logic
9. Error Handling

---

## 1. Field Extraction Patterns

### 1.1 Extract Specific Fields

**Use case**: Extract subset of fields from complex object

**Template**:
```javascript
return items.map(item => ({
  json: {
    field1: item.json.path.to.field1,
    field2: item.json.path.to.field2,
    field3: item.json.path.to.field3
  }
}));
```

**Example**: Extract user info
```javascript
// Input: { "user": { "profile": { "name": "Alice", "email": "alice@example.com", "phone": "123-456" } } }
// Output: Just name and email

return items.map(item => ({
  json: {
    name: item.json.user.profile.name,
    email: item.json.user.profile.email
  }
}));
```

### 1.2 Extract from Nested Arrays

**Template**:
```javascript
return items.flatMap(item => {
  return item.json.arrayField.map(element => ({
    json: {
      extracted: element.field
    }
  }));
});
```

**Example**: Extract all order IDs
```javascript
// Input: { "orders": [{"id": 1}, {"id": 2}] }
// Output: Separate item per order

return items.flatMap(item => {
  return item.json.orders.map(order => ({
    json: {
      orderId: order.id
    }
  }));
});
```

### 1.3 Extract with Computed Fields

**Template**:
```javascript
return items.map(item => ({
  json: {
    original: item.json.field,
    computed: /* calculation based on original */
  }
}));
```

**Example**: Add full name
```javascript
// Input: { "firstName": "Alice", "lastName": "Smith" }
// Output: Include fullName

return items.map(item => ({
  json: {
    firstName: item.json.firstName,
    lastName: item.json.lastName,
    fullName: `${item.json.firstName} ${item.json.lastName}`
  }
}));
```

---

## 2. Filtering Patterns

### 2.1 Simple Condition Filter

**Template**:
```javascript
return items.filter(item => {
  return item.json.field operator value;
});
```

**Example**: Filter high-value orders
```javascript
// Keep only orders over $1000
return items.filter(item => {
  return item.json.amount > 1000;
});
```

### 2.2 Multiple Conditions (AND)

**Template**:
```javascript
return items.filter(item => {
  return condition1 && condition2 && condition3;
});
```

**Example**: Filter active premium users
```javascript
return items.filter(item => {
  return item.json.status === 'active' &&
         item.json.plan === 'premium' &&
         item.json.verified === true;
});
```

### 2.3 Multiple Conditions (OR)

**Template**:
```javascript
return items.filter(item => {
  return condition1 || condition2 || condition3;
});
```

**Example**: Filter urgent items
```javascript
return items.filter(item => {
  return item.json.priority === 'urgent' ||
         item.json.dueDate < Date.now() ||
         item.json.flagged === true;
});
```

### 2.4 Filter with String Matching

**Template**:
```javascript
return items.filter(item => {
  const text = item.json.field.toLowerCase();
  return text.includes('search term');
});
```

**Example**: Filter emails containing keyword
```javascript
return items.filter(item => {
  const subject = item.json.subject.toLowerCase();
  return subject.includes('urgent') || subject.includes('important');
});
```

### 2.5 Filter by Array Contents

**Template**:
```javascript
return items.filter(item => {
  return item.json.arrayField.some(element => condition);
});
```

**Example**: Filter users with specific tag
```javascript
return items.filter(item => {
  return item.json.tags.includes('premium');
});
```

---

## 3. Data Transformation Patterns

### 3.1 Restructure Object

**Template**:
```javascript
return items.map(item => ({
  json: {
    // New structure
    newField1: item.json.oldPath.field1,
    newField2: item.json.oldPath.field2
  }
}));
```

**Example**: Flatten nested user structure
```javascript
// Input: { "user": { "profile": { "name": "Alice" }, "account": { "id": 123 } } }
// Output: Flat structure

return items.map(item => ({
  json: {
    userId: item.json.user.account.id,
    userName: item.json.user.profile.name
  }
}));
```

### 3.2 Array to Object (Key-Value Map)

**Template**:
```javascript
const result = {};
items.forEach(item => {
  result[item.json.keyField] = item.json.valueField;
});
return [{ json: result }];
```

**Example**: Create user lookup by ID
```javascript
// Input: [{ "id": 1, "name": "Alice" }, { "id": 2, "name": "Bob" }]
// Output: { "1": "Alice", "2": "Bob" }

const userMap = {};
items.forEach(item => {
  userMap[item.json.id] = item.json.name;
});
return [{ json: userMap }];
```

### 3.3 Group by Field

**Template**:
```javascript
const grouped = {};
items.forEach(item => {
  const key = item.json.groupField;
  if (!grouped[key]) grouped[key] = [];
  grouped[key].push(item.json);
});
return [{ json: grouped }];
```

**Example**: Group orders by customer
```javascript
// Group all orders by customerId
const ordersByCustomer = {};
items.forEach(item => {
  const customerId = item.json.customerId;
  if (!ordersByCustomer[customerId]) {
    ordersByCustomer[customerId] = [];
  }
  ordersByCustomer[customerId].push({
    orderId: item.json.orderId,
    amount: item.json.amount
  });
});
return [{ json: ordersByCustomer }];
```

### 3.4 Pivot/Transpose

**Template**:
```javascript
const pivoted = {};
items.forEach(item => {
  const row = item.json.rowKey;
  const col = item.json.colKey;
  const val = item.json.value;
  if (!pivoted[row]) pivoted[row] = {};
  pivoted[row][col] = val;
});
return [{ json: pivoted }];
```

---

## 4. Aggregation Patterns

### 4.1 Sum

**Template**:
```javascript
const sum = items.reduce((total, item) => {
  return total + item.json.numberField;
}, 0);
return [{ json: { sum } }];
```

**Example**: Total revenue
```javascript
const totalRevenue = items.reduce((sum, item) => {
  return sum + item.json.amount;
}, 0);
return [{ json: { totalRevenue } }];
```

### 4.2 Average

**Template**:
```javascript
const sum = items.reduce((total, item) => total + item.json.field, 0);
const average = sum / items.length;
return [{ json: { average } }];
```

### 4.3 Count

**Template**:
```javascript
const count = items.length;
const conditionalCount = items.filter(item => condition).length;
return [{ json: { total: count, filtered: conditionalCount } }];
```

### 4.4 Min/Max

**Template**:
```javascript
const values = items.map(item => item.json.numberField);
const min = Math.min(...values);
const max = Math.max(...values);
return [{ json: { min, max } }];
```

### 4.5 Count Unique Values

**Template**:
```javascript
const uniqueValues = new Set(items.map(item => item.json.field));
const uniqueCount = uniqueValues.size;
return [{ json: { uniqueCount, values: Array.from(uniqueValues) } }];
```

### 4.6 Group and Aggregate

**Template**:
```javascript
const aggregated = {};
items.forEach(item => {
  const key = item.json.groupField;
  if (!aggregated[key]) {
    aggregated[key] = { count: 0, sum: 0 };
  }
  aggregated[key].count++;
  aggregated[key].sum += item.json.valueField;
});

// Add averages
Object.keys(aggregated).forEach(key => {
  aggregated[key].average = aggregated[key].sum / aggregated[key].count;
});

return [{ json: aggregated }];
```

---

## 5. Array Operations

### 5.1 Flatten Nested Arrays

**Template**:
```javascript
return items.flatMap(item => {
  return item.json.nestedArray.map(element => ({
    json: {
      parent: item.json.parentField,
      ...element
    }
  }));
});
```

### 5.2 Deduplicate

**Template**:
```javascript
const seen = new Set();
return items.filter(item => {
  const key = item.json.uniqueField;
  if (seen.has(key)) return false;
  seen.add(key);
  return true;
});
```

### 5.3 Sort

**Template**:
```javascript
return items.sort((a, b) => {
  return a.json.field - b.json.field;  // Ascending numbers
  // return b.json.field - a.json.field;  // Descending
  // return a.json.field.localeCompare(b.json.field);  // Strings
});
```

### 5.4 Chunk/Batch

**Template**:
```javascript
const batchSize = 10;
const batches = [];
for (let i = 0; i < items.length; i += batchSize) {
  batches.push(items.slice(i, i + batchSize));
}
return [{ json: { batches } }];
```

### 5.5 Join Arrays

**Template**:
```javascript
const joined = items.map(item => {
  return {
    json: {
      ...item.json,
      combined: item.json.array1.concat(item.json.array2)
    }
  };
});
return joined;
```

---

## 6. String Processing Patterns

### 6.1 Extract Email Addresses

**Template**:
```javascript
return items.map(item => {
  const text = item.json.textField;
  const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
  const emails = text.match(emailRegex) || [];
  return { json: { emails } };
});
```

### 6.2 Extract URLs

**Template**:
```javascript
return items.map(item => {
  const text = item.json.textField;
  const urlRegex = /https?:\/\/[^\s]+/g;
  const urls = text.match(urlRegex) || [];
  return { json: { urls } };
});
```

### 6.3 Clean/Normalize Text

**Template**:
```javascript
return items.map(item => {
  let text = item.json.textField;
  text = text.trim();                    // Remove whitespace
  text = text.toLowerCase();             // Lowercase
  text = text.replace(/\s+/g, ' ');      // Normalize spaces
  text = text.replace(/[^\w\s]/g, '');   // Remove special chars
  return { json: { cleaned: text } };
});
```

### 6.4 Split and Parse

**Template**:
```javascript
return items.flatMap(item => {
  const lines = item.json.text.split('\n');
  return lines.map(line => ({
    json: { line: line.trim() }
  }));
});
```

### 6.5 Template String Generation

**Template**:
```javascript
return items.map(item => {
  const message = `Hello ${item.json.name}, your order #${item.json.orderId} totaling $${item.json.amount} is ready!`;
  return {
    json: {
      ...item.json,
      message
    }
  };
});
```

---

## 7. Date and Time Patterns

### 7.1 Parse Date String

**Template**:
```javascript
return items.map(item => {
  const date = new Date(item.json.dateString);
  return {
    json: {
      ...item.json,
      timestamp: date.getTime(),
      isoDate: date.toISOString()
    }
  };
});
```

### 7.2 Format Date

**Template**:
```javascript
return items.map(item => {
  const date = new Date(item.json.timestamp);
  const formatted = date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  return {
    json: {
      ...item.json,
      formattedDate: formatted
    }
  };
});
```

### 7.3 Calculate Date Difference

**Template**:
```javascript
return items.map(item => {
  const start = new Date(item.json.startDate);
  const end = new Date(item.json.endDate);
  const diffMs = end - start;
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  return {
    json: {
      ...item.json,
      durationDays: diffDays
    }
  };
});
```

### 7.4 Filter by Date Range

**Template**:
```javascript
const startDate = new Date('2024-01-01').getTime();
const endDate = new Date('2024-12-31').getTime();

return items.filter(item => {
  const itemDate = new Date(item.json.date).getTime();
  return itemDate >= startDate && itemDate <= endDate;
});
```

---

## 8. Conditional Logic Patterns

### 8.1 If-Else Assignment

**Template**:
```javascript
return items.map(item => ({
  json: {
    ...item.json,
    category: item.json.value > threshold ? 'high' : 'low'
  }
}));
```

### 8.2 Switch-Case Logic

**Template**:
```javascript
return items.map(item => {
  let status;
  switch(item.json.code) {
    case 1: status = 'pending'; break;
    case 2: status = 'approved'; break;
    case 3: status = 'rejected'; break;
    default: status = 'unknown';
  }
  return {
    json: {
      ...item.json,
      status
    }
  };
});
```

### 8.3 Nested Conditions

**Template**:
```javascript
return items.map(item => {
  let tier;
  if (item.json.amount > 10000) {
    tier = 'platinum';
  } else if (item.json.amount > 5000) {
    tier = 'gold';
  } else if (item.json.amount > 1000) {
    tier = 'silver';
  } else {
    tier = 'bronze';
  }
  return {
    json: {
      ...item.json,
      tier
    }
  };
});
```

---

## 9. Error Handling Patterns

### 9.1 Safe Property Access

**Template**:
```javascript
return items.map(item => ({
  json: {
    value: item.json.nested?.deeply?.field || 'default'
  }
}));
```

### 9.2 Try-Catch for Parsing

**Template**:
```javascript
return items.map(item => {
  let parsed;
  try {
    parsed = JSON.parse(item.json.jsonString);
  } catch (error) {
    parsed = { error: 'Invalid JSON' };
  }
  return { json: parsed };
});
```

### 9.3 Type Validation

**Template**:
```javascript
return items.filter(item => {
  return typeof item.json.field === 'number' &&
         !isNaN(item.json.field) &&
         isFinite(item.json.field);
}).map(item => ({
  json: item.json
}));
```

---

## Pattern Selection Guide

| Task | Pattern Category |
|------|------------------|
| Get specific fields | Field Extraction |
| Remove unwanted items | Filtering |
| Change data structure | Transformation |
| Calculate totals/averages | Aggregation |
| Work with lists | Array Operations |
| Process text | String Processing |
| Handle dates | Date and Time |
| Apply business rules | Conditional Logic |
| Prevent errors | Error Handling |

---

## Summary

**Remember**:
- Start with schema analysis
- Choose appropriate pattern
- Add error handling
- Test with edge cases
- Return correct n8n format

**Most Common Patterns** (80% of use cases):
1. Field extraction
2. Filtering
3. Simple transformation
4. Aggregation (sum/count)
5. String processing
