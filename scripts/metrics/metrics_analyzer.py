#!/usr/bin/env python3
"""
TrevanBox 高级度量分析工具
提供深度的系统健康度分析和趋势追踪功能
"""

import os
import json
import re
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import argparse

@dataclass
class SystemMetrics:
    """系统度量数据结构"""
    date: str
    total_files: int
    para_distribution: Dict[str, Dict[str, float]]
    pending_items: int
    oldest_pending_age: int
    overall_health: float
    content_quality: Dict[str, float]
    efficiency_metrics: Dict[str, float]
    growth_metrics: Dict[str, float]

class TrevanBoxMetricsAnalyzer:
    """TrevanBox 度量分析器"""

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.reports_dir = self.base_path / "docs" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.history_file = self.reports_dir / "metrics_history.json"

        # PARA目录配置
        self.para_config = {
            "1-Projects": {"ideal_range": (15, 25), "weight": 0.3},
            "2-Areas": {"ideal_range": (25, 35), "weight": 0.25},
            "3-Resources": {"ideal_range": (35, 45), "weight": 0.25},
            "4-Archives": {"ideal_range": (5, 15), "weight": 0.2}
        }

    def analyze_system(self) -> SystemMetrics:
        """分析系统状态，返回度量数据"""
        print("🔍 开始分析系统状态...")

        # 基础统计
        para_stats = self._analyze_para_distribution()
        pending_stats = self._analyze_pending_items()

        # 内容质量分析
        content_quality = self._analyze_content_quality()

        # 效率指标分析
        efficiency_metrics = self._analyze_efficiency()

        # 成长指标分析
        growth_metrics = self._analyze_growth()

        # 计算总体健康度
        overall_health = self._calculate_overall_health(para_stats, content_quality, efficiency_metrics)

        metrics = SystemMetrics(
            date=datetime.datetime.now().isoformat(),
            total_files=sum(stats["count"] for stats in para_stats.values()),
            para_distribution=para_stats,
            pending_items=pending_stats["count"],
            oldest_pending_age=pending_stats["oldest_age"],
            overall_health=overall_health,
            content_quality=content_quality,
            efficiency_metrics=efficiency_metrics,
            growth_metrics=growth_metrics
        )

        print(f"✅ 分析完成，总体健康度: {overall_health:.1f}/100")
        return metrics

    def _analyze_para_distribution(self) -> Dict[str, Dict[str, float]]:
        """分析PARA分布"""
        print("📁 分析PARA分布...")

        distribution = {}
        total_files = 0

        # 统计各类别文件数量
        for category in self.para_config.keys():
            count = self._count_markdown_files(category)
            size = self._get_directory_size(category)

            distribution[category] = {
                "count": count,
                "size_mb": size,
                "ratio": 0.0,  # 稍后计算
                "health": 0.0   # 稍后计算
            }
            total_files += count

        # 计算比例和健康度
        for category, stats in distribution.items():
            if total_files > 0:
                stats["ratio"] = (stats["count"] / total_files) * 100

            ideal_min, ideal_max = self.para_config[category]["ideal_range"]
            stats["health"] = self._calculate_range_score(stats["ratio"], ideal_min, ideal_max)

        return distribution

    def _analyze_pending_items(self) -> Dict[str, int]:
        """分析待处理项目"""
        print("⏳ 分析待处理项目...")

        pending_dir = self.base_path / "0-Inbox" / "pending"
        if not pending_dir.exists():
            return {"count": 0, "oldest_age": 0}

        pending_files = list(pending_dir.glob("**/*.md"))
        count = len(pending_files)

        if count == 0:
            return {"count": 0, "oldest_age": 0}

        # 计算最旧文件年龄
        current_time = datetime.datetime.now().timestamp()
        oldest_timestamp = min(f.stat().st_mtime for f in pending_files)
        oldest_age = int((current_time - oldest_timestamp) / 86400)  # 转换为天

        return {"count": count, "oldest_age": oldest_age}

    def _analyze_content_quality(self) -> Dict[str, float]:
        """分析内容质量"""
        print("📝 分析内容质量...")

        total_files = 0
        files_with_metadata = 0
        files_with_links = 0
        total_links = 0
        recently_updated = 0

        # 统计所有markdown文件
        for md_file in self.base_path.glob("**/*.md"):
            if "0-Inbox" in str(md_file):
                continue  # 跳过待处理文件

            total_files += 1

            # 检查是否有标准化元数据
            content = md_file.read_text(encoding='utf-8', errors='ignore')
            if self._has_frontmatter(content):
                files_with_metadata += 1

            # 统计链接数量
            links = re.findall(r'\[\[([^\]]+)\]\]', content)
            if links:
                files_with_links += 1
                total_links += len(links)

            # 检查最近更新（30天内）
            file_age_days = (datetime.datetime.now().timestamp() - md_file.stat().st_mtime) / 86400
            if file_age_days <= 30:
                recently_updated += 1

        # 计算质量指标
        return {
            "metadata_coverage": (files_with_metadata / total_files * 100) if total_files > 0 else 0,
            "linked_files_ratio": (files_with_links / total_files * 100) if total_files > 0 else 0,
            "avg_links_per_file": (total_links / total_files) if total_files > 0 else 0,
            "content_activity": (recently_updated / total_files * 100) if total_files > 0 else 0,
            "overall_quality": 0  # 稍后计算
        }

    def _analyze_efficiency(self) -> Dict[str, float]:
        """分析效率指标"""
        print("⚡ 分析效率指标...")

        # 这里可以根据实际情况添加更多效率指标
        # 目前提供基础的结构，用户可以根据需要扩展

        return {
            "processing_efficiency": 75.0,  # 示例值，需要实际测量
            "search_efficiency": 80.0,      # 示例值，需要实际测量
            "decision_speed": 70.0,         # 示例值，需要实际测量
            "overall_efficiency": 75.0      # 稍后计算
        }

    def _analyze_growth(self) -> Dict[str, float]:
        """分析成长指标"""
        print("🌱 分析成长指标...")

        # 从历史数据中计算增长趋势
        history = self._load_history()
        if len(history) < 2:
            return {
                "content_growth_rate": 0.0,
                "skill_development": 0.0,
                "goal_achievement": 0.0,
                "overall_growth": 0.0
            }

        latest = history[-1]
        previous = history[-2]

        # 计算内容增长率
        content_growth = ((latest["total_files"] - previous["total_files"]) /
                         previous["total_files"] * 100) if previous["total_files"] > 0 else 0

        return {
            "content_growth_rate": content_growth,
            "skill_development": 0.0,  # 需要用户手动输入或从其他数据源获取
            "goal_achievement": 0.0,   # 需要用户手动输入或从其他数据源获取
            "overall_growth": 0.0      # 稍后计算
        }

    def _calculate_overall_health(self, para_stats: Dict, content_quality: Dict,
                                efficiency_metrics: Dict) -> float:
        """计算总体健康度"""

        # PARA分布健康度（权重40%）
        para_health = sum(stats["health"] * self.para_config[category]["weight"]
                         for category, stats in para_stats.items())

        # 内容质量健康度（权重30%）
        quality_health = content_quality["overall_quality"]

        # 效率指标健康度（权重30%）
        efficiency_health = efficiency_metrics["overall_efficiency"]

        overall = (para_health * 0.4 + quality_health * 0.3 + efficiency_health * 0.3)
        return round(overall, 1)

    def _calculate_range_score(self, value: float, min_val: float, max_val: float) -> float:
        """计算数值在理想范围内的得分"""
        if min_val <= value <= max_val:
            return 100.0
        elif value < min_val:
            return max(0.0, 100.0 - (min_val - value) * 2)
        else:
            return max(0.0, 100.0 - (value - max_val) * 2)

    def _count_markdown_files(self, directory: str) -> int:
        """统计指定目录中的markdown文件数量"""
        dir_path = self.base_path / directory
        if not dir_path.exists():
            return 0
        return len(list(dir_path.glob("**/*.md")))

    def _get_directory_size(self, directory: str) -> float:
        """获取目录大小（MB）"""
        dir_path = self.base_path / directory
        if not dir_path.exists():
            return 0.0

        total_size = 0
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size

        return round(total_size / (1024 * 1024), 2)  # 转换为MB

    def _has_frontmatter(self, content: str) -> bool:
        """检查文件是否有frontmatter"""
        return bool(re.match(r'^---\n.*?\n---', content, re.DOTALL))

    def _load_history(self) -> List[Dict]:
        """加载历史数据"""
        if not self.history_file.exists():
            return []

        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _save_history(self, metrics: SystemMetrics):
        """保存历史数据"""
        history = self._load_history()

        # 转换为可序列化的格式
        metrics_dict = asdict(metrics)
        history.append(metrics_dict)

        # 保留最近12个月的数据
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=365)
        history = [m for m in history if datetime.datetime.fromisoformat(m["date"]) > cutoff_date]

        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def generate_report(self, metrics: SystemMetrics) -> str:
        """生成详细报告"""
        report_date = datetime.datetime.now().strftime("%Y-%m-%d")
        report_file = self.reports_dir / f"detailed-metrics-{report_date}.md"

        # 计算各项质量指标的总体得分
        metrics.content_quality["overall_quality"] = (
            metrics.content_quality["metadata_coverage"] * 0.3 +
            metrics.content_quality["linked_files_ratio"] * 0.3 +
            metrics.content_quality["avg_links_per_file"] * 5 +  # 平均链接数*5作为得分
            metrics.content_quality["content_activity"] * 0.4
        )
        metrics.content_quality["overall_quality"] = min(100, metrics.content_quality["overall_quality"])

        metrics.efficiency_metrics["overall_efficiency"] = (
            metrics.efficiency_metrics["processing_efficiency"] * 0.4 +
            metrics.efficiency_metrics["search_efficiency"] * 0.3 +
            metrics.efficiency_metrics["decision_speed"] * 0.3
        )

        metrics.growth_metrics["overall_growth"] = (
            min(100, max(0, metrics.growth_metrics["content_growth_rate"])) * 0.4 +
            metrics.growth_metrics["skill_development"] * 0.3 +
            metrics.growth_metrics["goal_achievement"] * 0.3
        )

        report_content = f"""# TrevanBox 详细度量分析报告

**生成时间**: {report_date}
**分析器版本**: v2.0
**系统路径**: {self.base_path}

## 📊 系统概览

| 核心指标 | 数值 | 状态 |
|---------|------|------|
| 总文件数 | {metrics.total_files} | - |
| 系统健康度 | {metrics.overall_health}/100 | {self._get_health_emoji(metrics.overall_health)} |
| 待处理积压 | {metrics.pending_items} 项 | {self._get_pending_emoji(metrics.pending_items, metrics.oldest_pending_age)} |
| 最旧积压年龄 | {metrics.oldest_pending_age} 天 | {self._get_age_emoji(metrics.oldest_pending_age)} |

## 📁 PARA分布详细分析

### 分布概况
{self._generate_para_table(metrics.para_distribution)}

### 健康度分析
{self._generate_health_analysis(metrics.para_distribution)}

## 📝 内容质量分析

| 质量指标 | 数值 | 理想范围 | 状态 |
|----------|------|----------|------|
| 元数据覆盖率 | {metrics.content_quality['metadata_coverage']:.1f}% | >90% | {self._get_quality_emoji(metrics.content_quality['metadata_coverage'], 90)} |
| 链接文件比例 | {metrics.content_quality['linked_files_ratio']:.1f}% | >80% | {self._get_quality_emoji(metrics.content_quality['linked_files_ratio'], 80)} |
| 平均链接数/文件 | {metrics.content_quality['avg_links_per_file']:.1f} | >3 | {self._get_quality_emoji(metrics.content_quality['avg_links_per_file'] * 20, 60)} |
| 内容活跃度 | {metrics.content_quality['content_activity']:.1f}% | >40% | {self._get_quality_emoji(metrics.content_quality['content_activity'], 40)} |
| **总体质量** | **{metrics.content_quality['overall_quality']:.1f}/100** | **>80** | **{self._get_health_emoji(metrics.content_quality['overall_quality'])}** |

## ⚡ 效率指标分析

| 效率指标 | 数值/100 | 状态 | 建议 |
|----------|----------|------|------|
| 处理效率 | {metrics.efficiency_metrics['processing_efficiency']:.1f} | {self._get_health_emoji(metrics.efficiency_metrics['processing_efficiency'])} | {self._get_efficiency_advice('processing', metrics.efficiency_metrics['processing_efficiency'])} |
| 搜索效率 | {metrics.efficiency_metrics['search_efficiency']:.1f} | {self._get_health_emoji(metrics.efficiency_metrics['search_efficiency'])} | {self._get_efficiency_advice('search', metrics.efficiency_metrics['search_efficiency'])} |
| 决策速度 | {metrics.efficiency_metrics['decision_speed']:.1f} | {self._get_health_emoji(metrics.efficiency_metrics['decision_speed'])} | {self._get_efficiency_advice('decision', metrics.efficiency_metrics['decision_speed'])} |
| **总体效率** | **{metrics.efficiency_metrics['overall_efficiency']:.1f}** | **{self._get_health_emoji(metrics.efficiency_metrics['overall_efficiency'])}** | **综合优化各项效率指标** |

## 🌱 成长指标分析

| 成长指标 | 数值 | 趋势 | 说明 |
|----------|------|------|------|
| 内容增长率 | {metrics.growth_metrics['content_growth_rate']:.1f}% | {self._get_trend_emoji(metrics.growth_metrics['content_growth_rate'])} | 相对上期的内容增长 |
| 技能发展 | {metrics.growth_metrics['skill_development']:.1f}/100 | {self._get_health_emoji(metrics.growth_metrics['skill_development'])} | 个人技能提升情况 |
| 目标达成 | {metrics.growth_metrics['goal_achievement']:.1f}/100 | {self._get_health_emoji(metrics.growth_metrics['goal_achievement'])} | 目标完成情况 |
| **总体成长** | **{metrics.growth_metrics['overall_growth']:.1f}/100** | **{self._get_health_emoji(metrics.growth_metrics['overall_growth'])}** | **综合成长评估** |

## 🎯 个性化建议

### 立即行动（本周内）
{self._generate_immediate_actions(metrics)}

### 短期改进（本月内）
{self._generate_short_term_improvements(metrics)}

### 长期优化（本季度）
{self._generate_long_term_optimizations(metrics)}

## 📈 历史趋势

> *需要积累更多历史数据才能生成趋势图表*

## 📋 数据导出

### 完整数据（JSON格式）
```json
{json.dumps(asdict(metrics), indent=2, ensure_ascii=False)}
```

---

**报告生成器**: TrevanBox Metrics Analyzer v2.0
**下次分析时间**: {(datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')}
**配置文件**: {self.base_path / "scripts" / "metrics_config.json"}
"""

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        return str(report_file)

    def _get_health_emoji(self, score: float) -> str:
        """根据分数返回健康度emoji"""
        if score >= 80:
            return "🟢 优秀"
        elif score >= 60:
            return "🟡 良好"
        else:
            return "🔴 需关注"

    def _get_pending_emoji(self, count: int, age: int) -> str:
        """根据积压情况返回emoji"""
        if count <= 5 and age <= 3:
            return "🟢 正常"
        elif count <= 15 and age <= 7:
            return "🟡 需处理"
        else:
            return "🔴 积压严重"

    def _get_age_emoji(self, age: int) -> str:
        """根据年龄返回emoji"""
        if age <= 3:
            return "🟢 正常"
        elif age <= 7:
            return "🟡 需关注"
        else:
            return "🔴 严重积压"

    def _get_quality_emoji(self, value: float, threshold: float) -> str:
        """根据质量指标返回emoji"""
        if value >= threshold:
            return "🟢"
        elif value >= threshold * 0.8:
            return "🟡"
        else:
            return "🔴"

    def _get_trend_emoji(self, growth_rate: float) -> str:
        """根据增长率返回趋势emoji"""
        if growth_rate > 5:
            return "📈 快速增长"
        elif growth_rate > 0:
            return "📊 稳步增长"
        elif growth_rate > -5:
            return "➡️ 基本稳定"
        else:
            return "📉 需要关注"

    def _get_efficiency_advice(self, metric_type: str, score: float) -> str:
        """获取效率建议"""
        advice_map = {
            'processing': {
                (80, 100): "保持当前处理流程",
                (60, 80): "优化AI预处理配置",
                (0, 60): "重新设计处理流程"
            },
            'search': {
                (80, 100): "搜索效率优秀",
                (60, 80): "改进标签和链接系统",
                (0, 60): "学习高级搜索技巧"
            },
            'decision': {
                (80, 100): "决策效率很高",
                (60, 80): "加强决策框架使用",
                (0, 60): "建立标准化决策流程"
            }
        }

        for range_tuple, advice in advice_map[metric_type].items():
            if range_tuple[0] <= score <= range_tuple[1]:
                return advice
        return "需要深度优化"

    def _generate_para_table(self, para_stats: Dict) -> str:
        """生成PARA分布表格"""
        table = "| 类别 | 文件数 | 占比 | 大小(MB) | 健康度 | 状态 |\n"
        table += "|------|--------|------|----------|--------|------|\n"

        for category, stats in para_stats.items():
            category_name = category.split('-')[1]  # 去掉前缀数字
            status_emoji = self._get_health_emoji(stats["health"])
            table += f"| {category_name} | {stats['count']} | {stats['ratio']:.1f}% | {stats['size_mb']:.1f} | {stats['health']:.1f}/100 | {status_emoji} |\n"

        return table

    def _generate_health_analysis(self, para_stats: Dict) -> str:
        """生成健康度分析"""
        analysis = []

        for category, stats in para_stats.items():
            category_name = category.split('-')[1]
            health = stats["health"]
            ratio = stats["ratio"]

            if health < 60:
                analysis.append(f"- **{category_name}分布异常**：占比{ratio:.1f}%，健康度{health:.1f}/100，需要重点优化")
            elif health < 80:
                analysis.append(f"- **{category_name}分布一般**：占比{ratio:.1f}%，建议适当调整")
            else:
                analysis.append(f"- **{category_name}分布良好**：占比{ratio:.1f}%，继续保持")

        return "\n".join(analysis)

    def _generate_immediate_actions(self, metrics: SystemMetrics) -> str:
        """生成立即行动建议"""
        actions = []

        if metrics.oldest_pending_age > 7:
            actions.append(f"- 处理积压超过{metrics.oldest_pending_age}天的待处理内容")

        if metrics.pending_items > 15:
            actions.append(f"- 清理{metrics.pending_items}项待处理内容")

        if metrics.overall_health < 60:
            actions.append("- 重点提升系统健康度")

        if metrics.content_quality['metadata_coverage'] < 80:
            actions.append("- 补充缺失的元数据")

        return "\n".join(actions) if actions else "- 系统状态良好，继续保持当前使用习惯"

    def _generate_short_term_improvements(self, metrics: SystemMetrics) -> str:
        """生成短期改进建议"""
        improvements = []

        # PARA分布优化
        for category, stats in metrics.para_distribution.items():
            if stats["health"] < 80:
                category_name = category.split('-')[1]
                improvements.append(f"- 优化{category_name}分布，当前占比{stats['ratio']:.1f}%")

        # 内容质量提升
        if metrics.content_quality['linked_files_ratio'] < 80:
            improvements.append("- 增加内容间的链接和关联")

        if metrics.content_quality['avg_links_per_file'] < 3:
            improvements.append("- 提升平均链接密度")

        return "\n".join(improvements) if improvements else "- 各项指标良好，继续精细化使用"

    def _generate_long_term_optimizations(self, metrics: SystemMetrics) -> str:
        """生成长期优化建议"""
        optimizations = []

        optimizations.append("- 建立定期回顾和优化机制")
        optimizations.append("- 深度应用PARA方法论到更多生活场景")
        optimizations.append("- 探索AI工具的深度集成")
        optimizations.append("- 建立个人知识图谱")

        return "\n".join(optimizations)

    def run_analysis(self, save_history: bool = True, generate_report: bool = True) -> str:
        """运行完整分析流程"""
        print("🚀 开始TrevanBox系统度量分析...")

        # 分析系统
        metrics = self.analyze_system()

        # 保存历史数据
        if save_history:
            self._save_history(metrics)
            print("💾 历史数据已保存")

        # 生成报告
        report_path = ""
        if generate_report:
            report_path = self.generate_report(metrics)
            print(f"📊 详细报告已生成: {report_path}")

        # 显示关键结果
        print("\n" + "="*50)
        print("📋 分析结果摘要")
        print("="*50)
        print(f"总体健康度: {metrics.overall_health}/100 {self._get_health_emoji(metrics.overall_health)}")
        print(f"文件总数: {metrics.total_files}")
        print(f"待处理积压: {metrics.pending_items} 项 (最旧: {metrics.oldest_pending_age} 天)")
        print(f"内容质量: {metrics.content_quality['overall_quality']:.1f}/100")
        print(f"使用效率: {metrics.efficiency_metrics['overall_efficiency']:.1f}/100")

        return report_path

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="TrevanBox 高级度量分析工具")
    parser.add_argument("--base-path", default=".", help="TrevanBox系统根目录路径")
    parser.add_argument("--no-save", action="store_true", help="不保存历史数据")
    parser.add_argument("--no-report", action="store_true", help="不生成详细报告")
    parser.add_argument("--quiet", action="store_true", help="静默模式，只输出结果")

    args = parser.parse_args()

    try:
        analyzer = TrevanBoxMetricsAnalyzer(args.base_path)
        report_path = analyzer.run_analysis(
            save_history=not args.no_save,
            generate_report=not args.no_report
        )

        if not args.quiet and report_path:
            print(f"\n📄 查看详细报告: {report_path}")

    except Exception as e:
        print(f"❌ 分析过程中出现错误: {e}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())