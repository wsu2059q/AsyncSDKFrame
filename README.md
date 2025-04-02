# 🚀 ErisPulse - 异步机器人开发框架

基于 [RyhBotPythonSDK V2](https://github.com/runoneall/RyhBotPythonSDK2) 构建，由 [sdkFrame](https://github.com/runoneall/sdkFrame) 提供支持的异步机器人开发框架。

## ✨ 核心特性
- 完全异步架构设计
- 模块化插件系统
- 多协议支持
- 模块热更新
- 跨平台兼容

---

## 📦 安装

```bash
pip install ErisPulse --upgrade
```

**系统要求**：
- Python ≥ 3.7
- pip ≥ 20.0

---

## 🛠️ 开发工具

### CLI 命令大全

#### 模块管理
| 命令 | 参数 | 描述 | 示例 |
|------|------|------|------|
| `enable` | `<module>` | 激活模块 | `enable chatgpt` |
| `disable` | `<module>` | 停用模块 | `disable weather` |
| `list` | `[--module]` | 模块清单 | `list --module=payment` |
| `update` | - | 更新索引 | `update` |
| `upgrade` | `[--force]` | 升级模块 | `upgrade --force` |
| `install` | `<module...>` | 安装模块 | `install translator analyzer` |
| `uninstall` | `<module>` | 移除模块 | `uninstall old-module` |

#### 源管理
| 命令 | 参数 | 描述 | 示例 |
|------|------|------|------|
| `origin add` | `<url>` | 添加源 | `origin add https://example.com/source.json` |
| `origin list` | - | 源列表 | `origin list` |
| `origin del` | `<url>` | 删除源 | `origin del old-source` |

---

## 🌐 模块源

### 官方源仓库

#### 全功能源
| 源名称 | 类型 | 协议 | 地址 |
|--------|------|------|------|
| *AsyncRBPS | 异步 | HTTPS | `https://github.com/wsu2059q/AsyncRBPS-Origin/raw/main/map.json` |
| SDKFrame CDN | 异步 | HTTPS | `https://sdkframe.anran.xyz/map.json` |
| *r1a 同步 | 同步 | HTTPS | `https://runoneall.serv00.net/ryhsdk2/map.json` |

#### 协议专用源
| 源名称 | 类型 | 协议 | 地址 |
|--------|------|------|------|
| OneBot 协议源 | 异步 | HTTPS | `https://sdkframe.anran.xyz/onebot.json` |
| 云湖平台源 | 异步 | HTTPS | `https://sdkframe.anran.xyz/yunhu.json` |

### 自定义源

**示例配置**：
```json
{
  "name": "Custom-Origin",
  "base": "https://example.com/modules",
  "modules": {
    "CustomModule": {
      "path": "/CustomModule.zip",
      "version": "1.0.0",
      "description": "自定义模块示例",
      "author": "YourName",
      "dependencies": [],
      "optional_dependencies": []
    }
  }
}
```

---

## ⚠️ 注意事项
1. 生产环境建议使用官方认证源
2. 模块升级前请备份配置
3. 异步/同步模块不可混用
