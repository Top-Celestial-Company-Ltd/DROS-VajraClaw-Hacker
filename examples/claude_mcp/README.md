# 🤖 Claude Desktop & Claude Code (MCP Integration)

Connect Anthropic's Claude Desktop or Claude Code Agent directly to DROS VajraClaw for real-time tool governance.

## Setup Instructions
1. Ensure DROS Hacker Gateway is running:
   ```bash
   docker run -d -p 8080:8080 --name dros-gateway dros/hacker-gateway:v1.0.0
   ```
2. Copy `claude_desktop_config.json` into:
   * **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   * **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
3. Restart Claude Desktop. You will see `dros-vajraclaw` active in the installed MCP tools!
