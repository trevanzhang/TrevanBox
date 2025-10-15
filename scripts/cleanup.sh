#!/bin/bash

# PARA System Cleanup Script
# 用于清理导入目录中的文件并移动到待处理目录

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(dirname "$SCRIPT_DIR")"

# 导入目录列表
IMPORT_DIRS=("follow" "clippings" "readwise" "zotero")
INBOX_DIR="$VAULT_ROOT/0-Inbox/pending"

# 确保目标目录存在
mkdir -p "$INBOX_DIR"

echo "=== PARA System Cleanup ==="
echo "Vault Root: $VAULT_ROOT"
echo "Target Directory: $INBOX_DIR"
echo ""

# 统计移动的文件
total_moved=0

# 遍历每个导入目录
for dir in "${IMPORT_DIRS[@]}"; do
    import_dir="$VAULT_ROOT/$dir"

    if [ -d "$import_dir" ] && [ "$(ls -A "$import_dir" 2>/dev/null)" ]; then
        echo "Processing $dir directory..."

        # 移动所有文件到待处理目录
        file_count=$(find "$import_dir" -type f -name "*.md" | wc -l)

        if [ "$file_count" -gt 0 ]; then
            find "$import_dir" -type f -name "*.md" -exec mv {} "$INBOX_DIR/" \;
            echo "  Moved $file_count files from $dir to pending"
            total_moved=$((total_moved + file_count))
        else
            echo "  No markdown files found in $dir"
        fi

    else
        echo "Directory $dir not found or empty"
    fi
done

echo ""
echo "=== Cleanup Complete ==="
echo "Total files moved: $total_moved"
echo "Files are now in: $INBOX_DIR"

# 显示待处理目录中的文件数量
pending_count=$(find "$INBOX_DIR" -type f -name "*.md" | wc -l)
echo "Pending files count: $pending_count"