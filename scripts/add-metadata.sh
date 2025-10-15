#!/bin/bash

# Add Metadata Script
# 为导入的笔记添加标准化元数据

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(dirname "$SCRIPT_DIR")"
PENDING_DIR="$VAULT_ROOT/0-Inbox/pending"

# 获取当前时间戳
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# 函数：为文件添加元数据
add_metadata_to_file() {
    local file="$1"
    local filename=$(basename "$file" .md)

    # 检测来源
    local source_tag=""
    if [[ "$file" == *"follow"* ]]; then
        source_tag="follow"
    elif [[ "$file" == *"clippings"* ]]; then
        source_tag="clippings"
    elif [[ "$file" == *"readwise"* ]]; then
        source_tag="readwise"
    elif [[ "$file" == *"zotero"* ]]; then
        source_tag="zotero"
    fi

    # 读取文件内容
    local content=$(cat "$file")

    # 检查是否已有YAML frontmatter
    if [[ "$content" =~ ^---[[:space:]]*$ ]]; then
        echo "File $filename already has frontmatter, skipping..."
        return 0
    fi

    # 生成新的frontmatter
    local frontmatter="---
created: $TIMESTAMP
updated: $TIMESTAMP
status: sprout
type: note
tags: [$source_tag, 待处理]
author: \"\"
source: \"$filename\"
url: \"\"
published:
---

"

    # 写入新内容
    echo "$frontmatter$content" > "$file"
    echo "Added metadata to: $filename"
}

# 主函数
echo "=== Adding Metadata to Pending Files ==="
echo "Processing files in: $PENDING_DIR"
echo ""

# 计数器
processed_count=0

# 遍历待处理目录中的所有markdown文件
find "$PENDING_DIR" -type f -name "*.md" | while read -r file; do
    add_metadata_to_file "$file"
    processed_count=$((processed_count + 1))
done

echo ""
echo "=== Metadata Addition Complete ==="
echo "Processed files: $processed_count"