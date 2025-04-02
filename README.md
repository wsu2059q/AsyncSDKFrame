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
**全局参数说明**：  
`--init`：执行命令前先初始化模块状态 
''
| 命令       | 参数                      | 描述                                  | 示例                          |
|------------|---------------------------|---------------------------------------|-------------------------------|
| `enable`   | `<module> [--init]`       | 激活指定模块                          | `python -m ErisPulse enable chatgpt --init`       |
| `disable`  | `<module> [--init]`       | 停用指定模块                          | `python -m ErisPulse disable weather`             |
| `list`     | `[--module=<name>] [--init]` | 列出模块（可筛选）                   | `python -m ErisPulse list --module=payment`       |
| `update`   | -                         | 更新模块索引                           | `python -m ErisPulse update`                      |
| `upgrade`  | `[--force] [--init]`      | 升级模块（`--force` 强制覆盖）        | `python -m ErisPulse upgrade --force --init`      |
| `install`  | `<module...> [--init]`    | 安装一个或多个模块（逗号分隔）        | `python -m ErisPulse install translator,analyzer` |
| `uninstall`| `<module> [--init]`       | 移除指定模块                          | `python -m ErisPulse uninstall old-module --init` |

#### 源管理
| 命令 | 参数 | 描述 | 示例 |
|------|------|------|------|
| `origin add` | `<url>` | 添加源 | `python -m ErisPulse origin add https://example.com/source.json` |
| `origin list` | - | 源列表 | `python -m ErisPulse origin list` |
| `origin del` | `<url>` | 删除源 | `python -m ErisPulse origin del https://example.com/source.json` |

---

## 🌐 模块源配置指南

### 官方源仓库

#### 全功能源
| 源名称 | 类型 | 协议 | 地址 |
|--------|------|------|------|
| AsyncRBPS | 异步 | HTTPS | `https://github.com/wsu2059q/AsyncRBPS-Origin/raw/main/`
| SDKFrame CDN | 异步 | HTTPS | `https://sdkframe.anran.xyz/`
| r1a 同步 | 同步 | HTTPS | `https://runoneall.serv00.net/ryhsdk2/`

#### 协议专用源
| 源名称 | 类型 | 协议 | 地址 | 适用协议 |
|--------|------|------|------|------|
| OneBot 协议源 | 异步 | HTTPS | `https://sdkframe.anran.xyz/onebot.json` | 专为OneBot协议优化 |
| 云湖平台源 | 异步 | HTTPS | `https://sdkframe.anran.xyz/yunhu.json` | 云湖平台专用模块 |

### 自定义源配置

#### 基础配置
```json
{
  "name": "源名称",
  "base": "基础URL地址",
  "modules": {
    "模块名": {
      "path": "模块路径",
      "version": "版本号",
      "description": "模块描述",
      "author": "作者"
    }
  }
}
```

#### 高级配置
```json
{
  "dependencies": ["必需依赖模块"],
  "optional_dependencies": [
    "可选模块",
    ["组依赖模块1", "组依赖模块2"]
  ],
  "pip_dependencies": ["Python依赖包"]
}
```

#### 配置说明
1. **组依赖规则**：
   - 单独列出的模块是可选的
   - 用数组包裹的模块组表示为一个整体（即：组依赖模块1+组依赖模块2 和 可选模块 存在一个便符合）

2. **版本规范**：
   - 遵循语义化版本控制（SemVer）
   - 格式：主版本号.次版本号.修订号

3. **路径规则**：
   - 相对路径基于base URL
   - 支持.zip格式压缩包

#### 最佳实践
1. 保持模块体积小于10MB
2. 版本号每次更新递增
3. 提供完整的依赖说明
4. 测试所有依赖组合

> 💡 提示：可以使用JSON验证工具检查配置格式是否正确

---

## ⚠️ 注意事项
1. 生产环境建议使用官方认证源
2. 模块升级前请备份配置
3. 异步/同步模块不可混用
