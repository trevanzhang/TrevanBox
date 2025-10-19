---
description: 周报撰写助手 - 使用writing-weekly-report技能和weekly-report-assistant代理撰写专业工作周报
argument-hint: [工作内容描述]
---

# 周报撰写助手

## 功能描述
专业的风控合规部工作周报撰写工具，通过调用 `writing-weekly-report` 技能和 `weekly-report-assistant` 代理，为您生成结构完整、内容详实的专业周报。

## 使用方法
```bash
/weekly-report-assist [工作内容描述]
```

## 参数说明
- **工作内容描述**（可选）：您可以提供本周的工作要点，如：
  - "完成了风控检查，合规培训，下周要做内控审计"
  - "本周主要处理了3个合规项目，1个风险评估"
  - 不提供描述时，助手会引导您逐步提供信息

## 工作流程
1. **信息收集**：根据风控合规部模板引导您提供工作内容
2. **文件处理**：支持您上传工作清单、会议纪要等文件
3. **专业撰写**：调用 weekly-report-assistant 代理进行周报撰写
4. **模板生成**：基于风控合规部标准模板生成最终文档

## 模板包含
- 部门常态化工作
- 风控方面重点工作
- 合规方面重点工作
- 内控方面重点工作
- 法务方面重点工作
- 审计巡查相关工作
- 下周工作计划

## 使用示例

### 示例1：简要描述
```bash
/weekly-report-assist 本周完成了风控检查和合规培训，下周要做内控审计
```

### 示例2：无参数
```bash
/weekly-report-assist
```
助手会引导您逐步提供各项工作内容

### 示例3：文件处理
```bash
/weekly-report-assist 我有工作清单文件需要处理
```

## 注意事项
- 此命令专门针对风控合规部的周报需求
- 生成的周报符合金融行业汇报标准
- 支持 Templater 语法的自动日期填充
- 每个工作事项控制在150字以内，确保简洁专业

## 相关技能
- **writing-weekly-report**：周报撰写核心技能
- **weekly-report-assistant**：专业周报撰写代理

---
Use your writing-weekly-report skill to help users create professional weekly reports for the compliance and risk management department.
