"""
NapCat QQ 适配器 — 注册到 Hermes 插件系统。
实际适配器实现在 napcat_adapter.py 中。
"""

import logging

日志 = logging.getLogger(__name__)


def _检查依赖() -> bool:
    """检查运行时依赖是否可用。"""
    try:
        import websockets
        return True
    except ImportError:
        return False


def _验证配置(配置) -> bool:
    """检查 NapCat 是否正确配置。"""
    return 配置.enabled


def _是否已连接(配置) -> bool:
    """检查 NapCat 是否已连接/启用。"""
    return 配置.enabled


def register(ctx):
    """插件入口 — 由 Hermes 插件系统调用。"""
    from napcat_adapter import NapCat适配器, 检查依赖

    ctx.register_platform(
        name="napcat",
        label="NapCat (QQ)",
        adapter_factory=lambda 配置: NapCat适配器(配置),
        check_fn=检查依赖,
        validate_config=_验证配置,
        is_connected=_是否已连接,
        required_env=[],
        install_hint="pip install websockets",
        # 用户授权环境变量
        allowed_users_env="NAPCAT_ALLOWED_USERS",
        allow_all_env="NAPCAT_ALLOW_ALL_USERS",
        # QQ 没有严格的消息长度限制
        max_message_length=0,
        # 显示
        emoji="🐱",
        # QQ 用户 ID 需要脱敏
        pii_safe=False,
        allow_update_command=True,
        # LLM 提示
        platform_hint=(
            "你正在通过 NapCat (QQ) 对话。"
            "支持文字、图片、语音、文件收发。回复保持简洁自然。"
            "\n\n【CQ码规则】发送图片/文件/语音/视频时必须用CQ码，"
            "整条消息必须是完整的CQ码块，不能在CQ码前后加任何文字！"
            "格式：```CQ\n文本[CQ:image,file=/path/to/file]\n```"
            "混用文本和CQ码会导致发送失败。"
        ),
    )