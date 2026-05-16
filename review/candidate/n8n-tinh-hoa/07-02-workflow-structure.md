# n8n Workflow JSON Structure

This document describes the complete structure of an n8n workflow JSON file.

## Overview

An n8n workflow is represented as a JSON object that contains all the information needed to define the workflow's logic, including nodes, connections, and settings.

## Top-Level Structure

```json
{
  "name": "Workflow Name",
  "nodes": [...],
  "connections": {...},
  "active": false,
  "settings": {...},
  "pinData": {...},
  "tags": [...],
  "hash": "workflow-hash",
  "id": "workflow-id",
  "meta": {...}
}
```

## Key Fields

### name (required)
**Type:** `string`

The display name of the workflow.

```json
"name": "Customer Data Processing"
```

### nodes (required)
**Type:** `array`

An array of node objects. Each node represents a specific action or data transformation in the workflow.

**Node Object Structure:**
```json
{
  "parameters": {...},           // Node-specific configuration
  "id": "unique-node-id",       // UUID for the node
  "name": "Node Display Name",  // Display name (must be unique in workflow)
  "type": "node-type",          // e.g., "n8n-nodes-base.httpRequest"
  "typeVersion": 1,             // Version of the node type
  "position": [x, y]            // Canvas position [x, y] coordinates
}
```

**Example Node:**
```json
{
  "parameters": {
    "method": "POST",
    "url": "https://api.example.com/data"
  },
  "id": "a2f85497-260d-4489-a957-2b7d88e2f33d",
  "name": "HTTP Request",
  "type": "n8n-nodes-base.httpRequest",
  "typeVersion": 4.2,
  "position": [400, 260]
}
```

### connections (required)
**Type:** `object`

Defines how nodes are connected. The structure maps source nodes to their target nodes.

**Connection Object Structure:**
```json
{
  "Source Node Name": {
    "main": [                    // Main output
      [                          // Output index 0
        {
          "node": "Target Node Name",
          "type": "main",
          "index": 0             // Target input index
        }
      ]
    ]
  }
}
```

**Special Connection Types:**
- `main`: Regular data flow
- `ai_languageModel`: AI language model connection
- `ai_tool`: AI tool connection
- `ai_memory`: AI memory connection
- `ai_document`: AI document connection
- `ai_embedding`: AI embedding connection
- `ai_textSplitter`: AI text splitter connection
- `ai_outputParser`: AI output parser connection

**Example Connections:**
```json
{
  "Manual Trigger": {
    "main": [
      [
        {
          "node": "HTTP Request",
          "type": "main",
          "index": 0
        }
      ]
    ]
  },
  "HTTP Request": {
    "main": [
      [
        {
          "node": "Set",
          "type": "main",
          "index": 0
        }
      ]
    ]
  }
}
```

**AI Node Connection Example:**
```json
{
  "OpenAI Chat Model": {
    "ai_languageModel": [
      [
        {
          "node": "AI Agent",
          "type": "ai_languageModel",
          "index": 0
        }
      ]
    ]
  },
  "Calculator Tool": {
    "ai_tool": [
      [
        {
          "node": "AI Agent",
          "type": "ai_tool",
          "index": 0
        }
      ]
    ]
  }
}
```

### active (optional)
**Type:** `boolean`

Whether the workflow is currently active (enabled for execution).

```json
"active": false
```

### settings (optional)
**Type:** `object`

Workflow-level settings such as execution order, timezone, etc.

```json
"settings": {
  "executionOrder": "v1",
  "saveManualExecutions": true,
  "callerPolicy": "workflowsFromSameOwner",
  "errorWorkflow": "workflow-id"
}
```

**Common Settings:**
- `executionOrder`: `"v1"` (new) or `"legacy"`
- `saveManualExecutions`: Save manual test executions
- `saveExecutionProgress`: Save intermediate execution data
- `executionTimeout`: Maximum execution time in seconds
- `timezone`: Timezone for schedule triggers

### pinData (optional)
**Type:** `object`

Fixed data pinned to specific nodes for testing purposes.

```json
"pinData": {
  "HTTP Request": [
    {
      "json": {
        "id": 1,
        "name": "Test Data"
      }
    }
  ]
}
```

### tags (optional)
**Type:** `array`

Tags for organizing workflows.

```json
"tags": [
  {
    "name": "production",
    "id": "tag-id"
  }
]
```

### hash (optional)
**Type:** `string`

Hash of the workflow for change detection.

### id (optional)
**Type:** `string` or `number`

Unique identifier for the workflow (assigned by n8n).

### meta (optional)
**Type:** `object`

Metadata about the workflow instance.

```json
"meta": {
  "instanceId": "instance-uuid"
}
```

## Common Node Types

### Trigger Nodes
- `n8n-nodes-base.manualTrigger`: Manual execution trigger
- `n8n-nodes-base.scheduleTrigger`: Time-based trigger
- `n8n-nodes-base.webhook`: Webhook trigger
- `n8n-nodes-base.emailTrigger`: Email-based trigger

### Data Processing Nodes
- `n8n-nodes-base.set`: Transform and set data fields
- `n8n-nodes-base.code`: Execute custom JavaScript/Python code
- `n8n-nodes-base.if`: Conditional branching
- `n8n-nodes-base.merge`: Merge data from multiple sources
- `n8n-nodes-base.splitInBatches`: Process data in batches (deprecated, avoid using)

### Integration Nodes
- `n8n-nodes-base.httpRequest`: Make HTTP/API requests
- `n8n-nodes-base.googleSheets`: Google Sheets integration
- `n8n-nodes-base.slack`: Slack integration
- `n8n-nodes-base.gmail`: Gmail integration
- `n8n-nodes-base.airtable`: Airtable integration

### AI Nodes
- `@n8n/n8n-nodes-langchain.agent`: AI Agent (main)
- `@n8n/n8n-nodes-langchain.agentTool`: AI Agent Tool (sub-node)
- `@n8n/n8n-nodes-langchain.chatOpenAi`: OpenAI Chat Model
- `@n8n/n8n-nodes-langchain.chatAnthropic`: Anthropic Chat Model
- `@n8n/n8n-nodes-langchain.lmChatGoogleGemini`: Google Gemini Chat Model
- `@n8n/n8n-nodes-langchain.vectorStoreInMemory`: In-Memory Vector Store
- `@n8n/n8n-nodes-langchain.vectorStorePinecone`: Pinecone Vector Store
- `@n8n/n8n-nodes-langchain.embeddingsOpenAi`: OpenAI Embeddings
- `@n8n/n8n-nodes-langchain.documentDefaultDataLoader`: Default Data Loader
- `@n8n/n8n-nodes-langchain.textSplitterTokenSplitter`: Token Text Splitter
- `@n8n/n8n-nodes-langchain.outputParserStructured`: Structured Output Parser
- `@n8n/n8n-nodes-langchain.memoryBufferWindow`: Window Buffer Memory

### Tool Nodes (Support $fromAI expressions)
- `@n8n/n8n-nodes-langchain.toolCode`: Code Tool
- `@n8n/n8n-nodes-langchain.toolCalculator`: Calculator Tool
- `@n8n/n8n-nodes-langchain.toolHttpRequest`: HTTP Request Tool
- `@n8n/n8n-nodes-langchain.toolWorkflow`: Execute Workflow Tool
- Integration tool nodes (Gmail Tool, Slack Tool, etc.)

## Node Positioning Guidelines

Nodes are positioned on a 2D canvas using [x, y] coordinates.

**Best Practices:**
- Start at [220, 260] for the trigger node
- Horizontal spacing: 180-200 pixels between nodes
- Vertical spacing: 180-200 pixels for parallel branches
- Keep workflows flowing left-to-right
- Align parallel branches horizontally when possible

**Example Positions:**
```json
"nodes": [
  {
    "name": "Manual Trigger",
    "position": [220, 260]
  },
  {
    "name": "HTTP Request",
    "position": [400, 260]
  },
  {
    "name": "Set",
    "position": [580, 260]
  }
]
```

## Data Flow

Data flows through the workflow via connections:

1. **Trigger Node** initiates the workflow
2. **Processing Nodes** transform, filter, or route data
3. **Action Nodes** perform operations (API calls, database updates, etc.)
4. **End Nodes** conclude the workflow execution

Each node receives input data, processes it according to its parameters, and outputs the result to connected nodes.

## Best Practices

1. **Always include a trigger node** - Every workflow needs a starting point
2. **Use descriptive node names** - Makes workflows easier to understand
3. **Configure all parameters** - Don't rely on defaults
4. **Add Workflow Configuration node** - Centralize common values
5. **Test with pinned data** - Use pinData for development
6. **Handle errors gracefully** - Use error workflows or try-catch patterns
7. **Keep it simple** - Avoid over-engineering
8. **Use expressions wisely** - Reference data from previous nodes when needed
9. **Document complex logic** - Use sticky notes or node names
10. **Version control** - Export and save workflow JSON files

## Minimal Valid Workflow

The smallest valid workflow contains a trigger and at least one action node:

```json
{
  "name": "Minimal Workflow",
  "nodes": [
    {
      "parameters": {},
      "id": "trigger-id",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [220, 260]
    },
    {
      "parameters": {
        "jsCode": "return $input.all();"
      },
      "id": "code-id",
      "name": "Code",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [400, 260]
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [
        [
          {
            "node": "Code",
            "type": "main",
            "index": 0
          }
        ]
      ]
    }
  },
  "active": false,
  "settings": {}
}
```
