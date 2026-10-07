"""
DROS 7.0 契約管理模組 - 終極防彈版
支援多種強度契約的載入、管理、智能展平與安全過濾驗證
"""

import yaml
import logging
from pathlib import Path
from dataclasses import dataclass, field, fields
from typing import Dict, Any, Optional

logger = logging.getLogger("DROS.Contract")


@dataclass
class InferenceContract:
    """DROS 推理契約核心類別"""
    
    # 基本設定 (對應 YAML 裡的 ContractMeta 與 SystemConstraints)
    Name: str = "Unnamed Contract"
    Version: str = "7.0.1"
    InferenceMode: str = "Bodhisattva"
    FallbackMode: str = "Bodhisattva"
    HardeningLevel: int = 5
    AuthorityNodesOnly: bool = False
    
    # 算力設定
    ComputeEngine: Dict[str, Any] = field(default_factory=dict)
    
    # 教理規則
    DoctrinalRules: Dict[str, Any] = field(default_factory=dict)
    
    # 禁令
    ForbiddenPhrases: list = field(default_factory=list)
    
    # 系統提示詞模板
    SystemPromptTemplate: str = ""
    
    # 內部狀態 (不從 YAML 讀取，由程式運行時賦值)
    contract_name: str = ""
    is_valid: bool = True

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """驗證契約內容的合法性"""
        valid_modes = {"Vajra", "Bodhisattva", "Interpretive", "Speculative"}
        if self.InferenceMode not in valid_modes:
            logger.warning(f"無效的推演模式 '{self.InferenceMode}'，已自動降級為 'Bodhisattva'")
            self.InferenceMode = "Bodhisattva"
            self.is_valid = False

    @classmethod
    def load(cls, name: str = "bodhisattva_default", contracts_dir: Optional[Path] = None) -> 'InferenceContract':
        """載入方式：支援智能展平與安全參數過濾，防禦 Dataclass 崩潰陷阱"""
        if contracts_dir is None:
            contracts_dir = Path("contracts")
        
        # 支援多種命名習慣
        possible_names = [
            f"{name}.yaml",
            f"{name.replace('_', '-')}.yaml",
            f"{name}.yml"
        ]
        
        for filename in possible_names:
            filepath = contracts_dir / filename
            if filepath.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or {}
                    
                    # 1. 智能展平 (Flatten)：將 YAML 的巢狀結構提取到頂層
                    if "ContractMeta" in data:
                        data.update(data.pop("ContractMeta"))
                    if "SystemConstraints" in data:
                        data.update(data.pop("SystemConstraints"))
                        
                    # 2. 安全過濾 (Filter)：只保留 Dataclass 中有定義的欄位
                    valid_keys = {f.name for f in fields(cls)}
                    filtered_data = {k: v for k, v in data.items() if k in valid_keys}
                    
                    # 3. 實例化
                    contract = cls(**filtered_data)
                    contract.contract_name = name
                    logger.info(f"✅ 契約載入成功 → {contract.Name} ({contract.InferenceMode} 模式 | 硬化等級: {contract.HardeningLevel})")
                    return contract
                    
                except Exception as e:
                    logger.error(f"❌ 契約載入失敗 {filename}: {e}")
        
        # Fallback：若找不到指定檔案，則生成安全的預設菩薩契約
        logger.warning(f"⚠️ 未找到契約檔案 '{name}'，已啟用系統預設 Bodhisattva 模式")
        return cls(Name="Fallback Bodhisattva", InferenceMode="Bodhisattva", HardeningLevel=4)


    def to_prompt_envelope(self) -> str:
        """編譯成 Prompt 可用的契約描述，直接注入給大模型"""
        mode_mapping = {
            "Vajra": "【金剛模式 · 嚴格宗派推演】",
            "Interpretive": "【詮釋模式 · 義理跨界映射】",
            "Speculative": "【般若模式 · 高階湧現推演】",
            "Bodhisattva": "【菩薩模式 · 適應性導航】"
        }
        mode_text = mode_mapping.get(self.InferenceMode, "【菩薩模式 · 適應性導航】")
        return f"""
[DROS CONTRACT ENVELOPE]
Contract Name: {self.Name}
Mode: {mode_text}
Hardening Level: {self.HardeningLevel}/10
Require Authority Coordinates (T-Number): {self.AuthorityNodesOnly}
"""
