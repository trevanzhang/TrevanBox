# AI预处理器命令

使用本地Ollama模型对导入内容进行智能分析，自动生成标题、标签、摘要和分类建议。
**支持智能降级处理**：当脚本无法运行时，Claude会接管处理，确保功能始终可用。

## 使用方法

```
/para-process [命令] [选项]
```

## 命令选项

### 简化命令（推荐日常使用）

- **无参数** - 处理所有导入目录并移动到待处理（默认操作）
- `auto` - 等同于无参数，自动处理所有内容

### 基本命令

- `status` - 检查Ollama服务状态和系统环境
- `process <目录>` - 处理指定目录的内容
- `process all` - 处理所有导入目录

### 可选参数

- `--dry-run` - 预览模式，查看处理结果但不修改文件
- `--move-to-inbox` - 处理完成后自动移动到待处理目录
- `--force-claude` - 强制使用Claude原生处理模式（跳过Python脚本）

## 使用示例

### 简化使用（推荐）

```bash
# 最简单用法 - 处理所有导入目录并移动到待处理
/para-process

# 等同于上面，更明确的表达
/para-process auto

# 预览模式 - 查看将要处理的内容但不修改
/para-process --dry-run
```

### 完整用法

```bash
# 检查系统状态
/para-process status

# 预览处理manual目录
/para-process process manual --dry-run

# 处理所有导入目录并移动到待处理（完整命令）
/para-process process all --move-to-inbox

# 处理特定目录
/para-process process follow clippings --move-to-inbox

# 强制使用Claude原生处理（当脚本环境有问题时）
/para-process process manual --force-claude
```

### 日常推荐流程

```bash
# 1. 快速检查状态（可选）
/para-process status

# 2. 一键处理所有新内容（推荐日常使用）
/para-process

# 3. 如果需要预览，可以使用
/para-process --dry-run
```

## 支持的导入目录

- `follow` - RSS订阅内容
- `clippings` - 浏览器插件摘录
- `readwise` - 阅读笔记系统
- `zotero` - 学术文献
- `webdav` - 云存储同步
- `manual` - 手动导入
- `ainotes` - AI生成内容

## 处理功能

### uv脚本模式（优先）

基于uv的现代化Python环境管理，当Ollama服务可用时，AI预处理器会自动为每个文件：

1. **智能标题生成** - 提取或生成简洁标题（8-15字）
2. **标签提取** - 识别关键词和主题标签（最多7个，每个不超过4字）
3. **摘要生成** - 生成200字以内的内容摘要
4. **元数据标准化** - 添加完整的YAML frontmatter
5. **分类建议** - 推荐适合的PARA分类

**技术特点**：
- 使用`uv run --project .`统一管理Python环境
- 自动检测和安装依赖包
- 智能缓存和并行处理，提升执行速度
- 完整的错误处理和用户友好提示

### Claude原生处理模式（备用）

当脚本无法运行时，Claude会接管处理：

1. **智能内容分析** - 基于内容理解生成标题和标签
2. **标准化元数据** - 按照TrevanBox标准格式生成frontmatter
3. **来源识别** - 根据目录自动添加来源标签
4. **内容摘要** - 提取核心观点和关键信息
5. **文件组织** - 支持移动到待处理目录

### 智能降级逻辑

```
1. 检查uv环境和虚拟状态
2. 尝试基于uv的Python脚本处理
3. 如果uv环境有问题，自动切换到Claude原生处理
4. 生成符合TrevanBox标准的元数据
5. 确保处理结果的一致性和可用性
```

## 输出格式

处理后的文件会包含标准化元数据：

```yaml
---
created: 2025-10-16T10:30:00+08:00
updated: 2025-10-16T10:30:00+08:00
status: sprout
type: note
tags: [manual, AI生成标签1, AI生成标签2]
area: "Personal-Growth"
title: "AI生成的简洁标题"
author: "作者"
description: "AI生成的200字内容摘要"
source: "manual"
---
```

### TrevanBox元数据标准

**核心必填字段**：

- `created` - 创建时间（ISO格式）
- `updated` - 更新时间
- `status` - 生命周期状态（sprout|evergreen|discharged）
- `type` - 内容类型（project|area|resource|journal|note|article|excerpt|reading|reference|sync|ai）
- `tags` - 结构化标签数组
- `area` - 所属领域（可选）

**扩展字段**：

- `title` - 文件标题
- `description` - 内容摘要
- `author` - 作者
- `source` - 来源目录
- `url` - 原始链接
- `deadline` - 截止日期
- `priority` - 优先级
- `mood` - 个人状态
- `difficulty` - 内容难度
- `usefulness` - 实用性评估

## 系统要求

### 推荐环境（完整功能）

- **uv工具**：现代化的Python包管理器
- **虚拟环境**：项目根目录下的`.venv`（使用`uv venv .venv`创建）
- Ollama服务运行在 `http://localhost:11434`
- 已下载 `qwen3:8b` 模型
- Python 3.7+ 环境（由uv自动管理）
- 必要的Python包：requests, PyYAML, chardet（由uv自动安装）

### 最低环境（基础功能）

- 无特殊要求，Claude原生处理模式可在任何环境运行

### 环境设置

```bash
# 1. 安装uv（如果没有）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 在项目根目录创建虚拟环境
uv venv .venv

# 3. 安装依赖（脚本会自动检查和安装）
uv pip install requests pyyaml chardet

# 4. 测试环境
./scripts/preprocessor.sh status
```

## 故障排除

### 智能降级处理

该命令支持自动降级，即使环境不完善也能正常工作：

1. **Ollama服务未启动**：自动切换到Claude原生处理
2. **模型未安装**：使用Claude内置智能分析
3. **uv工具未安装**：跳过脚本，直接使用Claude处理
4. **虚拟环境缺失**：提示用户创建环境，同时启用Claude备用处理
5. **依赖包缺失**：脚本会自动尝试安装，失败则启用备用模式
6. **Python环境问题**：跳过脚本，直接使用Claude处理

### 手动故障排除

如果需要优化处理效果：

1. **检查Ollama状态**：运行 `/para-process status`
2. **确认模型存在**：`ollama list` 查看已安装模型
3. **检查uv环境**：确保已安装uv且创建了`.venv`虚拟环境
4. **验证脚本功能**：直接运行 `./scripts/preprocessor.sh status`
5. **检查文件大小**：单个文件不超过10MB
6. **查看错误信息**：命令会显示详细的错误提示

### uv环境快速修复

```bash
# 重新创建虚拟环境
rm -rf .venv
uv venv .venv

# 重新安装依赖
uv pip install requests pyyaml chardet

# 测试环境
./scripts/preprocessor.sh status
```

### 强制使用Claude处理

```bash
# 当脚本有问题时，可以强制使用Claude处理
/para-process process manual --force-claude
```

## 注意事项

- **极简使用**：直接输入 `/para-process` 即可处理所有内容并移动到待处理目录
- **零故障保证**：即使环境不完善，命令也能提供基础处理功能
- **智能降级**：自动检测环境并选择最适合的处理方式
- **一致性保证**：无论使用哪种处理方式，都生成符合TrevanBox标准的元数据
- **建议预览**：首次使用前建议先使用 `--dry-run` 预览处理结果
- **自动备份**：原文件会自动备份，不用担心数据丢失
- **处理提示**：会明确告知用户使用了哪种处理方式

## 最佳实践

### 日常使用（推荐）

```bash
# 每天或每周一次，一键处理所有新内容
/para-process
```

### 首次使用

```bash
# 1. 检查系统状态
/para-process status

# 2. 预览处理内容
/para-process --dry-run

# 3. 正式处理
/para-process
```
