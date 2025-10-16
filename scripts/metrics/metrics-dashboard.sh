#!/bin/bash

# TrevanBox 度量指标仪表板生成脚本
# 用于自动生成系统健康度报告和指标统计

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
REPORTS_DIR="$BASE_DIR/docs/reports"

# 创建报告目录
mkdir -p "$REPORTS_DIR"

# 当前日期
CURRENT_DATE=$(date +"%Y-%m-%d")
CURRENT_MONTH=$(date +"%Y-%m")
REPORT_FILE="$REPORTS_DIR/metrics-report-$CURRENT_DATE.md"

echo -e "${BLUE}=== TrevanBox 度量指标仪表板 ===${NC}"
echo -e "${BLUE}报告日期: $CURRENT_DATE${NC}"
echo

# 函数：统计文件数量
count_files() {
    local dir="$1"
    if [ -d "$BASE_DIR/$dir" ]; then
        find "$BASE_DIR/$dir" -name "*.md" | wc -l
    else
        echo "0"
    fi
}

# 函数：统计目录大小
get_dir_size() {
    local dir="$1"
    if [ -d "$BASE_DIR/$dir" ]; then
        du -sh "$BASE_DIR/$dir" 2>/dev/null | cut -f1
    else
        echo "0"
    fi
}

# 函数：获取最旧文件年龄
get_oldest_file_age() {
    local dir="$1"
    if [ -d "$BASE_DIR/$dir" ]; then
        find "$BASE_DIR/$dir" -name "*.md" -type f -exec stat -c %Y {} \; 2>/dev/null | sort -n | head -1 | while read timestamp; do
            if [ ! -z "$timestamp" ]; then
                echo $(( ($(date +%s) - $timestamp) / 86400 ))
            fi
        done
    else
        echo "0"
    fi
}

# 函数：计算健康度得分（不依赖bc命令）
calculate_health_score() {
    local value="$1"
    local min="$2"
    local max="$3"

    # 转换为整数计算（乘以10避免浮点数）
    local value_int=$((${value%.*} * 10))
    local min_int=$((min * 10))
    local max_int=$((max * 10))

    if [ $value_int -ge $min_int ] && [ $value_int -le $max_int ]; then
        echo "100"
    elif [ $value_int -lt $min_int ]; then
        local score=$((100 - (min_int - value_int) / 5))
        if [ $score -lt 0 ]; then echo "0"; else echo "$score"; fi
    else
        local score=$((100 - (value_int - max_int) / 5))
        if [ $score -lt 0 ]; then echo "0"; else echo "$score"; fi
    fi
}

# 开始统计
echo -e "${YELLOW}正在统计PARA分布...${NC}"

# PARA统计
PROJECTS_COUNT=$(count_files "1-Projects")
AREAS_COUNT=$(count_files "2-Areas")
RESOURCES_COUNT=$(count_files "3-Resources")
ARCHIVES_COUNT=$(count_files "4-Archives")
TOTAL_COUNT=$((PROJECTS_COUNT + AREAS_COUNT + RESOURCES_COUNT + ARCHIVES_COUNT))

# 计算分布比例（不依赖bc）
if [ $TOTAL_COUNT -gt 0 ]; then
    PROJECTS_RATIO=$((PROJECTS_COUNT * 1000 / TOTAL_COUNT))
    PROJECTS_RATIO=$(echo "scale=1; $PROJECTS_RATIO / 10" | sed 's/\.0//')

    AREAS_RATIO=$((AREAS_COUNT * 1000 / TOTAL_COUNT))
    AREAS_RATIO=$(echo "scale=1; $AREAS_RATIO / 10" | sed 's/\.0//')

    RESOURCES_RATIO=$((RESOURCES_COUNT * 1000 / TOTAL_COUNT))
    RESOURCES_RATIO=$(echo "scale=1; $RESOURCES_RATIO / 10" | sed 's/\.0//')

    ARCHIVES_RATIO=$((ARCHIVES_COUNT * 1000 / TOTAL_COUNT))
    ARCHIVES_RATIO=$(echo "scale=1; $ARCHIVES_RATIO / 10" | sed 's/\.0//')
else
    PROJECTS_RATIO=0
    AREAS_RATIO=0
    RESOURCES_RATIO=0
    ARCHIVES_RATIO=0
fi

# 计算健康度得分
PROJECTS_HEALTH=$(calculate_health_score "$PROJECTS_RATIO" 15 25)
AREAS_HEALTH=$(calculate_health_score "$AREAS_RATIO" 25 35)
RESOURCES_HEALTH=$(calculate_health_score "$RESOURCES_RATIO" 35 45)
ARCHIVES_HEALTH=$(calculate_health_score "$ARCHIVES_RATIO" 5 15)

# 总体健康度
OVERALL_HEALTH=$(( (PROJECTS_HEALTH + AREAS_HEALTH + RESOURCES_HEALTH + ARCHIVES_HEALTH) / 4 ))

echo -e "${YELLOW}正在检查待处理积压...${NC}"

# 待处理统计
PENDING_COUNT=$(count_files "0-Inbox/pending")
OLDEST_PENDING_AGE=$(get_oldest_file_age "0-Inbox/pending")

# 目录大小统计
PROJECTS_SIZE=$(get_dir_size "1-Projects")
AREAS_SIZE=$(get_dir_size "2-Areas")
RESOURCES_SIZE=$(get_dir_size "3-Resources")
ARCHIVES_SIZE=$(get_dir_size "4-Archives")

# 生成报告
cat > "$REPORT_FILE" << EOF
# TrevanBox 系统度量报告

**生成时间**: $CURRENT_DATE
**报告周期**: 月度报告
**系统版本**: v1.2.0

## 📊 系统概览

| 指标 | 数值 | 状态 |
|------|------|------|
| 总文件数 | $TOTAL_COUNT | - |
| PARA健康度 | $OVERALL_HEALTH/100 | $(if [ $OVERALL_HEALTH -ge 80 ]; then echo "🟢 优秀"; elif [ $OVERALL_HEALTH -ge 60 ]; then echo "🟡 良好"; else echo "🔴 需关注"; fi) |
| 待处理积压 | $PENDING_COUNT 项 | $(if [ $PENDING_COUNT -le 5 ]; then echo "🟢 正常"; elif [ $PENDING_COUNT -le 15 ]; then echo "🟡 需处理"; else echo "🔴 积压严重"; fi) |
| 最旧积压年龄 | $OLDEST_PENDING_AGE 天 | $(if [ $OLDEST_PENDING_AGE -le 3 ]; then echo "🟢 正常"; elif [ $OLDEST_PENDING_AGE -le 7 ]; then echo "🟡 需关注"; else echo "🔴 严重积压"; fi) |

## 📁 PARA分布分析

### 文件数量分布

| 类别 | 文件数 | 占比 | 理想范围 | 健康度 | 状态 |
|------|--------|------|----------|--------|------|
| Projects | $PROJECTS_COUNT | $PROJECTS_RATIO% | 15-25% | $PROJECTS_HEALTH/100 | $(if [ $PROJECTS_HEALTH -ge 80 ]; then echo "🟢"; elif [ $PROJECTS_HEALTH -ge 60 ]; then echo "🟡"; else echo "🔴"; fi) |
| Areas | $AREAS_COUNT | $AREAS_RATIO% | 25-35% | $AREAS_HEALTH/100 | $(if [ $AREAS_HEALTH -ge 80 ]; then echo "🟢"; elif [ $AREAS_HEALTH -ge 60 ]; then echo "🟡"; else echo "🔴"; fi) |
| Resources | $RESOURCES_COUNT | $RESOURCES_RATIO% | 35-45% | $RESOURCES_HEALTH/100 | $(if [ $RESOURCES_HEALTH -ge 80 ]; then echo "🟢"; elif [ $RESOURCES_HEALTH -ge 60 ]; then echo "🟡"; else echo "🔴"; fi) |
| Archives | $ARCHIVES_COUNT | $ARCHIVES_RATIO% | 5-15% | $ARCHIVES_HEALTH/100 | $(if [ $ARCHIVES_HEALTH -ge 80 ]; then echo "🟢"; elif [ $ARCHIVES_HEALTH -ge 60 ]; then echo "🟡"; else echo "🔴"; fi) |

### 存储空间分布

| 类别 | 大小 | 说明 |
|------|------|------|
| Projects | $PROJECTS_SIZE | 当前活跃项目 |
| Areas | $AREAS_SIZE | 长期维护领域 |
| Resources | $RESOURCES_SIZE | 知识资源储备 |
| Archives | $ARCHIVES_SIZE | 历史存档内容 |

## 📈 趋势分析

### 月度变化
> *需要历史数据才能生成趋势图表*

### 建议和行动

#### 🔴 紧急关注
EOF

# 添加紧急关注项目
if [ $OLDEST_PENDING_AGE -gt 7 ]; then
    echo "- **待处理积压严重**：有 $OLDEST_PENDING_AGE 天的积压内容需要立即处理" >> "$REPORT_FILE"
fi

if [ $PROJECTS_HEALTH -lt 60 ]; then
    echo "- **Projects分布异常**：占比 $PROJECTS_RATIO%，建议归档已完成项目或重新评估项目必要性" >> "$REPORT_FILE"
fi

if [ $AREAS_HEALTH -lt 60 ]; then
    echo "- **Areas分布异常**：占比 $AREAS_RATIO%，长期责任关注不足，需要补充生活领域管理" >> "$REPORT_FILE"
fi

if [ $RESOURCES_HEALTH -lt 60 ]; then
    echo "- **Resources分布异常**：占比 $RESOURCES_RATIO%，可能存在资源囤积或缺乏应用转化" >> "$REPORT_FILE"
fi

if [ $ARCHIVES_HEALTH -lt 60 ]; then
    echo "- **Archives分布异常**：占比 $ARCHIVES_RATIO%，归档机制需要优化" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

#### 🟡 需要关注
EOF

# 添加需要关注的项目
if [ $PENDING_COUNT -gt 10 ]; then
    echo "- **待处理数量较多**：$PENDING_COUNT 项待处理，建议安排时间集中处理" >> "$REPORT_FILE"
fi

if [ $OVERALL_HEALTH -lt 80 ]; then
    echo "- **系统健康度一般**：总体健康度 $OVERALL_HEALTH/100，需要优化PARA分布" >> "$REPORT_FILE"
fi

cat >> "$REPORT_FILE" << EOF

#### 🟢 继续保持
EOF

# 添加继续保持的项目
if [ $OVERALL_HEALTH -ge 80 ]; then
    echo "- **系统健康度良好**：总体健康度 $OVERALL_HEALTH/100，继续保持当前使用习惯" >> "$REPORT_FILE"
fi

if [ $OLDEST_PENDING_AGE -le 3 ] && [ $PENDING_COUNT -le 5 ]; then
    echo "- **内容处理及时**：待处理积压控制良好，继续保持高效处理习惯" >> "$REPORT_FILE"
fi

# 添加个性化建议
cat >> "$REPORT_FILE" << EOF

## 🎯 个性化建议

### 基于当前分布的建议
EOF

if [ "${PROJECTS_RATIO%.*}" -gt 25 ]; then
    echo "- **项目管理**：当前项目较多，建议：\n  - 优先完成重要项目\n  - 归档已完成或暂停的项目\n  - 避免同时启动过多新项目" >> "$REPORT_FILE"
elif [ "${PROJECTS_RATIO%.*}" -lt 15 ]; then
    echo "- **项目管理**：当前项目较少，建议：\n  - 评估是否有重要想法需要转化为项目\n  - 从Areas中识别可以项目化的改进点\n  - 设定具体的项目目标和时间表" >> "$REPORT_FILE"
fi

if [ "${AREAS_RATIO%.*}" -gt 35 ]; then
    echo "- **领域管理**：当前领域占比较高，建议：\n  - 检查是否有领域内容可以项目化\n  - 合并或简化部分领域\n  - 重点关注核心领域的维护质量" >> "$REPORT_FILE"
elif [ "${AREAS_RATIO%.*}" -lt 25 ]; then
    echo "- **领域管理**：当前领域覆盖可能不足，建议：\n  - 补充重要的生活领域管理\n  - 建立定期领域回顾机制\n  - 识别长期责任并纳入领域管理" >> "$REPORT_FILE"
fi

if [ "${RESOURCES_RATIO%.*}" -gt 45 ]; then
    echo "- **资源管理**：当前资源较多，建议：\n  - 定期清理低价值资源\n  - 加强资源的应用和转化\n  - 建立资源质量评估标准" >> "$REPORT_FILE"
elif [ "${RESOURCES_RATIO%.*}" -lt 35 ]; then
    echo "- **资源管理**：当前资源储备可能不足，建议：\n  - 主动收集高质量资源\n  - 建立系统的资源获取渠道\n  - 增强资源的整理和关联" >> "$REPORT_FILE"
fi

# 添加改进计划模板
cat >> "$REPORT_FILE" << EOF

## 📋 下月改进计划

### 优先级1：紧急处理
- [ ] 处理积压超过7天的待处理内容
- [ ] 优化PARA分布，调整到理想范围

### 优先级2：系统优化
- [ ] 建立定期回顾机制
- [ ] 完善元数据标准化
- [ ] 加强内容关联和链接

### 优先级3：能力提升
- [ ] 学习高级搜索技巧
- [ ] 掌握自动化工具使用
- [ ] 优化个人工作流程

## 📊 数据导出

### 原始数据
\`\`\`json
{
  "date": "$CURRENT_DATE",
  "para_distribution": {
    "projects": {"count": $PROJECTS_COUNT, "ratio": $PROJECTS_RATIO, "health": $PROJECTS_HEALTH},
    "areas": {"count": $AREAS_COUNT, "ratio": $AREAS_RATIO, "health": $AREAS_HEALTH},
    "resources": {"count": $RESOURCES_COUNT, "ratio": $RESOURCES_RATIO, "health": $RESOURCES_HEALTH},
    "archives": {"count": $ARCHIVES_COUNT, "ratio": $ARCHIVES_RATIO, "health": $ARCHIVES_HEALTH}
  },
  "pending": {
    "count": $PENDING_COUNT,
    "oldest_age_days": $OLDEST_PENDING_AGE
  },
  "overall_health": $OVERALL_HEALTH,
  "total_files": $TOTAL_COUNT
}
\`\`\`

---

**报告生成时间**: $(date)
**下次检查时间**: $(date -d "+7 days" +"%Y-%m-%d")
**工具版本**: metrics-dashboard.sh v1.0
EOF

# 显示关键结果
echo
echo -e "${GREEN}=== 度量报告生成完成 ===${NC}"
echo -e "${GREEN}报告文件: $REPORT_FILE${NC}"
echo
echo -e "${BLUE}关键指标:${NC}"
echo -e "总文件数: $TOTAL_COUNT"
echo -e "系统健康度: $OVERALL_HEALTH/100 $(if [ $OVERALL_HEALTH -ge 80 ]; then echo -e "${GREEN}🟢 优秀${NC}"; elif [ $OVERALL_HEALTH -ge 60 ]; then echo -e "${YELLOW}🟡 良好${NC}"; else echo -e "${RED}🔴 需关注${NC}"; fi)"
echo -e "待处理积压: $PENDING_COUNT 项 (最旧: $OLDEST_PENDING_AGE 天)"
echo
echo -e "${BLUE}PARA分布:${NC}"
echo -e "Projects: $PROJECTS_COUNT ($PROJECTS_RATIO%) $(if [ $PROJECTS_HEALTH -ge 80 ]; then echo -e "${GREEN}🟢${NC}"; elif [ $PROJECTS_HEALTH -ge 60 ]; then echo -e "${YELLOW}🟡${NC}"; else echo -e "${RED}🔴${NC}"; fi)"
echo -e "Areas: $AREAS_COUNT ($AREAS_RATIO%) $(if [ $AREAS_HEALTH -ge 80 ]; then echo -e "${GREEN}🟢${NC}"; elif [ $AREAS_HEALTH -ge 60 ]; then echo -e "${YELLOW}🟡${NC}"; else echo -e "${RED}🔴${NC}"; fi)"
echo -e "Resources: $RESOURCES_COUNT ($RESOURCES_RATIO%) $(if [ $RESOURCES_HEALTH -ge 80 ]; then echo -e "${GREEN}🟢${NC}"; elif [ $RESOURCES_HEALTH -ge 60 ]; then echo -e "${YELLOW}🟡${NC}"; else echo -e "${RED}🔴${NC}"; fi)"
echo -e "Archives: $ARCHIVES_COUNT ($ARCHIVES_RATIO%) $(if [ $ARCHIVES_HEALTH -ge 80 ]; then echo -e "${GREEN}🟢${NC}"; elif [ $ARCHIVES_HEALTH -ge 60 ]; then echo -e "${YELLOW}🟡${NC}"; else echo -e "${RED}🔴${NC}"; fi)"
echo

# 显示建议
if [ $OVERALL_HEALTH -lt 80 ]; then
    echo -e "${YELLOW}💡 建议: 系统健康度有待提升，请查看报告中的详细建议${NC}"
fi

if [ $OLDEST_PENDING_AGE -gt 7 ]; then
    echo -e "${RED}⚠️  警告: 待处理积压严重，建议立即处理${NC}"
fi

echo -e "${BLUE}📊 查看完整报告: $REPORT_FILE${NC}"