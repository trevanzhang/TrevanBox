#!/bin/bash

# TrevanBox AI预处理器主脚本
# 提供统一的AI预处理功能接口

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PREHANDLER_DIR="$SCRIPT_DIR/ollama"
PREHANDLER_PY="$PREHANDLER_DIR/prehandler.py"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印彩色消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    # 检测Python命令
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_error "Python 未安装"
        exit 1
    fi

    if [ ! -f "$PREHANDLER_PY" ]; then
        print_error "预处理器脚本未找到: $PREHANDLER_PY"
        exit 1
    fi

    # 检查Python依赖
    if ! $PYTHON_CMD -c "import requests, yaml, chardet" 2>/dev/null; then
        print_warning "缺少Python依赖，正在安装..."
        if command -v pip3 &> /dev/null; then
            pip3 install requests pyyaml chardet
        elif command -v pip &> /dev/null; then
            pip install requests pyyaml chardet
        else
            print_error "pip 未安装，无法安装依赖"
            exit 1
        fi
    fi
}

# 显示帮助信息
show_help() {
    cat << EOF
TrevanBox AI预处理器

用法: $0 [命令] [选项]

命令:
  status                  检查系统状态
  process <目录>         处理指定目录
  process all            处理所有导入目录

选项:
  --dry-run              预览模式，不实际修改文件
  --move-to-inbox        处理完成后移动到待处理目录
  --help                 显示此帮助信息

示例:
  $0 status
  $0 process manual --dry-run
  $0 process all --move-to-inbox
  $0 process follow clippings --move-to-inbox

支持的导入目录:
  follow     - RSS订阅内容
  clippings  - 浏览器插件摘录
  readwise   - 阅读笔记系统
  zotero     - 学术文献
  webdav     - 云存储同步
  manual     - 手动导入
  ainotes    - AI生成内容

EOF
}

# 主函数
main() {
    # 检查依赖
    check_dependencies

    # 解析参数
    local command=""
    local directories=()
    local dry_run=false
    local move_to_inbox=false

    while [[ $# -gt 0 ]]; do
        case $1 in
            status|process)
                command="$1"
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --move-to-inbox)
                move_to_inbox=true
                shift
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            -*)
                print_error "未知选项: $1"
                show_help
                exit 1
                ;;
            *)
                directories+=("$1")
                shift
                ;;
        esac
    done

    # 执行命令
    case "$command" in
        status)
            print_info "检查系统状态..."
            cd "$PREHANDLER_DIR" && $PYTHON_CMD "$PREHANDLER_PY" status
            ;;
        process)
            if [ ${#directories[@]} -eq 0 ]; then
                print_error "请指定要处理的目录"
                show_help
                exit 1
            fi

            # 构建Python命令
            local python_cmd="$PYTHON_CMD \"$PREHANDLER_PY\" process"

            # 添加目录参数
            for dir in "${directories[@]}"; do
                python_cmd="$python_cmd \"$dir\""
            done

            # 添加选项
            if [ "$dry_run" = true ]; then
                python_cmd="$python_cmd --dry-run"
            fi

            if [ "$move_to_inbox" = true ]; then
                python_cmd="$python_cmd --move-to-inbox"
            fi

            print_info "开始处理..."
            cd "$PREHANDLER_DIR" && eval "$python_cmd"
            ;;
        "")
            print_error "请指定命令"
            show_help
            exit 1
            ;;
        *)
            print_error "未知命令: $command"
            show_help
            exit 1
            ;;
    esac
}

# 如果直接运行脚本，则执行主函数
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi