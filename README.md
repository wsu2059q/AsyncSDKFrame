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

---
