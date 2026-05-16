# Prompt Repeater v2 Runbook

## 完整流程

```
输入 Prompt
    ↓
自动检测任务类型（长文/定位/提取）
    ↓
reprompter 结构化
    ↓
prompt-engineering 优化
    ↓
生成 repeat x2/3 变体
    ↓
A/B 测试（cosine similarity 打分）
    ↓
输出 BEST_PROMPT.md + 提升报告
```

## 步骤详解

### 1. 任务检测

**检测逻辑：**
- 长文任务：prompt 长度 > 500 tokens
- 定位任务：包含 "find", "locate", "search", "找"
- 提取任务：包含 "extract", "pull", "get", "提取"

### 2. 结构化

使用 reprompter 技能：
```bash
reprompter structure --input "your-prompt"
```

### 3. 优化

使用 prompt-engineering 技能：
```bash
prompt-engineering optimize --input "structured-prompt"
```

### 4. 变体生成

**Repeat x2：**
```
原始："Find the 25th name in the list"
变体1："Find the 25th name in the list. Find the 25th name in the list."
变体2："Find the 25th name in the list. Please locate the 25th entry."
```

**Repeat x3：**
```
原始："Extract the phone number"
变体1："Extract the phone number. Extract the phone number. Extract the phone number."
变体2："Extract the phone number. Pull out the digits. Find the contact number."
```

### 5. A/B 测试

**Metrics：**
- cosine similarity vs 预期输出
- 准率 %
- token 消耗
- 响应时间

### 6. 输出

**BEST_PROMPT.md：**
```markdown
# Best Prompt

## 原始
[original-prompt]

## 最优变体
[best-variant]

## 得分
- Cosine Similarity: 0.92
- 准率: 89%
- Token 增加: 15%
- 速度影响: -8%
```

**提升报告：**
```markdown
# 提升报告

## 基准 vs 最优
| Metric | Baseline | Best | Delta |
|--------|----------|------|-------|
| 准率 | 45% | 79% | +76% |
| Token | 100 | 115 | +15% |
| Speed | 1.0s | 1.1s | -10% |

## 分析
- 重复策略：x2 变体表现最佳
- 优化点：任务明确性提升
- 建议：对于定位任务，推荐 x2 重复
```

## NameIndex Benchmark

### 测试集
- 50 名单
- 目标：找第 25 个
- 模型：Gemini/Claude/GPT/DeepSeek

### 运行
```bash
python3 scripts/repeat_bench.py
```

### 输出
```
NameIndex Benchmark Results
============================
Model: Gemini
  Baseline: 42%
  Repeat x2: 78% (+86%)
  Repeat x3: 75% (+79%)

Model: Claude
  Baseline: 45%
  Repeat x2: 79% (+76%)
  Repeat x3: 77% (+71%)

Best: Claude + Repeat x2 (79%)
```

## A/B Tester

### 使用
```bash
python3 scripts/ab_tester.py --prompt "your-prompt" --expected "expected-output"
```

### 输出
```
A/B Test Results
=================
Variant 1: cosine=0.85, tokens=115, time=1.1s
Variant 2: cosine=0.92, tokens=112, time=1.05s
Variant 3: cosine=0.88, tokens=120, time=1.15s

Winner: Variant 2 (cosine=0.92)
```

## Proactive Hook

### Cron 任务前
```json
{
  "pre_hook": "prompt-repeater-v2 --optimize --prompt \"{{task_prompt}}\""
}
```

### 子代理前
```json
{
  "pre_hook": "prompt-repeater-v2 --repeat-x2 --prompt \"{{subagent_prompt}}\""
}
```

## 安全检查

### ADL Scan
```bash
# 检查漂移
prompt-repeater-v2 --adl-scan
```

### VT Scan
```bash
# 检查 prompt injection
prompt-repeater-v2 --vt-scan --prompt "your-prompt"
```

## 故障排除

### 问题：准率没提升
**解决方案：**
- 检查任务类型检测是否正确
- 尝试不同的重复策略（x2 vs x3）
- 调整 prompt-engineering 参数

### 问题：Token 增加过多
**解决方案：**
- 使用更紧凑的重复变体
- 优化 prompt-engineering 阶段
- 启用 token 优化模式

### 问题：速度太慢
**解决方案：**
- 减少变体数量（从 5 → 3）
- 使用更快的模型进行打分
- 启用缓存
