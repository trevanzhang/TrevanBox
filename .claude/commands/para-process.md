# AI预处理器命令

使用本地Ollama模型对导入内容进行智能分析，自动生成标题、标签、摘要和分类建议。

## 使用方法

```
/para-process [命令] [选项]
```

## 命令选项

### 基本命令
- `status` - 检查Ollama服务状态和系统环境
- `process <目录>` - 处理指定目录的内容
- `process all` - 处理所有导入目录

### 可选参数
- `--dry-run` - 预览模式，查看处理结果但不修改文件
- `--move-to-inbox` - 处理完成后自动移动到待处理目录

## 使用示例

```bash
# 检查系统状态
/para-process status

# 预览处理manual目录
/para-process process manual --dry-run

# 处理所有导入目录并移动到待处理
/para-process process all --move-to-inbox

# 处理特定目录
/para-process process follow clippings --move-to-inbox
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

AI预处理器会自动为每个文件：

1. **智能标题生成** - 提取或生成简洁标题
2. **标签提取** - 识别关键词和主题标签（最多7个）
3. **摘要生成** - 生成200字以内的内容摘要
4. **元数据标准化** - 添加完整的YAML frontmatter
5. **分类建议** - 推荐适合的PARA分类

## 输出格式

处理后的文件会包含标准化元数据：

```yaml
---
created: 2025-10-16T10:30:00+08:00
updated: 2025-10-16T10:30:00+08:00
status: sprout
type: note
tags: [标签1, 标签2]
area: "Personal-Growth"
title: "文件标题"
description: "内容摘要"
source: "manual"
---
```

## 系统要求

- Ollama服务运行在 `http://localhost:11434`
- 已下载 `qwen3:8b` 模型
- Python 3.7+ 环境
- 必要的Python包：requests, PyYAML, chardet

## 故障排除

如果遇到问题：

1. **检查Ollama状态**：运行 `/para-process status`
2. **确认模型存在**：`ollama list` 查看已安装模型
3. **检查文件大小**：单个文件不超过10MB
4. **查看错误信息**：命令会显示详细的错误提示

## 注意事项

- 首次使用前请确保Ollama服务正常运行
- 建议先使用 `--dry-run` 预览处理结果
- 处理大文件时请耐心等待，AI分析需要时间
- 原文件会自动备份，不用担心数据丢失