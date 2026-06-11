# NapCat QQ 适配器

基于 OneBot v11 协议的 QQ 平台适配器，为 Hermes Agent 添加 QQ 支持。

支持 NapCat / go-cqhttp / Lagrange.OneBot / LLOneBot 等兼容实现。

## 架构

```
QQ 客户端 ←→ NapCat (OneBot 实现)
                  ↓ 反向 WebSocket (NapCat 主动连过来)
             NapCat 适配器 (hermes-qq-onebot)
                  ↓ 可选 HTTP API (图片发送、文件获取)
             OneBot API
```

- **反向 WebSocket**：适配器起 server，NapCat 主动连接
- **HTTP API**：可选但推荐，解决图片发送超时、文件获取等问题

## 安装

```bash
hermes plugins install landamao/hermes-qq-onebot --enable
```

## 消息标签格式

每种媒体都带详细信息，Agent 可直接获取路径或 URL：

| 类型 | 标签格式 |
|------|----------|
| 图片 | `[图片:file=/tmp/xxx.jpg]` 或 `[图片:url=https://...]` |
| 语音 | `[语音:file=/tmp/xxx.ogg]` 或 `[语音:url=https://...]` |
| 视频 | `[视频:url=https://...]` 或 `[视频:file=/tmp/xxx.mp4]` |
| 文件 | `[文件:name=report.pdf,file=/tmp/xxx]` 或 `[文件:name=report.pdf,url=https://...]` |
| 表情 | `[表情:id=123]` |
| @提及 | `@昵称(QQ:123456)` |

## CQ 码支持

Agent 可通过 CQ 码直接发送复杂消息（绕过网关的文件路径自动检测）：

```CQ
[CQ:at,qq=123456] 看看这个 [CQ:image,file=/tmp/test.jpg]
```

```CQ
这是你要的文件 [CQ:file,file=/tmp/document.pdf,name=文档.pdf]
```

**格式要求：**
- 必须用 ` ```CQ ` 和 ` ``` ` 包裹
- 整条消息必须是一个完整的 CQ 码块
- 所有内容（包括文字）都放在 CQ 码块内，不要拆分

**支持的 CQ 码类型：**
- `[CQ:at,qq=123]` — @某人
- `[CQ:image,file=路径或URL]` — 发送图片
- `[CQ:record,file=路径或URL]` — 发送语音
- `[CQ:video,file=路径或URL]` — 发送视频
- `[CQ:file,file=路径或URL,name=文件名]` — 发送文件
- `[CQ:face,id=123]` — 发送表情
- 更多 CQ 码参考 OneBot v11 文档

## 下载限制

超过配置体积的媒体不自动下载，只保留 URL，Agent 需要时再下载：

```yaml
extra:
  download_limits:
    image: 10MB       # 支持 B/KB/MB/GB，不区分大小写
    record: 50MB
    video: 100MB
    file: 50MB
```

## 消息链路追踪

每条消息分配 8 位追踪ID，贯穿全流程：

```
[纳猫][a1b2c3d4] ▶ 收到群聊: 用户=小明(123456) 群=789 消息ID=100
[纳猫][a1b2c3d4] 去重检查通过
[纳猫][a1b2c3d4] ✓ 群聊触发: 被@=True 关键词=False
[纳猫][a1b2c3d4] 文本: @机器人 你好
[纳猫][a1b2c3d4] 媒体: photo.jpg (image/jpeg)
[纳猫][a1b2c3d4] ✓ 消息就绪: 分类=photo 文本=6字 媒体=1个 → 分发到网关

[纳猫][e5f6g7h8] ▶ 发送: 会话=napcat_group_789 长度=42
[纳猫][e5f6g7h8] → group:789
[纳猫][e5f6g7h8] ✓ 发送成功
```

日志中搜索 `[纳猫][追踪ID]` 即可追踪完整生命周期。

## 功能

- 私聊 / 群聊消息收发
- @提及检测 + 关键词触发
- 图片、语音、文件收发
- 回复消息解析
- 长消息自动拆分 + 合并转发 (群聊)
- 用户白名单
- emoji 表情回应 / 戳一戳 (默认关闭)

## 配置

`~/.hermes/config.yaml`：

```yaml
platforms:
  napcat:
    enabled: true
    extra:
      # ── 反向 WS 配置 ──
      reverse_host: "0.0.0.0"          # 监听地址（默认 0.0.0.0）
      reverse_port: 6700                # 监听端口（默认 6700）
      access_token: ""                  # 访问令牌（可选，用于认证 NapCat 连接）

      # ── HTTP API（推荐开启）──
      http_api_url: "http://127.0.0.1:5700"  # OneBot HTTP API 地址

      # ── 机器人信息 ──
      bot_self_id: ""                   # 机器人 QQ 号（可选，会从消息中自动学习）

      # ── 显示选项 ──
      show_qq_id: false                 # 是否在用户名后显示 QQ 号（默认 false）

      # ── 媒体下载限制 ──
      # 有 file_size 时超限不下载，只保留 URL
      # 支持 B/KB/MB/GB（不区分大小写）
      download_limits:
        image: 10MB                     # 图片限制（默认 10MB）
        record: 10MB                    # 语音限制（默认 10MB）
        video: 10MB                     # 视频限制（默认 10MB）
        file: 10MB                      # 文件限制（默认 10MB）

      # ── 长消息处理 ──
      merge_forward_threshold: 800      # 群聊超过此字数触发合并转发（默认 800，私聊不触发）
      forward_name: "纳西妲"      # 合并转发显示的名字（默认 纳西妲）

      # ── 关键词触发 ──
      # 群聊中匹配这些正则时自动响应（不区分大小写）
      mention_patterns:
        - "纳猫"
        - "帮我"

      # ── 用户白名单 ──
      # 为空或不设置则允许所有用户
      allowed_qq_ids: "123456,789012"   # 逗号分隔的 QQ 号列表
```

## 环境变量 (可选)

所有配置项都可以通过环境变量覆盖（环境变量优先级低于 config.yaml）：

```bash
# 访问令牌
NAPCAT_ACCESS_TOKEN=your_token

# HTTP API 地址
NAPCAT_HTTP_API_URL=http://127.0.0.1:5700

# 机器人 QQ 号
NAPCAT_BOT_SELF_ID=123456789

# 用户白名单（逗号分隔）
NAPCAT_ALLOWED_USERS=123456,789012

# 允许所有用户（设置为 true 时忽略白名单）
NAPCAT_ALLOW_ALL_USERS=false

# 关键词触发（逗号分隔的正则）
NAPCAT_MENTION_PATTERNS=纳猫,帮我
```

## NapCat 端配置

在 NapCat 的配置文件中设置反向 WS 连接：

```json
{
  "ws_reverse": {
    "enable": true,
    "url": "ws://127.0.0.1:6700",
    "reconnect_interval": 3000,
    "token": ""
  }
}
```

如果配置了 `access_token`，NapCat 端也需要设置相同的 token。

## 卸载

```bash
rm -rf ~/.hermes/plugins/napcat
hermes gateway restart
```
