# Branching and Merging Deep Dive

This document provides an in-depth understanding of how branching and merging work in n8n workflows, including execution order, data flow, and the proper use of Merge nodes.

## Source
Extracted from: `packages/@n8n/ai-workflow-builder.ee/src/prompts/agents/builder.prompt.ts` (BRANCHING and MERGING sections)

---

## Overview

Understanding branching and merging is crucial for building correct n8n workflows. Many workflow bugs stem from misunderstanding how data flows through branches.

**Key Concepts**:
1. **Branching**: One node output connects to multiple nodes
2. **Execution Order**: Determined by canvas position (depth-first)
3. **Merging Without Merge Node**: Multiple executions (runs)
4. **Merging With Merge Node**: Combined data in single execution

---

## Part 1: Branching

### What Is Branching?

**Branching occurs when one node's output connects to multiple nodes.**

```
        ┌─→ Node B
Node A ─┤
        └─→ Node C
```

---

### Execution Behavior

**When A branches to B and C:**
1. **Both B and C execute** with the same data from A
2. **Execution is parallel** (conceptually)
3. **Order is deterministic** based on canvas position

---

### Execution Order Rule

**The highest node (lowest Y-coordinate) on the canvas executes first.**

**Example**:
```
         Y=100  ┌─→ Node B (executes FIRST)
Node A ─────────┤
         Y=200  └─→ Node C (executes SECOND)
```

If Node B is positioned higher on the canvas (Y=100) than Node C (Y=200), then:
1. Node B executes first
2. All nodes downstream of B execute (depth-first)
3. Then Node C executes
4. All nodes downstream of C execute

---

### Depth-First Execution

**n8n uses depth-first execution for branches.**

**Example workflow**:
```
         ┌─→ Node B ─→ Node D
Node A ─┤
         └─→ Node C ─→ Node E
```

**If B is higher than C on canvas**:

**Execution order**:
1. Node A
2. Node B (higher branch)
3. Node D (complete B's branch first)
4. Node C (lower branch)
5. Node E (complete C's branch)

**Not**:
1. Node A
2. Node B
3. Node C ← Wrong! (would be breadth-first)
4. Node D
5. Node E

---

### Routing Nodes (IF, Switch)

**Special behavior**: Routing nodes apply conditions to EACH input item independently.

**Example with IF node**:
```
Node A (3 items) ─→ IF Node ─→ True branch
                            └─→ False branch
```

**If Node A outputs**:
```json
[
  { "score": 85 },  // Item 1
  { "score": 45 },  // Item 2
  { "score": 92 }   // Item 3
]
```

**IF condition**: `score > 70`

**Result**:
- True branch receives: Items 1 and 3 (score 85, 92)
- False branch receives: Item 2 (score 45)

**Both branches can execute in the same workflow execution** if items route to different branches.

---

### Branching Patterns

#### Pattern 1: Parallel Processing

**Use case**: Process data through different transformations simultaneously

```
              ┌─→ Transform A ─→ Save to Database
HTTP Request ─┤
              └─→ Transform B ─→ Send Email
```

**Behavior**:
- Transform A and Database save complete first (if A is higher)
- Then Transform B and Email send execute
- Same source data used for both branches

---

#### Pattern 2: Conditional Split

**Use case**: Route items to different destinations based on criteria

```
                  ┌─→ True ─→ Send to Sales Team
Fetch Leads ─→ IF Node
                  └─→ False ─→ Send to Marketing Team
```

**Behavior**:
- Each lead evaluated individually
- High-value leads → Sales
- Other leads → Marketing
- Both branches can execute in same run

---

#### Pattern 3: Multi-Destination Broadcasting

**Use case**: Send same data to multiple systems

```
           ┌─→ Save to CRM
Webhook ─→─┼─→ Log to Database
           └─→ Send Notification
```

**Behavior**:
- All three destinations receive identical data
- Executes in order of canvas position
- Each branch is independent

---

## Part 2: Merging (Without Merge Node)

### What Happens Without Merge Node?

**When multiple nodes connect to the same target, the target executes MULTIPLE TIMES (runs).**

```
Node A ─┐
        ├─→ Node C (executes TWICE)
Node B ─┘
```

---

### The Two-Run Behavior

**Node C executes as two separate runs**:

**Run 1**:
- Input: Data from Node A
- Node C processes this data
- Downstream nodes process Run 1 data

**Run 2**:
- Input: Data from Node B
- Node C processes this data
- Downstream nodes process Run 2 data

**CRITICAL**: Run 1 and Run 2 are **independent** - no data mixing occurs.

---

### Visualizing Two Runs

```
Node A (3 items) ─┐
                  ├─→ Node C ─→ Node D
Node B (2 items) ─┘

Execution:
  Run 1:
    Node C receives 3 items from A
    Node C outputs 3 processed items
    Node D receives these 3 items

  Run 2:
    Node C receives 2 items from B
    Node C outputs 2 processed items
    Node D receives these 2 items
```

**In workflow execution view**: You'll see Node C with "2 runs" indicated.

---

### When Is This Useful?

**Scenario 1: Processing from multiple sources separately**

```
Fetch Users ─┐
             ├─→ Transform ─→ Save to Database
Fetch Admins ─┘
```

**Result**:
- Users processed and saved (Run 1)
- Admins processed and saved (Run 2)
- Logged separately in database

**Scenario 2: Error handling with fallback**

```
Primary API ─┐
             ├─→ Process Data
Fallback API ─┘
```

**Result**:
- If Primary API returns data → Run 1
- If Fallback API returns data → Run 2
- Both might execute if both APIs return data

---

### When Is This NOT Wanted?

**Problem**: Want to combine data from both branches, not process separately.

**Example - WRONG approach**:
```
Fetch Product Details ─┐
                       ├─→ Create Report (Want COMBINED data!)
Fetch Pricing Info ────┘
```

**Result with no Merge node**:
- Report Run 1: Only has product details
- Report Run 2: Only has pricing info
- **NEVER get combined data in one report**

**Solution**: Use Merge node (see Part 3)

---

## Part 3: Merging (With Merge Node)

### What Is Merge Node?

**Merge node combines data from multiple branches into a single execution.**

```
Node A ─┐
        ├─→ Merge ─→ Node C (executes ONCE with combined data)
Node B ─┘
```

**Key Difference**:
- **Without Merge**: Node C executes twice (2 runs)
- **With Merge**: Node C executes once with merged data (1 run)

---

### Merge Node Modes

The Merge node supports 6 different operations, each serving a specific use case.

---

### Mode 1: Union (Append)

**SQL Equivalent**: `UNION ALL`

**Configuration**:
- Mode: `append`

**Behavior**: Combines all items from both inputs into one array.

**Example**:

**Input 1** (3 items):
```json
[
  { "name": "Alice", "score": 85 },
  { "name": "Bob", "score": 90 },
  { "name": "Charlie", "score": 78 }
]
```

**Input 2** (2 items):
```json
[
  { "name": "David", "score": 92 },
  { "name": "Eve", "score": 88 }
]
```

**Output** (5 items):
```json
[
  { "name": "Alice", "score": 85 },
  { "name": "Bob", "score": 90 },
  { "name": "Charlie", "score": 78 },
  { "name": "David", "score": 92 },
  { "name": "Eve", "score": 88 }
]
```

**Use Cases**:
- Combining results from multiple API calls
- Aggregating data from different sources
- Creating a complete dataset from partial sources

---

### Mode 2: Inner Join (Keep Matches)

**SQL Equivalent**: `INNER JOIN`

**Configuration**:
- Mode: `combine`
- Combine by: `Matching fields`
- Output type: `Keep matches`

**Behavior**: Returns only items that have matching field values in both inputs.

**Example**:

**Input 1** (Users):
```json
[
  { "id": 1, "name": "Alice" },
  { "id": 2, "name": "Bob" },
  { "id": 3, "name": "Charlie" }
]
```

**Input 2** (Orders):
```json
[
  { "userId": 1, "orderId": 101 },
  { "userId": 2, "orderId": 102 },
  { "userId": 4, "orderId": 103 }
]
```

**Match Field**: `id` (Input 1) = `userId` (Input 2)

**Output** (2 items - only matching):
```json
[
  { "id": 1, "name": "Alice", "userId": 1, "orderId": 101 },
  { "id": 2, "name": "Bob", "userId": 2, "orderId": 102 }
]
```

**Note**: Charlie (id:3) excluded (no matching order). Order for userId:4 excluded (no matching user).

**Use Cases**:
- Find users who made purchases
- Match customers with support tickets
- Identify products with reviews

---

### Mode 3: Left Join (Enrich Input 1)

**SQL Equivalent**: `LEFT JOIN`

**Configuration**:
- Mode: `combine`
- Combine by: `Matching fields`
- Output type: `Enrich input 1`

**Behavior**: Returns ALL items from Input 1, adding matching data from Input 2 when available.

**Example**:

**Input 1** (Users):
```json
[
  { "id": 1, "name": "Alice" },
  { "id": 2, "name": "Bob" },
  { "id": 3, "name": "Charlie" }
]
```

**Input 2** (Orders):
```json
[
  { "userId": 1, "orderId": 101 },
  { "userId": 4, "orderId": 103 }
]
```

**Match Field**: `id` (Input 1) = `userId` (Input 2)

**Output** (3 items - all from Input 1):
```json
[
  { "id": 1, "name": "Alice", "userId": 1, "orderId": 101 },
  { "id": 2, "name": "Bob" },  // No matching order
  { "id": 3, "name": "Charlie" }  // No matching order
]
```

**Use Cases**:
- Enrich user records with optional order data
- Add LinkedIn data to contacts (when available)
- Augment products with optional review scores

---

### Mode 4: Right Join (Enrich Input 2)

**SQL Equivalent**: `RIGHT JOIN`

**Configuration**:
- Mode: `combine`
- Combine by: `Matching fields`
- Output type: `Enrich input 2`

**Behavior**: Returns ALL items from Input 2, adding matching data from Input 1 when available.

**Example**:

**Input 1** (Users):
```json
[
  { "id": 1, "name": "Alice" }
]
```

**Input 2** (Orders):
```json
[
  { "userId": 1, "orderId": 101 },
  { "userId": 2, "orderId": 102 },
  { "userId": 3, "orderId": 103 }
]
```

**Output** (3 items - all from Input 2):
```json
[
  { "userId": 1, "orderId": 101, "id": 1, "name": "Alice" },
  { "userId": 2, "orderId": 102 },  // No matching user
  { "userId": 3, "orderId": 103 }   // No matching user
]
```

**Use Cases**:
- List all orders with customer details (when available)
- Show all tickets with assignee info (when assigned)

---

### Mode 5: Outer Join (Keep Everything)

**SQL Equivalent**: `FULL OUTER JOIN`

**Configuration**:
- Mode: `combine`
- Combine by: `Matching fields`
- Output type: `Keep everything`

**Behavior**: Returns ALL items from both inputs, combining when match found.

**Example**:

**Input 1** (Users):
```json
[
  { "id": 1, "name": "Alice" },
  { "id": 2, "name": "Bob" }
]
```

**Input 2** (Orders):
```json
[
  { "userId": 1, "orderId": 101 },
  { "userId": 3, "orderId": 102 }
]
```

**Output** (3 items - all from both):
```json
[
  { "id": 1, "name": "Alice", "userId": 1, "orderId": 101 },  // Matched
  { "id": 2, "name": "Bob" },  // From Input 1, no match
  { "userId": 3, "orderId": 102 }  // From Input 2, no match
]
```

**Use Cases**:
- Complete reconciliation of two datasets
- Identifying all records regardless of match status
- Audit comparisons

---

### Mode 6: Cross Join (All Combinations)

**SQL Equivalent**: `CROSS JOIN`

**Configuration**:
- Mode: `combine`
- Combine by: `All possible combinations`

**Behavior**: Creates EVERY possible combination of items from both inputs.

**Example**:

**Input 1** (Sizes):
```json
[
  { "size": "S" },
  { "size": "M" }
]
```

**Input 2** (Colors):
```json
[
  { "color": "Red" },
  { "color": "Blue" }
]
```

**Output** (4 items - 2 × 2 combinations):
```json
[
  { "size": "S", "color": "Red" },
  { "size": "S", "color": "Blue" },
  { "size": "M", "color": "Red" },
  { "size": "M", "color": "Blue" }
]
```

**Use Cases**:
- Generate product variants (size × color)
- Create test case combinations
- Build parameter grids

---

## Merge Node Usage Examples

### Example 1: Enriching Dataset (Left Join)

**Scenario**: Enrich customer records with purchase history

```
Fetch Customers ─┐
                 ├─→ Merge (Left Join) ─→ Update CRM
Fetch Purchases ─┘
```

**Configuration**:
- Mode: `combine`
- Combine by: `Matching fields`
- Match: `customers.id` = `purchases.customerId`
- Output type: `Enrich input 1`

**Result**: All customers in output, with purchase data added when available.

---

### Example 2: Matching Items (Inner Join)

**Scenario**: Find users with active subscriptions

```
Fetch All Users ────┐
                    ├─→ Merge (Inner Join) ─→ Send Renewal Email
Fetch Active Subs ──┘
```

**Configuration**:
- Mode: `combine`
- Combine by: `Matching fields`
- Match: `users.id` = `subscriptions.userId`
- Output type: `Keep matches`

**Result**: Only users with active subscriptions.

---

### Example 3: Combining Results (Union)

**Scenario**: Aggregate data from multiple sources

```
Fetch From API A ─┐
                  ├─→ Merge (Append) ─→ Process All Data
Fetch From API B ─┘
```

**Configuration**:
- Mode: `append`

**Result**: All items from both APIs in one array.

---

## Decision Guide: Merge or No Merge?

### Use NO Merge Node When:
- ✅ You want separate processing of each source
- ✅ Sources should trigger independent workflows
- ✅ Error handling with fallback sources
- ✅ Logging different data streams separately

### Use Merge Node When:
- ✅ Need combined data in single execution
- ✅ Relating data from multiple sources (joins)
- ✅ Aggregating results for unified processing
- ✅ Enriching one dataset with another

---

## Common Mistakes

### ❌ Mistake 1: Expecting Merge Without Merge Node

```
Fetch Products ─┐
                ├─→ Create Report
Fetch Prices ───┘
```

**Problem**: Report executes twice (separate runs), never sees combined data.

**Fix**: Add Merge node.

---

### ❌ Mistake 2: Wrong Merge Mode

**Scenario**: Want to enrich users with purchases, keeping users without purchases.

**Wrong**:
```
Mode: combine
Output type: Keep matches  ← Inner join, excludes users without purchases
```

**Correct**:
```
Mode: combine
Output type: Enrich input 1  ← Left join, keeps all users
```

---

### ❌ Mistake 3: Not Considering Execution Order

```
Node B (Y=50)  ─┐
                ├─→ Merge
Node A (Y=200) ─┘
```

**Issue**: Node B executes first (higher position), but you expected A first.

**Fix**: Position nodes intentionally or account for execution order in logic.

---

## Summary

### Branching
- One output → multiple nodes
- All branches execute with same data
- Execution order: highest node first (depth-first)
- Routing nodes (IF/Switch) split items per condition

### Merging Without Merge Node
- Multiple nodes → one target
- Target executes MULTIPLE TIMES (runs)
- Each run is independent
- Use when separate processing is desired

### Merging With Merge Node
- Multiple nodes → Merge → one target
- Target executes ONCE with combined data
- 6 modes: Union, Inner Join, Left Join, Right Join, Outer Join, Cross Join
- Use when combined data is needed

### Quick Reference

| Goal | Solution |
|------|----------|
| Process data through parallel transformations | Branch without Merge |
| Route items to different destinations | IF or Switch node |
| Process two sources separately | Branch without Merge (2 runs) |
| Combine two datasets completely | Merge (Append) |
| Match related items | Merge (Inner Join) |
| Enrich main dataset with secondary data | Merge (Left Join) |
| Keep all records from both sources | Merge (Outer Join) |
| Generate all combinations | Merge (Cross Join) |
