# Best Practices for n8n Code Generation

Guidelines for generating robust, maintainable, and error-free code for n8n Code nodes.

## Core Principles

1. **Schema-First**: Always understand input structure before generating code
2. **Fail-Safe**: Handle null/undefined values gracefully
3. **Type-Aware**: Use correct operators for data types
4. **n8n-Native**: Return proper n8n format (`items` array with `json` property)
5. **Self-Documenting**: Add comments for complex logic

---

## 1. Error Handling

### Always Use Optional Chaining

✅ **Good**:
```javascript
const email = item.json.user?.contact?.email || 'no-email@example.com';
```

❌ **Bad**:
```javascript
const email = item.json.user.contact.email;  // Crashes if null!
```

### Provide Default Values

✅ **Good**:
```javascript
return items.map(item => ({
  json: {
    name: item.json.name || 'Unknown',
    score: item.json.score ?? 0,  // Use ?? for 0 values
    tags: item.json.tags || []
  }
}));
```

### Try-Catch for Risky Operations

✅ **Good**:
```javascript
return items.map(item => {
  let parsed;
  try {
    parsed = JSON.parse(item.json.dataString);
  } catch (error) {
    parsed = { error: 'Invalid JSON', raw: item.json.dataString };
  }
  return { json: parsed };
});
```

---

## 2. Type Safety

### Check Types Before Operations

✅ **Good**:
```javascript
return items.filter(item => {
  const amount = item.json.amount;
  return typeof amount === 'number' && amount > 1000;
});
```

### Use Correct Operators for Types

```javascript
// Numbers
item.json.age > 18        // ✅
item.json.age === 18      // ✅

// Strings
item.json.status === 'active'           // ✅ Exact match
item.json.email.includes('@')           // ✅ Contains
item.json.name.startsWith('A')          // ✅ Starts with
item.json.text.toLowerCase().includes() // ✅ Case-insensitive

// Arrays
item.json.tags.includes('urgent')       // ✅ Array contains
item.json.items.length > 0              // ✅ Array not empty
item.json.items.some(i => i.active)     // ✅ Array has matching item

// Booleans
item.json.active === true               // ✅ Explicit
item.json.active                        // ✅ Truthy check
```

---

## 3. Performance

### Optimize Large Datasets

✅ **Efficient** (filter before map):
```javascript
return items
  .filter(item => item.json.active)
  .map(item => ({
    json: { name: item.json.name }
  }));
```

❌ **Inefficient** (map then filter):
```javascript
return items
  .map(item => ({
    json: { name: item.json.name }
  }))
  .filter(item => item.json.active);  // Active check should be first!
```

### Avoid Nested Loops When Possible

✅ **Good** (use Set for O(1) lookup):
```javascript
const activeIds = new Set(item.json.activeUsers.map(u => u.id));
return items.filter(item => activeIds.has(item.json.userId));
```

❌ **Bad** (nested loop O(n²)):
```javascript
return items.filter(item =>
  activeUsers.some(user => user.id === item.json.userId)
);
```

---

## 4. Code Organization

### Add Comments for Complex Logic

✅ **Good**:
```javascript
return items.map(item => {
  // Calculate discount based on tier and amount
  const baseDiscount = item.json.tier === 'premium' ? 0.15 : 0.05;
  const volumeBonus = item.json.amount > 10000 ? 0.10 : 0;
  const finalDiscount = baseDiscount + volumeBonus;

  return {
    json: {
      ...item.json,
      discount: finalDiscount,
      finalAmount: item.json.amount * (1 - finalDiscount)
    }
  };
});
```

### Extract Complex Conditions

✅ **Good**:
```javascript
return items.filter(item => {
  const isHighValue = item.json.amount > 5000;
  const isPriority = item.json.tags.includes('priority');
  const isRecent = new Date(item.json.date) > Date.now() - 86400000;

  return isHighValue && (isPriority || isRecent);
});
```

❌ **Bad**:
```javascript
return items.filter(item =>
  item.json.amount > 5000 &&
  (item.json.tags.includes('priority') ||
   new Date(item.json.date) > Date.now() - 86400000)
);
```

---

## 5. Common Pitfalls

### Pitfall 1: Forgetting Return Array Wrapper

❌ **Wrong**:
```javascript
const result = items.reduce((sum, item) => sum + item.json.amount, 0);
return { json: { total: result } };  // Missing array!
```

✅ **Correct**:
```javascript
const result = items.reduce((sum, item) => sum + item.json.amount, 0);
return [{ json: { total: result } }];  // Array wrapper
```

### Pitfall 2: Modifying Original Data

❌ **Wrong**:
```javascript
return items.map(item => {
  item.json.processed = true;  // Mutates original!
  return item;
});
```

✅ **Correct**:
```javascript
return items.map(item => ({
  json: {
    ...item.json,
    processed: true
  }
}));
```

### Pitfall 3: Incorrect Date Comparison

❌ **Wrong**:
```javascript
return items.filter(item => item.json.date > '2024-01-01');  // String comparison!
```

✅ **Correct**:
```javascript
const cutoffDate = new Date('2024-01-01').getTime();
return items.filter(item => {
  const itemDate = new Date(item.json.date).getTime();
  return itemDate > cutoffDate;
});
```

### Pitfall 4: Case-Sensitive String Comparison

❌ **Wrong**:
```javascript
return items.filter(item => item.json.status === 'active');  // Misses "Active", "ACTIVE"
```

✅ **Correct**:
```javascript
return items.filter(item =>
  item.json.status.toLowerCase() === 'active'
);
```

---

## 6. Testing Checklist

Before finalizing code, mentally test:

- [ ] **Empty array**: What if `items` is `[]`?
- [ ] **Null values**: What if a field is `null` or `undefined`?
- [ ] **Wrong types**: What if number field contains string?
- [ ] **Empty strings**: What if string field is `""`?
- [ ] **Empty arrays**: What if array field is `[]`?
- [ ] **Single item**: Does it work with just one item?
- [ ] **Large dataset**: Will it perform well with 1000+ items?

---

## 7. Code Patterns by Scenario

### Scenario: User Asks to "Extract Names"

**Checklist**:
1. ✅ Confirm exact field path (`user.name` vs `profile.fullName`)
2. ✅ Handle null values with default
3. ✅ Return n8n format
4. ✅ Add comment if nested access

### Scenario: User Asks to "Filter Active Users"

**Checklist**:
1. ✅ Confirm field name and what "active" means
2. ✅ Use correct type comparison (boolean vs string)
3. ✅ Handle missing field
4. ✅ Keep full item structure

### Scenario: User Asks to "Calculate Total"

**Checklist**:
1. ✅ Use `reduce` for aggregation
2. ✅ Wrap result in array
3. ✅ Handle empty array (0 or null?)
4. ✅ Check for non-numeric values

---

## 8. Code Review Questions

Before providing code, ask yourself:

1. **Schema**: Did I use exact field names from the schema?
2. **Null Safety**: Did I add optional chaining or default values?
3. **Return Format**: Does it return `[{ json: ... }]`?
4. **Edge Cases**: What happens with empty/null/undefined?
5. **Type Safety**: Am I using correct operators for data types?
6. **Comments**: Did I add comments for complex logic?
7. **Performance**: Is this efficient for large datasets?

---

## Summary

**Golden Rules**:
1. ✅ Always return `[{ json: ... }]` format
2. ✅ Use optional chaining (`?.`) for nested access
3. ✅ Provide default values (`|| 'default'`)
4. ✅ Use exact field names from schema
5. ✅ Test mentally with edge cases
6. ✅ Add comments for complex operations
7. ✅ Use correct operators for data types
8. ✅ Handle errors gracefully

**Remember**: Good code works not just for happy path, but for all edge cases.
