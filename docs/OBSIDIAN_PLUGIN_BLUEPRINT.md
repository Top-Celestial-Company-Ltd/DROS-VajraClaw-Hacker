# 🔌 DROS Doctrinal Copilot - Obsidian 插件開發藍圖 (Plugin Blueprint)

## 🪷 打造最速降線的「隨身三藏十二部伴學」與「義理書僮」外掛

> **"Simplicity is the ultimate sophistication. By empowering the Obsidian ecosystem, DROS brings sovereign reasoning straight to the行者's fingertips."**  
> ── 康宸園有限公司/Jimmy Chen

本藍圖旨在為 **DROS Doctrinal Copilot (DROS 義理書僮)** 官方 Obsidian 插件提供完整的架構設計、核心 TypeScript 接口規格、Svelte 側邊欄組件樣式、以及從「本地 API 橋接」到「純本地 WASM 零依賴引擎」的兩階段開發路線圖。

---

## 🏛️ 一、 插件物理結構 (Anatomy of the Plugin)

一個標準的 DROS Obsidian 插件在目錄中由以下檔案組成：

```text
dros-copilot/
├── manifest.json         # 插件身份證（聲明名稱、版本、相依性）
├── styles.css            # 暗黑禪風與玻璃擬態樣式表
├── main.ts               # 插件入口（註冊 Ribbon 按鈕、命令快捷鍵、側邊欄視圖）
└── ChatPanel.svelte      # 使用 Svelte 建構的流式渲染對話與卡片預覽介面
```

### 1. manifest.json
```json
{
  "id": "dros-doctrinal-copilot",
  "name": "DROS Doctrinal Copilot",
  "version": "1.0.0",
  "minAppVersion": "1.0.0",
  "description": "Deterministic Runtime OS 隨身伴學與義理定錨 Copilot。提供金剛/菩薩雙軌合約推理、一鍵神經突觸雙向編織與義理卡片定錨。",
  "author": "康宸園有限公司/Jimmy Chen",
  "authorUrl": "https://github.com/JimmyChen-KC",
  "isDesktopOnly": false
}
```

---

## ⚡ 二、 第一階段：Local Proxy 橋接架構 (Fastest MVP)

在第一階段，插件作為前端 GUI，直接調用本機背景運行、佔用 100MB 內存的 FastAPI `gemini_proxy.py` 服務。

```
[ Obsidian UI Panel ] ───(HTTP fetch/stream)───> [ http://127.0.0.1:8000/chat ]
        │                                                     │
        ▼                                                     ▼
[ 選中文字 Alt+D ] ───────────────────────────────────> [ 讀取本地 16,071 內存字典 ]
```

### 1. main.ts (核心代碼實現)
```typescript
import { Plugin, WorkspaceLeaf, ItemView, Notice, requestUrl } from 'obsidian';

const VIEW_TYPE_DROS_CHAT = "dros-chat-view";

class DrosChatView extends ItemView {
    constructor(leaf: WorkspaceLeaf) {
        super(leaf);
    }

    getViewType() { return VIEW_TYPE_DROS_CHAT; }
    getDisplayText() { return "DROS 義理書僮"; }
    getIcon() { return "dharmachakra"; } // 自訂法輪圖標

    async onOpen() {
        const container = this.containerEl.children[1];
        container.empty();
        container.createEl("h3", { text: "🪷 DROS Copilot Panel" });
        
        // 這裡將掛載 Svelte 組件
        const chatContainer = container.createDiv({ cls: "dros-chat-container" });
        // new ChatPanel({ target: chatContainer });
    }
}

export default class DrosCopilotPlugin extends Plugin {
    async onload() {
        console.log('DROS Doctrinal Copilot 成功啟動！🪷');

        // 註冊側邊欄 View
        this.registerView(VIEW_TYPE_DROS_CHAT, (leaf) => new DrosChatView(leaf));

        // 在左側 Ribbon 區加入一鍵啟動按鈕
        this.addRibbonIcon('dharmachakra', '啟動 DROS 伴學', () => {
            this.activateView();
        });

        // 註冊快捷鍵 Alt + D：選中名相就地定錨與義理查詢
        this.addCommand({
            id: 'dros-quick-lookup',
            name: 'DROS：就地義理定錨與查詢',
            hotkeys: [{ modifiers: ["Alt"], key: "d" }],
            editorCallback: async (editor, view) => {
                const selectedText = editor.getSelection().trim();
                if (!selectedText) {
                    new Notice('請先選中您要定錨的義理名相！');
                    return;
                }

                new Notice(`🔍 正在向 DROS 請求定錨：${selectedText}...`);

                try {
                    const response = await requestUrl({
                        url: 'http://127.0.0.1:8000/chat',
                        method: 'POST',
                        contentType: 'application/json',
                        body: JSON.stringify({ query: selectedText })
                    });

                    // 在編輯器中將選中文字一鍵定錨為 [[名相]]
                    editor.replaceSelection(`[[${selectedText}]]`);
                    
                    // 彈出禪風卡片提示
                    new Notice(`【DROS 義理定錨成功】\n${response.json.reply}`);
                } catch (err) {
                    new Notice('❌ DROS 後端未啟動，請執行「DROS金剛注射器.bat」！');
                }
            }
        });
    }

    async activateView() {
        this.app.workspace.detachLeavesOfType(VIEW_TYPE_DROS_CHAT);
        await this.app.workspace.getRightLeaf(false).setViewState({
            type: VIEW_TYPE_DROS_CHAT,
            active: true,
        });
        this.app.workspace.revealLeaf(
            this.app.workspace.getLeavesOfType(VIEW_TYPE_DROS_CHAT)[0]
        );
    }
}
```

---

## 🎨 三、 禪風與玻璃擬態 UI 設計 (Styles & Svelte CSS)

為了營造極致的「數位道場」氛圍，插件界面採用 **暗黑禪風 + 玻璃擬態 (Glassmorphism) + 金色/玉色微光**：

```css
/* styles.css */
.dros-chat-container {
    background: rgba(30, 30, 30, 0.65) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 215, 0, 0.15); /* 金剛金色微框 */
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    color: #e0e0e0;
}

/* 菩薩隨流模式切換鈕 */
.dros-route-switch {
    background: linear-gradient(135deg, rgba(0, 128, 128, 0.2), rgba(255, 215, 0, 0.2));
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 8px 12px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.dros-route-switch:hover {
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
    transform: translateY(-1px);
}

/* 義理卡片 (Dharma Card) */
.dros-dharma-card {
    background: rgba(255, 255, 255, 0.05);
    border-left: 3px solid #ffd700; /* 金色定錨線 */
    border-radius: 4px;
    padding: 10px;
    margin: 8px 0;
    font-size: 0.9em;
}
```

---

## 🕸️ 四、 第二階段：Zero-Ops 純離線 TS/WASM 引擎 (No-Python)

為了實現大眾化零配置普及，在第二階段我們將徹底剔除 Python 背景服務，直接將 **DROS 內存拓撲尋址** 移植到插件的 JS 引擎中：

1.  **JSON 資產化 (Golden Manifest JSON)**：
    *   在每次 Release 時，使用 Python 腳本將 16,071 個節點的元數據（T-Number、定義、天台/唯識權重、雙向連結網格）編譯成一個高度壓縮的 `dros_golden_manifest.json`（約 5MB）。
2.  **JS 圖譜尋址器 (JS Graph Engine)**：
    *   在 `main.ts` 中直接載入此 JSON，並用 TypeScript 實現我們的圖譜搜尋算法：
    ```typescript
    class DrosLocalEngine {
        private graph: Map<string, any> = new Map();

        async init(jsonData: any) {
            for (const key in jsonData) {
                this.graph.set(key, jsonData[key]);
            }
        }

        // O(1) 毫秒級本地定錨與關聯檢索
        lookup(term: string) {
            return this.graph.get(term) || null;
        }

        // 突觸編織：尋找文本中包含的 16,071 個名相，並返回突觸坐標
        weave(text: string): string[] {
            const matched: string[] = [];
            this.graph.forEach((value, key) => {
                if (text.includes(key)) matched.push(key);
            });
            return matched;
        }
    }
    ```
3.  **直連 LLM API**：
    *   用戶直接在 Obsidian 插件設定面板中填入個人的 `Gemini API Key`。
    *   插件在本地完成圖譜檢索與 Prompt 合約拼裝，直接通過網頁端 `fetch` 發送請求給 Google API 端點，完全不需要任何雲端伺服器中轉！這實現了真正的 **「100% 隱私保護與零營運成本」**！

---

## 🚀 五、 發佈與生態收割策略 (Distribution Strategy)

1.  **測試期 (BRAT Release)**：
    *   將此目錄推送到 `https://github.com/JimmyChen-KC/obsidian-dros-copilot`。
    *   通知行者與種子研究者，在 Obsidian 中安裝 `BRAT` 插件，填入上述 Git 網址即可立刻搶先體驗。
2.  **官方發佈 (Official Registry)**：
    *   對 `obsidianmd/obsidian-releases` 提交 Pull Request，審核通過後，全球用戶均可在官方插件市場搜尋到 `DROS Doctrinal Copilot`。
3.  **商業數據金鑰 (Data Monetization)**：
    *   插件代碼完全開源（滿足 AGPL-3.0 協定）。
    *   `dros_golden_manifest.json`（16,071 個實心節點的完整校對黃金數據）採取專利授權。免費版僅內建 500 個高頻名相，完整版需輸入訂閱授權碼（License Key）啟用。此舉完美落實了「軟體開源、數據閉源商用」的雙軌防禦戰略！

---
*DROS v7.1 (Epistemic Edition) - Obsidian Plugin Development Blueprint. Created by 康宸園有限公司/Jimmy Chen.*
