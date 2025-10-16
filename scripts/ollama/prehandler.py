#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TrevanBox AI预处理器
基于Ollama qwen3:8b模型的智能内容预处理工具

功能：
- 元数据智能规整和标准化
- AI智能标题生成
- 智能标签识别
- 内容总结生成

支持的导入目录：
- follow/ - RSS订阅内容
- clippings/ - 浏览器插件摘录
- readwise/ - 阅读笔记系统
- zotero/ - 学术文献
- webdav/ - 云存储同步
- manual/ - 手动导入
- ainotes/ - AI生成内容
"""

import os
import sys
import json
import yaml
import requests
import argparse
import chardet
import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 默认配置
DEFAULT_CONFIG = {
    "ollama": {
        "base_url": "http://localhost:11434",
        "model": "qwen3:8b",
        "timeout": 30,
        "retry": 3
    },
    "metadata": {
        "default_status": "sprout",
        "default_type": "note",
        "standard_fields": ["created", "updated", "status", "type", "tags", "area", "title", "description"]
    },
    "processing": {
        "max_file_size": 10 * 1024 * 1024,  # 10MB
        "encoding_detection": True,
        "backup_enabled": True,
        "move_to_inbox": False  # 处理完成后是否移动到待处理目录
    },
    "ai": {
        "title_max_length": 15,
        "tags_max_count": 7,
        "summary_length": 200
    }
}

# 目录映射配置
DIRECTORY_MAPPING = {
    "follow": {"tag": "follow", "type": "article"},
    "clippings": {"tag": "clippings", "type": "excerpt"},
    "readwise": {"tag": "readwise", "type": "reading"},
    "zotero": {"tag": "zotero", "type": "reference"},
    "webdav": {"tag": "webdav", "type": "sync"},
    "manual": {"tag": "manual", "type": "note"},
    "ainotes": {"tag": "ainotes", "type": "ai"}
}


class TrevanPrehandler:
    """TrevanBox AI预处理器"""

    def __init__(self, config: Dict = None):
        self.config = config or DEFAULT_CONFIG
        self.ollama_url = self.config["ollama"]["base_url"]
        self.model = self.config["ollama"]["model"]
        self.timeout = self.config["ollama"]["timeout"]

    def check_ollama_status(self) -> bool:
        """检查Ollama服务状态"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def call_ollama(self, prompt: str, system_prompt: str = None) -> str:
        """调用Ollama模型"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        if system_prompt:
            payload["system"] = system_prompt

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "").strip()
        except Exception as e:
            print(f"Ollama调用失败: {e}")
            return ""

    def detect_encoding(self, file_path: str) -> str:
        """检测文件编码"""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
                result = chardet.detect(raw_data)
                encoding = result.get('encoding', 'utf-8')
                # 处理常见的中文编码
                if encoding.lower() in ['gb2312', 'gbk']:
                    return 'gb18030'
                return encoding or 'utf-8'
        except:
            return 'utf-8'

    def read_file_content(self, file_path: str) -> Tuple[str, Dict]:
        """读取文件内容和元数据"""
        encoding = self.detect_encoding(file_path)

        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
        except UnicodeDecodeError:
            # 尝试其他编码
            for enc in ['utf-8', 'gb18030', 'latin-1']:
                try:
                    with open(file_path, 'r', encoding=enc) as f:
                        content = f.read()
                        break
                except:
                    continue
            else:
                raise ValueError(f"无法解码文件: {file_path}")

        # 解析YAML frontmatter
        metadata = {}
        body_content = content

        if content.startswith('---'):
            try:
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    metadata_str = parts[1].strip()
                    body_content = parts[2].strip()
                    metadata = yaml.safe_load(metadata_str) or {}
            except:
                pass

        return body_content, metadata

    def write_file_content(self, file_path: str, metadata: Dict, content: str) -> bool:
        """写入文件内容"""
        # 创建备份
        if self.config["processing"]["backup_enabled"]:
            backup_path = file_path + '.bak'
            try:
                import shutil
                shutil.copy2(file_path, backup_path)
            except:
                pass

        try:
            # 构建新的内容
            if metadata:
                yaml_content = yaml.dump(metadata, allow_unicode=True, default_flow_style=False, sort_keys=False)
                new_content = f"---\n{yaml_content}---\n\n{content}"
            else:
                new_content = content

            # 原子写入
            temp_path = file_path + '.tmp'
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            # 替换原文件
            import shutil
            shutil.move(temp_path, file_path)

            # 清理备份
            if self.config["processing"]["backup_enabled"]:
                try:
                    os.remove(backup_path)
                except:
                    pass

            return True
        except Exception as e:
            print(f"写入文件失败: {e}")
            # 恢复备份
            if self.config["processing"]["backup_enabled"]:
                try:
                    import shutil
                    shutil.move(backup_path, file_path)
                except:
                    pass
            return False

    def move_file_to_inbox(self, file_path: str) -> str:
        """移动文件到待处理目录"""
        try:
            # 获取项目根目录
            script_dir = os.path.dirname(os.path.abspath(__file__))
            vault_root = os.path.dirname(os.path.dirname(script_dir))
            inbox_dir = os.path.join(vault_root, "0-Inbox", "pending")

            # 确保目标目录存在
            os.makedirs(inbox_dir, exist_ok=True)

            # 获取文件名
            filename = os.path.basename(file_path)
            target_file = os.path.join(inbox_dir, filename)

            # 检查目标文件是否已存在
            if os.path.exists(target_file):
                # 添加时间戳避免冲突
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                name, extension = os.path.splitext(filename)
                target_file = os.path.join(inbox_dir, f"{name}_{timestamp}{extension}")

            # 移动文件
            import shutil
            shutil.move(file_path, target_file)

            print(f"  [MOVE] {filename} → {target_file}")
            return target_file

        except Exception as e:
            print(f"移动文件失败: {e}")
            return file_path  # 返回原路径表示移动失败

    def clean_metadata(self, metadata: Dict, source_dir: str) -> Dict:
        """清理和标准化元数据"""
        # 定义标准字段顺序
        standard_order = ["created", "updated", "title", "author", "status", "type", "tags", "description", "source"]
        optional_fields = ["url", "area"]
        cleaned = {}

        # 设置时间戳
        current_time = datetime.datetime.now().isoformat()
        cleaned["created"] = metadata.get("created", current_time)
        cleaned["updated"] = current_time

        # 处理标题
        cleaned["title"] = metadata.get("title", "")

        # 处理来源信息
        cleaned["source"] = metadata.get("source", "")
        cleaned["author"] = metadata.get("author", "")

        # 处理状态和类型
        if "status" not in metadata:
            cleaned["status"] = self.config["metadata"]["default_status"]
        else:
            # 验证状态值
            valid_statuses = ["sprout", "evergreen", "discharged"]
            if metadata["status"] in valid_statuses:
                cleaned["status"] = metadata["status"]
            else:
                cleaned["status"] = self.config["metadata"]["default_status"]

        if "type" not in metadata:
            # 根据来源目录设置默认类型
            dir_name = os.path.basename(source_dir.rstrip('/'))
            if dir_name in DIRECTORY_MAPPING:
                cleaned["type"] = DIRECTORY_MAPPING[dir_name]["type"]
            else:
                cleaned["type"] = self.config["metadata"]["default_type"]
        else:
            # 验证类型值
            valid_types = ["project", "area", "resource", "journal", "note", "article", "excerpt", "reading", "reference", "sync", "ai"]
            if metadata["type"] in valid_types:
                cleaned["type"] = metadata["type"]
            else:
                dir_name = os.path.basename(source_dir.rstrip('/'))
                if dir_name in DIRECTORY_MAPPING:
                    cleaned["type"] = DIRECTORY_MAPPING[dir_name]["type"]
                else:
                    cleaned["type"] = self.config["metadata"]["default_type"]

        # 处理标签
        if "tags" not in metadata:
            cleaned["tags"] = []
        elif isinstance(metadata["tags"], str):
            cleaned["tags"] = [metadata["tags"]]
        elif metadata["tags"] is None:
            cleaned["tags"] = []
        else:
            cleaned["tags"] = metadata["tags"]

        # 添加来源标签
        dir_name = os.path.basename(source_dir.rstrip('/'))
        if dir_name in DIRECTORY_MAPPING:
            source_tag = DIRECTORY_MAPPING[dir_name]["tag"]
            if source_tag not in cleaned["tags"]:
                cleaned["tags"].insert(0, source_tag)

        # 处理描述
        cleaned["description"] = metadata.get("description", "")

        # 保留可选字段
        for field in optional_fields:
            if field in metadata and metadata[field]:
                cleaned[field] = metadata[field]

        # 按标准顺序重新组织
        ordered_metadata = {}
        for field in standard_order:
            if field in cleaned:
                ordered_metadata[field] = cleaned[field]

        # 添加其他字段
        for field in cleaned:
            if field not in standard_order:
                ordered_metadata[field] = cleaned[field]

        return ordered_metadata

    def generate_all_ai_content(self, content: str, current_title: str = "", existing_tags: List[str] = []) -> Tuple[str, List[str], str]:
        """一次性生成标题、标签和描述"""
        # 如果已有合适标题，直接使用
        if current_title and len(current_title) <= self.config["ai"]["title_max_length"]:
            # 只生成标签和描述
            prompt = f"""请分析以下内容并返回结构化结果：

内容：
{content[:2000]}

请按以下格式返回结果：
标签：[3-7个中文标签，每个标签不超过4个字，用逗号分隔]
描述：[100-200字中文总结，突出核心观点]

要求：
- 标签要相关且具体，每个标签不超过4个字
- 英文标签全部小写，避免重复
- 描述要结构化，包含核心观点和关键信息

请严格按格式返回，不要添加其他说明。"""
        else:
            # 生成所有内容
            prompt = f"""请分析以下内容并返回结构化结果：

内容：
{content[:2000]}

请按以下格式返回结果：
标题：[8-15字中文标题]
标签：[3-7个中文标签，每个标签不超过4个字，用逗号分隔]
描述：[100-200字中文总结，突出核心观点]

要求：
- 标题简洁准确，反映内容主题
- 标签要相关且具体，每个标签不超过4个字
- 英文标签全部小写，避免重复
- 描述要结构化，包含核心观点和关键信息

请严格按格式返回，不要添加其他说明。"""

        response = self.call_ollama(prompt)
        if not response:
            # 调用失败，返回默认值
            default_title = current_title if current_title else "未命名文档"
            return default_title, existing_tags, ""

        # 解析结构化响应
        title, tags, description = self._parse_ai_response(response, current_title)

        # 验证和清理标签
        validated_tags = self._validate_and_clean_tags(tags, existing_tags)

        return title, validated_tags, description

    def _parse_ai_response(self, response: str, current_title: str = "") -> Tuple[str, List[str], str]:
        """解析AI返回的结构化结果"""
        title = current_title
        tags = []
        description = ""

        # 提取标题 - 支持两种格式：有方括号和没有方括号
        title_match = re.search(r'标题：\s*(?:\[([^\]]+)\]|([^\n]+))', response)
        if title_match:
            title = (title_match.group(1) or title_match.group(2)).strip()

        # 提取标签 - 支持两种格式
        tags_match = re.search(r'标签：\s*(?:\[([^\]]+)\]|([^\n]+))', response)
        if tags_match:
            tags_str = (tags_match.group(1) or tags_match.group(2)).strip()
            tags = [tag.strip() for tag in tags_str.split(',') if tag.strip()]

        # 提取描述 - 支持两种格式
        desc_match = re.search(r'描述：\s*(?:\[([^\]]+)\]|([^\n]+))', response)
        if desc_match:
            description = (desc_match.group(1) or desc_match.group(2)).strip()

        return title, tags, description

    def _validate_and_clean_tags(self, tags: List[str], existing_tags: List[str]) -> List[str]:
        """验证和清理标签"""
        cleaned_tags = []
        seen_tags = set()

        # 合并现有标签
        all_tags = existing_tags + tags

        for tag in all_tags:
            # 清理标签
            clean_tag = tag.strip()

            # 处理英文标签：全部小写
            if clean_tag.isascii():
                clean_tag = clean_tag.lower()

            # 去重
            if clean_tag and clean_tag not in seen_tags:
                cleaned_tags.append(clean_tag)
                seen_tags.add(clean_tag)

        # 限制标签数量（但保留目录标签）
        max_tags = self.config["ai"]["tags_max_count"]
        if len(cleaned_tags) <= max_tags:
            return cleaned_tags

        # 如果超过限制，优先保留目录标签和AI标签
        directory_tags = [tag for tag in cleaned_tags if tag in [mapping["tag"] for mapping in DIRECTORY_MAPPING.values()]]
        ai_tags = [tag for tag in cleaned_tags if tag not in directory_tags]

        # 保留所有目录标签，然后添加AI标签直到达到限制
        result = directory_tags + ai_tags[:max_tags - len(directory_tags)]
        return result

    def process_file(self, file_path: str, source_dir: str, dry_run: bool = False, move_to_inbox: bool = False) -> Dict:
        """处理单个文件"""
        result = {
            "file": file_path,
            "success": False,
            "changes": {},
            "error": None
        }

        try:
            # 读取文件
            content, metadata = self.read_file_content(file_path)

            # 清理元数据
            new_metadata = self.clean_metadata(metadata, source_dir)

            # 使用统一AI处理函数
            current_title = metadata.get("title", "")
            current_tags = new_metadata.get("tags", [])

            new_title, new_tags, description = self.generate_all_ai_content(
                content, current_title, current_tags
            )

            new_metadata["title"] = new_title
            # 合并AI标签和现有标签（包含目录标签），确保目录标签保留
            # 保留目录标签，合并AI标签
            existing_tags_with_directory = new_metadata.get("tags", [])
            merged_tags = self._validate_and_clean_tags(new_tags, existing_tags_with_directory)
            new_metadata["tags"] = merged_tags
            new_metadata["description"] = description

            # 检测变化
            changes = {}
            if metadata != new_metadata:
                changes["metadata"] = {
                    "old": metadata,
                    "new": new_metadata
                }

            if description:
                changes["description"] = description

            result["changes"] = changes

            # 写入文件（如果不是预览模式）
            if not dry_run and changes:
                if self.write_file_content(file_path, new_metadata, content):
                    result["success"] = True

                    # 如果启用了移动到待处理目录且处理成功
                    if move_to_inbox and result["success"]:
                        new_file_path = self.move_file_to_inbox(file_path)
                        if new_file_path != file_path:  # 移动成功
                            result["file"] = new_file_path
                            result["moved"] = True
                        else:
                            result["moved"] = False
                else:
                    result["error"] = "文件写入失败"
            else:
                result["success"] = True  # 预览模式也视为成功

        except Exception as e:
            result["error"] = str(e)

        return result

    def process_directory(self, directory: str, dry_run: bool = False, move_to_inbox: bool = False) -> List[Dict]:
        """处理目录中的所有markdown文件"""
        results = []

        if not os.path.exists(directory):
            print(f"目录不存在: {directory}")
            return results

        md_files = list(Path(directory).glob("**/*.md"))

        for md_file in md_files:
            print(f"处理文件: {md_file}")
            result = self.process_file(str(md_file), directory, dry_run, move_to_inbox)
            results.append(result)

            if result["success"]:
                if dry_run:
                    print(f"  [OK] 预览完成")
                else:
                    if result.get("moved"):
                        print(f"  [OK] 处理完成并移动到待处理目录")
                    else:
                        print(f"  [OK] 处理完成")
            else:
                print(f"  [ERROR] 失败: {result['error']}")

        return results


def main():
    parser = argparse.ArgumentParser(description="TrevanBox AI预处理器")
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # status命令
    status_parser = subparsers.add_parser('status', help='检查系统状态')

    # process命令
    process_parser = subparsers.add_parser('process', help='处理导入目录')
    process_parser.add_argument('directories', nargs='+', help='要处理的目录')
    process_parser.add_argument('--dry-run', action='store_true', help='预览模式')
    process_parser.add_argument('--move-to-inbox', action='store_true', help='处理完成后移动到待处理目录')

    # title命令
    title_parser = subparsers.add_parser('title', help='生成标题')
    title_parser.add_argument('directories', nargs='+', help='要处理的目录')

    # tags命令
    tags_parser = subparsers.add_parser('tags', help='生成标签')
    tags_parser.add_argument('directories', nargs='+', help='要处理的目录')

    # summary命令
    summary_parser = subparsers.add_parser('summary', help='生成总结')
    summary_parser.add_argument('directories', nargs='+', help='要处理的目录')

    args = parser.parse_args()

    prehandler = TrevanPrehandler()

    if args.command == 'status':
        print("检查系统状态...")
        if prehandler.check_ollama_status():
            print("[OK] Ollama服务正常")
            print(f"[OK] 使用模型: {prehandler.model}")
        else:
            print("[ERROR] Ollama服务不可用")
            print("请确保Ollama服务正在运行: ollama serve")

    elif args.command == 'process':
        directories = []
        for dir_arg in args.directories:
            if dir_arg == 'all':
                directories.extend(DIRECTORY_MAPPING.keys())
            else:
                directories.append(dir_arg)

        for directory in directories:
            if directory in DIRECTORY_MAPPING:
                dir_path = os.path.join('..', '..', directory)
            else:
                dir_path = directory

            print(f"\n处理目录: {dir_path}")
            if args.move_to_inbox:
                print("  [MOVE] 处理完成后将移动到待处理目录")
            results = prehandler.process_directory(dir_path, args.dry_run, args.move_to_inbox)

            success_count = sum(1 for r in results if r["success"])
            moved_count = sum(1 for r in results if r.get("moved"))
            print(f"完成: {success_count}/{len(results)} 个文件")
            if moved_count > 0:
                print(f"移动: {moved_count}/{success_count} 个文件到待处理目录")

    elif args.command in ['title', 'tags', 'summary']:
        print(f"{args.command}功能正在开发中...")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()