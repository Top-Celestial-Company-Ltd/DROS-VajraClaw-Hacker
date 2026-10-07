import { Plugin, WorkspaceLeaf, ItemView, Notice, requestUrl, TFile, Setting, PluginSettingTab, App, addIcon, Platform } from 'obsidian';

declare const require: any;

const VIEW_TYPE_DROS_CHAT = "dros-chat-view";

interface DrosPluginSettings {
    langMode: "auto" | "zh" | "en";
    customPromptPath: string;
    injectContract: boolean;
    injectNodes: boolean;
    injectRuntimeMode: boolean;
    customPromptPosition: "prefix" | "suffix" | "advanced";
    engineMode: "direct" | "proxy" | "custom";
    geminiApiKey: string;
    routerModel: string;
    synthesizerModel: string;
    customEndpoint: string;
    customModel: string;
    customRouterModel: string;
    customApiKey: string;
    customApiFormat: "openai" | "gemini";
}

const DEFAULT_SETTINGS: DrosPluginSettings = {
    langMode: 'auto',
    customPromptPath: '',
    injectContract: true,
    injectNodes: true,
    injectRuntimeMode: true,
    customPromptPosition: 'suffix',
    engineMode: 'direct',
    geminiApiKey: '',
    routerModel: 'gemini-2.5-flash',
    synthesizerModel: 'gemini-2.5-pro',
    customEndpoint: '',
    customModel: '',
    customRouterModel: '',
    customApiKey: '',
    customApiFormat: 'openai'
};

const LOCALIZATION = {
    ZH: {
        title: "☸️ DROS Copilot",
        vajra: "📿 金剛",
        prajna: "🌊 菩薩",
        welcome: "隨身三藏十二部伴學已啟動。我是您的「DROS 義理書僮」。「金剛」與「菩薩」雙軌戒律已就緒，請隨時向我提問，或框選名相/文字、連結文件，按 Alt+D 進行快速定錨！",
        linkNote: "📎 連結當前編輯筆記",
        linkedNote: "📎 已連結當前筆記",
        placeholder: "輸入問題，或探討義理...",
        send: "發送 ☸️",
        clearNotice: "對話已清除。請隨時向我發問！",
        loading: "義理開採中，請靜候法音... 📿",
        saveBtn: "💾 存入館藏 (User_Pavilion)",
        saveNoteSuccess: "🎉 已成功建立館藏筆記：",
        saveNoteUpdate: "🗂️ 已成功更新館藏筆記：",
        saveNoteError: "❌ 儲存筆記失敗: ",
        linkNoticeSuccess: "📎 當前筆記內容已加入 AI 推理上下文！",
        linkNoticeCancel: "📎 已取消筆記連結",
        connError: "❌ 無法與 DROS 後端取得連線。請雙擊執行「雙擊執行-DROS金剛注射器.bat」啟動 Quart API 服務 (連接埠 5000)！",
        noticeSelectText: "請先選中您要定錨的義理名相！",
        noticeRequesting: "🔍 正在向 DROS 請求定錨：",
        noticeAnchorSuccess: "【DROS 義理定錨成功】",
        noticeNoBackend: "❌ DROS 後端未啟動，請執行「DROS金剛注射器.bat」！",
        unnamed: "未命名名相",
        anchorRecord: "DROS 義理定錨記錄",
        coreDoctrinal: "核心義理",
        searchTerm: "查詢名相",
        contractMode: "合約模式",
        anchorTime: "定錨時間",
        doctrinalAnalysis: "## 義理解析",
        vajraName: "金剛合約 (規約)",
        prajnaName: "菩薩合約 (詮釋)",
        switchedToVajra: "🧠 已切換至：金剛模式 (嚴格原典規約)",
        switchedToPrajna: "✨ 已切換至：菩薩隨流 (現代詮釋與推演)",
        settings: {
            tabTitle: "🪷 DROS Copilot 設定",
            guideTitle: "📖 快速使用指南與安裝步驟 | Quick Start & Installation Guide",
            installTitle: "📥 簡易安裝三步驟 | Simple 3-Step Installation",
            installSteps: [
                "<strong>啟用外掛</strong>：進入 <code>設定 (Settings)</code> -> <code>社群外掛載入 (Community Plugins)</code>，找到 <strong>DROS Doctrinal Copilot</strong> 並點擊啟用。",
                "<strong>啟動本地後端</strong>：前往專案根目錄，執行 <code>雙擊執行-DROS金剛注射器.bat</code> 啟動本地知識守護後端服務（若採 Gemini 直連模式則免此步）。",
                "<strong>喚醒伴學面板</strong>：點擊 Obsidian 左側功能列的 <strong>🪷 輪寶圖標 (Dharma Chakra Icon)</strong> 即可展開右側對話伴學視窗！"
            ],
            sopTitle: "💡 極簡操作 SOP",
            sopSteps: [
                "<strong>精準法義對話</strong>：在伴學對話框中發問，AI 將檢索召回原典義理並進行零幻覺深度解答。",
                "<strong>推理契約切換</strong>：面板頂部可隨時切換 <strong>金剛 (嚴謹客觀)</strong> 與 <strong>菩薩 (統攝圓融)</strong> 雙軌合約。",
                "<strong>筆記智慧關聯</strong>：點擊 <code>📎 連結當前編輯筆記</code>，即可無縫引入當前編輯筆記的內容作為對話上下文。",
                "<strong>一鍵儲存館藏</strong>：點擊 AI 回應下方的 <code>💾 存入館藏</code>，將對話紀錄自動以模式後綴防覆蓋格式存入 <code>User_Pavilion</code> 筆記庫。"
            ],
            langMode: {
                name: "🌐 介面語言 | Language Setting",
                desc: "選擇 DROS Copilot 的介面語系，支援自動偵測或手動切換，將雙向同步對話與設定面板。 | Select the interface language (supports auto-detection or manual switch, synced bi-directionally).",
                auto: "自動偵測 (Auto)",
                zh: "繁體中文 (ZH)",
                en: "English (EN)"
            },
            engineMode: {
                name: "🔌 引擎模式 | Engine Mode",
                desc: "直連模式 (與 Google Gemini API 進行通訊)、代理模式 (需啟動本機 Python Quart 後端) 或自訂模式 (自訂 API 服務)。 | Direct connection to Google Gemini API, Local Python Proxy mode, or Custom API Mode.",
                direct: "直連模式 | Zero-Ops Direct API",
                proxy: "代理模式 | Local Python Proxy",
                custom: "自訂模式 | Custom API Mode"
            },
            geminiApiKey: {
                name: "🔑 Gemini API Key",
                desc: "直連模式所需的 API 金鑰。 | API key required for Gemini Direct mode."
            },
            routerModel: {
                name: "🧭 路由模型 | Router Model",
                desc: "直連模式下，負責 Stage 1 JSON 路由與輕量任務的模型（推薦：gemini-2.5-flash）。 | The model responsible for Stage 1 JSON routing and lightweight tasks (Recommended: gemini-2.5-flash)."
            },
            synthesizerModel: {
                name: "🧠 合成與推理模型 | Synthesizer Model",
                desc: "直連模式下，負責 Stage 3 最終義理合成與深度推理的模型（推薦：gemini-2.5-pro）。 | The model responsible for Stage 3 final doctrinal synthesis and deep reasoning (Recommended: gemini-2.5-pro)."
            },
            customEndpoint: {
                name: "🔌 自訂 API 端點 | Custom API Endpoint",
                desc: "自訂 API 完整請求網址 (例如: https://openrouter.ai/api/v1/chat/completions)。 | Full custom API endpoint URL."
            },
            customModel: {
                name: "🧠 自訂模型名稱 | Custom Model Name",
                desc: "填寫自訂模型識別名稱 (例如: deepseek/deepseek-chat, gpt-4o 等)。 | Custom model identifier (e.g., deepseek-chat)."
            },
            customRouterModel: {
                name: "🧭 自訂路由模型 | Custom Router Model",
                desc: "填寫自訂路由模型識別名稱，負責 Stage 1 JSON 路由與輕量任務。留空則預設與自訂模型名稱一致。 | Custom model identifier for routing. Leave blank to match custom model name."
            },
            customApiKey: {
                name: "🔑 自訂 API 金鑰 | Custom API Key",
                desc: "自訂 API 模式所需的金鑰 (Bearer Token)。 | API token required for custom API mode."
            },
            customApiFormat: {
                name: "📡 自訂 API 協定格式 | API Format",
                desc: "指定自訂 API 相容的通訊協定格式。 | Specify the compatible protocol format for custom API.",
                openai: "OpenAI Chat Completions 格式 | OpenAI Format",
                gemini: "Gemini generateContent 格式 | Gemini Format"
            },
            customPromptPath: {
                name: "📜 自訂 Prompt 筆記路徑 | Custom Prompt Path",
                desc: "指定自訂 AI 提示詞筆記路徑（例如: User_Pavilion/custom-prompt.md）。留空則以「物理安全隔離防污染艙」直接讀取隱藏的系統預設 System_Prompt_v5.5.md。 | Path to your custom prompt note. Leave blank to use system default."
            },
            customPromptPosition: {
                name: "🎯 自訂 Prompt 整合模式 | Custom Prompt Mode",
                desc: "決定如何將大覺藏核心技術組件注入您的自訂提示詞中。 | Determine how doctrinal components are injected into your custom prompt.",
                suffix: "後置模式 | Suffix Mode (Core prompt first, custom prompt after)",
                prefix: "前置模式 | Prefix Mode (Custom prompt first, core prompt after)",
                advanced: "進階完全自訂模式 | Advanced Custom Mode (Manually place tags like {{EXECUTION_CONTRACT}})"
            },
            injectContract: {
                name: "📿 自動注入推理契約 | Auto Inject Contract",
                desc: "自動拼接 {{EXECUTION_CONTRACT}}，使您的自訂 Prompt 依然受到金剛/菩薩合約規則與禁用詞的嚴格約束。 | Auto-inject {{EXECUTION_CONTRACT}} to bind custom prompts under canonical rules."
            },
            injectNodes: {
                name: "📚 自動注入大覺藏節點 | Auto Inject Doctrinal Nodes",
                desc: "自動拼接 {{INJECTED_NODES}}，自動將本地檢索出的實心名相與 T-Number 座標動態注入上下文，拒絕幻覺。 | Auto-inject {{INJECTED_NODES}} to retrieve local nodes into the context."
            },
            injectRuntimeMode: {
                name: "⚙️ 自動注入運行時模式 | Auto Inject Runtime Mode",
                desc: "自動拼接 {{RUNTIME_MODE}}，標示本次對話為 Vajra/Interpretive/Speculative 模式以引導 AI 行為。 | Auto-inject {{RUNTIME_MODE}} to flag Vajra/Bodhisattva execution mode."
            }
        }
    },
    EN: {
        title: "☸️ DROS Copilot",
        vajra: "📿 Vajra",
        prajna: "🌊 Bodhisattva",
        welcome: "Tripiṭaka companion initialized. I am your DROS Doctrinal Assistant. 'Vajra' (Canonical) & 'Bodhisattva' (Interpretive) contracts injected. Ask me anything, or press Alt+D on a concept to anchor it!",
        linkNote: "📎 Link Active Note",
        linkedNote: "📎 Linked Active Note",
        placeholder: "Enter question or explore Buddhist doctrine...",
        send: "Send ☸️",
        clearNotice: "Chat history cleared. Ask me anything!",
        loading: "Mining doctrine, waiting for Dharma transmission... 📿",
        saveBtn: "💾 Archive to Pavilion",
        saveNoteSuccess: "🎉 Note created successfully in Pavilion: ",
        saveNoteUpdate: "🗂️ Note updated successfully in Pavilion: ",
        saveNoteError: "❌ Failed to save note: ",
        linkNoticeSuccess: "📎 Active note content linked to AI context!",
        linkNoticeCancel: "📎 Unlinked active note context",
        connError: "❌ Failed to connect to DROS. Please double-click 'DROS金剛注射器.bat' to launch the Quart API (Port 5000)!",
        noticeSelectText: "Please select a doctrinal term to anchor first!",
        noticeRequesting: "🔍 Requesting anchoring from DROS: ",
        noticeAnchorSuccess: "[DROS Doctrinal Anchoring Succeeded]",
        noticeNoBackend: "❌ DROS backend is offline, please run 'DROS金剛注射器.bat'!",
        unnamed: "Unnamed Concept",
        anchorRecord: "DROS Doctrinal Anchor Record",
        coreDoctrinal: "Core Doctrine",
        searchTerm: "Search Term",
        contractMode: "Contract Mode",
        anchorTime: "Anchor Time",
        doctrinalAnalysis: "## Doctrinal Analysis",
        vajraName: "Vajra Contract (Canonical)",
        prajnaName: "Bodhisattva Contract (Interpretive)",
        switchedToVajra: "🧠 Switched to: Vajra Mode (Strict Canonical Rules)",
        switchedToPrajna: "✨ Switched to: Bodhisattva Mode (Modern Interpretation & Deduction)",
        settings: {
            tabTitle: "🪷 DROS Copilot Settings",
            guideTitle: "📖 Quick Start & Installation Guide",
            installTitle: "📥 Simple 3-Step Installation",
            installSteps: [
                "<strong>Enable Plugin</strong>: Go to <code>Settings</code> -> <code>Community Plugins</code>, find <strong>DROS Doctrinal Copilot</strong> and enable it.",
                "<strong>Start Local Backend</strong>: Go to the project root directory and double-click <code>DROS金剛注射器.bat</code> to start the local backend service (not needed for Gemini direct mode).",
                "<strong>Open Copilot Panel</strong>: Click the <strong>🪷 Dharma Chakra Icon</strong> in the left ribbon to expand the chat panel on the right!"
            ],
            sopTitle: "💡 Quick Operation SOP",
            sopSteps: [
                "<strong>Precise Dialogue</strong>: Ask questions in the chat panel, and the AI will retrieve canonical texts and provide high-fidelity answers.",
                "<strong>Contract Switch</strong>: Easily switch between the <strong>Vajra (Strict/Canonical)</strong> and <strong>Bodhisattva (Modern/Interpretive)</strong> contracts at the top.",
                "<strong>Note Integration</strong>: Click <code>📎 Link Active Note</code> to seamlessly include your active note as conversational context.",
                "<strong>Archive to Pavilion</strong>: Click <code>💾 Archive to Pavilion</code> below the response to automatically save chat history to the <code>User_Pavilion</code> folder."
            ],
            langMode: {
                name: "🌐 Interface Language",
                desc: "Select the interface language for DROS Copilot (supports auto-detection or manual switch, synced bi-directionally with the chat panel).",
                auto: "Auto Detect",
                zh: "繁體中文 (ZH)",
                en: "English (EN)"
            },
            engineMode: {
                name: "🔌 Engine Mode",
                desc: "Direct Mode (communicate with Google Gemini API), Proxy Mode (local Python Quart backend required), or Custom Mode (custom API service).",
                direct: "Direct Mode | Zero-Ops Direct API",
                proxy: "Proxy Mode | Local Python Proxy",
                custom: "Custom Mode | Custom API Mode"
            },
            geminiApiKey: {
                name: "🔑 Gemini API Key",
                desc: "API key required for Direct mode."
            },
            routerModel: {
                name: "🧭 Router Model",
                desc: "In direct mode, the model responsible for Stage 1 JSON routing and lightweight tasks (Recommended: gemini-2.5-flash)."
            },
            synthesizerModel: {
                name: "🧠 Synthesizer Model",
                desc: "In direct mode, the model responsible for Stage 3 final synthesis and deep reasoning (Recommended: gemini-2.5-pro)."
            },
            customEndpoint: {
                name: "🔌 Custom API Endpoint",
                desc: "Full API endpoint URL for custom API mode (e.g. https://openrouter.ai/api/v1/chat/completions or https://api.deepseek.com/chat/completions)."
            },
            customModel: {
                name: "🧠 Custom Model Name",
                desc: "Custom model identifier name (e.g. deepseek/deepseek-chat, gpt-4o, etc.)."
            },
            customRouterModel: {
                name: "🧭 Custom Router Model",
                desc: "Custom router model name responsible for Stage 1 JSON routing and lightweight tasks. Leave blank to inherit the custom model name."
            },
            customApiKey: {
                name: "🔑 Custom API Key",
                desc: "API token required for custom API mode (Bearer Token)."
            },
            customApiFormat: {
                name: "📡 API Format",
                desc: "Specify the compatible communication protocol format for custom API.",
                openai: "OpenAI Chat Completions Format",
                gemini: "Gemini generateContent Format"
            },
            customPromptPath: {
                name: "📜 Custom Prompt Path",
                desc: "Specify the note path for your custom prompt (e.g. User_Pavilion/custom-prompt.md). Leave blank to read the hidden default System_Prompt_v5.5.md from the safety vault."
            },
            customPromptPosition: {
                name: "🎯 Custom Prompt Mode",
                desc: "Determine how the core doctrinal components are injected into your custom prompt.",
                suffix: "Suffix Mode (Recommended / Core prompt first, custom prompt after)",
                prefix: "Prefix Mode (Custom prompt first, core prompt after)",
                advanced: "Advanced Custom Mode (Manually place tags like {{EXECUTION_CONTRACT}} in your note)"
            },
            injectContract: {
                name: "📿 Auto Inject Contract",
                desc: "Automatically append {{EXECUTION_CONTRACT}} to bind your custom prompt under the strict rules of Vajra/Bodhisattva contracts."
            },
            injectNodes: {
                name: "📚 Auto Inject Doctrinal Nodes",
                desc: "Automatically append {{INJECTED_NODES}} to dynamically inject localized search terms and coordinate indexes into the context."
            },
            injectRuntimeMode: {
                name: "⚙️ Auto Inject Runtime Mode",
                desc: "Automatically append {{RUNTIME_MODE}} to mark the conversation mode (Vajra/Interpretive/Speculative) and guide AI behavior."
            }
        }
    }
};

function parseContractYaml(yamlText: string): any {
    const res: any = {
        Name: "Fallback Contract",
        InferenceMode: "Bodhisattva",
        FallbackMode: "Bodhisattva",
        AuthorityNodesOnly: false,
        HardeningLevel: 5,
        Temperature: 0.2,
        Model: ""
    };
    const lines = yamlText.split("\n");
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith("#")) continue;
        const parts = trimmed.split(":");
        if (parts.length >= 2) {
            const key = parts[0].trim();
            let val = parts.slice(1).join(":").trim();
            if (val.includes("#")) {
                val = val.split("#")[0].trim();
            }
            if (val.startsWith('"') && val.endsWith('"')) {
                val = val.substring(1, val.length - 1);
            } else if (val.startsWith("'") && val.endsWith("'")) {
                val = val.substring(1, val.length - 1);
            }
            if (key === "Name") res.Name = val;
            else if (key === "InferenceMode") res.InferenceMode = val;
            else if (key === "FallbackMode") res.FallbackMode = val;
            else if (key === "AuthorityNodesOnly") res.AuthorityNodesOnly = val === "true";
            else if (key === "HardeningLevel") res.HardeningLevel = parseInt(val, 10) || 5;
            else if (key === "Temperature") res.Temperature = parseFloat(val) || 0.2;
            else if (key === "Model") res.Model = val;
        }
    }
    return res;
}

async function nlmQueryAsync(query: string, notebookName: string): Promise<string> {
    if (typeof require === "undefined") return "";
    try {
        const { exec } = require("child_process");
        const notebookMapping: Record<string, string> = {
            "AI佛學總論": "387b899a-2095-4f68-945f-e2fa35c5670b",
            "AI善導大師-淨土宗": "f0535e46-586a-44e2-bffd-59b12b21e77a",
            "AI龍樹-中觀": "359f6065-dbec-4e5e-b85d-8377c7eea534",
            "AI惠能-禪宗": "396d76a0-c781-48fe-8a73-534b1d25fc37",
            "數位佛堂_3.0": "32e46b09-02f5-42d5-91c7-ca8147ffdcaa",
            "AI彌勒-唯識宗": "b2a15532-edba-4f18-9565-96ab1ab045d9",
            "AI智者大師-天台宗": "9b4b3b81-7bd6-492b-9e71-63a1c63a60c4",
        };
        const notebookId = notebookMapping[notebookName] || notebookName;
        return new Promise((resolve) => {
            exec(`nlm query notebook ${notebookId} "${query.replace(/"/g, '\\"')}"`, (error: any, stdout: string, stderr: any) => {
                if (error) {
                    console.warn("NotebookLM RAG fallback failed:", error);
                    resolve("");
                } else {
                    const cleanResult = stdout.replace(/\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])|\[\*\]|\[\+\]/g, "");
                    resolve(`\n--- NotebookLM Vector RAG 檢索結果 ---\n${cleanResult}\n`);
                }
            });
        });
    } catch (e) {
        console.warn("Child process not available for nlm:", e);
        return "";
    }
}

async function getLocalNodeContent(app: App, coreNodes: string[], relatedNodes: string[]): Promise<string> {
    const files = app.vault.getMarkdownFiles();
    let context = "";
    let totalLen = 0;

    const findFileByName = (name: string) => {
        const cleanTarget = name.replace(/[^\u4e00-\u9fa5\w]/g, "").toLowerCase();
        if (!cleanTarget) return null;

        let bestFile = null;
        let maxScore = 0;

        for (const file of files) {
            const path = file.path.toLowerCase();
            if (!path.startsWith("core/") && !path.startsWith("user_pavilion/")) {
                continue;
            }

            const cleanBasename = file.basename.replace(/[^\u4e00-\u9fa5\w]/g, "").toLowerCase();

            if (cleanBasename === cleanTarget) {
                return file;
            }

            let score = 0;
            if (cleanBasename.includes(cleanTarget) || cleanTarget.includes(cleanBasename)) {
                score = 0.8;
            }

            let intersection = 0;
            const setBasename = new Set(cleanBasename.split(""));
            for (const char of cleanTarget) {
                if (setBasename.has(char)) {
                    intersection++;
                }
            }
            const overlap = intersection / Math.max(cleanTarget.length, cleanBasename.length);
            const totalScore = score + overlap * 0.19;

            if (totalScore > maxScore && totalScore >= 0.4) {
                maxScore = totalScore;
                bestFile = file;
            }
        }

        return bestFile;
    };

    const readAndProcessFile = async (file: TFile, isCore: boolean) => {
        try {
            let contentText = await app.vault.read(file);
            let data = "";

            const summaryRegex = /> \[!NOTE\] (?:核心義理|歷史精鍊).*?\n(?:> .*?\n)+/is;
            const quoteRegex = /> \[(?:!QUOTE|!NOTE)\] (?:原典引文|跨館開採|語義融合).*?\n(?:> .*?\n)+/is;

            const summaryMatch = contentText.match(summaryRegex);
            const quoteMatch = contentText.match(quoteRegex);

            if (summaryMatch || quoteMatch) {
                if (summaryMatch) data += summaryMatch[0] + "\n";
                if (quoteMatch) data += quoteMatch[0] + "\n";
            } else {
                data = contentText;
            }

            if (!isCore) {
                if (totalLen > 12000) {
                    console.log(`[!] Context Watchdog: Discarded non-core node: ${file.basename}`);
                    return;
                } else if (totalLen > 8000) {
                    console.log(`[!] Context Watchdog: Dimension reduction for: ${file.basename}`);
                    data = data.substring(0, 150) + "\n... (Token 限制，內容已折疊)\n";
                }
            }

            context += `\n--- 節點: ${file.basename} ---\n${data}\n`;
            totalLen += data.length;
        } catch (e) {
            console.error(`[!] Failed to read node ${file.basename}:`, e);
        }
    };

    for (const name of coreNodes) {
        const file = findFileByName(name);
        if (file) {
            await readAndProcessFile(file, true);
        }
    }

    for (const name of relatedNodes) {
        const file = findFileByName(name);
        if (file) {
            await readAndProcessFile(file, false);
        }
    }

    return context;
}

function getEffectiveConfig(settings: DrosPluginSettings): DrosPluginSettings {
    const config = { ...settings };

    if (Platform.isMobile) {
        // 📱 行動端「不對稱熔斷器」：
        // 1. 若為代理模式，因行動端連不上 127.0.0.1，強制熔斷並降級回 direct
        // 2. 若為自訂模式且 Endpoint 是本地 IP/localhost，同樣強制降級為 direct
        const endpoint = config.customEndpoint || "";
        const isLocalCustom = config.engineMode === "custom" && 
            (endpoint.includes("127.0.0.1") || 
             endpoint.includes("localhost") || 
             endpoint.includes("192.168."));

        if (config.engineMode === "proxy" || isLocalCustom) {
            console.log("[Dros Core] 行動端檢測：偵測到本地端點，啟動物理熔斷，降級為直連雲端 Google API 模式。");
            return {
                ...config,
                engineMode: "direct",
                routerModel: "gemini-2.5-flash",
                synthesizerModel: "gemini-2.5-pro",
                customEndpoint: "",
                customModel: "",
                customRouterModel: ""
            };
        }
    }

    return config;
}

async function queryDrosEngine(
    query: string,
    contractId: string,
    customPromptContent: string,
    lang: string,
    app: App,
    settings: DrosPluginSettings
): Promise<string> {
    const effectiveSettings = getEffectiveConfig(settings);

    if (effectiveSettings.engineMode === "proxy") {
        const response = await requestUrl({
            url: 'http://127.0.0.1:5000/v1/chat/completions',
            method: 'POST',
            contentType: 'application/json',
            body: JSON.stringify({
                messages: [{ role: "user", content: query }],
                contract: contractId,
                custom_prompt: customPromptContent || undefined,
                lang: lang,
                stream: false
            })
        });
        return response.json.choices[0].message.content;
    } else {
        const apiKey = effectiveSettings.geminiApiKey;

        // 如果是 direct 模式，必須先檢查 API 金鑰
        if (effectiveSettings.engineMode === "direct" && !apiKey) {
            throw new Error(lang === "ZH" ? "請先在外掛設定中填寫您的 Gemini API Key！" : "Please configure your Gemini API Key in the plugin settings first!");
        }

        const routingPrompt = `分析使用者提問，並決定調用節點。請嚴格輸出 JSON。
提問內容：${query}
格式：{"tool": "graph_query", "core_nodes": ["核心節點名稱"], "related_nodes": ["關聯節點名稱"], "fallback_notebook": "AI佛學總論"}
`;
        let plan: { core_nodes: string[]; related_nodes: string[]; fallback_notebook: string } = {
            core_nodes: [],
            related_nodes: [],
            fallback_notebook: "AI佛學總論"
        };

        if (effectiveSettings.engineMode === "custom") {
            const endpoint = effectiveSettings.customEndpoint;
            if (!endpoint) {
                console.log("[Dros Core] 自訂端點未設定，跳過 Stage 1 路由。");
            } else {
                const routerModelName = effectiveSettings.customRouterModel || effectiveSettings.customModel || "gpt-4o-mini";
                console.log(`[DROS JS Engine] Stage 1: Custom Routing with ${routerModelName}`);
                if (effectiveSettings.customApiFormat === "openai") {
                    try {
                        const headers: Record<string, string> = {
                            'Content-Type': 'application/json'
                        };
                        if (effectiveSettings.customApiKey) {
                            headers['Authorization'] = `Bearer ${effectiveSettings.customApiKey}`;
                        }
                        
                        const bodyData: any = {
                            model: routerModelName,
                            messages: [
                                { role: "user", content: routingPrompt }
                            ],
                            temperature: 0.1
                        };
                        
                        try {
                            const response = await requestUrl({
                                url: endpoint,
                                method: 'POST',
                                headers: headers,
                                body: JSON.stringify({
                                    ...bodyData,
                                    response_format: { type: "json_object" }
                                })
                            });
                            const routeText = response.json.choices[0].message.content;
                            const jsonMatch = routeText.match(/\{.*\}/s);
                            if (jsonMatch) {
                                plan = JSON.parse(jsonMatch[0]);
                            }
                        } catch (jsonErr) {
                            console.warn("Retrying custom router without response_format...", jsonErr);
                            const response = await requestUrl({
                                url: endpoint,
                                method: 'POST',
                                headers: headers,
                                body: JSON.stringify(bodyData)
                            });
                            const routeText = response.json.choices[0].message.content;
                            const jsonMatch = routeText.match(/\{.*\}/s);
                            if (jsonMatch) {
                                plan = JSON.parse(jsonMatch[0]);
                            }
                        }
                        console.log(`[DROS JS Engine] Custom Routed -> Core: ${JSON.stringify(plan.core_nodes)} / Related: ${JSON.stringify(plan.related_nodes)}`);
                    } catch (e) {
                        console.warn("[DROS JS Engine] Custom Router step failed, fallback to direct query:", e);
                    }
                } else {
                    // gemini 格式的自訂端點
                    try {
                        const headers: Record<string, string> = {
                            'Content-Type': 'application/json'
                        };
                        if (effectiveSettings.customApiKey) {
                            headers['Authorization'] = `Bearer ${effectiveSettings.customApiKey}`;
                        }
                        const response = await requestUrl({
                            url: endpoint,
                            method: 'POST',
                            headers: headers,
                            body: JSON.stringify({
                                contents: [{ role: "user", parts: [{ text: routingPrompt }] }],
                                generationConfig: {
                                    responseMimeType: "application/json",
                                    temperature: 0.1
                                }
                            })
                        });
                        const routeText = response.json.candidates[0].content.parts[0].text;
                        const jsonMatch = routeText.match(/\{.*\}/s);
                        if (jsonMatch) {
                            plan = JSON.parse(jsonMatch[0]);
                        }
                        console.log(`[DROS JS Engine] Custom Gemini Routed -> Core: ${JSON.stringify(plan.core_nodes)} / Related: ${JSON.stringify(plan.related_nodes)}`);
                    } catch (e) {
                        console.warn("[DROS JS Engine] Custom Gemini Router step failed:", e);
                    }
                }
            }
        } else if (effectiveSettings.engineMode === "direct") {
            if (apiKey) {
                console.log(`[DROS JS Engine] Stage 1: Routing with ${effectiveSettings.routerModel}`);
                try {
                    const routeResponse = await requestUrl({
                        url: `https://generativelanguage.googleapis.com/v1beta/models/${effectiveSettings.routerModel}:generateContent?key=${apiKey}`,
                        method: "POST",
                        contentType: "application/json",
                        body: JSON.stringify({
                            contents: [{ role: "user", parts: [{ text: routingPrompt }] }],
                            generationConfig: {
                                responseMimeType: "application/json",
                                temperature: 0.1
                            }
                        })
                    });
                    const routeText = routeResponse.json.candidates[0].content.parts[0].text;
                    const jsonMatch = routeText.match(/\{.*\}/s);
                    if (jsonMatch) {
                        plan = JSON.parse(jsonMatch[0]);
                    }
                    console.log(`[DROS JS Engine] Routed -> Core: ${JSON.stringify(plan.core_nodes)} / Related: ${JSON.stringify(plan.related_nodes)}`);
                } catch (e) {
                    console.warn("[DROS JS Engine] Router step failed, fallback to direct query:", e);
                }
            } else {
                console.log("[Dros Core] 無 Gemini API Key，跳過 Stage 1 路由，直接進行全庫定錨。");
            }
        }

        let context = "";
        try {
            context = await getLocalNodeContent(app, plan.core_nodes || [], plan.related_nodes || []);
        } catch (e) {
            console.error("[DROS JS Engine] Node ingestion failed:", e);
        }

        if (!context || !context.trim()) {
            console.log("[DROS JS Engine] Local nodes not found, attempting NotebookLM RAG fallback...");
            try {
                context = await nlmQueryAsync(query, plan.fallback_notebook || "AI佛學總論");
            } catch (e) {
                console.warn("[DROS JS Engine] NotebookLM RAG fallback failed:", e);
            }
        }

        const hasStrongAuthority = context.includes("--- 節點:");
        let runtimeMode = "Bodhisattva";
        let temperature = 0.2;
        let modelToUse = effectiveSettings.engineMode === "custom" 
            ? effectiveSettings.customModel 
            : effectiveSettings.synthesizerModel;
        let contractEnvelopeText = "";

        try {
            const contractPath = `contracts/${contractId}.yaml`;
            const fileExists = await app.vault.adapter.exists(contractPath);
            let contractData: any = null;
            if (fileExists) {
                const yamlText = await app.vault.adapter.read(contractPath);
                contractData = parseContractYaml(yamlText);
            }
            
            if (contractData) {
                if (hasStrongAuthority) {
                    runtimeMode = contractData.InferenceMode || "Bodhisattva";
                    temperature = contractData.Temperature !== undefined ? contractData.Temperature : 0.2;
                    if (contractData.Model) modelToUse = contractData.Model;
                } else {
                    runtimeMode = contractData.FallbackMode || "Bodhisattva";
                    temperature = 0.2;
                    modelToUse = effectiveSettings.engineMode === "custom"
                        ? (effectiveSettings.customRouterModel || effectiveSettings.customModel)
                        : effectiveSettings.routerModel;
                }
                
                const modeMapping: Record<string, string> = {
                    "Vajra": "【金剛模式 · 嚴格宗派推演】",
                    "Interpretive": "【詮釋模式 · 義理跨界映射】",
                    "Speculative": "【般若模式 · 高階湧現推演】",
                    "Bodhisattva": "【菩薩模式 · 適應性導航】"
                };
                const modeText = modeMapping[runtimeMode] || "【菩薩模式 · 適應性導航】";
                contractEnvelopeText = `
[DROS CONTRACT ENVELOPE]
Contract Name: ${contractData.Name || contractId}
Mode: ${modeText}
Hardening Level: ${contractData.HardeningLevel || 5}/10
Require Authority Coordinates (T-Number): ${contractData.AuthorityNodesOnly || false}
`;
            }
        } catch (e) {
            console.warn("[DROS JS Engine] Failed to load or parse contract, using fallback default:", e);
        }

        if (!contractEnvelopeText) {
            const defaultMode = contractId.includes("vajra") ? "Vajra" : "Bodhisattva";
            runtimeMode = hasStrongAuthority ? defaultMode : "Bodhisattva";
            temperature = runtimeMode === "Vajra" ? 0.05 : 0.5;
            const modeText = runtimeMode === "Vajra" ? "【金剛模式 · 嚴格宗派推演】" : "【菩薩模式 · 適應性導航】";
            contractEnvelopeText = `
[DROS CONTRACT ENVELOPE]
Contract Name: ${contractId === "default_vajra" ? "Balanced Vajra" : "Speculative Prajna"}
Mode: ${modeText}
Hardening Level: 6/10
Require Authority Coordinates (T-Number): ${runtimeMode === "Vajra"}
`;
        }

        let promptTemplate = "";
        if (customPromptContent && customPromptContent.trim()) {
            promptTemplate = customPromptContent;
        } else {
            const defaultPromptPath = ".obsidian/plugins/dros-doctrinal-copilot/System_Prompt_v5.5.md";
            try {
                if (await app.vault.adapter.exists(defaultPromptPath)) {
                    promptTemplate = await app.vault.adapter.read(defaultPromptPath);
                }
            } catch (e) {
                console.error("[DROS JS Engine] Failed to read default system prompt:", e);
            }
        }

        if (!promptTemplate) {
            promptTemplate = `# DROS 核心提示詞：v5.5 契約感知與雙軌智慧引擎

## 🛑 系統核心定位
你是 DROS 7.2 的「法義推理與認識論治理單元」。你的所有行為完全由本次注入的 \`{{EXECUTION_CONTRACT}}\`、\`{{RUNTIME_MODE}}\` 與 \`{{INJECTED_NODES}}\` 決定。除此之外，其餘世界皆不存在。

## 📥 本次運行注入
- \`{{EXECUTION_CONTRACT}}\`：當前完整契約
- \`{{INJECTED_NODES}}\`：權威實心名相節點
- \`{{RUNTIME_MODE}}\`：Vajra 或 Bodhisattva
- \`{{TARGET_LANGUAGE}}\`：目標輸出語系

## ⚙️ 雙軌執行鐵律（必須嚴格遵守）

### 【Vajra 金剛模式】（嚴格治學模式）
- 極度嚴謹、客觀、學術化。
- **完全禁止**任何跨域比喻、現代科學、哲學、心理學等外部框架。
- 所有推論**必須**完全依據 \`{{INJECTED_NODES}}\`。
- 每段重要論述後**必須**標註真實出處或明確註記「[T-Number: 未載於當前節點]」。
- 若資料不足或無法嚴格依據注入內容，必須明確回答：「依據當前 DROS 授權庫，無法進行有效金剛推演。」

### 【Bodhisattva 菩薩模式】（普渡親和模式）
- 語言應**溫潤、親切、具慈悲感**，像一位善知識在循循善誘。
- 允許使用生活化譬喻與**受控的跨域比喻**，幫助現代人理解佛法。
- 進行跨域比喻時，**必須**在該段落最前方明確標示：

> [!ANALOGY] 跨域比喻（現代視角）
> 以下內容為方便理解所做的客觀類比，非佛法本義。

- 比喻結束後，必須立即回到佛法本位，並提醒「此僅為方便理解，請以佛法正見為依歸。」
- 結尾宜帶有溫和鼓勵，幫助使用者生起信心與歡喜心。

## ✍️ 通用鐵律（全模式適用）
- 輸出語言必須嚴格遵循 \`{{TARGET_LANGUAGE}}\` 所約定之語系。
- 嚴禁使用任何主觀 or 不確定詞彙（我認為、我覺得、大概是、可能、應該是等）。
- 嚴格遵守本次 \`{{EXECUTION_CONTRACT}}\` 中的所有規則。
- 保持學術誠實：有依據則精準闡述，無充分依據則誠實說明。
`;
        }

        const targetLanguage = lang === "ZH" ? "Traditional Chinese (zh-TW)" : "Academic English (en-US)";
        
        const systemContent = promptTemplate
            .replace("{{EXECUTION_CONTRACT}}", contractEnvelopeText)
            .replace("{{INJECTED_NODES}}", context.trim() ? context : "（未檢索到相關權威節點）")
            .replace("{{RUNTIME_MODE}}", runtimeMode)
            .replace("{{TARGET_LANGUAGE}}", targetLanguage);

        let finalPrompt = systemContent + `\n\n【使用者問題】：${query}`;

        // ------------------ 分流發送 ------------------
        if (effectiveSettings.engineMode === "custom") {
            const endpoint = effectiveSettings.customEndpoint;
            if (!endpoint) {
                throw new Error(lang === "ZH" ? "請先在外掛設定中填寫自訂 API 端點 (Endpoint)！" : "Please configure your Custom API Endpoint in the settings first!");
            }

            console.log(`[DROS JS Engine] Stage 3: Synthesizing with Custom API (${modelToUse}) under ${runtimeMode} mode (format: ${effectiveSettings.customApiFormat})`);

            if (effectiveSettings.customApiFormat === "openai") {
                const headers: Record<string, string> = {
                    'Content-Type': 'application/json'
                };
                if (effectiveSettings.customApiKey) {
                    headers['Authorization'] = `Bearer ${effectiveSettings.customApiKey}`;
                }

                const response = await requestUrl({
                    url: endpoint,
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify({
                        model: modelToUse || "gpt-4o",
                        messages: [
                            { role: "system", content: systemContent },
                            { role: "user", content: query }
                        ],
                        temperature: temperature
                    })
                });

                if (response.json && response.json.choices && response.json.choices[0] && response.json.choices[0].message) {
                    return response.json.choices[0].message.content;
                } else {
                    throw new Error(lang === "ZH" ? "自訂 API 未返回有效的回答，請檢查您的配置與端點。" : "Custom API returned an empty response. Please verify your configuration and endpoint.");
                }
            } else {
                // gemini 格式
                const headers: Record<string, string> = {
                    'Content-Type': 'application/json'
                };
                if (effectiveSettings.customApiKey) {
                    headers['Authorization'] = `Bearer ${effectiveSettings.customApiKey}`;
                }

                const response = await requestUrl({
                    url: endpoint,
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify({
                        contents: [{ role: "user", parts: [{ text: finalPrompt }] }],
                        generationConfig: {
                            temperature: temperature
                        }
                    })
                });

                if (response.json && response.json.candidates && response.json.candidates[0].content && response.json.candidates[0].content.parts) {
                    return response.json.candidates[0].content.parts[0].text;
                } else {
                    throw new Error(lang === "ZH" ? "自訂 Gemini API 未返回有效的回答，請檢查您的配置。" : "Custom Gemini API returned an empty response.");
                }
            }
        } else {
            console.log(`[DROS JS Engine] Stage 3: Synthesizing with ${modelToUse} under ${runtimeMode} mode (temp: ${temperature})`);

            let geminiModel = modelToUse;
            if (geminiModel === "pro" || geminiModel === "gemini-3.1-pro" || geminiModel === "gemini-3.1-pro-preview") {
                geminiModel = "gemini-2.5-pro";
            } else if (geminiModel === "flash-lite") {
                geminiModel = "gemini-2.5-flash";
            }

            const synthesisResponse = await requestUrl({
                url: `https://generativelanguage.googleapis.com/v1beta/models/${geminiModel}:generateContent?key=${apiKey}`,
                method: "POST",
                contentType: "application/json",
                body: JSON.stringify({
                    contents: [{ role: "user", parts: [{ text: finalPrompt }] }],
                    generationConfig: {
                        temperature: temperature
                    }
                })
            });

            if (synthesisResponse.json.candidates && synthesisResponse.json.candidates[0].content && synthesisResponse.json.candidates[0].content.parts) {
                return synthesisResponse.json.candidates[0].content.parts[0].text;
            } else {
                throw new Error(lang === "ZH" ? "Gemini API 未返回有效的回答，請檢查您的金鑰或配額。" : "Gemini API returned an empty response. Please verify your key and quota.");
            }
        }
    }
}

class DrosChatView extends ItemView {
    private messageListEl: HTMLDivElement;
    private inputEl: HTMLTextAreaElement;
    private selectedContract: string = "default_vajra";
    private injectActiveNote: boolean = false;
    private lastUserQuery: string = "DROS對話記錄"; 
    
    // 狀態變數
    currentLang: "ZH" | "EN" = "ZH";
    chatHistory: { sender: "user" | "assistant"; text: string }[] = [];

    plugin: DrosCopilotPlugin;

    constructor(leaf: WorkspaceLeaf, plugin: DrosCopilotPlugin) {
        super(leaf);
        this.plugin = plugin;
    }

    getViewType() { return VIEW_TYPE_DROS_CHAT; }
    getDisplayText() { return "DROS Copilot"; }
    getIcon() { return "dros-dharmachakra"; }

    getLanguage(): "ZH" | "EN" {
        return this.currentLang;
    }

    async onOpen() {
        this.currentLang = this.plugin.getEffectiveLang();
        // 如果歷史對話為空，初始化歡迎語；或者如果只有第一條歡迎語，也讓它對齊當前語系
        if (this.chatHistory.length === 0) {
            this.chatHistory.push({ sender: "assistant", text: LOCALIZATION[this.currentLang].welcome });
        } else if (this.chatHistory.length === 1 && 
            (this.chatHistory[0].text === LOCALIZATION.ZH.welcome || this.chatHistory[0].text === LOCALIZATION.EN.welcome)) {
            this.chatHistory[0].text = LOCALIZATION[this.currentLang].welcome;
        }
        this.renderView();
    }

    renderView() {
        const container = this.containerEl.children[1];
        container.empty();

        const t = LOCALIZATION[this.currentLang];

        // 建立最上層外框，自帶禪風玻璃擬態樣式
        const mainWrapper = container.createDiv({ cls: "dros-copilot-wrapper" });

        // 1. Header 部分
        const header = mainWrapper.createDiv({ cls: "dros-copilot-header" });
        header.createEl("h3", { text: t.title });
        
        // 模式切換器 (金剛/菩薩) 與 語言切換按鈕 的容器
        const headerRight = header.createDiv({ cls: "dros-header-right", attr: { style: "display: flex; gap: 6px; align-items: center;" } });

        // 🌐 語言切換按鈕
        const langToggle = headerRight.createEl("button", {
            text: this.currentLang === "ZH" ? "🌐 EN" : "🌐 中文",
            cls: "dros-lang-toggle-btn"
        });

        langToggle.addEventListener("click", async () => {
            // 翻轉語言狀態並全域儲存同步
            this.currentLang = this.currentLang === "ZH" ? "EN" : "ZH";
            this.plugin.settings.langMode = this.currentLang === "ZH" ? "zh" : "en";
            await this.plugin.saveSettings();

            // 如果第一條是舊歡迎語，自動翻譯歡迎語
            if (this.chatHistory.length > 0 && 
                (this.chatHistory[0].text === LOCALIZATION.ZH.welcome || this.chatHistory[0].text === LOCALIZATION.EN.welcome)) {
                this.chatHistory[0].text = LOCALIZATION[this.currentLang].welcome;
            }
            this.renderView();
            new Notice(this.currentLang === "ZH" ? "🌐 已啟用中文介面" : "🌐 English UI activated");

            // 同步刷新設定面板自身（若剛好開著）
            this.plugin.refreshSettingsTab();
        });
        
        const modeSelector = headerRight.createDiv({ cls: "dros-mode-selector" });
        const vajraBtn = modeSelector.createEl("button", { 
            text: t.vajra, 
            cls: `dros-mode-btn ${this.selectedContract === "default_vajra" ? "active" : ""}` 
        });
        const prajnaBtn = modeSelector.createEl("button", { 
            text: t.prajna, 
            cls: `dros-mode-btn ${this.selectedContract === "speculative_prajna" ? "active" : ""}` 
        });

        vajraBtn.addEventListener("click", () => {
            this.selectedContract = "default_vajra";
            vajraBtn.addClass("active");
            prajnaBtn.removeClass("active");
            new Notice(t.switchedToVajra);
        });

        prajnaBtn.addEventListener("click", () => {
            this.selectedContract = "speculative_prajna";
            prajnaBtn.addClass("active");
            vajraBtn.removeClass("active");
            new Notice(t.switchedToPrajna);
        });

        // 2. 聊天記錄滾動區
        this.messageListEl = mainWrapper.createDiv({ cls: "dros-message-list" });
        
        // 渲染對話歷史
        this.chatHistory.forEach((msg, idx) => {
            const isWelcome = idx === 0 && (msg.text === LOCALIZATION.ZH.welcome || msg.text === LOCALIZATION.EN.welcome);
            this.appendMessageEl(msg.sender, msg.text, isWelcome);
        });

        // 3. 注入當前筆記控制欄
        const controlBar = mainWrapper.createDiv({ cls: "dros-control-bar" });
        const injectToggle = controlBar.createEl("button", {
            text: this.injectActiveNote ? t.linkedNote : t.linkNote,
            cls: `dros-inject-btn ${this.injectActiveNote ? "active" : ""}`
        });
        
        injectToggle.addEventListener("click", () => {
            this.injectActiveNote = !this.injectActiveNote;
            if (this.injectActiveNote) {
                injectToggle.addClass("active");
                injectToggle.setText(t.linkedNote);
                new Notice(t.linkNoticeSuccess);
            } else {
                injectToggle.removeClass("active");
                injectToggle.setText(t.linkNote);
                new Notice(t.linkNoticeCancel);
            }
        });

        // 4. 輸入區域
        const inputArea = mainWrapper.createDiv({ cls: "dros-input-area" });
        this.inputEl = inputArea.createEl("textarea", {
            placeholder: t.placeholder
        });

        const sendBtn = inputArea.createEl("button", {
            text: t.send,
            cls: "dros-send-btn"
        });

        const clearBtn = inputArea.createEl("button", {
            text: "🧹",
            cls: "dros-clear-btn"
        });

        // 發送按鈕點擊事件
        sendBtn.addEventListener("click", () => this.handleSend());
        
        // 鍵盤 Ctrl + Enter / Enter 發送
        this.inputEl.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                this.handleSend();
            }
        });

        // 清除對話
        clearBtn.addEventListener("click", () => {
            this.chatHistory = [{ sender: "assistant", text: t.clearNotice }];
            this.renderView();
        });

        // 自動滾動到底部
        this.messageListEl.scrollTop = this.messageListEl.scrollHeight;
    }

    // 物理建立並添加單條消息 DOM 節點
    appendMessageEl(sender: "user" | "assistant", text: string, isWelcome: boolean = false) {
        const t = LOCALIZATION[this.currentLang];
        const msgBubble = this.messageListEl.createDiv({ 
            cls: `dros-chat-bubble ${sender}` 
        });
        
        const avatar = msgBubble.createDiv({ cls: "avatar" });
        avatar.setText(sender === "user" ? "👤" : "☸️");

        const bubbleContainer = msgBubble.createDiv({ cls: "bubble-container" });
        const content = bubbleContainer.createDiv({ cls: "content" });
        content.setText(text);

        // 如果是 AI 回應，在下方加上一鍵存為筆記按鈕
        if (sender === "assistant" && !isWelcome) {
            const actions = bubbleContainer.createDiv({ cls: "dros-message-actions" });
            const saveBtn = actions.createEl("button", {
                text: t.saveBtn,
                cls: "dros-save-note-btn"
            });

            saveBtn.addEventListener("click", async () => {
                await this.saveAsPavilionNote(this.lastUserQuery, text);
            });
        }

        // 自動滾動到底部
        this.messageListEl.scrollTop = this.messageListEl.scrollHeight;
        return msgBubble;
    }

    // 專用對話推送方法，同時記錄歷史狀態
    appendMessage(sender: "user" | "assistant", text: string) {
        this.chatHistory.push({ sender, text });
        const isWelcome = this.chatHistory.length === 1 && (text === LOCALIZATION.ZH.welcome || text === LOCALIZATION.EN.welcome);
        return this.appendMessageEl(sender, text, isWelcome);
    }

    async handleSend() {
        let query = this.inputEl.value.trim();
        if (!query) return;

        const t = LOCALIZATION[this.currentLang];

        this.inputEl.value = "";
        this.appendMessage("user", query);
        this.lastUserQuery = query; 

        // 如果開啟了「連結當前編輯筆記」，獲取當前編輯器中的文字
        let activeNoteContent = "";
        if (this.injectActiveNote) {
            const activeFile = this.app.workspace.getActiveFile();
            if (activeFile) {
                activeNoteContent = await this.app.vault.read(activeFile);
                query = this.currentLang === "ZH" 
                    ? `【參考當前編輯筆記內容】\n${activeNoteContent}\n\n【使用者提問】：${query}`
                    : `[Reference Active Note Content]\n${activeNoteContent}\n\n[User Question]: ${query}`;
            }
        }

        // 🌟 英文模式下，隱性注入「學術梵漢英定錨編譯指令」
        if (this.currentLang === "EN") {
            query += "\n\n[System Directive: Regardless of the retrieval language, compile your final response in high-fidelity academic English. Maintain key Sanskrit terms in italics and write original classical Chinese concepts in brackets, e.g. Tathātā [真如] or Ālayavijñāna [阿賴耶識].]";
        }

        // 插入載入中氣泡
        const loadingBubble = this.appendMessage("assistant", t.loading);
        loadingBubble.addClass("shimmering");

        // 讀取自訂 Prompt 或 官方預設唯讀安全艙內的 Prompt
        let customPromptContent = "";
        const customPath = this.plugin.settings.customPromptPath;
        if (customPath) {
            try {
                const file = this.app.vault.getAbstractFileByPath(customPath);
                if (file && file instanceof TFile) {
                    const rawPrompt = await this.app.vault.read(file);
                    
                    // 根據選單與開關設定，自動組裝核心佔位符
                    const pos = this.plugin.settings.customPromptPosition || "suffix";
                    if (pos === "advanced") {
                        customPromptContent = rawPrompt;
                    } else if (pos === "suffix") {
                        // 核心技術提示詞在上，使用者自訂 Prompt 在下 (後置模式)
                        let combined = "";
                        if (this.plugin.settings.injectContract) combined += "{{EXECUTION_CONTRACT}}\n\n";
                        if (this.plugin.settings.injectNodes) combined += "{{INJECTED_NODES}}\n\n";
                        if (this.plugin.settings.injectRuntimeMode) combined += "{{RUNTIME_MODE}}\n\n";
                        customPromptContent = combined + rawPrompt;
                    } else {
                        // 使用者自訂 Prompt 在上，核心技術提示詞在下 (前置模式)
                        let combined = rawPrompt + "\n\n";
                        if (this.plugin.settings.injectContract) combined += "{{EXECUTION_CONTRACT}}\n\n";
                        if (this.plugin.settings.injectNodes) combined += "{{INJECTED_NODES}}\n\n";
                        if (this.plugin.settings.injectRuntimeMode) combined += "{{RUNTIME_MODE}}\n\n";
                        customPromptContent = combined;
                    }
                } else {
                    new Notice(this.currentLang === "ZH" 
                        ? `❌ 找不到自訂 Prompt 檔案：${customPath}`
                        : `❌ Custom prompt file not found: ${customPath}`);
                }
            } catch (e) {
                console.error("Failed to read custom prompt:", e);
            }
        } else {
            // 強制從外掛的隱藏唯讀路徑載入預設提示詞
            const defaultPromptPath = ".obsidian/plugins/dros-doctrinal-copilot/System_Prompt_v5.5.md";
            try {
                if (await this.app.vault.adapter.exists(defaultPromptPath)) {
                    customPromptContent = await this.app.vault.adapter.read(defaultPromptPath);
                }
            } catch (e) {
                console.error("Failed to read default system prompt from plugin folder:", e);
            }
        }

        try {
            const reply = await queryDrosEngine(
                query,
                this.selectedContract,
                customPromptContent,
                this.currentLang,
                this.app,
                this.plugin.settings
            );

            loadingBubble.removeClass("shimmering");
            loadingBubble.querySelector(".content").setText(reply);
            
            // 同步更新記憶體中的 assistant 回應
            this.chatHistory[this.chatHistory.length - 1].text = reply;
            
            // 重新為回應綁定存檔事件
            this.bindSaveEvent(loadingBubble, reply);
            
            this.messageListEl.scrollTop = this.messageListEl.scrollHeight;
        } catch (err) {
            loadingBubble.removeClass("shimmering");
            let errText = err.message || t.connError;
            if (this.plugin.settings.engineMode === "proxy") {
                errText = t.connError;
            }
            loadingBubble.querySelector(".content").setText(errText);
            this.chatHistory[this.chatHistory.length - 1].text = errText;
        }
    }

    async saveAsPavilionNote(query: string, replyText: string) {
        const t = LOCALIZATION[this.currentLang];
        let cleanedTitle = query
            .replace(/[^\w\u4e00-\u9fa5\- 　]/g, "")
            .trim()
            .replace(/[\.\s]+$/, "");
        
        if (cleanedTitle.length > 30) {
            cleanedTitle = cleanedTitle.substring(0, 30);
        }
        // 若擷取後以「請」結尾（通常是「請教」、「請開示」等問句被截斷），移除以防與後置角色後綴（如 _金剛、_菩薩）拼接突兀
        cleanedTitle = cleanedTitle.replace(/請$/, "").trim().replace(/[\.\s]+$/, "");

        if (!cleanedTitle) {
            cleanedTitle = t.unnamed;
        }

        // 根據當前選中的合約與語言決定前置角色標記 (roleTag)
        let roleTag = "";
        if (this.currentLang === "ZH") {
            roleTag = this.selectedContract === "default_vajra" ? "金剛" : "菩薩";
        } else {
            roleTag = this.selectedContract === "default_vajra" ? "Vajra" : "Bodhisattva";
        }

        const folderPath = "User_Pavilion";
        try {
            const folder = this.app.vault.getAbstractFileByPath(folderPath);
            if (!folder) {
                await this.app.vault.createFolder(folderPath);
            }

            // 新命名結構：DROS-角色-擷取標題
            let fullPath = `${folderPath}/DROS-${roleTag}-${cleanedTitle}.md`;
            let existingFile = this.app.vault.getAbstractFileByPath(fullPath);
            let counter = 1;
            while (existingFile) {
                fullPath = `${folderPath}/DROS-${roleTag}-${cleanedTitle}-${counter}.md`;
                existingFile = this.app.vault.getAbstractFileByPath(fullPath);
                counter++;
            }

            // 根據當前語言輸出 DROS 7.0 結構化定錨標籤
            let markdownContent = `# ${t.anchorRecord}\n\n`;
            markdownContent += `> [!NOTE] ${t.coreDoctrinal}\n`;
            markdownContent += `> - **${t.searchTerm}**：[[${query}]]\n`;
            markdownContent += `> - **${t.contractMode}**：${this.selectedContract === "default_vajra" ? t.vajraName : t.prajnaName}\n`;
            markdownContent += `> - **${t.anchorTime}**：${new Date().toLocaleString()}\n\n`;
            markdownContent += `${t.doctrinalAnalysis}\n\n${replyText}\n`;

            try {
                const newFile = await this.app.vault.create(fullPath, markdownContent);
                new Notice(`${t.saveNoteSuccess}${fullPath}`);
                await this.app.workspace.getLeaf().openFile(newFile);
            } catch (createErr) {
                console.warn("Vault create failed, falling back to adapter write:", createErr);
                await this.app.vault.adapter.write(fullPath, markdownContent);
                new Notice(`${t.saveNoteSuccess}${fullPath}`);
                if (typeof (this.app.vault as any).trigger === "function") {
                    await (this.app.vault as any).trigger("refresh");
                }
                const scannedFile = this.app.vault.getAbstractFileByPath(fullPath);
                if (scannedFile && scannedFile instanceof TFile) {
                    await this.app.workspace.getLeaf().openFile(scannedFile);
                }
            }
        } catch (e) {
            new Notice(`${t.saveNoteError}${e.message}`);
        }
    }

    bindSaveEvent(bubbleEl: HTMLDivElement, replyText: string) {
        const bubbleContainer = bubbleEl.querySelector(".bubble-container");
        if (!bubbleContainer) return;

        const t = LOCALIZATION[this.currentLang];

        const existingActions = bubbleContainer.querySelector(".dros-message-actions");
        if (existingActions) existingActions.remove();

        const actions = bubbleContainer.createDiv({ cls: "dros-message-actions" });
        const saveBtn = actions.createEl("button", {
            text: t.saveBtn,
            cls: "dros-save-note-btn"
        });

        saveBtn.addEventListener("click", async () => {
            await this.saveAsPavilionNote(this.lastUserQuery, replyText);
        });
    }
}

export default class DrosCopilotPlugin extends Plugin {
    settings: DrosPluginSettings;

    getEffectiveLang(): "ZH" | "EN" {
        const mode = this.settings.langMode || "auto";
        if (mode === "zh") return "ZH";
        if (mode === "en") return "EN";
        
        try {
            const obsLang = (window.localStorage.getItem("language") || "en").toLowerCase();
            if (obsLang.includes("zh")) {
                return "ZH";
            }
        } catch (e) {
            console.warn("Failed to detect Obsidian language:", e);
        }
        return "EN";
    }

    refreshSettingsTab() {
        try {
            const settingTab = (this.app as any).setting?.settingTabs?.find((tab: any) => tab.id === this.manifest.id);
            if (settingTab && (this.app as any).setting?.activeTab === settingTab) {
                settingTab.display();
            }
        } catch (e) {
            console.warn("Failed to refresh settings tab:", e);
        }
    }

    async onload() {
        console.log('DROS Doctrinal Copilot 成功啟動！☸️');
        await this.loadSettings();

        this.registerView(VIEW_TYPE_DROS_CHAT, (leaf) => new DrosChatView(leaf, this));

        addIcon('dros-dharmachakra', `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><circle cx="6.5" cy="12.5" r="3.5" /><circle cx="15.5" cy="16.5" r="3.5" /><path d="M 6.5,9 A 7.5,7.5 0 0,1 15.5,13" /><path d="M 3,12.5 A 11,11 0 0,0 15.5,20" /><path d="M 10,8.5 C 10,3.5 13.5,2 17,8" /><path d="M 7.5,10 C 8,5 14,4 17.5,11" /><path d="M 10,8.5 L 14,13" /></svg>`);

        this.addRibbonIcon('dros-dharmachakra', '☸️ 啟動 DROS 伴學 / Open DROS Copilot', () => {
            this.activateView();
        });

        this.addSettingTab(new DrosSettingTab(this.app, this));

        // Alt + D 快捷定錨
        this.addCommand({
            id: 'dros-quick-lookup',
            name: 'DROS：就地義理定錨與查詢 / Doctrinal Anchoring',
            hotkeys: [{ modifiers: ["Alt"], key: "d" }],
            editorCallback: async (editor, view) => {
                const selectedText = editor.getSelection().trim();
                
                // 動態獲取當前語言
                const leaves = this.app.workspace.getLeavesOfType(VIEW_TYPE_DROS_CHAT);
                let currentLang: "ZH" | "EN" = "ZH";
                if (leaves.length > 0) {
                    const chatView = leaves[0].view as DrosChatView;
                    currentLang = chatView.getLanguage();
                }
                const t = LOCALIZATION[currentLang];

                if (!selectedText) {
                    new Notice(t.noticeSelectText);
                    return;
                }

                new Notice(`${t.noticeRequesting}${selectedText}...`);

                // 英文模式下同樣在 API payload 中注入翻譯指令
                let apiQuery = selectedText;
                if (currentLang === "EN") {
                    apiQuery += "\n\n[System Directive: Regardless of the retrieval language, compile your final response in high-fidelity academic English. Maintain key Sanskrit terms in italics and write original classical Chinese concepts in brackets, e.g. Tathātā [真如] or Ālayavijñāna [阿賴耶識].]";
                }

                let customPromptContent = "";
                const customPath = this.settings.customPromptPath;
                if (customPath) {
                    try {
                        const file = this.app.vault.getAbstractFileByPath(customPath);
                        if (file && file instanceof TFile) {
                            const rawPrompt = await this.app.vault.read(file);
                            const pos = this.settings.customPromptPosition || "suffix";
                            if (pos === "advanced") {
                                customPromptContent = rawPrompt;
                            } else if (pos === "suffix") {
                                let combined = "";
                                if (this.settings.injectContract) combined += "{{EXECUTION_CONTRACT}}\n\n";
                                if (this.settings.injectNodes) combined += "{{INJECTED_NODES}}\n\n";
                                if (this.settings.injectRuntimeMode) combined += "{{RUNTIME_MODE}}\n\n";
                                customPromptContent = combined + rawPrompt;
                            } else {
                                let combined = rawPrompt + "\n\n";
                                if (this.settings.injectContract) combined += "{{EXECUTION_CONTRACT}}\n\n";
                                if (this.settings.injectNodes) combined += "{{INJECTED_NODES}}\n\n";
                                if (this.settings.injectRuntimeMode) combined += "{{RUNTIME_MODE}}\n\n";
                                customPromptContent = combined;
                            }
                        }
                    } catch (e) {
                        console.error(e);
                    }
                } else {
                    // 強制從外掛的隱藏唯讀路徑載入預設提示詞
                    const defaultPromptPath = ".obsidian/plugins/dros-doctrinal-copilot/System_Prompt_v5.5.md";
                    try {
                        if (await this.app.vault.adapter.exists(defaultPromptPath)) {
                            customPromptContent = await this.app.vault.adapter.read(defaultPromptPath);
                        }
                    } catch (e) {
                        console.error(e);
                    }
                }

                try {
                    const reply = await queryDrosEngine(
                        apiQuery,
                        "default_vajra",
                        customPromptContent,
                        currentLang,
                        this.app,
                        this.settings
                    );

                    // 編輯器中一鍵定錨為雙鏈 [[名相]]
                    editor.replaceSelection(`[[${selectedText}]]`);
                    new Notice(`${t.noticeAnchorSuccess}\n${reply}`);
                } catch (err) {
                    if (this.settings.engineMode === "proxy") {
                        new Notice(t.noticeNoBackend);
                    } else {
                        new Notice(err.message || "Request failed");
                    }
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

    async loadSettings() {
        this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
    }

    async saveSettings() {
        await this.saveData(this.settings);
    }
}

class DrosSettingTab extends PluginSettingTab {
    plugin: DrosCopilotPlugin;

    constructor(app: App, plugin: DrosCopilotPlugin) {
        super(app, plugin);
        this.plugin = plugin;
    }

    display(): void {
        const { containerEl } = this;
        containerEl.empty();

        const lang = this.plugin.getEffectiveLang();
        const t = LOCALIZATION[lang].settings;

        containerEl.createEl('h2', { text: t.tabTitle });

        // 📖 隨身使用手冊與安裝指引 (Quick Start Guide & Installation Steps)
        const guideDetails = containerEl.createEl('details', {
            cls: 'dros-settings-guide-container',
            attr: { open: 'true' }
        });
        
        guideDetails.createEl('summary', {
            text: t.guideTitle,
            cls: 'dros-settings-guide-summary'
        });

        const guideContent = guideDetails.createDiv({ cls: 'dros-settings-guide-content' });
        
        guideContent.createEl('h3', { text: t.installTitle });
        const stepsOl = guideContent.createEl('ol');
        t.installSteps.forEach(step => {
            stepsOl.createEl('li').innerHTML = step;
        });

        guideContent.createEl('h3', { text: t.sopTitle });
        const sopsUl = guideContent.createEl('ul');
        t.sopSteps.forEach(sop => {
            sopsUl.createEl('li').innerHTML = sop;
        });

        // 🌐 介面語言 / Interface Language
        new Setting(containerEl)
            .setName(t.langMode.name)
            .setDesc(t.langMode.desc)
            .addDropdown(dropdown => dropdown
                .addOption('auto', t.langMode.auto)
                .addOption('zh', t.langMode.zh)
                .addOption('en', t.langMode.en)
                .setValue(this.plugin.settings.langMode || 'auto')
                .onChange(async (value: "auto" | "zh" | "en") => {
                    this.plugin.settings.langMode = value;
                    await this.plugin.saveSettings();
                    
                    // 同步更新所有已打開的對話視窗語系與歡迎語
                    const leaves = this.app.workspace.getLeavesOfType(VIEW_TYPE_DROS_CHAT);
                    const newEffectiveLang = this.plugin.getEffectiveLang();
                    leaves.forEach(leaf => {
                        if (leaf.view instanceof DrosChatView) {
                            const chatView = leaf.view;
                            chatView.currentLang = newEffectiveLang;
                            if (chatView.chatHistory.length > 0 && 
                                (chatView.chatHistory[0].text === LOCALIZATION.ZH.welcome || chatView.chatHistory[0].text === LOCALIZATION.EN.welcome)) {
                                chatView.chatHistory[0].text = LOCALIZATION[newEffectiveLang].welcome;
                            }
                            chatView.renderView();
                        }
                    });
                    this.display(); // 刷新設定頁自身
                }));

        // 🔌 引擎模式
        new Setting(containerEl)
            .setName(t.engineMode.name)
            .setDesc(t.engineMode.desc)
            .addDropdown(dropdown => dropdown
                .addOption('direct', t.engineMode.direct)
                .addOption('proxy', t.engineMode.proxy)
                .addOption('custom', t.engineMode.custom)
                .setValue(this.plugin.settings.engineMode || 'direct')
                .onChange(async (value: "direct" | "proxy" | "custom") => {
                    this.plugin.settings.engineMode = value;
                    await this.plugin.saveSettings();
                    this.display(); // 刷新以顯示/隱藏與 API Key 相關的設定
                }));

        if (this.plugin.settings.engineMode === 'direct') {
            new Setting(containerEl)
                .setName(t.geminiApiKey.name)
                .setDesc(t.geminiApiKey.desc)
                .addText(text => {
                    text.inputEl.type = 'password';
                    text.setPlaceholder('AIzaSy...')
                        .setValue(this.plugin.settings.geminiApiKey || '')
                        .onChange(async (value) => {
                            this.plugin.settings.geminiApiKey = value.trim();
                            await this.plugin.saveSettings();
                        });
                });

            new Setting(containerEl)
                .setName(t.routerModel.name)
                .setDesc(t.routerModel.desc)
                .addDropdown(dropdown => dropdown
                    .addOption('gemini-2.5-flash', 'gemini-2.5-flash')
                    .addOption('gemini-2.5-pro', 'gemini-2.5-pro')
                    .addOption('gemini-1.5-flash', 'gemini-1.5-flash')
                    .addOption('gemini-1.5-pro', 'gemini-1.5-pro')
                    .setValue(this.plugin.settings.routerModel || 'gemini-2.5-flash')
                    .onChange(async (value) => {
                        this.plugin.settings.routerModel = value;
                        await this.plugin.saveSettings();
                    }));

            new Setting(containerEl)
                .setName(t.synthesizerModel.name)
                .setDesc(t.synthesizerModel.desc)
                .addDropdown(dropdown => dropdown
                    .addOption('gemini-2.5-pro', 'gemini-2.5-pro')
                    .addOption('gemini-2.5-flash', 'gemini-2.5-flash')
                    .addOption('gemini-1.5-pro', 'gemini-1.5-pro')
                    .addOption('gemini-1.5-flash', 'gemini-1.5-flash')
                    .setValue(this.plugin.settings.synthesizerModel || 'gemini-2.5-pro')
                    .onChange(async (value) => {
                        this.plugin.settings.synthesizerModel = value;
                        await this.plugin.saveSettings();
                    }));
        }

        if (this.plugin.settings.engineMode === 'custom') {
            new Setting(containerEl)
                .setName(t.customEndpoint.name)
                .setDesc(t.customEndpoint.desc)
                .addText(text => text
                    .setPlaceholder('https://openrouter.ai/api/v1/chat/completions')
                    .setValue(this.plugin.settings.customEndpoint || '')
                    .onChange(async (value) => {
                        this.plugin.settings.customEndpoint = value.trim();
                        await this.plugin.saveSettings();
                    }));

            new Setting(containerEl)
                .setName(t.customModel.name)
                .setDesc(t.customModel.desc)
                .addText(text => text
                    .setPlaceholder('deepseek/deepseek-chat')
                    .setValue(this.plugin.settings.customModel || '')
                    .onChange(async (value) => {
                        this.plugin.settings.customModel = value.trim();
                        await this.plugin.saveSettings();
                    }));

            new Setting(containerEl)
                .setName(t.customRouterModel.name)
                .setDesc(t.customRouterModel.desc)
                .addText(text => text
                    .setPlaceholder('gpt-4o-mini')
                    .setValue(this.plugin.settings.customRouterModel || '')
                    .onChange(async (value) => {
                        this.plugin.settings.customRouterModel = value.trim();
                        await this.plugin.saveSettings();
                    }));

            new Setting(containerEl)
                .setName(t.customApiKey.name)
                .setDesc(t.customApiKey.desc)
                .addText(text => {
                    text.inputEl.type = 'password';
                    text.setPlaceholder('sk-...')
                        .setValue(this.plugin.settings.customApiKey || '')
                        .onChange(async (value) => {
                            this.plugin.settings.customApiKey = value.trim();
                            await this.plugin.saveSettings();
                        });
                });

            new Setting(containerEl)
                .setName(t.customApiFormat.name)
                .setDesc(t.customApiFormat.desc)
                .addDropdown(dropdown => dropdown
                    .addOption('openai', t.customApiFormat.openai)
                    .addOption('gemini', t.customApiFormat.gemini)
                    .setValue(this.plugin.settings.customApiFormat || 'openai')
                    .onChange(async (value: "openai" | "gemini") => {
                        this.plugin.settings.customApiFormat = value;
                        await this.plugin.saveSettings();
                    }));
        }

        new Setting(containerEl)
            .setName(t.customPromptPath.name)
            .setDesc(t.customPromptPath.desc)
            .addText(text => text
                .setPlaceholder('User_Pavilion/custom-prompt.md')
                .setValue(this.plugin.settings.customPromptPath)
                .onChange(async (value) => {
                    this.plugin.settings.customPromptPath = value.trim();
                    await this.plugin.saveSettings();
                    this.display(); // 動態顯隱進階選單
                }));

        if (this.plugin.settings.customPromptPath) {
            new Setting(containerEl)
                .setName(t.customPromptPosition.name)
                .setDesc(t.customPromptPosition.desc)
                .addDropdown(dropdown => dropdown
                    .addOption('suffix', t.customPromptPosition.suffix)
                    .addOption('prefix', t.customPromptPosition.prefix)
                    .addOption('advanced', t.customPromptPosition.advanced)
                    .setValue(this.plugin.settings.customPromptPosition || 'suffix')
                    .onChange(async (value: "prefix" | "suffix" | "advanced") => {
                        this.plugin.settings.customPromptPosition = value;
                        await this.plugin.saveSettings();
                        this.display();
                    }));

            if (this.plugin.settings.customPromptPosition !== 'advanced') {
                new Setting(containerEl)
                    .setName(t.injectContract.name)
                    .setDesc(t.injectContract.desc)
                    .addToggle(toggle => toggle
                        .setValue(this.plugin.settings.injectContract)
                        .onChange(async (value) => {
                            this.plugin.settings.injectContract = value;
                            await this.plugin.saveSettings();
                        }));

                new Setting(containerEl)
                    .setName(t.injectNodes.name)
                    .setDesc(t.injectNodes.desc)
                    .addToggle(toggle => toggle
                        .setValue(this.plugin.settings.injectNodes)
                        .onChange(async (value) => {
                            this.plugin.settings.injectNodes = value;
                            await this.plugin.saveSettings();
                        }));

                new Setting(containerEl)
                    .setName(t.injectRuntimeMode.name)
                    .setDesc(t.injectRuntimeMode.desc)
                    .addToggle(toggle => toggle
                        .setValue(this.plugin.settings.injectRuntimeMode)
                        .onChange(async (value) => {
                            this.plugin.settings.injectRuntimeMode = value;
                            await this.plugin.saveSettings();
                        }));
            }
        }
    }
}

