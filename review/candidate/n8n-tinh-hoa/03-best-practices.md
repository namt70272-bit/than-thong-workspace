# n8n Workflow Best Practices

Best practices for creating robust, maintainable, and efficient n8n workflows.

## Workflow Structure

### 1. Always Include a Workflow Configuration Node

**Why**: Centralizes configuration, makes workflows maintainable, enables easy environment switching.

**Pattern**:
```
Trigger → Workflow Configuration (Set) → Processing Nodes
```

**What to include**:
- API URLs and endpoints
- Thresholds and limits
- String constants
- Any reusable values

**How to reference**:
```javascript
={{ $('Workflow Configuration').first().json.apiUrl }}
```

**Important**:
- Enable "includeOtherFields" to pass through input data
- Don't use for credentials (use n8n's credential system)
- Don't reference from trigger nodes (they run before it)

### 2. Use Descriptive Node Names

**Why**: Makes workflows easier to understand and debug.

❌ BAD:
- "HTTP Request"
- "Set1"
- "Code"

✅ GOOD:
- "Fetch User Data"
- "Transform Customer Records"
- "Calculate Total Price"

### 3. Organize Nodes Logically

**Horizontal flow**: Left to right for main workflow
**Vertical spacing**: Group related parallel branches
**Alignment**: Align nodes at same workflow stage

### 4. Never Rely on Default Values

**CRITICAL**: Always explicitly configure node parameters.

**Common failures**:
- Document Loader: Defaults to 'json' but needs 'binary' for files
- Vector Store: Mode parameter affects connections
- HTTP Request: Default method might not match API requirements

### 5. Configure ALL Nodes

Even "simple" nodes need configuration:
- HTTP Request: URL, method, headers
- Set: Field definitions
- Code: Actual code logic
- AI nodes: Prompts, models, parameters

## Error Handling

### 1. Use Error Workflows

Set up dedicated error handling workflows for critical processes.

**Settings → Error Workflow**: Specify a workflow to handle errors

### 2. Configure Retry Logic

For unreliable external services:

**Node Settings**:
- Enable "Retry On Fail"
- Set max tries (2-5)
- Set wait time between retries

### 3. Use Try-Catch Patterns

For complex error handling:
```
Try Branch → Process
          ↓ (on error)
Catch Branch → Error Handler
```

### 4. Continue On Fail

When you want workflow to continue despite errors:

**Node Settings**:
- Set "On Error" to "Continue Regular Output" or "Continue Error Output"

## Performance Optimization

### 1. Use Batch Processing for Large Datasets

For processing thousands of records:
- Read data in chunks
- Use pagination when possible
- Process in batches (but avoid Split In Batches node)

### 2. Minimize API Calls

- Cache frequently used data
- Combine multiple operations when API supports it
- Use bulk endpoints instead of individual calls

### 3. Use Appropriate Node Types

- **Structured Output Parser** for AI-generated data (not Code node)
- **Extract From File** for binary data
- **Code node** only for simple transformations

### 4. Parallel Execution

When operations are independent:
- Branch workflow to run parallel operations
- Merge results after parallel branches complete

## Security Best Practices

### 1. Never Hardcode Credentials

❌ WRONG:
```json
{
  "headers": {
    "Authorization": "Bearer sk-1234567890"
  }
}
```

✅ CORRECT:
```json
{
  "authentication": "genericCredentialType",
  "genericAuthType": "oAuth2"
}
```

### 2. Use n8n Credentials System

Store all sensitive data in n8n's encrypted credential store.

### 3. Use Environment Variables

For configuration that varies by environment:

```javascript
={{ $env.API_URL }}
={{ $env.DATABASE_NAME }}
```

### 4. Sanitize User Input

When processing external data:
- Validate input format
- Check for expected fields
- Sanitize strings to prevent injection
- Use Type Validation in IF nodes

## Data Flow Best Practices

### 1. Validate Data Early

Add validation nodes early in the workflow:
- Check required fields exist
- Verify data types
- Validate ranges/formats

### 2. Transform Data Between Incompatible Formats

Use Set nodes to:
- Map field names
- Convert data types
- Restructure objects

### 3. Use Expressions for Dynamic Data

Reference previous nodes instead of hardcoding:

```javascript
={{ $('Fetch User').item.json.userId }}
```

### 4. Handle Empty/Null Values

Use null coalescing and defaults:

```javascript
={{ $('Node').item.json.field ?? 'default' }}
={{ $('Node').item.json.user?.email }}
```

## AI Workflow Specific Practices

### 1. Understand AI Node Connection Types

**Sub-nodes are SOURCES**:
- OpenAI Model → AI Agent (provides capability)
- Tool → AI Agent (provides tool)
- Memory → AI Agent (provides memory)

**Not the other way around**!

### 2. RAG Pattern

Correct pattern:
```
Data Source → Vector Store (main)
Document Loader → Vector Store (ai_document)
Embeddings → Vector Store (ai_embedding)
Text Splitter → Document Loader (ai_textSplitter)
```

### 3. Configure Document Loader Properly

When processing files:
- Set `dataType: 'binary'` (not 'json')
- Set appropriate loader type (PDF, DOCX, etc.)
- Configure chunking parameters

### 4. Use $fromAI for Tool Nodes

In tool nodes (ending with "Tool"):

```javascript
{
  "sendTo": "={{ $fromAI('to') }}",
  "subject": "={{ $fromAI('subject') }}",
  "message": "={{ $fromAI('message_html') }}"
}
```

## Testing and Debugging

### 1. Use Pin Data for Development

Pin sample data to nodes for testing:
- Right-click node → "Pin data"
- Test with realistic data
- Remove pins before production

### 2. Test Each Stage

Don't build entire workflow at once:
1. Build and test trigger
2. Add and test first processing node
3. Gradually add more nodes
4. Test after each addition

### 3. Use Workflow Executions View

Monitor executions to:
- See data at each step
- Identify bottlenecks
- Debug errors

### 4. Enable Execution Logging

For critical workflows:
- Save execution data
- Review logs regularly
- Set up alerting for failures

## Maintenance and Documentation

### 1. Use Tags

Organize workflows with tags:
- Environment (dev, staging, prod)
- Department (sales, marketing, ops)
- Type (data-sync, notification, report)

### 2. Version Control

Export workflows regularly:
- Save JSON files to git repository
- Document changes in commit messages
- Use branches for major changes

### 3. Document Complex Logic

- Use node descriptions for complex expressions
- Add sticky notes for workflow sections
- Maintain separate documentation for business logic

### 4. Regular Maintenance

- Review and update credentials
- Check for deprecated node versions
- Update to latest n8n version
- Review and optimize slow workflows

## Common Anti-Patterns to Avoid

### ❌ Don't Use Split In Batches

This node is deprecated and can cause issues. Use alternative patterns.

### ❌ Don't Over-Engineer

Keep workflows simple:
- Use built-in nodes instead of custom code when possible
- Don't add unnecessary complexity
- Follow YAGNI (You Aren't Gonna Need It)

### ❌ Don't Ignore Errors

Always handle potential failure points:
- External API calls
- Database operations
- File processing

### ❌ Don't Create Monolithic Workflows

Break large workflows into:
- Multiple smaller workflows
- Reusable sub-workflows
- Modular components

### ❌ Don't Forget About Rate Limits

When calling external APIs:
- Implement rate limiting
- Add delays between calls
- Use retry logic with backoff

## Checklist for Production Workflows

Before deploying to production:

- [ ] All nodes properly configured (no defaults relied upon)
- [ ] Credentials stored securely (no hardcoded secrets)
- [ ] Error handling implemented
- [ ] Retry logic configured for unreliable services
- [ ] Workflow Configuration node included
- [ ] Node names are descriptive
- [ ] Tested with realistic data
- [ ] Performance optimized (no unnecessary API calls)
- [ ] Logging/monitoring enabled
- [ ] Documentation updated
- [ ] Version controlled (JSON exported)
- [ ] Tags applied
- [ ] Team members notified
