"""
DROS 7.0 配置管理模組
集中管理所有設定，支援環境變數覆蓋
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass, field
from dotenv import load_dotenv

# 解決 PyInstaller 環境下的路徑問題
def get_base_dir() -> Path:
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).resolve().parent.parent

# 嘗試載入 .env
load_dotenv(get_base_dir() / '.env')

# 解決 Windows 繁體中文環境 cp950 / UTF-8 終端機顯示 Emoji 的編碼崩潰問題
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

@dataclass
class DrosConfig:
    """DROS 全域配置類別"""
    version: str = "7.0"
    
    # 路徑
    core_path: Path = Path("core")
    vault_path: Path = Path("Vault_DajueZang")
    contracts_path: Path = Path("contracts")
    docs_path: Path = Path("docs")
    
    # 模型
    model_router: str = "gemini-2.5-flash-lite"
    model_synthesizer: str = "gemini-3.1-pro"
    model_fallback: str = "gemini-2.5-flash-lite"
    
    # 系統行為
    default_mode: str = "Bodhisattva"
    hardening_level: int = 5
    authority_nodes_only: bool = False
    max_context_length: int = 12000
    
    # GuardVM
    forbidden_phrases: List[str] = field(default_factory=list)

    @classmethod
    def load(cls, config_path: str | Path = "config.yaml") -> 'DrosConfig':
        """載入配置（支援 env 變數覆蓋）"""
        path = Path(config_path)
        
        if not path.exists():
            raise FileNotFoundError(f"找不到配置文件: {path}")
        
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        # 環境變數覆蓋機制
        def env(key, default):
            return os.getenv(f"DROS_{key.upper()}", default)

        return cls(
            core_path=Path(env("core_path", data["paths"]["core"])),
            vault_path=Path(env("vault_path", data["paths"]["vault"])),
            contracts_path=Path(env("contracts_path", data["paths"]["contracts"])),
            docs_path=Path(env("docs_path", data["paths"]["docs"])),
            
            model_router=env("model_router", data["models"]["default_router"]),
            model_synthesizer=env("model_synthesizer", data["models"]["default_synthesizer"]),
            model_fallback=env("model_fallback", data["models"]["fallback"]),
            
            default_mode=env("default_mode", data["system"]["default_mode"]),
            hardening_level=int(env("hardening_level", data["system"]["hardening_level"])),
            authority_nodes_only=env("authority_nodes_only", str(data["system"]["authority_nodes_only"])).lower() == "true",
            max_context_length=int(env("max_context_length", data["system"]["max_context_length"])),
            
            forbidden_phrases=data["guard_vm"]["strict_forbidden_phrases"]
        )


def _find_config_yaml() -> Path:
    """自動探測 config.yaml 的路徑，支援向上追溯尋找"""
    # 支援 PyInstaller 編譯模式
    if getattr(sys, 'frozen', False):
        exe_dir = Path(sys.executable).parent
        if (exe_dir / "config.yaml").exists():
            return exe_dir / "config.yaml"
            
    current = Path(__file__).resolve().parent
    for _ in range(5):
        probe = current / "config.yaml"
        if probe.exists():
            return probe
        probe_parent = current.parent / "config.yaml"
        if probe_parent.exists():
            return probe_parent
        current = current.parent
    return Path("config.yaml")  # 回退到當前目錄


# 全域實例 (導入時自動加載，防止任何模組導入後為 None 導致崩潰)
config_yaml_path = _find_config_yaml()
try:
    config = DrosConfig.load(config_yaml_path)
except Exception:
    # 回退空物件，防止無設定檔時直接導入崩潰
    config = DrosConfig(
        core_path=Path("core"),
        vault_path=Path("Vault_DajueZang"),
        contracts_path=Path("contracts"),
        docs_path=Path("docs"),
        model_router="gemini-2.5-flash-lite",
        model_synthesizer="gemini-3.1-pro",
        model_fallback="gemini-2.5-flash-lite",
        default_mode="Bodhisattva",
        hardening_level=5,
        authority_nodes_only=False,
        max_context_length=12000,
        forbidden_phrases=["我認為", "我覺得", "大概是", "可能", "應該是", "我猜", "個人認為", "在我看來"]
    )


def init_config(config_path: str = "config.yaml"):
    global config
    loaded = DrosConfig.load(config_path)
    
    # 【金剛防綁定陷阱】：直接就地修改 config 的欄位值！
    # 這能確保其他早已 "from src.config import config" 的模組也能動態看見更新，免除引用不對齊的魔咒！
    for field_info in loaded.__dataclass_fields__:
        setattr(config, field_info, getattr(loaded, field_info))
        
    print(f"[OK] DROS 配置載入完成 (v{config.version})")
    return config
