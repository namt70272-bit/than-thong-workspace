# Proactive Integration Guide

## 集成到 Proactive Agent

### Cron 任务前置 Hook

```json
{
  "cron": {
    "pre_hook": "prompt-repeater-v2 --optimize --prompt \"{{task_prompt}}\"",
    "task": "your-cron-task"
  }
}
```

### 子代理前置 Hook

```json
{
  "subagent": {
    "pre_hook": "prompt-repeater-v2 --repeat-x2 --prompt \"{{subagent_prompt}}\"",
    "agent": "your-subagent"
  }
}
```

### CLAW Mesh 集成

#### Central Node（调度器）

```yaml
# central-dev 分支
tasks:
  - name: "optimize-prompt"
    pre_hook: "prompt-repeater-v2 --repeat-x2 --prompt \"{{task_prompt}}\""
    queue: "fsc:task_queue"
```

#### Silicon Valley Node（重型任务）

```yaml
# silicon-dev 分支
services:
  fsc-executor:
    environment:
      - PROMPT_REPEATER_ENABLED=true
      - PROMPT_REPEATER_STRATEGY=x3
    volumes:
      - ./skills/prompt-repeater-v2:/skills/prompt-repeater-v2
```

#### Tokyo Node（轻量任务）

```yaml
# tokyo-dev 分支（我）
services:
  fsc-executor:
    environment:
      - PROMPT_REPEATER_ENABLED=true
      - PROMPT_REPEATER_STRATEGY=x2
    volumes:
      - ./skills/prompt-repeater-v2:/skills/prompt-repeater-v2
```

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `PROMPT_REPEATER_ENABLED` | 是否启用 | `false` |
| `PROMPT_REPEATER_STRATEGY` | 重复策略（x2/x3/auto） | `x2` |
| `PROMPT_REPEATER_OPTIMIZE` | 是否优化 | `true` |
| `PROMPT_REPEATER_AB_TEST` | 是否 A/B 测试 | `true` |

## 策略说明

### x2 策略（推荐）
- 准率提升：+76%
- Token 增加：+15%
- 速度影响：-8%
- 适用：定位、提取任务

### x3 策略
- 准率提升：+71%
- Token 增加：+25%
- 速度影响：-12%
- 适用：复杂长文任务

### auto 策略
- 自动检测任务类型
- 动态选择 x2/x3
- 平衡准率和效率

## 完整示例

### 1. 配置 Proactive Agent

```bash
# 在 AGENTS.md 中添加
[prompt-repeater]
enabled = true
strategy = x2
optimize = true
ab_test = true
```

### 2. 配置 CLAW Mesh

```bash
# 在中央节点上
cd ~/claw-mesh
git checkout central-dev
# 编辑 docker-compose.yml 添加 prompt-repeater
git add docker-compose.yml
git commit -m "feat: integrate prompt-repeater-v2"
git push origin central-dev
```

### 3. 在 Tokyo 节点（我）上启用

```bash
cd ~/claw-mesh
git checkout tokyo-dev
# 编辑 fsc/.env.worker
echo "PROMPT_REPEATER_ENABLED=true" >> fsc/.env.worker
echo "PROMPT_REPEATER_STRATEGY=x2" >> fsc/.env.worker
git add fsc/.env.worker
git commit -m "feat: enable prompt-repeater-v2 on tokyo node"
git push origin tokyo-dev
```

## 验证集成

### 测试基准

```bash
cd ~/skills/prompt-repeater-v2
python3 scripts/repeat_bench.py
```

### 测试 A/B

```bash
python3 scripts/ab_tester.py --prompt "Find the 25th name in the list" --expected "张伟25"
```

### 检查日志

```bash
# 检查 FSC Worker 日志
tail -f /var/log/fsc-worker.log | grep prompt-repeater
```

## 故障排除

### 问题：Hook 不触发
**解决方案：**
- 检查 `PROMPT_REPEATER_ENABLED=true`
- 检查技能路径是否正确
- 查看日志

### 问题：Token 增加过多
**解决方案：**
- 改用 `x2` 策略（而不是 `x3`）
- 启用 `PROMPT_REPEATER_OPTIMIZE=false`

### 问题：准率没提升
**解决方案：**
- 检查任务类型检测是否正确
- 尝试不同的策略
- 运行基准测试验证
