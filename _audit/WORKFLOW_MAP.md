# OpenClaw Workflow Map

## 1. Main Interaction Flow

```mermaid
flowchart TD
    A[User: Telegram / WebChat] --> B[OpenClaw Gateway]
    B --> C{Than Thong Gate}
    C -->|Local OK| D[Local Scripts / Tools]
    C -->|Web Search| E[Web Search / Fetch]
    C -->|Blocked| F[Billing Guard - STOP]
    D --> G[Result]
    E --> G
    G --> H[Memory Consolidator]
    G --> I[Final Response to User]
```

## 2. Startup Flow

```mermaid
flowchart LR
    A[Windows Boot] --> B[GitHub Runner Service]
    A --> C[Ollama Service]
    B --> D[Self-hosted Runner Ready]
    C --> E[Local LLM API Ready]
    A --> F[Docker Desktop]
    F --> G[Qdrant Container]
    F --> H[Dozzle Container]
    F --> I[Portainer Container]
    F --> J[Tinyproxy Container]
    A --> K[OpenClaw Gateway]
```

## 3. CI/CD Pipeline (GitHub Actions)

```mermaid
flowchart LR
    A[Git Push] --> B[GitHub Trigger]
    B --> C[Self-Hosted Runner]
    C --> D[Checkout Code]
    D --> E[Pytest: 13 Tests]
    E --> F[Syntax Check: 66 .py]
    F --> G[Ruff Lint]
    G --> H[Deploy to Workspace]
    H --> I[Memory Consolidation]
```

### Workflow List

| Workflow | Trigger | What it does |
|---|---|---|
| **test.yml** | Push / PR | pytest + syntax + ruff |
| **deploy.yml** | Push master | Test + deploy to workspace |
| **pr-review.yml** | PR | Test + syntax + ruff + compliance |
| **auto-fix.yml** | Push | Auto-create PR for BOM fixes |
| **issue-handler.yml** | Issue | Classify + label + comment |
| **wiki-sync.yml** | Push / Weekly | MEMORY.md -> GitHub Wiki |
| **skill-check.yml** | Weekly Mon | Check awesome-skills for updates |
| **auto-backup.yml** | Daily 22:00 | Consolidate + commit + push |
| **release.yml** | Tag v* | Build + GitHub Release |
| **health-check.yml** | Daily 07:00 | Syntax + pip + service + disk |
| **pip-check.yml** | Weekly Mon | Check pip dependencies |
| **auto-review.yml** | PR | Local LLM reviews code changes |

## 4. Memory Pipeline

```mermaid
flowchart LR
    A[Daily Notes] --> B[memory_consolidator.py]
    B --> C[INDEX.md]
    B --> D[Consolidation Report]
    B --> E[MEMORY.md Suggestions]
    E --> F[Manual Update or Cron]
    C --> G[RAG Index: workspace_rag.py]
    D --> G
    G --> H[Qdrant Vector DB]
    H --> I[Semantic Search / Q&A]
```

## 5. Local AI Pipeline

```mermaid
flowchart LR
    A[Ollama: bge-m3] --> B[Embeddings]
    A[Ollama: qwen2.5-coder] --> C[Code Review]
    A[Ollama: gemma3:1b] --> D[Quick Answers]
    B --> E[Qdrant Vector Search]
    E --> F[workspace_rag.py --ask]
    C --> G[Auto Review PR Workflow]
```

## 6. Security Gate Flow

```mermaid
flowchart TD
    A[Any User Request] --> B{Than Thong Gate}
    B -->|Local command| C[Execute with scripts]
    B -->|Web/API| D{Billing Check}
    D -->|Free| E[Allow]
    D -->|Paid| F[Block - Ask User]
    C --> G[Result]
    E --> G
    B -->|Sensitive| H[Ask Approval]
    H -->|Approved| C
    H -->|Denied| I[Cancel]
```

## 7. Error Handling Flow

```mermaid
flowchart TD
    A[Script Error] --> B{Type?}
    B -->|Syntax Error| C[auto-fix.yml PR]
    B -->|Runtime Error| D[Health Check Report]
    B -->|Dependency| E[pip-check Report]
    C --> F[GitHub Issue Created]
    D --> F
    E --> F
```

## 8. Data Flow Diagram

```mermaid
flowchart LR
    subgraph Input
        A[GitHub Push]
        B[User Message]
        C[GitHub Issue]
        D[Scheduled Cron]
    end
    
    subgraph Processing
        E[GitHub Runner]
        F[OpenClaw Agent]
        G[than_thong_console.py]
        H[memory_consolidator.py]
    end
    
    subgraph Storage
        I[GitHub Repo]
        J[Qdrant Vector DB]
        K[memory/*.md]
        L[MEMORY.md]
    end
    
    subgraph Output
        M[Telegram Response]
        N[GitHub Wiki]
        O[GitHub Release]
        P[PR Comment]
    end
    
    A --> E
    B --> F --> G
    C --> E
    D --> E
    E --> I
    F --> K --> H --> L
    H --> J
    G --> M
    E --> N
    E --> O
    E --> P
```
