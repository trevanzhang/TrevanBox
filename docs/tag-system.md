# 标签系统说明

## 标签设计原则

1. **一致性**：在整个库中使用相同的标签名称
2. **目的驱动**：添加能回答具体问题的标签
3. **渐进式**：无需一次性完美分类，逐步完善
4. **可搜索**：标签应该能被Obsidian原生搜索和Dataview查询

## 标签分类体系

### 1. 来源标签 (Source Tags)

标识内容的来源渠道，自动根据导入目录添加

```
#follow        - Follow RSS导入
#clippings     - Obsidian浏览器插件导入
#readwise      - Readwise导入
#zotero        - Zotero文献管理导入
#webdav        - WebDAV跨平台同步导入
#manual        - 手动创建或复制粘贴
#ainotes       - AI生成内容保存
```

### 2. 处理状态标签 (Status Tags)

标识内容的处理状态

```
#待处理        - 新导入，尚未分类整理
#已处理        - 已完成分类，放入PARA体系
#需要整理      - 内容需要进一步整理或完善
#待归档        - 准备归档的内容
```

### 3. PARA分类标签 (PARA Category Tags)

细粒度的PARA分类标识

```
#project/active      - 活跃项目
#project/completed   - 已完成项目
#project/on_hold     - 暂停项目
#project/cancelled   - 取消项目

#area/health         - 健康领域
#area/finance        - 财务领域
#area/work           - 工作领域
#area/learning       - 学习领域
#area/family         - 家庭领域

#resource/learning   - 学习资源
#resource/technology - 技术资源
#resource/creative   - 创意资源
#resource/reference  - 参考资料

#archive/2025        - 2025年存档
#archive/work        - 工作相关存档
```

### 4. 内容类型标签 (Content Type Tags)

标识笔记的内容类型

```
#摘录         - 文章、书籍的摘录内容
#想法         - 个人思考和创意
#任务         - 具体的行动项
#会议         - 会议记录
#项目         - 项目相关内容
#学习         - 学习笔记
#参考         - 参考资料
#模板         - 模板文件
#日记         - 个人日记和日志
```

### 5. 优先级标签 (Priority Tags)

标识内容的重要性和紧急程度

```
#高优先级      - 高重要性，需要优先处理
#中优先级      - 中等重要性，正常处理
#低优先级      - 低重要性，可延后处理
#紧急          - 需要立即处理
#重要          - 重要但不紧急
```

### 6. 主题标签 (Topic Tags)

标识具体的话题或主题

```
#技术          - 技术相关
#管理          - 管理相关
#设计          - 设计相关
#营销          - 营销相关
#产品          - 产品相关
#数据分析      - 数据分析
#人工智能      - 人工智能
#个人成长      - 个人成长
```

## 标签使用规范

### 1. 标签格式
- 使用中文标签时，不包含空格或特殊字符
- 英文标签使用小写字母和连字符
- 标签应该简洁明了，便于记忆和输入

### 2. 标签数量
- 每个笔记建议不超过5-7个标签
- 优先使用最重要的标签
- 避免过度细分和冗余标签

### 3. 标签层级
- 使用斜杠表示层级关系，如`#project/active`
- 层级不宜过深，建议不超过2-3层
- 保持层级逻辑清晰

### 4. 标签一致性
- 使用统一的标签名称，避免同义词混用
- 定期检查和清理重复或相似标签
- 维护标签词典，确保团队成员使用一致

## 自动化规则

### 1. 导入时自动添加
```yaml
# 根据文件路径自动添加来源标签
if path contains "follow/" → add #follow
if path contains "clippings/" → add #clippings
if path contains "readwise/" → add #readwise
if path contains "zotero/" → add #zotero
if path contains "webdav/" → add #webdav
if path contains "manual/" → add #manual
if path contains "ainotes/" → add #ainotes
```

### 2. 创建时默认添加
```yaml
# 新建笔记默认添加
- #待处理 (导入内容)
- #sprout (新建内容)
```

### 3. 状态变更时自动更新
```yaml
# 状态变更规则
if status = "completed" → remove #待处理, add #已处理
if moved to archive → add #待归档
```

## 标签查询示例

### Dataview查询
```dataview
LIST FROM #待处理
LIST FROM #project/active AND #高优先级
LIST FROM #clippings AND #技术
TABLE status, priority FROM #项目
```

### 搜索查询
```
tag:#待处理
tag:#project AND tag:#active
tag:#follow AND tag:#技术
```

## 标签维护

### 1. 定期清理
- 每月检查一次标签使用情况
- 删除不常用的标签
- 合并相似标签

### 2. 标签统计
- 使用Dataview统计标签使用频率
- 识别热门标签和冷门标签
- 优化标签结构

### 3. 标签重命名
- 批量重命名功能
- 保持链接的有效性
- 更新相关模板

## 最佳实践

1. **从简开始**：先用基本标签，逐步细化
2. **保持一致**：建立标签使用规范
3. **定期回顾**：定期检查和优化标签系统
4. **平衡详细与简洁**：既要足够详细，又要避免过度复杂
5. **服务于目标**：标签应该帮助实现信息管理目标

---

*创建时间：2025-10-15*
*最后更新：2025-10-15*
*版本：1.0*