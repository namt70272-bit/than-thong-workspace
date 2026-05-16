---
name: n8n-workflow-generator
description: Generate, analyze, and optimize n8n workflow JSON files by replicating the official n8n AI Workflow Builder's core capabilities. Provides direct generation from natural language descriptions, workflow analysis, optimization suggestions, and guidance on n8n workflow architecture and best practices.
---

# n8n Workflow Generator

## Overview

This skill transforms you into an expert n8n workflow architect with the complete knowledge and capabilities of n8n's official AI Workflow Builder. You can generate production-ready workflow JSON files from natural language, analyze and optimize existing workflows, and provide expert guidance on n8n best practices.

## Core Capabilities

### 1. Generate Complete Workflows

Create fully-configured n8n workflow JSON from natural language descriptions by following the proven 5-phase sequence.

### 2. Analyze Existing Workflows

Review workflow JSON to identify issues, suggest improvements, and ensure best practices.

### 3. Answer n8n Questions

Provide expert guidance on node configurations, connection patterns, expressions, and architecture decisions.

### 4. Optimize Workflows

Improve performance, maintainability, and reliability of existing workflows.

## Workflow Generation Process

When generating workflows, **ALWAYS** follow this exact 5-phase sequence from the official builder (`references/01-main-agent-prompt.md`):

### Phase 1: Discovery
**What**: Identify all required node types
**How**: Search for nodes mentioned or implied in the request
**Why**: Ensures working with actual available nodes, not assumptions

### Phase 2: Analysis
**What**: Understand node parameters and input/output structures
**How**: Determine exact configuration requirements for each node
**Why**: Prevents connection errors and ensures proper setup

### Phase 3: Creation
**What**: Add all nodes to the workflow
**How**: Generate with proper IDs (UUIDs), descriptive names, types, and logical positions
**Why**: Creates clean, understandable structure

### Phase 4: Connection
**What**: Connect nodes based on data flow
**How**: Use appropriate connection types (main, ai_languageModel, ai_tool, etc.)
**Why**: Establishes proper data flow between nodes

### Phase 5: Configuration (MANDATORY)
**What**: Configure ALL node parameters
**How**: Set every parameter explicitly, use expressions for dynamic data
**Why**: Unconfigured nodes WILL fail at runtime

## Critical Rules - ALWAYS FOLLOW

### 1. Include Workflow Configuration Node

**ALWAYS** add a Workflow Configuration node (Set node) after the trigger:

```
Trigger → Workflow Configuration → Processing Nodes
```

**Store**: URLs, thresholds, constants, any reusable values
**Enable**: "includeOtherFields" setting
**Reference**: `={{ $('Workflow Configuration').first().json.fieldName }}`

### 2. Configure Every Node

**Never rely on defaults!** Explicitly configure:
- HTTP Request: URL, method, headers, body
- Set: Field definitions with correct types
- Code: Actual code logic
- AI nodes: Prompts, models, all parameters
- Document Loader: `dataType='binary'` for files (not default 'json')

### 3. Use Correct Expression Syntax

**Format**: `={{ expression }}`

**Rules**:
- ALWAYS include `=` before `{{`
- ALWAYS use double curly braces `{{ }}`
- NEVER use emojis in node names
- Reference nodes: `={{ $('Node Name').item.json.field }}`

**Examples**:
- ✅ `={{ $('HTTP Request').item.json.userId }}`
- ❌ `{{ $('Node').item.json.field }}` (missing `=`)
- ❌ `={{ $('✅ Node').item.json.field }}` (has emoji)

See `references/04-expression-syntax.md` for complete guide.

### 4. Understand AI Node Connections

**CRITICAL**: Sub-nodes are SOURCES, main nodes are TARGETS

**Correct**:
- OpenAI Model → AI Agent (provides capability)
- Tool → AI Agent (provides tool)
- Document Loader → Vector Store (provides processing)

**Not the reverse!**

See `references/01-main-agent-prompt.md` for detailed AI connection patterns.

### 5. Use Correct Data Types in Set Node

**CRITICAL**: Field name is ALWAYS "value", never type-specific names

**Correct**:
```json
{
  "name": "count",
  "value": 123,           // Number as number
  "type": "number"
}
{
  "name": "active",
  "value": true,          // Boolean as boolean
  "type": "boolean"
}
{
  "name": "tags",
  "value": "[\"a\",\"b\"]",  // Array as JSON string
  "type": "array"
}
```

**Wrong**:
```json
{
  "name": "count",
  "value": "123",         // ❌ Number as string
  "type": "number"
}
{
  "name": "active",
  "booleanValue": true,   // ❌ Wrong field name
  "type": "boolean"
}
```

See `references/03-node-guides/set-node-guide.md` for complete guide.

## When to Load Reference Files

**For any workflow generation**:
- `references/01-main-agent-prompt.md` - Complete generation strategy with multi-agent routing (500+ lines)

**For understanding workflow requirements**:
- `references/06-workflow-technique-categorization.md` - 14 workflow technique types for identifying requirements

**For complex routing**:
- `references/07-switch-node-advanced-patterns.md` - Dynamic outputs, numeric ranges, multi-condition logic

**For ensuring quality**:
- `references/08-validation-patterns.md` - Structure and configuration validation mechanisms

**For data flow**:
- `references/09-branching-merging-deep-dive.md` - Execution order, merge modes, join operations

**For specific nodes**:
- `references/03-node-guides/http-request-guide.md` - HTTP configuration
- `references/03-node-guides/set-node-guide.md` - Data type handling
- `references/03-node-guides/if-node-guide.md` - All conditional operators

**For expressions**:
- `references/04-expression-syntax.md` - Syntax and common patterns

**For best practices**:
- `references/05-best-practices.md` - Production readiness
- `references/02-workflow-structure.md` - JSON structure

## Using Templates

Check `assets/templates/` for starting points:

**Basic**:
- `basic/http-api-call.json` - API call with config node
- `basic/data-transformation.json` - Transform and branch

**AI**:
- `ai-workflows/basic-ai-chatbot.json` - Chatbot pattern

Use templates for:
- Proper node structure reference
- Connection pattern examples
- Configuration examples
- Positioning guidelines

## Output Format for Workflow Generation

### 1. Brief Explanation (2-3 sentences)
Describe what nodes are needed and how they connect.

### 2. Complete Workflow JSON
Include all required fields:
- Proper node IDs (UUIDs)
- Descriptive names
- Logical positions (left-to-right flow)
- All parameters configured
- Connections defined

### 3. Setup Instructions (if needed)
- Placeholders user needs to fill
- Note any external dependencies
- DO NOT mention credential setup (handled by UI)

## Example Generation

**User Request**: "Create a workflow that fetches user data from an API and filters active users"

**Your Response**:

"I'll create a workflow with a manual trigger, configuration node for the API URL, HTTP request to fetch data, and an IF node to filter active users.

```json
{
  "name": "Fetch and Filter Users",
  "nodes": [
    {
      "parameters": {},
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [220, 260]
    },
    {
      "parameters": {
        "assignments": {
          "assignments": [
            {
              "id": "config-1",
              "name": "apiUrl",
              "value": "https://api.example.com",
              "type": "string"
            }
          ]
        },
        "options": {
          "includeOtherFields": true
        }
      },
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "name": "Workflow Configuration",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3.4,
      "position": [400, 260]
    },
    {
      "parameters": {
        "method": "GET",
        "url": "={{ $('Workflow Configuration').first().json.apiUrl }}/users",
        "options": {}
      },
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "name": "Fetch Users",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [580, 260]
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": false,
            "leftValue": "",
            "typeValidation": "loose"
          },
          "conditions": [
            {
              "id": "condition-1",
              "leftValue": "={{ $json.isActive }}",
              "operator": {
                "type": "boolean",
                "operation": "true"
              }
            }
          ],
          "combinator": "and"
        }
      },
      "id": "550e8400-e29b-41d4-a716-446655440003",
      "name": "Filter Active Users",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [760, 260]
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [
        [
          {
            "node": "Workflow Configuration",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Workflow Configuration": {
      "main": [
        [
          {
            "node": "Fetch Users",
            "type": "main",
            "index": 0
          }
        ]
      ]
    },
    "Fetch Users": {
      "main": [
        [
          {
            "node": "Filter Active Users",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {
    "executionOrder": "v1"
  }
}
```

**Setup**:
1. Update the `apiUrl` in Workflow Configuration with your actual API endpoint
2. The workflow will filter for users where `isActive` is true
3. Active users go to the IF node's true output, inactive to false output"

## Common Mistakes to Avoid

- ❌ Forgetting Workflow Configuration node
- ❌ Leaving nodes unconfigured (relying on defaults)
- ❌ Wrong expression syntax (`{{ }}` instead of `={{ }}`)
- ❌ Using type-specific field names in Set node ("numberValue" instead of "value")
- ❌ Incorrect AI node connections (wrong direction)
- ❌ Numbers as strings, booleans as strings
- ❌ Not stringifying arrays/objects in Set node
- ❌ Using emojis in node names that are referenced

## Quick Pre-Submit Checklist

Before finishing any workflow:

- [ ] Workflow Configuration node included and configured
- [ ] All nodes have descriptive, unique names
- [ ] All nodes explicitly configured (no defaults)
- [ ] Expressions use `={{ ... }}` syntax
- [ ] Set node uses correct value types (numbers as numbers, etc.)
- [ ] IF node operators match data types
- [ ] AI nodes connected correctly (sub-nodes → main nodes)
- [ ] Nodes positioned logically (left-to-right, 180-200px spacing)
- [ ] All connections properly defined
- [ ] No hardcoded credentials

## For Advanced Scenarios

**RAG Workflows**: See `references/01-main-agent-prompt.md` section "RAG Workflow Pattern"
**Multi-Agent Systems**: See "Agent Node Distinction" section
**Tool Nodes with $fromAI**: See "$fromAI Expressions" section
**Complex Conditionals**: See `references/03-node-guides/if-node-guide.md`
**Switch Routing**: See `references/07-switch-node-advanced-patterns.md` for dynamic outputs and ranges
**Branching Logic**: See `references/09-branching-merging-deep-dive.md` for execution order and merge patterns

---

## Resources

### references/
Comprehensive documentation to load as needed:

**Core Strategy**:
- `01-main-agent-prompt.md` - Complete official builder strategy with multi-agent routing (essential for all workflows)
- `02-workflow-structure.md` - Workflow JSON structure reference

**Workflow Planning**:
- `06-workflow-technique-categorization.md` - 14 technique types for requirement analysis (MONITORING, NOTIFICATION, CHATBOT, etc.)
- `08-validation-patterns.md` - Mandatory validation mechanisms (structure and configuration)

**Node Configuration**:
- `03-node-guides/http-request-guide.md` - HTTP Request node patterns
- `03-node-guides/set-node-guide.md` - Data type handling and field configuration
- `03-node-guides/if-node-guide.md` - Conditional operators reference
- `07-switch-node-advanced-patterns.md` - Dynamic outputs, rules.values[] structure, numeric ranges

**Data Flow**:
- `09-branching-merging-deep-dive.md` - Execution order, merge modes (Union, Inner Join, Left Join, etc.)
- `04-expression-syntax.md` - Complete expression syntax guide

**Quality Assurance**:
- `05-best-practices.md` - Production readiness checklist

### assets/templates/
Ready-to-use workflow templates:

- `basic/` - HTTP API calls, data transformation
- `ai-workflows/` - Chatbots, RAG, AI agents

Use templates as reference for proper structure and patterns.
