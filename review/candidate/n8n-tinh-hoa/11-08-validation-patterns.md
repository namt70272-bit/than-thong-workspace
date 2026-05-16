# Workflow Validation Patterns

This document describes the official n8n AI Workflow Builder's validation mechanisms that ensure workflows are properly structured and configured before completion.

## Source
Extracted from:
- `packages/@n8n/ai-workflow-builder.ee/src/prompts/agents/builder.prompt.ts` (EXECUTION_SEQUENCE)
- `packages/@n8n/ai-workflow-builder.ee/src/prompts/agents/configurator.prompt.ts` (EXECUTION_SEQUENCE)

---

## Overview

The n8n AI Workflow Builder uses a **mandatory validation system** to ensure workflows are production-ready. There are two types of validation:

1. **Structure Validation** - Ensures nodes and connections are valid
2. **Configuration Validation** - Ensures node parameters are properly set

**Critical Rule**: You CANNOT complete workflow generation without validation. This is not optional.

---

## Two-Phase Validation

### Phase 1: Structure Validation (Builder Agent)

**When**: After creating nodes and connections, before responding to user

**Purpose**: Verify workflow structure is valid

**Tool**: `validate_structure`

**Checks**:
- Workflow has a trigger node
- All connections are valid (correct connection types)
- No orphaned nodes (unreachable nodes)
- Connection flow makes logical sense
- Dynamic output nodes (Switch, Merge) configured correctly

---

### Phase 2: Configuration Validation (Configurator Agent)

**When**: After configuring all node parameters, before responding to user

**Purpose**: Verify all nodes are properly configured

**Tool**: `validate_configuration`

**Checks**:
- All required parameters are set
- Parameter values are correct types
- Expressions are valid syntax
- Default values that cause failures are overridden
- Tool nodes use appropriate $fromAI expressions

---

## Mandatory Execution Sequence

### Builder Agent Sequence

```
STEP 1: CREATE NODES
  ↓
STEP 2: CONNECT NODES
  ↓
STEP 3: VALIDATE (REQUIRED)
  - Call validate_structure
  - If issues found, fix and validate again
  - Maximum 3 validation attempts
  ↓
STEP 4: RESPOND TO USER
  - Only after validation passes
```

**CRITICAL RULES**:
- NEVER respond before calling validate_structure
- NEVER skip validation even if you think structure is correct
- If validation finds issues, FIX them and validate again
- After 3 validation attempts, proceed regardless of remaining issues

---

### Configurator Agent Sequence

```
STEP 1: CONFIGURE ALL NODES
  ↓
STEP 2: VALIDATE (REQUIRED)
  - Call validate_configuration
  - If issues found, fix and validate again
  - Maximum 3 validation attempts
  ↓
STEP 3: RESPOND TO USER
  - Only after validation passes
```

**CRITICAL RULES**:
- NEVER respond before calling validate_configuration
- NEVER skip validation even if you think configuration is correct
- If validation finds issues, FIX them and validate again
- After 3 validation attempts, proceed regardless of remaining issues

---

## The 3-Attempt Rule

### Why Maximum 3 Attempts?

**Prevents infinite loops**: Without a limit, validation-fix-validation cycles could continue indefinitely.

**Forces progress**: After 3 attempts, the agent must proceed and inform the user of any remaining issues.

**Balances quality and completion**: Most issues are fixed within 3 attempts; remaining issues are often edge cases requiring user input.

### How It Works

```
Attempt 1: validate_structure → Issues found → Fix issues
Attempt 2: validate_structure → Issues found → Fix issues
Attempt 3: validate_structure → Issues found or not → PROCEED

After Attempt 3:
- If validation passed: Respond with success
- If issues remain: Respond with issue details and proceed
```

---

## Common Structure Validation Issues

### Issue 1: Missing Trigger Node

**Problem**: Workflow has no trigger node

**Validation Error**: "Workflow must have a trigger node"

**Fix**:
```javascript
// Add a trigger node at the start
add_nodes({
  nodeType: "n8n-nodes-base.manualTrigger",
  name: "Manual Trigger",
  ...
})
```

---

### Issue 2: Invalid Connection Type

**Problem**: Wrong connection type used (e.g., main connection to AI sub-node)

**Validation Error**: "Invalid connection type: expected ai_languageModel, got main"

**Fix**:
```javascript
// Correct the connection type
connect_nodes({
  sourceNodeId: "OpenAI Chat Model",
  targetNodeId: "AI Agent",
  connectionType: "ai_languageModel"  // Not "main"
})
```

---

### Issue 3: Unreachable Nodes

**Problem**: Nodes exist but aren't connected to the workflow

**Validation Error**: "Node 'Process Data' is unreachable from trigger"

**Fix**:
```javascript
// Connect the orphaned node
connect_nodes({
  sourceNodeId: "Previous Node",
  targetNodeId: "Process Data"
})
```

---

### Issue 4: Connection to Non-Existent Output

**Problem**: Trying to connect to a Switch output that doesn't exist

**Validation Error**: "Output index 2 does not exist on node 'Route by Status'"

**Fix**:
```javascript
// Add another entry to rules.values[] to create the output
update_node_parameters({
  nodeId: "Route by Status",
  instructions: [
    "Add third routing rule with outputKey 'Low Priority'"
  ]
})
```

---

### Issue 5: Missing AI Sub-Node Connections

**Problem**: AI Agent lacks required language model connection

**Validation Error**: "AI Agent requires ai_languageModel connection"

**Fix**:
```javascript
// Add the missing AI sub-node and connection
add_nodes({
  nodeType: "@n8n/n8n-nodes-langchain.openAiChatModel",
  name: "OpenAI GPT-4",
  ...
})

connect_nodes({
  sourceNodeId: "OpenAI GPT-4",
  targetNodeId: "AI Agent",
  connectionType: "ai_languageModel"
})
```

---

## Common Configuration Validation Issues

### Issue 1: Unconfigured HTTP Request

**Problem**: HTTP Request node has no URL set

**Validation Error**: "HTTP Request 'Fetch Data' missing required parameter: url"

**Fix**:
```javascript
update_node_parameters({
  nodeId: "Fetch Data",
  instructions: [
    "Set URL to https://api.example.com/data",
    "Set method to GET"
  ]
})
```

---

### Issue 2: Document Loader with Wrong dataType

**Problem**: Document Loader defaulted to 'json' when processing PDFs

**Validation Error**: "Document Loader processing binary files must have dataType='binary'"

**Fix**:
```javascript
update_node_parameters({
  nodeId: "PDF Loader",
  instructions: [
    "Set dataType to 'binary'",
    "Set loader to 'pdfLoader'"
  ]
})
```

---

### Issue 3: Empty Set Node

**Problem**: Set node has no fields defined

**Validation Error**: "Set node 'Transform Data' has no fields configured"

**Fix**:
```javascript
update_node_parameters({
  nodeId: "Transform Data",
  instructions: [
    "Add field 'status' with value 'processed'",
    "Add field 'timestamp' with value ={{ $now }}"
  ]
})
```

---

### Issue 4: Code Node with No Code

**Problem**: Code node exists but has no code

**Validation Error**: "Code node 'Process' has empty code"

**Fix**:
```javascript
update_node_parameters({
  nodeId: "Process",
  instructions: [
    "Set code to: return items.map(item => ({ json: { ...item.json, processed: true } }))"
  ]
})
```

---

### Issue 5: Invalid Expression Syntax

**Problem**: Expression missing '=' or has wrong bracket format

**Validation Error**: "Invalid expression syntax in 'Transform': {{ $json.field }}"

**Fix**:
```javascript
update_node_parameters({
  nodeId: "Transform",
  instructions: [
    "Fix expression to: ={{ $json.field }}"  // Add '=' before {{
  ]
})
```

---

## Validation Flow Examples

### Example 1: Structure Validation Success (First Attempt)

```
Builder creates workflow:
  Manual Trigger → HTTP Request → Set → Email

Call validate_structure:
  ✅ Trigger present
  ✅ All connections valid
  ✅ All nodes reachable
  ✅ Connection types correct

Result: Validation passed on Attempt 1
Action: Proceed to respond
```

---

### Example 2: Structure Validation with Fixes (Two Attempts)

```
Builder creates workflow:
  Manual Trigger → HTTP Request → AI Agent (missing language model)

Attempt 1 - Call validate_structure:
  ❌ AI Agent missing ai_languageModel connection

Fix issues:
  - Add OpenAI Chat Model node
  - Connect: OpenAI Chat Model → AI Agent [ai_languageModel]

Attempt 2 - Call validate_structure:
  ✅ All checks passed

Result: Validation passed on Attempt 2
Action: Proceed to respond
```

---

### Example 3: Configuration Validation with Multiple Fixes

```
Configurator updates parameters:
  HTTP Request: (unconfigured)
  Set: (unconfigured)

Attempt 1 - Call validate_configuration:
  ❌ HTTP Request missing URL
  ❌ HTTP Request missing method
  ❌ Set has no fields

Fix issues:
  - Configure HTTP Request URL and method
  - Add fields to Set node

Attempt 2 - Call validate_configuration:
  ❌ HTTP Request URL uses invalid expression: {{ $json.url }}

Fix issues:
  - Fix expression to: ={{ $json.url }}

Attempt 3 - Call validate_configuration:
  ✅ All checks passed

Result: Validation passed on Attempt 3
Action: Proceed to respond
```

---

### Example 4: Maximum Attempts Reached

```
Configurator updates parameters

Attempt 1 - Call validate_configuration:
  ❌ Complex validation issues

Fix issues (partial)

Attempt 2 - Call validate_configuration:
  ❌ Additional issues found

Fix issues (partial)

Attempt 3 - Call validate_configuration:
  ❌ Some issues still remain

Result: Maximum attempts reached
Action: Proceed and inform user of remaining issues:
  "The workflow is mostly configured, but these parameters may need
   your attention: [list issues]. Please review before executing."
```

---

## Best Practices

### 1. Always Call Validation Tools

**Never skip validation**, even if you're confident the workflow is correct.

❌ Wrong:
```
Create nodes → Connect nodes → Respond to user
```

✅ Correct:
```
Create nodes → Connect nodes → validate_structure → Respond to user
```

---

### 2. Fix Issues Immediately

When validation finds issues, fix them before the next validation attempt.

**Pattern**:
```
validate → identify issues → fix all issues → validate again
```

**Not**:
```
validate → fix one issue → validate → fix another issue → validate
```

---

### 3. Track Validation Attempts

Keep count of validation calls to respect the 3-attempt limit.

```javascript
// Pseudocode
let attempts = 0;

while (attempts < 3) {
  attempts++;
  const result = validate_structure();

  if (result.passed) {
    break;  // Success
  }

  if (attempts < 3) {
    fixIssues(result.issues);
  }
}

// Proceed regardless after 3 attempts
```

---

### 4. Provide Clear Error Context

When reporting remaining issues after 3 attempts:

❌ Bad: "Validation failed"

✅ Good: "The workflow structure is complete, but the HTTP Request node
         'Fetch Data' still needs a URL configured. You can set this in
         the node's parameters after import."

---

### 5. Validate Before Responding

**CRITICAL**: Never provide your final response before validation.

❌ Wrong:
```
Build workflow
Respond: "I've created a workflow that..."  ← NO!
validate_structure  ← Too late
```

✅ Correct:
```
Build workflow
validate_structure
IF passed:
  Respond: "I've created a workflow that..."
```

---

## Validation Checklist

### Before Calling validate_structure:
- [ ] All nodes created
- [ ] All connections created
- [ ] No planned changes remaining

### After validate_structure fails:
- [ ] Identify all issues from validation result
- [ ] Fix all issues (don't fix just one)
- [ ] Call validate_structure again
- [ ] Track attempt count

### Before Calling validate_configuration:
- [ ] All nodes configured with update_node_parameters
- [ ] No placeholder parameters remaining (unless intentional)
- [ ] All expressions use correct syntax

### After validate_configuration fails:
- [ ] Identify all issues from validation result
- [ ] Fix all issues
- [ ] Call validate_configuration again
- [ ] Track attempt count

### After 3 Attempts (if issues remain):
- [ ] Document remaining issues clearly
- [ ] Explain what needs user attention
- [ ] Provide guidance on how to fix
- [ ] Proceed with response

---

## Integration with Workflow Creation

### Complete Builder Flow with Validation

```
1. DISCOVERY
   - Search for node types
   - Get node details

2. CREATION
   - Add all nodes in parallel
   - Set connection parameters

3. CONNECTION
   - Connect all nodes
   - Use correct connection types

4. VALIDATION (REQUIRED)
   Attempt 1:
     - Call validate_structure
     - Check result

   IF issues found:
     - Fix all issues
     - Attempt 2: validate_structure

   IF issues still found:
     - Fix all issues
     - Attempt 3: validate_structure

   After 3 attempts:
     - PROCEED regardless

5. RESPONSE
   - Provide setup instructions
   - Note any remaining issues
```

---

### Complete Configurator Flow with Validation

```
1. CONFIGURATION
   - Update all nodes in parallel
   - Set all required parameters
   - Override problematic defaults

2. VALIDATION (REQUIRED)
   Attempt 1:
     - Call validate_configuration
     - Check result

   IF issues found:
     - Fix all issues
     - Attempt 2: validate_configuration

   IF issues still found:
     - Fix all issues
     - Attempt 3: validate_configuration

   After 3 attempts:
     - PROCEED regardless

3. RESPONSE
   - List what was configured
   - Note placeholders needing user input
   - Mention any validation issues
```

---

## Why Validation Matters

### Without Validation:
- ❌ Workflows fail at runtime
- ❌ Users encounter confusing errors
- ❌ Poor user experience
- ❌ Time wasted debugging
- ❌ Loss of trust in AI generation

### With Validation:
- ✅ Workflows work on first run
- ✅ Issues caught early
- ✅ Clear error messages
- ✅ Professional output
- ✅ User confidence in AI capabilities

---

## Summary

**Key Principles**:

1. **Validation is MANDATORY** - Not optional, not skippable
2. **Two validation types** - Structure (connections) and Configuration (parameters)
3. **Maximum 3 attempts** - Prevents infinite loops
4. **Always validate before responding** - Never skip this step
5. **Fix all issues at once** - Don't fix one at a time
6. **Inform user of remaining issues** - After 3 attempts, proceed but document problems

**Remember**: Validation is what makes the difference between AI-generated workflows that "might work" and workflows that "definitely work". It's the quality assurance step that ensures professional output.
