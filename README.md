# ErisPulse

本项目基于 [RyhBotPythonSDK V2](https://github.com/runoneall/RyhBotPythonSDK2) 构建，并由 [sdkFrame](https://github.com/runoneall/sdkFrame) 提供支持。这是一个异步版本的 SDK，可能在功能和特性上与原库存在一定差异。

ErisPulse 是一个模块化、可扩展的异步 Python SDK 框架，主要用于构建高效、可维护的机器人应用程序。

## 通过以下命令安装 `ErisPulse`：

```bash
pip install ErisPulse

## 开发指南

项目的模块化设计允许开发者通过实现符合规范的模块快速扩展功能。模块的结构和接口规范可以参考 [异步模块开发指南](https://github.com/wsu2059q/AsyncRyhBotPythonSDK2/blob/main/%E5%BC%82%E6%AD%A5%E6%A8%A1%E5%9D%97%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97.md)。

## 项目结构

```
ErisPulse/
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

### CLI命令介绍

`ErisPulse` 提供了丰富的 CLI 命令，用于管理模块、源和环境配置。以下是主要命令：

| 命令                          | 功能描述                           |
|-------------------------------|------------------------------------|
| `enable <module_name>`        | 启用指定模块                      |
| `disable <module_name>`       | 禁用指定模块                      |
| `list [--module <module_name>]` | 列出所有模块或指定模块的详细信息  |
| `update`                      | 更新模块列表                      |
| `upgrade [--force]`           | 升级所有模块到最新版本            |
| `uninstall <module_name>`     | 删除指定模块                      |
| `install <module_name>`       | 安装指定模块，支持多个模块         |

#### 模块源管理命令

| 命令                          | 功能描述                           |
|-------------------------------|------------------------------------|
| `origin add <url>`            | 添加新的模块源                    |
| `origin list`                 | 列出所有已配置的模块源            |
| `origin del <url>`            | 删除指定的模块源                  |


---

### 模块源

在使用 `ErisPulse` 时，模块源是管理模块的重要组成部分。根据不同的使用场景，模块源分为两种类型：**异步模块源** 和 **同步模块源**。以下是它们的详细说明：

#### 异步模块源
- URL 1: [https://github.com/wsu2059q/AsyncRBPS-Origin/raw/refs/heads/main/map.json](https://github.com/wsu2059q/AsyncRBPS-Origin/raw/refs/heads/main/map.json)
- URL 2: [https://sdkframe.anran.xyz/map.json](https://sdkframe.anran.xyz/map.json)
- 特性：
  - 支持异步加载模块。
  - 适用于需要高性能和非阻塞操作的场景。
  - 推荐用于现代异步框架和应用。

#### 同步模块源
- URL: [https://runoneall.serv00.net/ryhsdk2/map.json](https://runoneall.serv00.net/ryhsdk2/map.json)
- 特性：
  - 传统同步加载模块。
  - 适用于兼容性要求较高的场景。
  - 可能会在某些高并发场景下表现不如异步源。

#### 自定义模块源
用户可以搭建自己的模块源，以下是一个示例格式：
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

#### 提供以下命令方便您快速添加源
```bash
# 添加异步模块源
python -m ErisPulse origin add https://github.com/wsu2059q/AsyncRBPS-Origin/raw/refs/heads/main/map.json
# 添加同步模块源
python -m ErisPulse origin add https://runoneall.serv00.net/ryhsdk2/map.json

# 添加自定义模块源
# python -m ErisPulse origin add https://example.com/modules/map.json

# 查看当前配置的模块源
python -m ErisPulse origin list

# 更新模块列表
python -m ErisPulse update
```
