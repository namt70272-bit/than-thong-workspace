# Content management patterns
> Nguon: G:AiOpenClaw-QuanLy
> Ngay: 2026-05-13

# Multi-Agent Telegram Setup â€” Multi-Bot Accounts  Route different forum topics (or groups) to different AI agents by using **separate Telegram bots**, each bound to its own agent.  ---  ## How It Works  ``` @researchbot (Account: researchbot) â”€â”€â†’ Agent: research @coderbot    (Account: coderbot)    â”€â”€â†’ Agent: coder ```  Each bot is a separate Telegram account in OpenClaw. You add both bots to the same group, and each responds independently with its own agent/personality/memory. 
