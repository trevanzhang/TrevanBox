#!/bin/bash

# Weekly Review Script
# 执行PARA系统的每周回顾流程

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(dirname "$SCRIPT_DIR")"

# 目录定义
INBOX_DIR="$VAULT_ROOT/0-Inbox/pending"
PROJECTS_DIR="$VAULT_ROOT/1-Projects"
AREAS_DIR="$VAULT_ROOT/2-Areas"
RESOURCES_DIR="$VAULT_ROOT/3-Resources"
ARCHIVES_DIR="$VAULT_ROOT/4-Archives"

# 获取当前日期
CURRENT_DATE=$(date +"%Y-%m-%d")
WEEK_START=$(date -d "1 week ago" +"%Y-%m-%d")

echo "=== PARA System Weekly Review ==="
echo "Review Period: $WEEK_START to $CURRENT_DATE"
echo "===================================="
echo ""

# 1. 统计当前系统状态
echo "📊 Current System Status"
echo "------------------------"

function count_files() {
    local dir="$1"
    local name="$2"
    if [ -d "$dir" ]; then
        local count=$(find "$dir" -type f -name "*.md" | wc -l)
        echo "$name: $count files"
    else
        echo "$name: Directory not found"
    fi
}

count_files "$INBOX_DIR" "📥 Pending"
count_files "$PROJECTS_DIR" "🚀 Projects"
count_files "$AREAS_DIR" "🌍 Areas"
count_files "$RESOURCES_DIR" "📚 Resources"
count_files "$ARCHIVES_DIR" "📦 Archives"

echo ""

# 2. 检查待处理文件
echo "📋 Pending Files Review"
echo "-----------------------"

pending_count=$(find "$INBOX_DIR" -type f -name "*.md" | wc -l)
if [ "$pending_count" -gt 0 ]; then
    echo "Found $pending_count pending files that need processing:"
    find "$INBOX_DIR" -type f -name "*.md" -exec basename {} \; | sed 's/^/  - /'
else
    echo "✅ No pending files found"
fi

echo ""

# 3. 活跃项目回顾
echo "🎯 Active Projects Review"
echo "-------------------------"

if [ -d "$PROJECTS_DIR" ]; then
    echo "Current projects:"
    find "$PROJECTS_DIR" -type f -name "*.md" -exec basename {} .md \; | sed 's/^/  - /'
else
    echo "No projects directory found"
fi

echo ""

# 4. 建议行动
echo "💡 Recommended Actions"
echo "----------------------"

if [ "$pending_count" -gt 0 ]; then
    echo "1. Process $pending_count pending files in $INBOX_DIR"
    echo "2. Move processed files to appropriate PARA categories"
else
    echo "1. Review and update active projects"
    echo "2. Archive completed projects"
fi

echo "3. Check for outdated resources in $RESOURCES_DIR"
echo "4. Update area maintenance logs in $AREAS_DIR"

echo ""

# 5. 生成回顾报告
REPORT_FILE="$VAULT_ROOT/weekly-review-$CURRENT_DATE.md"
echo "📝 Generating weekly review report: $REPORT_FILE"

cat > "$REPORT_FILE" << EOF
# Weekly Review Report

**Date**: $CURRENT_DATE
**Review Period**: $WEEK_START to $CURRENT_DATE

## System Statistics
- **Pending Files**: $pending_count
- **Projects**: $(find "$PROJECTS_DIR" -type f -name "*.md" 2>/dev/null | wc -l)
- **Areas**: $(find "$AREAS_DIR" -type f -name "*.md" 2>/dev/null | wc -l)
- **Resources**: $(find "$RESOURCES_DIR" -type f -name "*.md" 2>/dev/null | wc -l)

## Key Observations

## Actions Taken

## Next Week's Priorities

---
*Generated on $CURRENT_DATE*
EOF

echo "✅ Weekly review complete!"
echo "Report saved to: $REPORT_FILE"