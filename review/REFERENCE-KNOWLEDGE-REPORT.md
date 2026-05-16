# 📚 REFERENCE KNOWLEDGE REPORT

> Generated from 2,434 files across 21 categories
> Date: 2026-05-14

**Total:** 2434 files, 23051KB

## Category Index

- [spark](#spark): 727 files, API Server, Training, Vector Store
- [other](#other): 675 files, API Server, Agent, Data Collection, Inference, LLM
- [mcp](#mcp): 221 files, API Server, Agent
- [langchain](#langchain): 120 files, API Server, Agent, Data Collection, Search
- [web-scraping](#web-scraping): 118 files, Data Collection
- [test-files](#test-files): 101 files, Data Collection, LLM, Search, Training
- [finance](#finance): 98 files, API Server, Agent, Backtesting, Data Collection, Inference
- [utils](#utils): 90 files, API Server, Agent, Backtesting
- [firecrawl](#firecrawl): 56 files, API Server, Agent, Search
- [mem0](#mem0): 44 files, Agent, Search, Vector Store
- [openai](#openai): 32 files, API Server, Inference, LLM, Search
- [fastapi](#fastapi): 29 files, API Server, Agent
- [torch](#torch): 23 files, Training
- [llm-integration](#llm-integration): 22 files, 
- [ml-models](#ml-models): 20 files, Agent, Data Collection, Training
- [spark-data](#spark-data): 18 files, 
- [data-sources](#data-sources): 17 files, 
- [docs-processing](#docs-processing): 10 files, 
- [memory](#memory): 8 files, 
- [transformers](#transformers): 5 files, 

---

## spark

- **Files:** 727 | **Size:** 6397KB
- **Capabilities:** API Server, Training, Vector Store
- **Key Imports:** pyspark, typing, numpy, sys, inspect
- **Notable Classes:** `PandasOnSparkFrameMethods`, `SpecialAccumulatorIds`, `Accumulator`, `AccumulatorParam`
- **Notable Functions:** `attach_id_column`, `apply_batch`, `_deserialize_accumulator`, `__reduce__`, `value`

**Top Files:**
- [495KB] frame.py
- [139KB] classification.py
- [138KB] builtin.py

---

## other

- **Files:** 675 | **Size:** 7869KB
- **Capabilities:** API Server, Agent, Data Collection, Inference, LLM, Search, Training, Vector Store
- **Key Imports:** typing, sqlalchemy, alembic, re, sys
- **Notable Functions:** `upgrade`, `downgrade`, `upgrade`, `downgrade`, `upgrade`

**Top Files:**
- [69KB] modules.py
- [67KB] quality_analysis.py
- [64KB] asset_analysis.py

---

## mcp

- **Files:** 221 | **Size:** 2469KB
- **Capabilities:** API Server, Agent
- **Key Imports:** fastmcp, mcp, starlette, pydantic, __future__
- **Notable Classes:** `AccessToken`, `TokenHandler`, `AuthProvider`, `Auth0Provider`, `AuthorizationHandler`
- **Notable Functions:** `list_tools`, `read_skill`, `run_script`, `list_skills`, `memory_store`

**Top Files:**
- [57KB] test_json_schema_type.py
- [55KB] test_mount.py
- [48KB] test_local_provider_tools.py

---

## langchain

- **Files:** 120 | **Size:** 359KB
- **Capabilities:** API Server, Agent, Data Collection, Search
- **Key Imports:** browser_use, os, sys, dotenv, langchain_openai
- **Notable Classes:** `Person`, `PersonList`, `DiscordBot`
- **Notable Functions:** `is_login_page`, `get_llm`, `parse_arguments`, `initialize_agent`, `b64_to_png`

**Top Files:**
- [19KB] neptunedb.py
- [18KB] neptunegraph.py
- [17KB] test_agent_multiprocessing.py

---

## web-scraping

- **Files:** 118 | **Size:** 675KB
- **Capabilities:** Data Collection
- **Key Imports:** utils, downloader, os, ree, io
- **Notable Classes:** `LoginRequired`, `Downloader_afreeca`, `Video`, `Live_afreeca`, `File_artstation`
- **Notable Functions:** `init`, `fix_url`, `read`, `_get_stream`, `get`

**Top Files:**
- [27KB] youtube_downloader.py
- [26KB] edgar_fetcher.py
- [20KB] pixiv_downloader.py

---

## test-files

- **Files:** 101 | **Size:** 624KB
- **Capabilities:** Data Collection, LLM, Search, Training
- **Key Imports:** embedchain, browser_use, pytest, asyncio, playwright
- **Notable Classes:** `EmptyParamModel`, `TestActionFilters`, `TestActionParams`, `TestContext`, `ModelWithBrowserSession`
- **Notable Functions:** `print_ax_tree`, `print_all_fields`, `flatten_ax_tree`, `test_get_prompt_description_no_filters`, `test_page_filter_matching`

**Top Files:**
- [45KB] test_controller.py
- [45KB] test_registry.py
- [32KB] test_browser_session_start.py

---

## finance

- **Files:** 98 | **Size:** 1456KB
- **Capabilities:** API Server, Agent, Backtesting, Data Collection, Inference, Search, Training
- **Key Imports:** fast_trade, typing, numpy, pandas, datetime
- **Notable Classes:** `CoarseFineUniverseSelectionBenchmark`, `ContingentClaimsAnalysisDefaultPredictionAlpha`, `ContingentClaimsAnalysisAlphaModel`, `DataQualityReport`, `DataValidator`
- **Notable Functions:** `fetch_data`, `was_last_fetch_synthetic`, `fetch_ohlcv`, `_generate_synthetic`, `_generate_ohlcv_synthetic`

**Top Files:**
- [57KB] qlib_service.py
- [56KB] bt_provider.py
- [54KB] skfolio_core.py

---

## utils

- **Files:** 90 | **Size:** 804KB
- **Capabilities:** API Server, Agent, Backtesting
- **Key Imports:** agno, typing, sys, os, utils
- **Notable Classes:** `ChunkerConfig`, `LoaderConfig`, `AddConfig`, `ModelProvider`, `ReferencesFormat`
- **Notable Functions:** `load_func`, `_get_default_provider`, `_get_default_model_id`, `_get_default_temperature`, `_get_default_max_tokens`

**Top Files:**
- [77KB] helper_pandas_transform_with_state.py
- [45KB] base_pb2.py
- [36KB] variant_utils.py

---

## firecrawl

- **Files:** 56 | **Size:** 329KB
- **Capabilities:** API Server, Agent, Search
- **Key Imports:** firecrawl, os, dotenv, json, os,
- **Notable Classes:** `Colors`
- **Notable Functions:** `web_search`, `fetch_url`, `get_user_preferences`, `build_search_query`, `research_apartments`

**Top Files:**
- [40KB] test_recursive_schema_v1.py
- [37KB] test_recursive_schema.py
- [32KB] test_pagination.py

---

## mem0

- **Files:** 44 | **Size:** 424KB
- **Capabilities:** Agent, Search, Vector Store
- **Key Imports:** agno, mem0, google, llama_index, time
- **Notable Classes:** `MemoryADD`, `MultiAgentLearningSystem`
- **Notable Functions:** `load_data`, `add_memory`, `add_memories_for_speaker`, `process_conversation`, `process_all_conversations`

**Top Files:**
- [87KB] test_pgvector.py
- [30KB] test_valkey.py
- [30KB] project.py

---

## openai

- **Files:** 32 | **Size:** 217KB
- **Capabilities:** API Server, Inference, LLM, Search
- **Key Imports:** embedchain, gpt_oss, openai, os, typing
- **Notable Classes:** `AnswerRelevance`, `OpenAIAssistant`, `AIAssistant`, `ChatCompletionSampler`, `ContextRelevance`
- **Notable Functions:** `_generate_prompt`, `_generate_questions`, `_generate_embedding`, `_compute_similarity`, `_compute_score`

**Top Files:**
- [22KB] simple_browser_tool.py
- [17KB] service.py
- [16KB] gpt-4.1-company-researcher.py

---

## fastapi

- **Files:** 29 | **Size:** 159KB
- **Capabilities:** API Server, Agent
- **Key Imports:** fastapi, app, typing, uuid, sqlalchemy
- **Notable Classes:** `ExportRequest`, `BatchRequest`, `ScriptResult`, `FileService`
- **Notable Functions:** `get_app_or_404`, `_iso`, `_parse_iso`, `_export_sqlite`, `_export_logical_memories_gz`

**Top Files:**
- [22KB] memories.py
- [16KB] backup.py
- [15KB] test_users.py

---

## torch

- **Files:** 23 | **Size:** 287KB
- **Capabilities:** Training
- **Key Imports:** torch, datasets, open_mythos, open_r1, triton
- **Notable Classes:** `FineWebEduDataset`, `_attention`, `MultiHeadSelfAttention`, `AttentionCAE`, `AttentionCAETrainer`
- **Notable Functions:** `__iter__`, `get_lr`, `_list_ckpts`, `save_checkpoint`, `_attn_fwd`

**Top Files:**
- [43KB] moda.py
- [41KB] main.py
- [24KB] test_main.py

---

## llm-integration

- **Files:** 22 | **Size:** 123KB
- **Capabilities:** 
- **Key Imports:** anthropic, fastmcp, typing, os, browser_use
- **Notable Classes:** `AnthropicSamplingHandler`, `AzureOpenAIStructuredLLM`, `Colors`
- **Notable Functions:** `_iter_models_from_preferences`, `_convert_to_anthropic_messages`, `generate_response`, `get_llm`, `search_google`

**Top Files:**
- [15KB] test_providers_openai.py
- [13KB] anthropic.py
- [8KB] test_openai.py

---

## ml-models

- **Files:** 20 | **Size:** 154KB
- **Capabilities:** Agent, Data Collection, Training
- **Key Imports:** os, json, deepagents, dotenv, openai
- **Notable Classes:** `DeepAgentWrapper`, `Colors`, `Colors`
- **Notable Functions:** `_default_system_prompt`, `add_subagent`, `add_tool`, `add_middleware`, `build`

**Top Files:**
- [31KB] modeling_nekomind_moe.py
- [16KB] modeling.py
- [15KB] test_deepobject_style.py

---

## spark-data

- **Files:** 18 | **Size:** 138KB
- **Capabilities:** 
- **Key Imports:** pyspark, , typing, sys, functools
- **Notable Classes:** `ExecutionPipelineWorkflow`, `TechnicalFeaturesPipeline`
- **Notable Functions:** `run`, `_compute_indicators`, `_compute_rsi`, `_compute_macd`

**Top Files:**
- [30KB] zl_pipeline.py
- [16KB] pipelines_pb2.py
- [13KB] execution_pipeline.py

---

## data-sources

- **Files:** 17 | **Size:** 325KB
- **Capabilities:** 
- **Key Imports:** akshare, sys, json, pandas, datetime
- **Notable Classes:** `DateTimeEncoder`, `AKShareError`, `AlternativeDataWrapper`, `StockAnalysisError`, `StockAnalysisWrapper`
- **Notable Functions:** `default`, `to_dict`, `_convert_dataframe_to_json_safe`, `_safe_call_with_retry`, `get_energy_carbon`

**Top Files:**
- [81KB] ilostat_data.py
- [38KB] akshare_analysis.py
- [28KB] akshare_misc.py

---

## docs-processing

- **Files:** 10 | **Size:** 18KB
- **Capabilities:** 
- **Key Imports:** embedchain, hashlib, logging, typing, __future__
- **Notable Classes:** `BaseChunker`
- **Notable Functions:** `create_chunks`, `get_chunks`, `set_data_type`, `get_word_count`, `_split_by_paragraphs`

**Top Files:**
- [3KB] test_chunkers.py
- [3KB] chunker.py
- [3KB] base_chunker.py

---

## memory

- **Files:** 8 | **Size:** 208KB
- **Capabilities:** 
- **Key Imports:** sys, json, argparse, pathlib, re
- **Notable Classes:** `TurnRecord`, `FsVaultClient`, `IngestStats`
- **Notable Functions:** `download_evidence_file`, `discover_files`, `load_evidence_items`, `retrieve_for_item`, `_get_embedder`

**Top Files:**
- [117KB] longmemeval_bench.py
- [37KB] locomo_bench.py
- [16KB] longmemeval_adapter.py

---

## transformers

- **Files:** 5 | **Size:** 16KB
- **Capabilities:** 
- **Key Imports:** transformers, , subprocess, typing, logging
- **Notable Classes:** `DummyConfig`, `PushToHubRevisionCallback`, `ReflectedModelSpec`, `PreTrainedModelReflectionRegistry`
- **Notable Functions:** `is_slurm_available`, `on_save`, `run_benchmark_callback`, `get_callbacks`, `push_to_hub_revision`

**Top Files:**
- [5KB] hub.py
- [4KB] reflection.py
- [3KB] callbacks.py

---

