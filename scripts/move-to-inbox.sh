#!/bin/bash

# Move to Inbox Script
# 移动指定文件到待处理目录

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(dirname "$SCRIPT_DIR")"
INBOX_DIR="$VAULT_ROOT/0-Inbox/pending"

# 确保目标目录存在
mkdir -p "$INBOX_DIR"

# 函数：移动单个文件
move_file() {
    local source_file="$1"
    local target_dir="$2"

    if [ ! -f "$source_file" ]; then
        echo "Error: Source file '$source_file' not found"
        return 1
    fi

    # 获取文件名
    local filename=$(basename "$source_file")
    local target_file="$target_dir/$filename"

    # 检查目标文件是否已存在
    if [ -f "$target_file" ]; then
        # 添加时间戳避免冲突
        local timestamp=$(date +"%Y%m%d_%H%M%S")
        local name="${filename%.*}"
        local extension="${filename##*.}"
        target_file="$target_dir/${name}_${timestamp}.${extension}"
    fi

    # 移动文件
    mv "$source_file" "$target_file"
    echo "Moved: $filename → $target_file"
}

# 函数：移动目录中的所有文件
move_directory() {
    local source_dir="$1"
    local file_count=0

    if [ ! -d "$source_dir" ]; then
        echo "Error: Directory '$source_dir' not found"
        return 1
    fi

    # 查找并移动所有markdown文件
    find "$source_dir" -type f -name "*.md" | while read -r file; do
        move_file "$file" "$INBOX_DIR"
        file_count=$((file_count + 1))
    done
}

# 主函数
echo "=== Move to Inbox Script ==="
echo "Target: $INBOX_DIR"
echo ""

# 根据参数执行不同操作
if [ $# -eq 0 ]; then
    echo "Usage: $0 [file_path|directory_path]"
    echo "  file_path     - Move a specific file"
    echo "  directory_path - Move all markdown files from directory"
    echo ""
    echo "Examples:"
    echo "  $0 follow/article.md"
    echo "  $0 clippings/"
    exit 1
fi

TARGET="$1"

if [ -f "$TARGET" ]; then
    echo "Moving single file: $TARGET"
    move_file "$TARGET" "$INBOX_DIR"
elif [ -d "$TARGET" ]; then
    echo "Moving directory: $TARGET"
    move_directory "$TARGET"
else
    echo "Error: '$TARGET' is not a valid file or directory"
    exit 1
fi

echo ""
echo "=== Move Complete ==="

# 显示待处理目录中的文件数量
pending_count=$(find "$INBOX_DIR" -type f -name "*.md" | wc -l)
echo "Pending files count: $pending_count"