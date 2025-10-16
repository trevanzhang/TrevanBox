# 项目管理命令

创建、管理和跟踪PARA系统中的项目，从项目启动到完成的完整生命周期管理。

## 使用方法

```
/para-project [命令] [项目名称] [选项]
```

## 命令选项

### 项目创建
- `create <项目名称>` - 创建新项目
- `template <模板类型>` - 使用指定模板创建项目

### 项目管理
- `list` - 列出所有项目及状态
- `status <项目名称>` - 查看项目详细状态
- `update <项目名称>` - 更新项目信息
- `complete <项目名称>` - 标记项目完成
- `archive <项目名称>` - 归档已完成项目

### 项目跟踪
- `active` - 显示所有活跃项目
- `stuck` - 显示停滞的项目
- `due` - 显示即将到期项目
- `review` - 项目回顾和分析

## 使用示例

```bash
# 创建新项目
/para-project create "学习Python编程"
/para-project create "2025年健身计划" --template goal

# 查看项目列表
/para-project list
/para-project active

# 更新项目状态
/para-project update "学习Python编程" --status active
/para-project update "学习Python编程" --progress 60

# 完成项目
/para-project complete "学习Python编程"
/para-project archive "学习Python编程"

# 项目回顾
/para-project review
/para-project status "学习Python编程"
```

## 选项参数

### 创建选项
- `--template <类型>` - 使用模板（goal, task, learning, standard）
- `--deadline <日期>` - 设置截止日期
- `--priority <级别>` - 设置优先级（high, medium, low）
- `--area <领域>` - 关联生活领域
- `--tags <标签>` - 添加项目标签

### 更新选项
- `--status <状态>` - 更新项目状态（planning, active, paused, completed）
- `--progress <百分比>` - 更新完成进度
- `--deadline <日期>` - 修改截止日期
- `--note <备注>` - 添加进度备注

## 项目状态

### 生命周期状态
- **planning** - 规划阶段，正在制定计划
- **active** - 活跃状态，正在执行中
- **paused** - 暂停状态，暂时停止
- **completed** - 已完成，目标达成
- **archived** - 已归档，移至4-Archives/

### 优先级
- **high** - 高优先级，需要重点关注
- **medium** - 中等优先级，正常推进
- **low** - 低优先级，时间允许时处理

## 项目模板

### 标准项目模板
```yaml
---
title: "项目标题"
created: 2025-10-16T10:30:00+08:00
updated: 2025-10-16T10:30:00+08:00
status: active
type: project
priority: medium
deadline: 2025-12-31
area: "Personal-Growth"
tags: [项目, 学习]
progress: 0
---

# 项目概述

## 目标
- 明确的项目目标和期望成果

## 行动项
- [ ] 任务1
- [ ] 任务2
- [ ] 任务3

## 时间线
- 开始日期：2025-10-16
- 截止日期：2025-12-31
- 里程碑：根据项目设定

## 资源需求
- 所需资源和工具

## 进度跟踪
- 定期更新项目进展
- 记录遇到的问题和解决方案
```

### 目标导向模板
适用于有明确目标的个人发展项目：

```yaml
---
title: "2025年目标：xxx"
type: project
template: goal
goal_type: personal
metrics: []
---
```

### 学习项目模板
适用于技能学习和知识获取：

```yaml
---
title: "学习：xxx技能"
type: project
template: learning
skill_level: beginner
target_level: intermediate
---
```

## 项目管理流程

### 1. 项目创建
```
确定目标 → 选择模板 → 设置基本信息 → 分解任务
```

### 2. 项目执行
```
定期更新 → 跟踪进度 → 调整计划 → 记录经验
```

### 3. 项目完成
```
成果验收 → 经验总结 → 归档保存 → 知识转化
```

## 输出示例

### 项目列表
```
🚀 活跃项目 (3个)
├── 📚 学习Python编程 [进度: 60%] [截止: 2025-12-31]
├── 💪 2025年健身计划 [进度: 30%] [截止: 2025-06-30]
└── 💼 职业技能提升 [进度: 15%] [截止: 2025-08-31]

⏸️ 暂停项目 (1个)
└── 🏠 家庭装修计划 [进度: 80%]

✅ 本月完成 (2个)
├── 📖 阅读《深度工作》
└── 🎯 建立晨间例程
```

### 项目详情
```
📚 项目：学习Python编程
📊 状态：活跃 (60% 完成)
📅 截止：2025-12-31 (剩余 76 天)
🎯 优先级：高
🏷️ 标签：[编程, Python, 技能, 职业发展]

📋 当前任务：
- [x] 基础语法学习
- [x] 面向对象编程
- [ ] Web框架开发 (进行中)
- [ ] 数据库操作
- [ ] 项目实战

📝 最新更新：
2025-10-15: 完成面向对象编程学习，开始学习Flask框架

🔗 相关资源：
- Python官方文档
- Flask教程合集
- 实战项目思路
```

## 智能功能

### 项目建议
基于现有内容自动推荐项目：
- 从学习笔记中发现技能提升机会
- 从目标设定中拆解可执行项目
- 从问题分析中创建改进项目

### 进度提醒
- 自动提醒即将到期项目
- 停滞项目预警
- 定期进度更新提醒

### 成果转化
- 项目完成后自动生成经验总结
- 将项目经验转化为可复用资源
- 识别可以孵化的新项目

## 最佳实践

### 项目管理原则
1. **明确目标**：每个项目都要有清晰的成果定义
2. **合理分解**：将大目标分解为可执行的小任务
3. **定期回顾**：每周更新项目进展和调整计划
4. **及时归档**：完成后及时整理和归档

### 命名规范
- 使用清晰描述性的项目名称
- 包含时间信息（如年度、季度）
- 避免过于宽泛或模糊的表述

### 时间管理
- 设定合理的截止日期
- 分配足够的执行时间
- 预留缓冲时间应对意外

## 相关链接

- 项目模板：`templates/project-note.md`
- 目标管理：`2-Areas/Personal-Growth/goal-management/`
- 定期回顾：`/para-review` 命令
- 内容组织：`/para-organize` 命令