import re

class GuardVM:
    """
    DROS 7.0 Guard Virtual Machine
    負責攔截 AI 輸出，校驗 T-Number 與義理邊界
    """
    def __init__(self, contract):
        self.contract = contract
        self.hallucination_triggers = [r"我認為", r"我覺得", r"大概是"] # 非金剛語氣誘發詞

    def intercept_and_verify(self, content: str) -> bool:
        """
        查驗輸出內容是否符合契約
        """
        # 1. 檢查是否包含 T-Number 或 X-Number (權威引用)
        if self.contract.AuthorityNodesOnly:
            citation_pattern = r"[T|X]\d{4,}"
            if not re.search(citation_pattern, content):
                return False # 缺乏權威引用，攔截
        
        # 2. 檢查是否有主觀幻覺語氣
        for trigger in self.hallucination_triggers:
            if re.search(trigger, content):
                return False # 檢出主觀幻覺，攔截
                
        return True

    def apply_fallback(self, content: str) -> str:
        """當金剛模式失敗時，切換至菩薩模式的柔性引導"""
        return f"【菩薩模式提醒】：由於相關權威數據稀疏，系統已切換為適應性模式。以下為參考見地：\n{content}"
