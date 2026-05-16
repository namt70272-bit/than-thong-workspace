# Switch Node Advanced Patterns

This document covers the advanced configuration patterns for the Switch node in n8n workflows, including dynamic output creation and complex conditional routing.

## Source
Extracted from:
- `packages/@n8n/ai-workflow-builder.ee/src/prompts/agents/builder.prompt.ts` (SWITCH_NODE_PATTERN)
- `packages/@n8n/ai-workflow-builder.ee/src/prompts/agents/configurator.prompt.ts` (SWITCH_NODE_CONFIGURATION)

---

## Overview

The Switch node in n8n provides dynamic routing capabilities where:
- The number of outputs is **determined by parameter values**
- Each output branch can have its own conditions
- Supports complex multi-condition logic

**Critical Understanding**: Switch nodes have **dynamic outputs** - the outputs don't exist until you configure the rules.

---

## Basic Concept

### Traditional Nodes vs Switch Node

**Traditional nodes** (HTTP Request, Set, Code):
- Fixed inputs and outputs
- Structure defined by node type

**Switch node**:
- Dynamic number of outputs
- Outputs created by `rules.values[]` array
- Each entry in the array = one output branch

---

## Connection Parameters

When adding a Switch node, you must specify connection parameters to create the output structure:

```javascript
{
  "mode": "rules",  // CRITICAL - enables rule-based routing
  "rules": {
    "values": [
      // Each object here creates ONE output
    ]
  }
}
```

**Why this matters**:
- Without `mode: "rules"`, the node won't route correctly
- The `rules.values[]` array determines how many outputs exist
- Other nodes can't connect to outputs that don't exist yet

---

## Complete rules.values[] Structure

Each entry in `rules.values[]` creates one output branch with this structure:

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
        "leftValue": "",
        "rightValue": "",
        "operator": {
          "type": "string|number|boolean|dateTime|array|object",
          "operation": "equals|notEquals|contains|gt|gte|lt|lte|..."
        }
      }
    ],
    "combinator": "and|or"
  },
  "renameOutput": true,
  "outputKey": "Descriptive Output Label"
}
```

---

## Two-Phase Workflow Creation

### Phase 1: Builder Agent (Structure Creation)

The Builder creates the **skeleton** with placeholder conditions:

```json
{
  "mode": "rules",
  "rules": {
    "values": [
      {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "leftValue": "",    // Empty - to be filled by Configurator
              "rightValue": "",   // Empty - to be filled by Configurator
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "High Priority"  // Descriptive label
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "leftValue": "",
              "rightValue": "",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Medium Priority"
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "leftValue": "",
              "rightValue": "",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Low Priority"
      }
    ]
  }
}
```

**Key Points**:
- **3 entries** = **3 outputs**
- `leftValue` and `rightValue` are empty placeholders
- `outputKey` provides descriptive labels
- Structure is ready for connections

### Phase 2: Configurator Agent (Fill Conditions)

The Configurator fills in the actual conditions:

```json
{
  "conditions": [
    {
      "leftValue": "={{ $json.priority }}",  // Now filled
      "rightValue": "high",                    // Now filled
      "operator": {
        "type": "string",
        "operation": "equals"
      }
    }
  ]
}
```

---

## Pattern 1: String Equality Routing

**Use case**: Route by status, category, type, etc.

**Example**: Route support tickets by priority

```json
{
  "mode": "rules",
  "rules": {
    "values": [
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "leftValue": "={{ $json.priority }}",
              "rightValue": "urgent",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Urgent Tickets"
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "leftValue": "={{ $json.priority }}",
              "rightValue": "normal",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Normal Tickets"
      }
    ]
  }
}
```

---

## Pattern 2: Numeric Range Routing

**Use case**: Route by amount, score, age, quantity ranges.

**Critical Technique**: Use TWO conditions with `combinator: "and"` for ranges.

**Example**: Route transactions by amount ranges

```json
{
  "mode": "rules",
  "rules": {
    "values": [
      {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "leftValue": "={{ $json.amount }}",
              "rightValue": 1000,
              "operator": {
                "type": "number",
                "operation": "gte"  // Greater than or equal
              }
            },
            {
              "leftValue": "={{ $json.amount }}",
              "rightValue": 5000,
              "operator": {
                "type": "number",
                "operation": "lte"  // Less than or equal
              }
            }
          ],
          "combinator": "and"  // BOTH conditions must be true
        },
        "renameOutput": true,
        "outputKey": "$1000-$5000"
      },
      {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "leftValue": "={{ $json.amount }}",
              "rightValue": 5000,
              "operator": {
                "type": "number",
                "operation": "gt"  // Greater than
              }
            }
          ],
          "combinator": "and"
        },
        "renameOutput": true,
        "outputKey": "Over $5000"
      }
    ]
  }
}
```

**Range Pattern Breakdown**:
```
$1000-$5000 range:
  Condition 1: amount >= 1000  (gte)
  Condition 2: amount <= 5000  (lte)
  Combinator: "and" (both must be true)
```

---

## Pattern 3: Multiple Conditions (AND Logic)

**Use case**: Route when multiple criteria must all be met.

**Example**: Route orders requiring special handling

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
        "leftValue": "={{ $json.amount }}",
        "rightValue": 10000,
        "operator": {
          "type": "number",
          "operation": "gt"
        }
      },
      {
        "leftValue": "={{ $json.isPriority }}",
        "operator": {
          "type": "boolean",
          "operation": "true"
        }
      },
      {
        "leftValue": "={{ $json.region }}",
        "rightValue": "US",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      }
    ],
    "combinator": "and"  // ALL three conditions must be true
  },
  "renameOutput": true,
  "outputKey": "High Value US Priority"
}
```

---

## Pattern 4: Multiple Conditions (OR Logic)

**Use case**: Route when any of several criteria is met.

**Example**: Route urgent communications

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
        "leftValue": "={{ $json.priority }}",
        "rightValue": "urgent",
        "operator": {
          "type": "string",
          "operation": "equals"
        }
      },
      {
        "leftValue": "={{ $json.subject }}",
        "rightValue": "CRITICAL",
        "operator": {
          "type": "string",
          "operation": "contains"
        }
      },
      {
        "leftValue": "={{ $json.senderVIP }}",
        "operator": {
          "type": "boolean",
          "operation": "true"
        }
      }
    ],
    "combinator": "or"  // ANY condition being true routes here
  },
  "renameOutput": true,
  "outputKey": "Urgent Communications"
}
```

---

## Complete 3-Way Routing Example

**Scenario**: Route customer feedback by sentiment score

**Node Name**: "Route by Sentiment"

**Builder Phase** (create structure):
```json
{
  "nodeType": "n8n-nodes-base.switch",
  "name": "Route by Sentiment",
  "connectionParameters": {
    "mode": "rules",
    "rules": {
      "values": [
        {
          "conditions": {
            "options": {
              "caseSensitive": true,
              "leftValue": "",
              "typeValidation": "strict"
            },
            "conditions": [
              {
                "leftValue": "",
                "rightValue": "",
                "operator": {
                  "type": "number",
                  "operation": "gte"
                }
              }
            ],
            "combinator": "and"
          },
          "renameOutput": true,
          "outputKey": "Positive Feedback"
        },
        {
          "conditions": {
            "options": {
              "caseSensitive": true,
              "leftValue": "",
              "typeValidation": "strict"
            },
            "conditions": [
              {
                "leftValue": "",
                "rightValue": "",
                "operator": {
                  "type": "number",
                  "operation": "gte"
                }
              },
              {
                "leftValue": "",
                "rightValue": "",
                "operator": {
                  "type": "number",
                  "operation": "lte"
                }
              }
            ],
            "combinator": "and"
          },
          "renameOutput": true,
          "outputKey": "Neutral Feedback"
        },
        {
          "conditions": {
            "options": {
              "caseSensitive": true,
              "leftValue": "",
              "typeValidation": "strict"
            },
            "conditions": [
              {
                "leftValue": "",
                "rightValue": "",
                "operator": {
                  "type": "number",
                  "operation": "lt"
                }
              }
            ],
            "combinator": "and"
          },
          "renameOutput": true,
          "outputKey": "Negative Feedback"
        }
      ]
    }
  }
}
```

**Configurator Phase** (fill conditions):
```javascript
// Instructions for update_node_parameters:
[
  "Set first rule leftValue to ={{ $json.sentimentScore }}",
  "Set first rule rightValue to 7",
  "Set second rule first leftValue to ={{ $json.sentimentScore }}",
  "Set second rule first rightValue to 4",
  "Set second rule second leftValue to ={{ $json.sentimentScore }}",
  "Set second rule second rightValue to 7",
  "Set third rule leftValue to ={{ $json.sentimentScore }}",
  "Set third rule rightValue to 4"
]
```

**Result**:
- Output 1: sentiment >= 7 → Positive Feedback
- Output 2: sentiment >= 4 AND sentiment <= 7 → Neutral Feedback
- Output 3: sentiment < 4 → Negative Feedback

---

## Options Configuration

### caseSensitive
- `true`: "Hello" ≠ "hello"
- `false`: "Hello" = "hello"
- **Use for**: String comparisons where case matters

### typeValidation
- `"strict"`: Enforces type matching (number ≠ "123")
- `"loose"`: Allows type coercion (number = "123")
- **Recommendation**: Use "strict" for numbers, "loose" for mixed data

### leftValue (at options level)
- Usually left empty (`""`)
- Can be used for default evaluation context

---

## Operator Types and Operations

### String Operators
```json
{
  "type": "string",
  "operation": "equals|notEquals|contains|notContains|startsWith|endsWith|regex"
}
```

### Number Operators
```json
{
  "type": "number",
  "operation": "equals|notEquals|gt|gte|lt|lte"
}
```

**Common Operations**:
- `equals`: = (exact match)
- `notEquals`: ≠
- `gt`: > (greater than)
- `gte`: >= (greater than or equal)
- `lt`: < (less than)
- `lte`: <= (less than or equal)

### Boolean Operators
```json
{
  "type": "boolean",
  "operation": "true|false|equals|notEquals"
}
```

### DateTime Operators
```json
{
  "type": "dateTime",
  "operation": "before|after|equals"
}
```

---

## Best Practices

### 1. Always Set renameOutput: true
```json
{
  "renameOutput": true,
  "outputKey": "Descriptive Name"
}
```

**Why**: Makes the workflow self-documenting and easier to understand.

### 2. Use Descriptive outputKey Labels
❌ Bad:
- "Output 1", "Output 2", "Output 3"

✅ Good:
- "High Priority Orders"
- "Medium Priority Orders"
- "Low Priority Orders"

### 3. Use Descriptive Node Names
❌ Bad: "Switch"
✅ Good: "Route by Order Amount", "Route by Status"

### 4. Create Structure First, Configure Later
- Builder: Create with placeholder conditions
- Configurator: Fill in actual values
- This enables proper connection planning

### 5. Use Strict Type Validation for Numbers
```json
{
  "typeValidation": "strict"
}
```

**Why**: Prevents "100" (string) from matching 100 (number).

### 6. For Ranges, Always Use Two Conditions with AND
```json
{
  "conditions": [
    { "operation": "gte", "rightValue": 100 },
    { "operation": "lte", "rightValue": 500 }
  ],
  "combinator": "and"
}
```

---

## Common Mistakes

### ❌ Mistake 1: Forgetting mode: "rules"
```json
{
  // Missing mode parameter - won't work correctly
  "rules": {
    "values": [...]
  }
}
```

✅ Correct:
```json
{
  "mode": "rules",  // REQUIRED
  "rules": {
    "values": [...]
  }
}
```

### ❌ Mistake 2: Single Condition for Ranges
```json
{
  // Only checks >= 100, no upper bound!
  "conditions": [
    { "leftValue": "={{ $json.amount }}", "rightValue": 100, "operation": "gte" }
  ]
}
```

✅ Correct:
```json
{
  // Checks >= 100 AND <= 500
  "conditions": [
    { "leftValue": "={{ $json.amount }}", "rightValue": 100, "operation": "gte" },
    { "leftValue": "={{ $json.amount }}", "rightValue": 500, "operation": "lte" }
  ],
  "combinator": "and"
}
```

### ❌ Mistake 3: Wrong Operator Type
```json
{
  "leftValue": "={{ $json.age }}",  // age is a number
  "rightValue": 18,
  "operator": {
    "type": "string",  // WRONG - should be "number"
    "operation": "equals"
  }
}
```

✅ Correct:
```json
{
  "leftValue": "={{ $json.age }}",
  "rightValue": 18,
  "operator": {
    "type": "number",  // Matches the data type
    "operation": "gte"
  }
}
```

### ❌ Mistake 4: Not Setting renameOutput
```json
{
  "renameOutput": false  // Outputs will be "0", "1", "2"
}
```

✅ Correct:
```json
{
  "renameOutput": true,
  "outputKey": "High Priority"  // Clear, descriptive label
}
```

---

## Quick Reference: Routing Patterns

### By String Field
```json
{
  "leftValue": "={{ $json.status }}",
  "rightValue": "approved",
  "operator": { "type": "string", "operation": "equals" }
}
```

### By Boolean
```json
{
  "leftValue": "={{ $json.isActive }}",
  "operator": { "type": "boolean", "operation": "true" }
}
```

### By Number Threshold
```json
{
  "leftValue": "={{ $json.score }}",
  "rightValue": 80,
  "operator": { "type": "number", "operation": "gte" }
}
```

### By Number Range
```json
{
  "conditions": [
    { "leftValue": "={{ $json.score }}", "rightValue": 60, "operator": { "type": "number", "operation": "gte" } },
    { "leftValue": "={{ $json.score }}", "rightValue": 80, "operator": { "type": "number", "operation": "lt" } }
  ],
  "combinator": "and"
}
```

### By Multiple Criteria (AND)
```json
{
  "conditions": [
    { "leftValue": "={{ $json.priority }}", "rightValue": "high", "operator": { "type": "string", "operation": "equals" } },
    { "leftValue": "={{ $json.amount }}", "rightValue": 1000, "operator": { "type": "number", "operation": "gt" } }
  ],
  "combinator": "and"
}
```

### By Multiple Criteria (OR)
```json
{
  "conditions": [
    { "leftValue": "={{ $json.urgent }}", "operator": { "type": "boolean", "operation": "true" } },
    { "leftValue": "={{ $json.vip }}", "operator": { "type": "boolean", "operation": "true" } }
  ],
  "combinator": "or"
}
```

---

## Summary

**Key Takeaways**:
1. Switch nodes have **dynamic outputs** based on `rules.values[]` array
2. **Always set** `mode: "rules"` in connection parameters
3. **Each entry** in `rules.values[]` creates **one output**
4. **Ranges require TWO conditions** with `combinator: "and"`
5. **Always use** `renameOutput: true` with descriptive `outputKey`
6. **Builder creates structure**, **Configurator fills conditions**
7. **Match operator type** to data type (number/string/boolean)

**When to Use Switch vs IF**:
- **IF node**: 2 outputs (true/false)
- **Switch node**: 3+ outputs with complex routing logic
