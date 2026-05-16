# CLI command structure patterns
> Nguon: G:AiOpenCLI
> Ngay: 2026-05-13

# Connecting OpenCLI via CDP (Remote/Headless Servers)  If you cannot use the Playwright MCP Bridge extension (e.g., in a remote headless server environment without a UI), OpenCLI provides an alternative: connecting directly to Chrome via **CDP (Chrome DevTools Protocol)**.  Because CDP binds to `localhost` by default for security reasons, accessing it from a remote server requires an additional networking tunnel.  This guide is broken down into three phases: 1. **Preparation**: Start Chrome with CDP enabled locally. 2. **Network Tunnels**: Expose that CDP port to your remote server using either **SSH Tunnels** or **Reverse Proxies**. 3. **Execution**: Run OpenCLI on your server.  ---  ## Phase 1: Preparation (Local Machine)  First, you need to start a Chrome browser on your local machine with remote debugging enabled.  **macOS:** ```bash /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
