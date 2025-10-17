# TrevanBox PARA系统度量分析命令

提供完整的系统健康度分析、趋势追踪和优化建议功能，完美集成PARA方法论。

## 使用方法

```bash
/para-metrics [选项]
```

## 选项参数

### 基础命令
- `/para-metrics` - 执行基础健康度检查
- `/para-metrics quick` - 快速概览，不生成报告文件
- `/para-metrics detailed` - 生成详细的度量分析报告

### 高级功能
- `/para-metrics trend` - 查看历史趋势数据
- `/para-metrics config` - 查看和配置度量参数
- `/para-metrics compare [日期1] [日期2]` - 对比两个时期的度量数据

### 特殊选项
- `--no-save` - 不保存历史数据
- `--no-report` - 不生成详细报告文件
- `--quiet` - 静默模式，只输出核心数据
- `--help` - 显示详细帮助信息

## 使用示例

### 快速健康检查
```bash
/para-metrics
```
> 显示系统总体健康度、文件分布和关键指标

### 生成详细报告
```bash
/para-metrics detailed
```
> 生成完整的度量分析报告，存储在 `2-Areas/Personal-Growth/review/2025/metrics/`

### 查看趋势分析
```bash
/para-metrics trend
```
> 显示系统健康度、文件数量等的历史变化趋势

### 配置度量参数
```bash
/para-metrics config
```
> 查看和调整PARA分布的理想范围、权重等参数

## 输出说明

### 健康度评分标准
- **🟢 优秀 (80-100分)**：系统状态良好，继续保持
- **🟡 良好 (60-79分)**：需要适度优化
- **🔴 需关注 (0-59分)**：需要重点改进

### PARA分布理想范围
- **Projects**: 15-25% (活跃项目数量适中)
- **Areas**: 25-35% (长期责任覆盖全面)
- **Resources**: 35-45% (知识储备充足)
- **Archives**: 5-15% (归档比例合理)

## 报告存储位置

根据PARA方法论，所有度量报告都存储在：
```
2-Areas/Personal-Growth/review/2025/metrics/
├── detailed-metrics-2025-10-17.md    # 详细分析报告
├── metrics-history.json               # 历史数据
└── trend-analysis.md                  # 趋势分析报告
```

## 工作原理

1. **扫描PARA目录**：统计各分类的文件数量和大小
2. **分析内容质量**：评估元数据覆盖、链接密度、更新频率
3. **计算健康度**：基于理想范围计算各项指标得分
4. **生成建议**：根据分析结果提供个性化优化建议
5. **保存历史**：记录度量数据，支持趋势分析

## 最佳实践

### 定期使用频率
- **每日**：`/para-metrics quick` - 快速检查待处理积压
- **每周**：`/para-metrics detailed` - 生成详细报告并回顾
- **每月**：`/para-metrics trend` - 分析月度趋势和改进效果
- **每季度**：深度回顾和系统优化

### 与PARA工作流集成
1. **周回顾时**：运行 `/para-metrics detailed` 作为数据支撑
2. **目标设定时**：参考metrics建议制定改进计划
3. **项目归档时**：检查对PARA分布的影响
4. **领域维护时**：评估领域健康度变化

## 故障排除

### 常见问题
1. **编码错误**：在Windows系统上如遇显示问题，使用 `--quiet` 模式
2. **权限错误**：确保脚本有执行权限
3. **路径问题**：在TrevanBox根目录下运行命令

### 调试选项
```bash
/para-metrics --quiet --no-save  # 最小化输出，不保存数据
```

## 相关命令

- `/para-review` - 完整的PARA系统回顾
- `/para-project` - 项目管理和分析
- `/para-area` - 领域健康度检查

---

**命令版本**: v1.0
**最后更新**: 2025-10-17
**集成版本**: TrevanBox v1.2.0