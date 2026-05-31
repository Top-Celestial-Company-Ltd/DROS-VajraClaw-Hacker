import yaml
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class InferenceContract:
    """
    DROS 7.0 Inference Contract AST
    負責將 YAML 契約轉譯為執行期對象
    """
    InferenceMode: str = "Bodhisattva"
    HardeningLevel: int = 5
    AuthorityNodesOnly: bool = True
    Fallback: str = "Bodhisattva"
    OutputFormat: str = "Markdown_DrosSpec"
    ComputeEngine: Dict[str, Any] = field(default_factory=dict)
    CustomRules: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load_from_file(cls, file_path: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return cls(**data)

    def compile_to_prompt_envelope(self) -> str:
        """將契約規則編譯成 AI 可理解的封裝指令"""
        envelope = f"[CONTRACT_EXECUTION_MODE: {self.InferenceMode}]\n"
        envelope += f"[HARDENING_LEVEL: {self.HardeningLevel}]\n"
        if self.AuthorityNodesOnly:
            envelope += "[CONSTRAINT: STRICT_AUTHORITY_ONLY]\n"
        return envelope
