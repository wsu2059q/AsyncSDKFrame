# AsyncSDKFrame

本项目基于 [RyhBotPythonSDK V2](https://github.com/runoneall/RyhBotPythonSDK2) 构建，并由 [sdkFrame](https://github.com/runoneall/sdkFrame) 提供支持。这是一个异步版本的 SDK，可能在功能和特性上与原库存在一定差异。

---

## 项目概述

AsyncSDKFrame 是一个模块化、可扩展的异步 Python SDK 框架，主要用于构建高效、可维护的机器人应用程序。

## 项目结构

```
AsyncSDKFrame/
├── __init__.py        # 项目初始化
├── __main__.py        # CLI 接口
├── envManager.py      # 环境配置管理
├── errors.py          # 自定义异常
├── logger.py          # 日志记录
├── origin.py          # 模块源管理
├── sdk.py             # SDK 核心
├── util.py            # 工具函数
└── modules/           # 功能模块目录
    └── ...
```

## 主要模块说明

- **envManager**: 负责管理环境配置和模块信息，使用 SQLite 数据库存储配置
- **logger**: 提供日志功能，支持不同日志级别
- **origin**: 管理模块源，添加、删除、更新模块源等方法在此处
- **util**: 提供工具函数，拓扑排序、异步执行
- **modules**: 功能模块目录

## 开发指南

项目的模块化设计允许开发者通过实现符合规范的模块快速扩展功能。模块的结构和接口规范可以参考 [异步模块开发指南](https://github.com/wsu2059q/AsyncRyhBotPythonSDK2/blob/main/%E5%BC%82%E6%AD%A5%E6%A8%A1%E5%9D%97%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97.md)。

## 使用说明

1. 安装依赖：`pip install -r requirements.txt`
2. 查看可用CLI命令：`python -m AsyncSDKFrame`

### CLI命令介绍

`AsyncSDKFrame` 提供了丰富的 CLI 命令，用于管理模块、源和环境配置。以下是主要的 CLI 命令及其功能：

1. **启用模块**
   ```bash
   python -m AsyncSDKFrame enable <module_name>
   ```
   启用指定模块。

2. **禁用模块**
   ```bash
   python -m AsyncSDKFrame disable <module_name>
   ```
   禁用指定模块。

3. **列出模块**
   ```bash
   python -m AsyncSDKFrame list [--module <module_name>]
   ```
   列出所有模块信息，或指定模块的详细信息。

4. **更新模块列表**
   ```bash
   python -m AsyncSDKFrame update
   ```
   更新模块列表，从已配置的源中获取最新的模块信息。

5. **升级模块**
   ```bash
   python -m AsyncSDKFrame upgrade [--force]
   ```
   升级所有模块到最新版本，可选 `--force` 参数跳过二次确认。

6. **卸载模块**
   ```bash
   python -m AsyncSDKFrame uninstall <module_name>
   ```
   删除指定模块。

7. **安装模块**
   ```bash
   python -m AsyncSDKFrame install <module_name> [--force] [--init]
   ```
   安装指定模块，支持多个模块（用逗号分隔）。可选 `--force` 参数强制重新安装，`--init` 参数在安装前初始化模块数据库。

8. **管理模块源**
   - **添加模块源**
     ```bash
     python -m AsyncSDKFrame origin add <url>
     ```
     添加新的模块源。
     
   - **列出模块源**
     ```bash
     python -m AsyncSDKFrame origin list
     ```
     列出所有已配置的模块源。
     
   - **删除模块源**
     ```bash
     python -m AsyncSDKFrame origin del <url>
     ```
     删除指定的模块源。

---

### 异步模块源与同步模块源

1. **异步模块源**
   - URL: [https://sdkframe.anran.xyz/map.json](https://sdkframe.anran.xyz/map.json)
   - 特性：
     - 支持异步加载模块。
     - 适用于需要高性能和非阻塞操作的场景。
     - 推荐用于现代异步框架和应用。

2. **同步模块源**
   - URL: [https://runoneall.serv00.net/ryhsdk2/map.json](https://runoneall.serv00.net/ryhsdk2/map.json)
   - 特性：
     - 传统同步加载模块。
     - 适用于兼容性要求较高的场景。
     - 可能会在某些高并发场景下表现不如异步源。

通过 `origin` 命令可以轻松管理这些模块源，例如添加、列出或删除源。例如：
```bash
# 添加异步模块源
python -m AsyncSDKFrame origin add https://sdkframe.anran.xyz/map.json

# 添加同步模块源
python -m AsyncSDKFrame origin add https://runoneall.serv00.net/ryhsdk2/map.json

# 查看当前配置的模块源
python -m AsyncSDKFrame origin list
```

无论是异步还是同步模块源，都可以通过 `update` 命令更新模块列表，确保使用的是最新的模块信息。
---
