import re
from typing import Dict, Any
from .contract import InferenceContract

class GuardVM:
    """
    DROS 7.0 護法虛擬機 - 定稿版
    負責即時校驗輸出是否符合契約與金剛標準 (具備高寬容度的 T-Number 識別力)
    """
    
    def __init__(self, contract: InferenceContract):
        self.contract = contract
        
        self.forbidden_patterns = [
            r"我認為", r"我覺得", r"大概是", r"可能", r"應該是", 
            r"我猜", r"個人認為", r"在我看來"
        ]
        
        self.required_patterns = [
            # 升級版 Regex：兼容 T31n1585, T31, no. 1585, p. 1a 等多元大正藏格式
            r"T\d{2,4}[a-zA-Z0-9,\.\s]*", 
            r"\[\!QUOTE\]",               # 必須有引用區塊
        ]

    def verify(self, content: str) -> Dict[str, Any]:
        """執行完整驗證"""
        issues = []

        # 1. 權威引用檢查 (僅在金剛模式或嚴格約束下觸發)
        if getattr(self.contract, 'AuthorityNodesOnly', False):
            has_t_number = False
            for pattern in self.required_patterns:
                if "T\\d" in pattern and re.search(pattern, content):
                    has_t_number = True
                    break
            if not has_t_number:
                issues.append("缺少權威 T-Number 引用座標 (或格式不符大正藏標準)")

        # 2. 幻覺語氣檢查
        for pattern in self.forbidden_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"偵測到主觀幻覺語氣: {pattern}")

        # 3. 長度與基本完整性檢查
        if len(content.strip()) < 30:
            issues.append("輸出內容過於簡短，無法形成嚴謹法義推演")

        passed = len(issues) == 0

        return {
            "passed": passed,
            "issues": issues,
            "severity": "high" if issues else "none",
            "score": max(0, 100 - len(issues) * 20)
        }

    def apply_fallback(self, content: str) -> str:
        """柔性降級：當 GuardVM 攔截時，強制轉換模式並加上系統聲明"""
        return f"""【菩薩模式 · 適應性導航】
由於當前檢索到的權威資料不足，或輸出內容未達合規標準，系統已自動切換至較寬鬆模式。

{content}

【DROS 系統建議】：若需更精確的金剛模式回答，請提供更明確的法義問題，或確認本地庫中已包含相應的 T-Number 實心節點。"""
