# Split Rules

[![Convert Meta Rules to Surge Format](https://github.com/sddpljx/split-rules/actions/workflows/convert-rules.yml/badge.svg)](https://github.com/sddpljx/split-rules/actions/workflows/convert-rules.yml)

这是一个自动转换 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat) 域名和 IP 分流规则为 Surge 格式的仓库。

## 功能特性

- 🔄 自动同步上游规则（每天北京时间 8:00）
- 🎯 支持域名匹配格式：
  - `DOMAIN` - 完整域名匹配
  - `DOMAIN-SUFFIX` - 域名后缀匹配
- 🌐 支持 IP 地址匹配格式：
  - `IP-CIDR` - IPv4 地址段匹配
  - `IP-CIDR6` - IPv6 地址段匹配
- 🔗 智能合并：自动将同名 IP 规则追加到域名规则文件中
- 📁 独立 IP 规则：无同名域名的 IP 规则单独保存在 `rules/geo/geoip/` 目录
- 📦 提供 GitHub Raw 和 jsDelivr CDN 两种访问方式
- ⚡ 自动清除 CDN 缓存：更新后立即 purge jsDelivr 缓存，确保用户获取最新规则
- 🚀 GitHub Actions 自动化构建

## 转换规则

源格式 → Surge 格式：

| 源格式 | Surge 格式 | 说明 |
|--------|-----------|------|
| `apple.com` | `DOMAIN,apple.com` | 完整域名匹配 |
| `+.apple.com` | `DOMAIN-SUFFIX,apple.com` | 域名后缀匹配 |
| `1.1.1.0/24` | `IP-CIDR,1.1.1.0/24,no-resolve` | IPv4 地址段匹配 |
| `2001:db8::/32` | `IP-CIDR6,2001:db8::/32,no-resolve` | IPv6 地址段匹配 |

> **注意**：所有 IP 规则均添加 `no-resolve` 参数，避免 DNS 泄露并提升匹配性能。

## 目录结构

```
rules/
├── geo/
│   ├── geosite/          # 域名规则（包含同名的 IP 规则）
│   │   ├── apple.list    # Apple 域名 + IP 规则
│   │   ├── google.list   # Google 域名 + IP 规则
│   │   └── ...
│   └── geoip/            # 独立的 IP 规则（无同名域名规则）
│       ├── cn.list       # 中国大陆 IP 段
│       ├── telegram.list # Telegram IP 段
│       └── ...
```

### 规则处理逻辑

1. **域名规则**：从 `meta-rules-dat/geo/geosite/` 转换，保存到 `rules/geo/geosite/`
2. **IP 规则**：从 `meta-rules-dat/geo-lite/geoip/` 转换
   - 如果存在同名域名规则文件（如 `apple.list`），IP 规则会追加到该文件末尾
   - 如果不存在同名域名规则文件，IP 规则单独保存到 `rules/geo/geoip/` 目录

## 常用规则文件

所有规则文件位于 `rules/geo/geosite/` 目录下，以下是一些常用的规则文件链接：

### Apple 相关

| 规则名称 | 说明 | GitHub Raw | jsDelivr CDN |
|---------|------|-----------|--------------|
| apple.list | Apple 主要服务 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/apple.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/apple.list) |
| apple-cn.list | Apple 中国服务 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/apple-cn.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/apple-cn.list) |
| apple-dev.list | Apple 开发者服务 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/apple-dev.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/apple-dev.list) |
| apple-tvplus.list | Apple TV+ | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/apple-tvplus.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/apple-tvplus.list) |
| apple-intelligence.list | Apple Intelligence | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/apple-intelligence.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/apple-intelligence.list) |
| apple-update.list | Apple 系统更新 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/apple-update.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/apple-update.list) |

### Google 相关

| 规则名称 | 说明 | GitHub Raw | jsDelivr CDN |
|---------|------|-----------|--------------|
| google.list | Google 主要服务 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/google.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/google.list) |
| google-cn.list | Google 中国服务 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/google-cn.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/google-cn.list) |
| google-gemini.list | Google Gemini AI | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/google-gemini.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/google-gemini.list) |
| google-deepmind.list | Google DeepMind | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/google-deepmind.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/google-deepmind.list) |
| google-scholar.list | Google 学术 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/google-scholar.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/google-scholar.list) |
| google-play.list | Google Play | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/google-play.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/google-play.list) |
| googlefcm.list | Google FCM 推送 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/googlefcm.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/googlefcm.list) |

### Microsoft 相关

| 规则名称 | 说明 | GitHub Raw | jsDelivr CDN |
|---------|------|-----------|--------------|
| microsoft.list | Microsoft 主要服务 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/microsoft.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/microsoft.list) |
| microsoft-dev.list | Microsoft 开发者服务 | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/microsoft-dev.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/microsoft-dev.list) |

### AI 公司服务

| 规则名称 | 说明 | GitHub Raw | jsDelivr CDN |
|---------|------|-----------|--------------|
| openai.list | OpenAI (ChatGPT) | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/openai.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/openai.list) |
| anthropic.list | Anthropic (Claude) | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/anthropic.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/anthropic.list) |
| xai.list | xAI (Grok) | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/xai.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/xai.list) |
| category-ai-!cn.list | AI 服务（非中国） | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/category-ai-!cn.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/category-ai-!cn.list) |
| category-ai-chat-!cn.list | AI 聊天服务（非中国） | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/category-ai-chat-!cn.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/category-ai-chat-!cn.list) |
| jetbrains-ai.list | JetBrains AI | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/jetbrains-ai.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/jetbrains-ai.list) |

### 其他常用服务

| 规则名称 | 说明 | GitHub Raw | jsDelivr CDN |
|---------|------|-----------|--------------|
| github.list | GitHub | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/github.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/github.list) |
| netflix.list | Netflix | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/netflix.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/netflix.list) |
| youtube.list | YouTube | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/youtube.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/youtube.list) |
| telegram.list | Telegram | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/telegram.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/telegram.list) |
| twitter.list | Twitter / X | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/twitter.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/twitter.list) |
| tiktok.list | TikTok | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/tiktok.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/tiktok.list) |
| spotify.list | Spotify | [链接](https://raw.githubusercontent.com/sddpljx/split-rules/refs/heads/main/rules/geo/geosite/spotify.list) | [链接](https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/spotify.list) |

## 在 Surge 中使用

在 Surge 配置文件中添加规则集：

```ini
[Rule]
# 使用 GitHub Raw（可能在中国大陆访问较慢）
RULE-SET,https://raw.githubusercontent.com/sddpljx/split-rules/main/rules/geo/geosite/openai.list,PROXY

# 使用 jsDelivr CDN（推荐，访问更快）
RULE-SET,https://cdn.jsdelivr.net/gh/sddpljx/split-rules@main/rules/geo/geosite/google.list,PROXY
```

## 浏览所有规则

- **域名规则（含同名 IP 规则）**：查看 [rules/geo/geosite](./rules/geo/geosite) 目录
- **独立 IP 规则**：查看 [rules/geo/geoip](./rules/geo/geoip) 目录

## 更新频率

- 自动更新：每天北京时间 8:00（UTC 0:00）
- 手动触发：在 Actions 页面手动运行 workflow
- 代码更新：当转换脚本或 workflow 配置被修改时自动运行
- CDN 缓存：每次更新后自动清除 jsDelivr CDN 缓存，用户可立即获取最新规则

## 技术栈

- **数据源**: [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)
- **自动化**: GitHub Actions
- **语言**: Python 3.11
- **CDN**: jsDelivr

## 许可证

本项目采用与上游项目相同的许可证。规则数据来源于 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)。

## 致谢

感谢 [MetaCubeX](https://github.com/MetaCubeX) 团队维护的高质量域名分流规则。
