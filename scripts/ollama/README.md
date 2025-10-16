# TrevanBox AI预处理器

> 基于Ollama的智能内容预处理系统，自动为导入内容生成标准化元数据

## 概述

AI预处理器是TrevanBox系统的核心自动化组件，使用本地Ollama模型对导入的内容进行智能分析，自动生成标题、标签、摘要和分类建议，确保所有内容都符合PARA系统的标准化格式。

## 功能特性

### 🤖 智能分析
- **标题生成**：根据内容自动提取或生成简洁标题
- **标签提取**：智能识别关键词和主题标签
- **摘要生成**：自动生成200字以内的内容摘要
- **分类建议**：推荐适合的PARA分类（Projects/Areas/Resources）
- **元数据标准化**：确保所有文件都有完整的YAML frontmatter

### 📁 多目录支持
支持所有TrevanBox导入目录：
- `follow` - RSS订阅内容
- `clippings` - 浏览器插件摘录
- `readwise` - 阅读笔记系统
- `zotero` - 学术文献
- `webdav` - 云存储同步
- `manual` - 手动导入
- `ainotes` - AI生成内容

### ⚙️ 灵活配置
- **预览模式**：`--dry-run`查看处理结果而不修改文件
- **自动移动**：`--move-to-inbox`处理后自动移动到待处理目录
- **批量处理**：支持单目录或多目录批量处理
- **错误恢复**：自动备份和处理失败恢复

## 安装要求

### 系统依赖
- **uv工具**：现代化Python包管理器
- Python 3.7+（由uv自动管理）
- Ollama服务运行在 `http://localhost:11434`
- Bash shell环境

### 快速环境设置
```bash
# 1. 安装uv（如果没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 在项目根目录创建虚拟环境
uv venv .venv

# 3. 安装Python依赖
uv pip install requests>=2.31.0 PyYAML>=6.0 chardet>=5.2.0

# 4. 验证环境
./scripts/preprocessor.sh status
```

### Ollama模型
```bash
ollama pull qwen3:8b
```

### 环境优势
- **10-100倍更快**：相比传统pip方式
- **智能缓存**：避免重复下载
- **跨平台兼容**：Windows/Linux/macOS统一体验
- **自动依赖管理**：脚本自动检查和安装缺失依赖

## 配置说明

### config.yaml配置文件

```yaml
ollama:
  base_url: "http://localhost:11434"  # Ollama服务地址
  model: "qwen3:8b"                  # 使用的模型
  timeout: 30                        # 请求超时时间（秒）
  retry: 3                          # 重试次数

metadata:
  default_status: "sprout"           # 默认内容状态
  default_type: "note"              # 默认内容类型
  standard_fields:                   # 标准元数据字段
    - "created"
    - "updated"
    - "status"
    - "type"
    - "tags"
    - "area"
    - "title"
    - "description"

processing:
  max_file_size: 10485760           # 最大文件大小（10MB）
  encoding_detection: true          # 自动检测文件编码
  backup_enabled: true              # 启用备份功能
  move_to_inbox: false             # 默认不移动到待处理目录

ai:
  title_max_length: 15              # 标题最大长度
  tags_max_count: 7                 # 最大标签数量
  summary_length: 200               # 摘要长度限制
```

### 目录映射配置
每个导入目录都有对应的默认标签和类型：

```yaml
directory_mapping:
  follow:
    tag: "follow"
    type: "article"
  clippings:
    tag: "clippings"
    type: "excerpt"
  # ... 其他目录配置
```

## 使用方法

### 1. 通过主脚本使用（推荐）

基于uv的现代化脚本，自动处理环境检查和依赖管理：

```bash
# 检查系统状态
./scripts/preprocessor.sh status

# 预览处理manual目录
./scripts/preprocessor.sh process manual --dry-run

# 处理所有导入目录并移动到待处理
./scripts/preprocessor.sh process all --move-to-inbox

# 处理特定目录
./scripts/preprocessor.sh process follow clippings --move-to-inbox
```

### 2. 直接使用Python脚本（高级用户）

```bash
cd scripts/ollama

# 使用uv运行Python脚本
uv run --project ../.. python prehandler.py status

# 处理单个目录
uv run --project ../.. python prehandler.py process manual --dry-run

# 处理多个目录
uv run --project ../.. python prehandler.py process follow clippings --move-to-inbox
```

### 3. 使用Claude命令（需要Claude Code）

```bash
# 最简单的使用方式
/para-process

# 预览模式
/para-process --dry-run

# 处理特定目录
/para-process process manual --move-to-inbox
```

## 处理流程

### 1. 文件分析
```
输入文件 → 编码检测 → 内容提取 → 大小检查
```

### 2. AI处理
```
内容文本 → Ollama API → 结构化输出 → 元数据生成
```

### 3. 文件更新
```
原始文件 → 添加frontmatter → 标准化格式 → 备份原文件
```

### 4. 可选移动
```
处理完成 → 移动到0-Inbox/pending/ → 等待人工分类
```

## 输出格式

处理后的文件会包含标准化的YAML frontmatter：

```yaml
---
created: 2025-10-16T10:30:00+08:00
updated: 2025-10-16T10:30:00+08:00
status: sprout
type: note
tags: [AI, 预处理, 自动化]
area: "Personal-Growth"
title: "AI预处理器使用指南"
description: "介绍如何使用TrevanBox的AI预处理器"
source: "manual"
---
```

## 故障排除

### 常见问题

1. **Ollama连接失败**
   ```bash
   # 检查Ollama服务状态
   ollama list

   # 确保服务正在运行
   ollama serve
   ```

2. **Python依赖缺失**
   ```bash
   # 重新安装依赖（使用uv）
   cd ../../
   rm -rf .venv
   uv venv .venv
   uv pip install requests pyyaml chardet

   # 或使用脚本自动修复
   ./scripts/preprocessor.sh status
   ```

3. **文件编码问题**
   - 系统会自动检测文件编码
   - 如果检测失败，会尝试UTF-8和GBK编码

4. **处理失败**
   - 检查`config.yaml`配置
   - 查看错误日志信息
   - 确认文件大小不超过限制

### 调试模式

```bash
# 启用详细输出
export DEBUG=1
./scripts/preprocessor.sh process manual --dry-run
```

## 性能优化

### 建议设置
- **模型选择**：qwen3:8b在速度和质量间取得平衡
- **批量处理**：一次处理多个文件减少API调用开销
- **文件大小限制**：避免处理过大的文件影响性能

### 硬件要求
- **内存**：建议8GB以上（用于8B模型）
- **存储**：至少1GB可用空间（用于模型和备份）
- **网络**：本地Ollama服务，无需外网连接

## 扩展开发

### 添加新的处理规则
1. 修改`config.yaml`中的`directory_mapping`
2. 在`prehandler.py`中添加自定义处理逻辑
3. 更新元数据标准字段

### 集成其他AI模型
1. 修改`config.yaml`中的`ollama`配置
2. 调整API调用参数
3. 适配模型输出格式

## 版本历史

- **v1.2.0** (2025-10-16)
  - **uv现代化升级**：基于uv的Python环境管理
  - **智能依赖处理**：自动检查和安装缺失依赖
  - **性能优化**：10-100倍更快的依赖安装
  - **跨平台兼容**：统一的使用体验
  - **更好的错误处理**：用户友好的提示和解决方案

- **v1.1.0** (2025-10-15)
  - 集成Ollama qwen3:8b模型
  - 完整的配置系统
  - 支持基本的AI预处理功能

- **v1.0.0** (2025-10-15)
  - 初始版本发布
  - 基础AI预处理功能

## 许可证

MIT License - 详见项目根目录的LICENSE文件

## 贡献指南

欢迎提交Issue和Pull Request来改进预处理器系统。

---

## 快速开始

```bash
# 1. 一键环境设置
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv .venv
uv pip install requests pyyaml chardet

# 2. 下载AI模型
ollama pull qwen3:8b

# 3. 测试系统
./scripts/preprocessor.sh status

# 4. 开始使用
./scripts/preprocessor.sh process manual --dry-run
```

**注意**：首次使用前请确保：
1. 已安装uv工具并创建了`.venv`虚拟环境
2. Ollama服务正常运行且已下载qwen3:8b模型
3. 项目根目录存在`CLAUDE.md`文件（用于项目识别）