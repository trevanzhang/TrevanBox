#!/bin/bash

# TrevanBox AI预处理器主脚本
# 基于uv的现代化Python环境管理

# 设置脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PREHANDLER_PY="$SCRIPT_DIR/ollama/prehandler.py"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_header() {
    echo -e "${PURPLE}=== $1 ===${NC}"
}

# 检查依赖
check_dependencies() {
    print_info "检查系统依赖..."

    # 检查uv是否安装
    if ! command -v uv &> /dev/null; then
        print_error "uv 未安装"
        print_info "请安装uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi

    # 检查虚拟环境
    if [ ! -d "$PROJECT_ROOT/.venv" ]; then
        print_error "虚拟环境不存在: $PROJECT_ROOT/.venv"
        print_info "请在项目根目录运行: uv venv .venv"
        exit 1
    fi

    # 检查预处理器脚本
    if [ ! -f "$PREHANDLER_PY" ]; then
        print_error "预处理器脚本未找到: $PREHANDLER_PY"
        exit 1
    fi

    # 检查并安装Python依赖
    print_info "检查Python依赖..."
    if ! uv run --project "$PROJECT_ROOT" python -c "import requests, yaml, chardet" 2>/dev/null; then
        print_warning "正在安装Python依赖..."
        cd "$PROJECT_ROOT" && uv pip install requests pyyaml chardet
        if [ $? -eq 0 ]; then
            print_success "依赖安装完成"
        else
            print_error "依赖安装失败"
            exit 1
        fi
    fi

    print_success "依赖检查完成"
}

# 检查Ollama服务
check_ollama() {
    print_info "检查Ollama服务..."
    if uv run --project "$PROJECT_ROOT" python -c "
import requests
try:
    response = requests.get('http://localhost:11434/api/tags', timeout=5)
    if response.status_code == 200:
        print('[OK] Ollama服务正常')
        models = response.json().get('models', [])
        if models:
            print(f'[OK] 可用模型: {len(models)}个')
        else:
            print('[WARNING] 未找到可用模型，请确保已下载模型')
    else:
        print('[ERROR] Ollama服务响应异常')
except Exception as e:
    print(f'[ERROR] 无法连接Ollama服务: {e}')
"; then
        return 0
    else
        return 1
    fi
}

# 显示帮助信息
show_help() {
    cat << 'EOF'
TrevanBox AI预处理器 - 基于uv的现代化版本

用法: ./scripts/preprocessor.sh [命令] [选项]

命令:
  status                  检查系统状态（Ollama服务、模型等）
  process <目录>         处理指定目录中的文件
  process all            处理所有导入目录

选项:
  --dry-run              预览模式，不实际修改文件
  --move-to-inbox        处理完成后移动到待处理目录(0-Inbox/pending/)
  --help, -h             显示此帮助信息

支持的导入目录:
  follow     - RSS订阅内容
  clippings  - 浏览器插件摘录
  readwise   - 阅读笔记系统
  zotero     - 学术文献
  webdav     - 云存储同步
  manual     - 手动导入
  ainotes    - AI生成内容

示例:
  ./scripts/preprocessor.sh status
  ./scripts/preprocessor.sh process manual --dry-run
  ./scripts/preprocessor.sh process all --move-to-inbox
  ./scripts/preprocessor.sh process follow clippings --move-to-inbox

工作流程:
  1. AI分析内容，生成标题、标签、描述
  2. 标准化YAML frontmatter元数据
  3. 可选择移动到待处理目录等待人工分类

EOF
}

# 构建uv命令
build_uv_command() {
    local cmd="uv run --project \"$PROJECT_ROOT\" python \"$PREHANDLER_PY\""
    echo "$cmd"
}

# 执行uv命令
execute_uv_command() {
    local cmd="$1"
    cd "$SCRIPT_DIR/ollama" && eval "$cmd"
    return $?
}

# 主函数
main() {
    # 检查项目根目录
    if [ ! -f "$PROJECT_ROOT/CLAUDE.md" ]; then
        print_error "请在TrevanBox项目根目录下运行此脚本"
        exit 1
    fi

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

    # 如果没有指定命令，显示帮助
    if [ -z "$command" ]; then
        show_help
        exit 0
    fi

    # 检查依赖
    check_dependencies

    # 执行命令
    case "$command" in
        status)
            print_header "系统状态检查"
            check_ollama
            ;;
        process)
            if [ ${#directories[@]} -eq 0 ]; then
                print_error "请指定要处理的目录"
                show_help
                exit 1
            fi

            print_header "AI预处理开始"

            # 构建uv命令
            local uv_cmd=$(build_uv_command)
            uv_cmd="$uv_cmd process"

            # 添加目录参数
            for dir in "${directories[@]}"; do
                uv_cmd="$uv_cmd \"$dir\""
            done

            # 添加选项
            if [ "$dry_run" = true ]; then
                uv_cmd="$uv_cmd --dry-run"
                print_info "模式: 预览（不会修改文件）"
            else
                print_info "模式: 实际处理"
            fi

            if [ "$move_to_inbox" = true ]; then
                uv_cmd="$uv_cmd --move-to-inbox"
                print_info "处理后将移动到: 0-Inbox/pending/"
            fi

            echo
            print_info "执行命令: $uv_cmd"
            echo

            # 执行命令
            if execute_uv_command "$uv_cmd"; then
                echo
                print_success "处理完成"
            else
                echo
                print_error "处理失败"
                exit 1
            fi
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