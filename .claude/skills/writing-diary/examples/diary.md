---
created: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
updated: <% tp.date.now("YYYY-MM-DDTHH:mm:ssZ") %>
status: sprout  # sprout|evergreen|discharged
type: journal
tags: [日记, <% tp.date.now("YYYY-MM-DD") %>, 自定义模板, 行动触发]
date: <% tp.date.now("YYYY-MM-DD") %>
weekday: <% tp.date.now("dddd") %>
mood:
weather:
energy_level:  # 1-10分
focus_areas: []  # 今日重点领域
action_items: []  # 需要转化的行动项
area: "Personal-Growth"
---
# <% tp.date.now("YYYY年MM月DD日 dddd") %>

## 📋 今日概览

**日期**：<% tp.date.now("YYYY年MM月DD日") %>
**星期**：<% tp.date.now("dddd") %>
**天气**：
**心情**：
**精力水平**：

## 🎯 今日重点 (最多3项)

- [ ]
- [ ]
- [ ]

## ✅ 完成事项

<!-- 记录今天完成的重要事项 -->

## 💭 深度思考

<!-- 记录今天的重要想法、感悟和学习 -->

## 🌟 今日闪念（可选）

<!-- 如有闪念内容，将自动整合到这里 -->

## 🔗 PARA连接

* [ ] 项目相关

<!-- 链接到相关项目，标记需要行动的内容 -->

### 领域维护

<!-- 链接到相关领域，记录维护状态 -->

资源收集

<!-- 链接到相关资源，标记值得收藏的内容 -->

## 📊 量化追踪

- **睡眠时间**：
- **运动情况**：
- **阅读时间**：
- **工作时长**：
- **专注度**：

## 💡 明日计划

<!-- 为明天做准备的提醒 -->

<< [[<% tp.date.now("YYYY-MM-DD", -1) %>]] | [[<% tp.date.now("YYYY-MM-DD", 1) %>]] >>

---

*基于PARA最佳实践的自定义日记模板*
