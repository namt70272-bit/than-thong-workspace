# Workflow Technique Categorization

This document describes the official n8n AI Workflow Builder's technique categorization system used to identify workflow requirements and select appropriate nodes.

## Source
Extracted from: `packages/@n8n/ai-workflow-builder.ee/src/prompts/agents/discovery.prompt.ts`

---

## Overview

When building workflows, the AI Workflow Builder categorizes user requests into one or more workflow techniques. This helps identify which nodes and patterns are needed.

**Key Principle**: Most workflows use 2-4 techniques. Select ALL techniques that apply, with a maximum of 5.

---

## 14 Workflow Techniques

### 1. MONITORING
**Description**: Workflows triggered by external events (new records, status changes, incoming webhooks, new messages).

**Use when**:
- Workflow TRIGGERS on external events
- NOT just scheduled runs
- Reacting to changes in external systems

**Examples**:
- "Trigger when a new contact is created in HubSpot"
- "Monitor social channels for product mentions"
- "Receive news from Telegram channels"

**Common nodes**: Webhook triggers, polling triggers, event-based triggers

---

### 2. NOTIFICATION
**Description**: SENDING emails, messages, or alerts (including broadcast-only channels).

**Use when**:
- Sending emails, Slack messages, SMS
- Posting to Telegram CHANNELS (broadcast-only)
- Delivering alerts or reports

**IMPORTANT**: Use NOTIFICATION when SENDING. Use CHATBOT when RECEIVING and REPLYING to conversations.

**Examples**:
- "Send email notifications to leads"
- "Post updates to Telegram channel"
- "Deliver weekly reports via Slack"

**Common nodes**: Gmail, Slack, Telegram, Email Send, SMS

---

### 3. CHATBOT
**Description**: RECEIVING and REPLYING to direct messages in a conversation (two-way communication).

**Use when**:
- Building conversational interfaces
- Responding to user messages
- Interactive Q&A systems

**IMPORTANT**: Only for two-way conversations, NOT for broadcasting messages.

**Examples**:
- "Create a chatbot that answers questions"
- "Build a support assistant"
- "Interactive customer service bot"

**Common nodes**: Chat Trigger, AI Agent, Chat Memory

---

### 4. SCRAPING_AND_RESEARCH
**Description**: Fetching data from EXTERNAL sources (APIs, websites, social media).

**Use when**:
- Calling external APIs
- Web scraping
- Gathering data from third-party services

**IMPORTANT**: Use for EXTERNAL sources. Use DATA_EXTRACTION for parsing INTERNAL data.

**Examples**:
- "Scrape competitor pricing pages"
- "Fetch trending topics from Google Trends and Reddit"
- "Get stock prices from financial APIs"

**Common nodes**: HTTP Request, HTML Extract, RSS Read

---

### 5. DATA_EXTRACTION
**Description**: Parsing and extracting information from INTERNAL data you already have.

**Use when**:
- Processing uploaded files
- Extracting fields from structured data
- Parsing existing documents

**IMPORTANT**: For INTERNAL data parsing, not external fetching.

**Examples**:
- "Process uploaded PDF contracts to extract client details"
- "Extract email addresses from text"
- "Parse JSON to get specific fields"

**Common nodes**: Extract From File, Code, Set (for field mapping)

---

### 6. TRIAGE
**Description**: SELECTING, PRIORITIZING, ROUTING, or QUALIFYING items.

**Use when**:
- Picking best options from multiple choices
- Routing to correct destination/team
- Qualifying leads or content
- Filtering by priority

**Examples**:
- "Select the best trending topics"
- "Route tickets to correct team"
- "Filter relevant news"
- "Qualify leads by score"

**Common nodes**: IF, Switch, Filter

---

### 7. DOCUMENT_PROCESSING
**Description**: Handling ANY file type (PDFs, images, videos, Excel, audio, etc.).

**Use when**:
- Processing PDFs, DOCX, images
- Handling file uploads in forms
- Working with spreadsheets or media files
- Any file-based operations

**Examples**:
- "Process uploaded PDF contracts"
- "Generate video reels from templates"
- "Extract data from Excel files"
- "Form submission with file upload"

**Common nodes**: Document Loader, Extract From File, Spreadsheet File, Binary nodes

---

### 8. HUMAN_IN_THE_LOOP
**Description**: Workflow PAUSES for human approval, review, or manual input before continuing.

**Use when**:
- Requiring approval steps
- Manual document signing
- Human review checkpoints
- Responding to polls/forms mid-workflow

**Examples**:
- "Collect partner referral submissions and verify"
- "Approval workflow for documents"
- "Manual review before sending"

**Common nodes**: Wait, Webhook (for callbacks), Form Trigger

---

### 9. DATA_ANALYSIS
**Description**: ANALYZING, CLASSIFYING, IDENTIFYING PATTERNS, or UNDERSTANDING data.

**Use when**:
- Analyzing patterns or trends
- Classifying data into categories
- Identifying insights
- Understanding outcomes
- Learning from historical data

**IMPORTANT**: Focus on understanding/analysis, not just transformation.

**Examples**:
- "Analyze YouTube video performance data"
- "Analyze volatility patterns"
- "Classify support tickets by type"
- "Identify trending topics"

**Common nodes**: AI Agent (for analysis), Code (for calculations), Aggregate

---

### 10. KNOWLEDGE_BASE
**Description**: Storing and retrieving from a DATA SOURCE for Q&A (vector DBs, spreadsheets as databases, document collections).

**Use when**:
- Building searchable knowledge bases
- RAG (Retrieval-Augmented Generation) workflows
- Using spreadsheets/databases for Q&A
- Document-based question answering

**Examples**:
- "Build a searchable internal knowledge base"
- "Chatbot that answers using Google Sheet data"
- "RAG system from past support tickets"

**Common nodes**: Vector Store, Pinecone, Supabase, Google Sheets (as database)

---

### 11. DATA_TRANSFORMATION
**Description**: CONVERTING data format, creating REPORTS/SUMMARIES from analyzed data, or restructuring output.

**Use when**:
- Reformatting data structures
- Generating reports from analysis
- Converting between formats
- Restructuring for downstream systems

**IMPORTANT**: For format conversion and report generation, not analysis itself.

**Examples**:
- "Transform customer records to CRM format"
- "Generate weekly report from analyzed data"
- "Convert JSON to CSV"

**Common nodes**: Set, Code, Edit Fields, Aggregate

---

### 12. CONTENT_GENERATION
**Description**: AI-generated content (text, social posts, emails, images).

**Use when**:
- Generating personalized messages
- Creating social media posts
- Writing email content
- Producing creative content

**Examples**:
- "AI agent that writes personalized emails"
- "Create social posts from trends"
- "Auto-respond with campaign messages"
- "Generate video descriptions"

**Common nodes**: AI Agent, OpenAI, Text generation nodes

---

### 13. ENRICHMENT
**Description**: Enhancing existing data with additional information from external sources.

**Use when**:
- Adding missing data fields
- Augmenting records with external info
- Enhancing profiles with third-party data

**Examples**:
- "Enrich profile with LinkedIn data"
- "Add company info from Clearbit"
- "Update records with CRM data"

**Common nodes**: HTTP Request, various API nodes, Merge

---

### 14. FORM_INPUT
**Description**: Workflows triggered by form submissions.

**Use when**:
- Processing form submissions
- Handling user input through forms
- Form-triggered workflows

**Examples**:
- "Form submission triggers document extraction"
- "Collect partner referral submissions"
- "Handle contact form submissions"

**Common nodes**: Form Trigger, Webhook

---

### 15. SCHEDULING
**Description**: Workflows that run on a schedule (cron jobs, recurring tasks).

**Use when**:
- Periodic execution
- Time-based triggers
- Recurring reports or tasks

**Examples**:
- "Scrape competitor pricing weekly"
- "Generate video reels on schedule"
- "Send daily digest"

**Common nodes**: Schedule Trigger, Cron

---

## Technique Distinction Guide

### Common Confusions and How to Resolve Them

#### NOTIFICATION vs CHATBOT
- ✅ **NOTIFICATION**: SENDING emails/messages/alerts (including Telegram CHANNELS which are broadcast-only)
- ✅ **CHATBOT**: RECEIVING and REPLYING to direct messages in a conversation

**Examples**:
- "Send alerts to Telegram channel" → NOTIFICATION (one-way broadcast)
- "Chatbot that answers questions" → CHATBOT (two-way conversation)

---

#### MONITORING vs SCHEDULING
- ✅ **MONITORING**: TRIGGERS on external events (new record, status change, incoming webhook)
- ✅ **SCHEDULING**: TRIGGERS on time-based schedule (every hour, daily, weekly)

**Examples**:
- "When new contact is created" → MONITORING (event-driven)
- "Every Monday at 9am" → SCHEDULING (time-driven)

---

#### SCRAPING_AND_RESEARCH vs DATA_EXTRACTION
- ✅ **SCRAPING_AND_RESEARCH**: Fetching from EXTERNAL sources (APIs, websites, social media)
- ✅ **DATA_EXTRACTION**: Parsing INTERNAL data you already have

**Examples**:
- "Fetch data from Twitter API" → SCRAPING_AND_RESEARCH
- "Extract fields from uploaded PDF" → DATA_EXTRACTION

---

#### DATA_ANALYSIS vs DATA_TRANSFORMATION
- ✅ **DATA_ANALYSIS**: ANALYZING, CLASSIFYING, IDENTIFYING PATTERNS, UNDERSTANDING
- ✅ **DATA_TRANSFORMATION**: CONVERTING format, creating REPORTS from analyzed data

**Examples**:
- "Analyze video performance patterns" → DATA_ANALYSIS
- "Generate report from analysis results" → DATA_TRANSFORMATION

**Note**: These often appear together (analyze first, then transform into report).

---

#### TRIAGE vs NOTIFICATION
- ✅ **TRIAGE**: SELECTING, PRIORITIZING, ROUTING, QUALIFYING
- ✅ **NOTIFICATION**: SENDING messages/alerts

**Examples**:
- "Filter relevant news and forward" → TRIAGE + NOTIFICATION (both)

---

## Example Categorizations

### Example 1
**Prompt**: "Monitor social channels for product mentions and auto-respond with campaign messages"

**Techniques**:
- MONITORING (trigger on new mentions)
- CHATBOT (responding to messages)
- CONTENT_GENERATION (generating campaign messages)

---

### Example 2
**Prompt**: "Collect partner referral submissions and verify client instances via BigQuery"

**Techniques**:
- FORM_INPUT (form submissions)
- HUMAN_IN_THE_LOOP (verification step)
- NOTIFICATION (inform about results)

---

### Example 3
**Prompt**: "Scrape competitor pricing pages weekly and generate a summary report of changes"

**Techniques**:
- SCHEDULING (weekly execution)
- SCRAPING_AND_RESEARCH (fetch from external websites)
- DATA_EXTRACTION (parse pricing data)
- DATA_ANALYSIS (identify changes)

---

### Example 4
**Prompt**: "Process uploaded PDF contracts to extract client details and update CRM records"

**Techniques**:
- DOCUMENT_PROCESSING (handling PDFs)
- DATA_EXTRACTION (extract client details)
- DATA_TRANSFORMATION (format for CRM)
- ENRICHMENT (update CRM with new data)

---

### Example 5
**Prompt**: "Build a searchable internal knowledge base from past support tickets"

**Techniques**:
- DATA_TRANSFORMATION (prepare ticket data)
- DATA_ANALYSIS (understand ticket patterns)
- KNOWLEDGE_BASE (store for searching)

---

### Example 6
**Prompt**: "Create an AI agent that writes and sends personalized emails to leads"

**Techniques**:
- CONTENT_GENERATION (AI writing emails)
- NOTIFICATION (sending emails)

---

### Example 7
**Prompt**: "Fetch trending topics from Google Trends and Reddit, select the best ones, and create social posts"

**Techniques**:
- SCRAPING_AND_RESEARCH (fetch from external sources)
- TRIAGE (select best topics)
- CONTENT_GENERATION (create social posts)

---

### Example 8
**Prompt**: "Trigger when a new contact is created in HubSpot and enrich their profile with LinkedIn data"

**Techniques**:
- MONITORING (trigger on new contact)
- ENRICHMENT (add LinkedIn data)

---

### Example 9
**Prompt**: "Get stock prices from financial APIs and analyze volatility patterns"

**Techniques**:
- SCRAPING_AND_RESEARCH (fetch from APIs)
- DATA_ANALYSIS (analyze volatility)

---

### Example 10
**Prompt**: "Generate video reels from templates and auto-post to social media on schedule"

**Techniques**:
- SCHEDULING (time-based trigger)
- DOCUMENT_PROCESSING (video generation)
- CONTENT_GENERATION (from templates)

---

## How to Use This System

### Step 1: Analyze User Request
Read the user's workflow description and identify key verbs and nouns.

### Step 2: Match to Techniques
- Look for trigger type (MONITORING, SCHEDULING, FORM_INPUT)
- Identify data sources (external = SCRAPING_AND_RESEARCH, internal = DATA_EXTRACTION)
- Check for processing types (analysis, transformation, extraction)
- Look for outputs (NOTIFICATION, CHATBOT, KNOWLEDGE_BASE)

### Step 3: Apply Distinction Rules
Use the confusion guide above to resolve ambiguities.

### Step 4: Select 2-4 Techniques
Most workflows use multiple techniques. Select ALL that clearly apply.

### Step 5: Maximum 5 Techniques
If you identify more than 5, prioritize the most central techniques.

---

## Impact on Node Selection

Technique categorization directly influences which nodes to search for:

- **MONITORING** → Polling triggers, Webhook triggers
- **NOTIFICATION** → Gmail, Slack, Telegram, Email Send
- **CHATBOT** → Chat Trigger, AI Agent, Memory nodes
- **SCRAPING_AND_RESEARCH** → HTTP Request, RSS Read, HTML Extract
- **DATA_EXTRACTION** → Extract From File, Code, Set
- **TRIAGE** → IF, Switch, Filter
- **DOCUMENT_PROCESSING** → Document Loader, Extract From File
- **HUMAN_IN_THE_LOOP** → Wait, Webhook (for callbacks)
- **DATA_ANALYSIS** → AI Agent, Code, Aggregate
- **KNOWLEDGE_BASE** → Vector Store, Pinecone, Supabase
- **DATA_TRANSFORMATION** → Set, Code, Edit Fields
- **CONTENT_GENERATION** → AI Agent, OpenAI
- **ENRICHMENT** → HTTP Request, API nodes, Merge
- **FORM_INPUT** → Form Trigger, Webhook
- **SCHEDULING** → Schedule Trigger, Cron

---

## Best Practices

1. **Select ALL applicable techniques** - Don't limit yourself to just one
2. **Only select techniques you're confident apply** - Better to miss one than add wrong ones
3. **Use distinction guide** - Resolve ambiguities systematically
4. **Think about the full workflow** - Consider trigger → processing → output
5. **Maximum 5 techniques** - If you identify more, you're over-categorizing

---

## Quick Reference Table

| Technique | Trigger? | Input? | Processing? | Output? |
|-----------|----------|--------|-------------|---------|
| MONITORING | ✅ | | | |
| SCHEDULING | ✅ | | | |
| FORM_INPUT | ✅ | | | |
| CHATBOT | | ✅ | | ✅ |
| NOTIFICATION | | | | ✅ |
| KNOWLEDGE_BASE | | ✅ | | ✅ |
| SCRAPING_AND_RESEARCH | | ✅ | | |
| DATA_EXTRACTION | | | ✅ | |
| DATA_ANALYSIS | | | ✅ | |
| DATA_TRANSFORMATION | | | ✅ | |
| DOCUMENT_PROCESSING | | | ✅ | |
| TRIAGE | | | ✅ | |
| ENRICHMENT | | | ✅ | |
| CONTENT_GENERATION | | | ✅ | ✅ |
