---
name: writing-weekly-report
description: Use when users execute /weekly-report-assist command - provides structured templates, automated data collection from work descriptions, and content expansion capabilities for creating comprehensive workplace reports through weekly-report-assistant agent
---

# 周报撰写技能

## 概述

专业的工作周报撰写技能，基于TrevanBox系统的标准化方法，调用weekly-report-assistant代理，提供职场工作汇报的完整解决方案。将简要的工作框架自动扩展为结构完整、内容详实的专业周报文档。

**核心能力：**
- **代理协作**：调用weekly-report-assistant专业代理进行周报撰写
- **自动化数据收集**：从用户描述或文件中提取工作要点和关键信息
- **模板化生成**：基于风控合规部标准模板快速生成结构化周报
- **智能内容扩展**：将简要框架合理扩展为详细工作内容
- **专业格式优化**：确保输出符合职场汇报标准

**重要提醒：必须调用weekly-report-assistant代理进行周报撰写**

## 使用时机

**唯一使用时机：**
- 用户明确执行 `/weekly-report-assist` 命令时触发

**不要使用：**
- 用户说"写周报"、"写工作报告"等自然语言表达
- 用户提及需要写周报但没有使用命令
- 个人成长回顾（使用周回顾功能）
- 项目特定的技术文档
- 学习笔记或知识整理

**重要提醒：此技能只在 `/weekly-report-assist` 命令时触发，不会自动感应周报相关需求**

## 核心模式

**之前：** 手动整理工作内容，缺乏结构化，信息不完整
**之后：** 自动化生成专业周报，内容完整，格式规范，重点突出

## 快速参考

| 步骤 | 操作 | 工具/方法 |
|------|--------|--------------|
| 1 | 信息收集 | 引导用户提供工作要点 |
| 2 | 数据整理 | 分类和结构化工作内容 |
| 3 | 模板应用 | 使用标准周报模板 |
| 4 | 内容扩展 | 基于关键词补充细节 |
| 5 | 格式优化 | 确保专业汇报格式 |
| 6 | 质量检查 | 字数控制和逻辑验证 |

## 实现细节

### 1. 代理调用策略

**必须调用weekly-report-assistant代理：**
- 使用Task工具调用weekly-report-assistant代理
- 提供收集到的用户输入和模板信息
- 让专业代理进行周报的实际撰写工作
- 确保输出的专业性和规范性

**代理调用示例：**
```python
Task(
    subagent_type="weekly-report-assistant",
    description="撰写风控合规部工作周报",
    prompt="基于以下信息撰写专业的工作周报：[用户提供的工作要点]"
)
```

### 2. 用户互动策略

**互动方式一：引导式提问**
基于模板结构引导用户提供信息：
- "请告诉我本周在部门常态化工作方面完成了哪些事项？"
- "风控方面有什么重点工作需要汇报？"
- "合规方面的工作进展如何？"
- "下周的工作计划是什么？"

**互动方式二：文件处理**
接受用户提供的工作文件：
- "您可以提供工作清单、会议纪要等文件，我来帮您整理成周报"
- "请上传相关的工作文档，我会基于模板生成周报"
- 支持文本文件、会议记录、工作清单等多种格式

**信息收集要点：**
- 部门常态化工作事项
- 风控、合规、内控、法务等专业工作
- 审计巡查相关工作
- 下周工作计划安排

### 3. 风控合规部周报结构

**基于实际模板的周报结构：**
1. **本周工作完成情况**
   - 部门常态化工作
   - 风控方面重点工作
   - 合规方面重点工作
   - 内控方面重点工作
   - 法务方面重点工作
   - 审计巡查相关工作
   - 其他工作

2. **下周工作计划**
   - 重点任务安排
   - 预期时间节点
   - 所需资源支持

### 4. 智能内容扩展

**扩展原则：**
- 基于关键词合理推测工作背景
- 补充具体的执行细节和过程
- 添加量化的成果数据
- 完善问题描述和解决方案

**质量控制：**
- 每个工作事项控制在150字以内
- 确保语言专业且简洁
- 保持逻辑清晰和重点突出
- 避免冗余表达和无关内容

### 5. 模板系统集成

**强制使用风控合规部模板：**
- 必须使用 `examples/weekly-report-template.md` 模板
- 模板已配置Templater语法支持自动日期等
- 包含风控合规部的专业分类（风控、合规、内控、法务）
- 支持审计巡查等专项工作汇报

**模板特性：**
- 部门标准化的章节结构
- 专业的分类体系
- Templater语法自动填充基础信息
- 灵活的内容填充区域
- 符合金融行业汇报规范

### 6. 多格式导出功能

**导出脚本集成：**
- 脚本位置：`scripts/export-to-docx.py`
- 自动剔除front matter信息，只导出正文内容
- 支持Word（.docx）和PDF（.pdf）两种格式
- 支持批量导出多种格式
- 智能转换为专业文档格式，保持中文显示效果
- 跨平台桌面路径支持（Windows/Linux/Mac）
- 自动生成带时间戳的专业文件名

**格式选择：**
- **PDF格式**：适合正式汇报，格式保持性好，跨平台兼容性强
- **Word格式**：便于编辑和修改，支持进一步个性化调整
- **批量导出**：同时生成PDF和Word两种格式

**依赖管理：**
- 使用uv统一管理Python包环境
- 依赖包：`python-docx`、`markdown`、`beautifulsoup4`、`reportlab`
- 安装命令：`uv add python-docx markdown beautifulsoup4 reportlab`
- 自动依赖检查和安装提示

**导出特性：**
- 完全移除YAML front matter
- **正确的Markdown格式渲染**：支持粗体、斜体、下划线等富文本格式
- 保持标题层级结构和列表格式
- 支持中文格式和字体（PDF使用SimHei字体）
- 自动调整页面布局和样式
- 提供详细的导出进度和结果反馈
- PDF格式专业美观，适合正式汇报
- 使用markdown和beautifulsoup4库确保格式正确解析

## 完整工作流程

### 步骤1：用户信息收集
**引导用户提供信息：**
- 询问本周各部门工作完成情况
- 收集风控、合规、内控、法务等专业工作事项
- 了解下周工作计划安排
- 接受用户提供的工作文件（如有）

### 步骤2：代理调用处理
**调用weekly-report-assistant代理：**
- 整理收集到的用户信息
- 提供模板结构作为参考
- 让专业代理进行周报撰写
- 确保内容的专业性和完整性

### 步骤3：输出优化
**最终输出处理：**
- 基于风控合规部模板格式化输出
- 确保符合汇报标准和要求
- 提供预览和调整机会
- 生成完整的周报文档

### 步骤4：导出询问
**询问导出需求：**
- 周报完成后询问用户："是否需要导出周报？"
- 提供格式选择："1. PDF格式（推荐，适合正式汇报）2. Word格式（便于编辑）3. 两种格式都要"
- 解释不同格式的优势和适用场景
- 等待用户选择

### 步骤5：脚本执行
**导出处理：**
- 根据用户选择调用相应的导出命令
- PDF格式：`python scripts/export-to-docx.py 周报.md --format pdf`
- Word格式：`python scripts/export-to-docx.py 周报.md --format docx`
- 批量导出：`python scripts/export-to-docx.py 周报.md --format both`
- 脚本自动剔除front matter信息
- 转换为专业文档格式并导出到桌面

### 步骤6：完成确认
**结果反馈：**
- 显示导出成功消息和文件数量
- 提供所有导出文件的完整路径和大小信息
- 确认导出文件的格式正确性
- 根据格式选择提供相应的使用建议

## 常见错误

**❌ 未调用专业代理**：直接使用通用模型撰写
**✅ 必须调用weekly-report-assistant**：确保专业性

**❌ 模板使用错误**：使用通用模板而非风控合规部专用模板
**✅ 使用专用模板**：确保格式和分类符合部门要求

**❌ 信息收集不完整**：遗漏重要的专业工作事项
**✅ 全面信息梳理**：按部门分类系统性收集工作内容

**❌ 互动方式单一**：只接受文字描述不接受文件
**✅ 多元化互动**：支持引导提问和文件处理两种方式

## 实际影响

- **效率提升**：周报撰写时间减少70%
- **质量改善**：汇报内容更加完整和专业
- **标准化**：统一的格式和风格提升企业形象
- **沟通效果**：清晰的汇报有助于上级理解工作价值

---

**技能版本**：2.0
**最后更新**：2025-10-19
**兼容系统**：TrevanBox v1.2.1

## 脚本调用方式

当用户确认导出需求时，使用以下命令调用导出脚本：

### 单一格式导出
```bash
# 导出为PDF（推荐）
python .claude/skills/writing-weekly-report/scripts/export-to-docx.py [周报文件路径] --format pdf

# 导出为Word
python .claude/skills/writing-weekly-report/scripts/export-to-docx.py [周报文件路径] --format docx
```

### 批量格式导出
```bash
# 同时导出PDF和Word两种格式
python .claude/skills/writing-weekly-report/scripts/export-to-docx.py [周报文件路径] --format both
```

### 自定义输出目录
```bash
# 导出到指定目录
python .claude/skills/writing-weekly-report/scripts/export-to-docx.py [周报文件路径] --output-dir ./exports
```

**调用示例**：
```bash
# PDF导出示例
python .claude/skills/writing-weekly-report/scripts/export-to-docx.py 2-Areas/Personal-Growth/review/2025/周报-2025-10-19.md --format pdf

# 批量导出示例
python .claude/skills/writing-weekly-report/scripts/export-to-docx.py 2-Areas/Personal-Growth/review/2025/周报-2025-10-19.md --format both
```

## 更新说明

### v2.0 (2025-10-19)
- **新增多格式导出功能**：支持PDF和Word两种格式导出
- **PDF格式支持**：专业的PDF文档生成，适合正式汇报
- **批量导出功能**：一次操作生成多种格式文件
- **增强的用户交互**：提供格式选择和使用建议
- **扩展的依赖管理**：新增markdown和reportlab依赖

### v1.2 (2025-10-19)
- **新增.docx导出功能**：完整的Word文档导出解决方案
- **front matter完全剔除**：导出文档只包含正文内容，符合正式汇报要求
- **uv环境集成**：使用项目统一的uv包管理，确保环境一致性
- **跨平台支持**：支持Windows/Linux/Mac桌面路径自动识别
- **脚本集成设计**：导出脚本位于技能目录内，符合Agent Skills最佳实践

### v1.1 (2025-10-19)
- **新增代理调用**：明确必须调用weekly-report-assistant代理进行周报撰写
- **优化用户互动**：支持引导式提问和文件处理两种互动方式
- **专业化模板**：集成风控合规部专用模板，包含Templater语法支持
- **完整工作流程**：定义了信息收集→代理调用→输出优化的三步流程
- **部门定制化**：针对风控合规部的专业分类（风控、合规、内控、法务）进行优化

### v1.0 (2025-10-19)
- 初始版本发布
- 基础周报撰写功能
- 标准模板集成
- 自动化数据收集能力
- 智能内容扩展功能
- 质量控制和格式优化

*此技能专注于风控合规部职场工作汇报的撰写，通过调用weekly-report-assistant代理确保专业性，与TrevanBox系统的个人成长回顾功能形成互补。*