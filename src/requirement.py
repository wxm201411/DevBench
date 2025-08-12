#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
需求分析评估器
根据测试集完善版.md中的需求分析评估标准评估AI生成的需求文档
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple


class RequirementAnalyzer:
    """需求分析评估器类"""

    def __init__(self, requirement_file_path: str):
        """
        初始化评估器

        Args:
            requirement_file_path: 需求文档文件路径
        """
        self.requirement_file_path = requirement_file_path
        self.requirement_content = ""

        # 功能点关键词列表（带权重）
        self.function_keywords = {
            # 核心功能（权重2）
            "用户注册": 2,
            "登录": 2,
            "书籍搜索": 2,
            "发布图书": 2,
            "自提": 2,
            "自付款": 2,
            # 重要功能（权重1.5）
            "分类浏览": 1.5,
            "订单管理": 1.5,
            "图书详情": 1.5,
            "个人中心": 1.5,
        }

        # 技术栈关键词
        self.tech_keywords = ["arco.design", "vue", "fastapi", "sqlmodel", "mysql"]

        # 需求结构部分
        self.structure_sections = [
            "技术约束",
            "功能需求",
            "非功能需求",
            "用户故事",
            "验收标准",
        ]

        # 可量化需求模式
        self.quantifiable_patterns = [
            r"\d+\s*个",  # 数字+个
            r"\d+\s*分钟",  # 数字+分钟
            r"\d+\s*小时",  # 数字+小时
            r"\d+\s*天",  # 数字+天
            r"\d+\s*%",  # 数字+%
            r"\d+\s*次",  # 数字+次
            r"\d+\s*条",  # 数字+条
            r"至少\s*\d+",  # 至少+数字
            r"最多\s*\d+",  # 最多+数字
            r"不超过\s*\d+",  # 不超过+数字
            r"响应时间\s*[<≤]\s*\d+",  # 响应时间<数字
            r"支持\s*\d+\s*[个]?用户",  # 支持数字用户
            r"\d+\s*秒",  # 数字+秒
            r"端口\s*\d+",  # 端口号
            r"版本\s*\d+",  # 版本号
            r"\d+\.\d+\.\d+",  # 版本号格式
        ]

    def load_requirement_file(self) -> bool:
        """
        加载需求文档文件

        Returns:
            bool: 是否成功加载文件
        """
        try:
            if not os.path.exists(self.requirement_file_path):
                print(f"错误：需求文档文件不存在: {self.requirement_file_path}")
                return False

            with open(self.requirement_file_path, "r", encoding="utf-8") as file:
                self.requirement_content = file.read()

            print(f"成功加载需求文档: {self.requirement_file_path}")
            return True

        except Exception as e:
            print(f"加载需求文档时发生错误: {e}")
            return False

    def evaluate_function_coverage(self) -> Dict[str, any]:
        """
        评估功能点覆盖率

        Returns:
            Dict: 包含功能点覆盖率评估结果，包括总分、最大分、匹配的关键字、未匹配的关键字、详细信息和加权详细信息
        """
        result = {
            "total_score": 0,
            "max_score": 20,
            "matched_keywords": [],
            "unmatched_keywords": [],
            "details": [],
        }
        content_lower = self.requirement_content.lower()
        total_weight = sum(self.function_keywords.values())

        for keyword, weight in self.function_keywords.items():
            if keyword.lower() in content_lower:
                result["matched_keywords"].append(keyword)
                score = (weight / total_weight) * result["max_score"]
                result["total_score"] += score
                result["details"].append(
                    f"✓ 找到关键词: {keyword} (权重: {weight}, 得分: {score:.1f})"
                )
            else:
                result["unmatched_keywords"].append(keyword)
                result["details"].append(f"✗ 未找到关键词: {keyword} (权重: {weight})")

        result["total_score"] = round(result["total_score"], 1)
        return result

    def evaluate_structure_completeness(self) -> Dict[str, any]:
        """
        评估需求完整性

        Returns:
            Dict: 包含需求完整性评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 20,
            "found_sections": [],
            "missing_sections": [],
            "details": [],
            "quality_scores": {},
        }

        content_lower = self.requirement_content.lower()

        # 结构部分及其评估标准
        structure_criteria = {
            "技术约束": {
                "keywords": ["前端", "后端", "数据库", "技术栈"],
                "min_content_length": 50,
                "weight": 3,
            },
            "功能需求": {
                "keywords": ["功能", "模块", "用户", "系统"],
                "min_content_length": 200,
                "weight": 5,
            },
            "非功能需求": {
                "keywords": ["性能", "安全", "可用性", "响应时间"],
                "min_content_length": 100,
                "weight": 4,
            },
            "用户故事": {
                "keywords": ["作为", "我希望", "以便", "用户"],
                "min_content_length": 150,
                "weight": 4,
            },
            "验收标准": {
                "keywords": ["验收", "标准", "测试", "条件"],
                "min_content_length": 100,
                "weight": 4,
            },
        }

        for section, criteria in structure_criteria.items():
            section_found = section.lower() in content_lower
            quality_score = 0

            if section_found:
                result["found_sections"].append(section)
                quality_score += 2  # 基础分：存在该部分

                # 检查关键词密度
                keyword_count = sum(
                    1 for kw in criteria["keywords"] if kw.lower() in content_lower
                )
                if keyword_count >= 2:
                    quality_score += 1  # 关键词充足

                # 检查内容长度（简单估算）
                section_pattern = rf"{section}.*?(?=##|\Z)"
                section_match = re.search(
                    section_pattern, self.requirement_content, re.DOTALL | re.IGNORECASE
                )
                if (
                    section_match
                    and len(section_match.group()) >= criteria["min_content_length"]
                ):
                    quality_score += 1  # 内容充实

                final_score = (quality_score / 4) * criteria["weight"]
                result["total_score"] += final_score
                result["quality_scores"][section] = quality_score
                result["details"].append(
                    f"✓ 找到结构部分: {section} (质量分: {quality_score}/4, 得分: {final_score:.1f})"
                )
            else:
                result["missing_sections"].append(section)
                result["details"].append(
                    f"✗ 未找到结构部分: {section} (权重: {criteria['weight']})"
                )

        result["total_score"] = round(result["total_score"], 1)
        return result

    def evaluate_description_clarity(self) -> Dict[str, any]:
        """
        评估描述清晰度

        Returns:
            Dict: 包含描述清晰度评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 15,
            "quantifiable_count": 0,
            "found_quantifiables": [],
            "details": [],
            "category_scores": {},
        }

        # 按类别分组的可量化模式
        quantifiable_categories = {
            "时间指标": [r"\d+\s*分钟", r"\d+\s*小时", r"\d+\s*天", r"\d+\s*秒"],
            "数量指标": [
                r"\d+\s*个",
                r"\d+\s*次",
                r"\d+\s*条",
                r"至少\s*\d+",
                r"最多\s*\d+",
                r"不超过\s*\d+",
            ],
            "性能指标": [
                r"\d+\s*%",
                r"响应时间\s*[<≤]\s*\d+",
                r"支持\s*\d+\s*[个]?用户",
            ],
            "技术指标": [r"端口\s*\d+", r"版本\s*\d+", r"\d+\.\d+\.\d+"],
        }

        for category, patterns in quantifiable_categories.items():
            category_count = 0
            for pattern in patterns:
                matches = re.findall(pattern, self.requirement_content)
                if matches:
                    category_count += len(matches)
                    result["found_quantifiables"].extend(matches)

            result["category_scores"][category] = category_count
            result["quantifiable_count"] += category_count

            if category_count > 0:
                result["details"].append(
                    f"✓ {category}: 找到 {category_count} 个量化指标"
                )
            else:
                result["details"].append(f"✗ {category}: 未找到量化指标")

        # 计算得分：每个类别最多3分，总共12分，额外3分给总体表现
        for category, count in result["category_scores"].items():
            category_score = min(count, 3)  # 每个类别最多3分
            result["total_score"] += category_score

        # 总体表现奖励分
        if result["quantifiable_count"] >= 10:
            result["total_score"] += 3
        elif result["quantifiable_count"] >= 5:
            result["total_score"] += 2
        elif result["quantifiable_count"] >= 2:
            result["total_score"] += 1

        return result

    def evaluate_tech_requirements(self) -> Dict[str, any]:
        """
        评估技术要求覆盖率

        Returns:
            Dict: 包含技术要求评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 10,
            "matched_keywords": [],
            "unmatched_keywords": [],
            "details": [],
            "context_scores": {},
        }

        # 技术栈及其上下文关键词
        tech_requirements = {
            "arco.design": ["前端", "UI", "组件库", "界面"],
            "vue": ["前端", "框架", "javascript", "js"],
            "fastapi": ["后端", "API", "接口", "服务"],
            "sqlmodel": ["数据库", "ORM", "模型", "数据"],
            "mysql": ["数据库", "存储", "数据", "连接"],
        }

        content_lower = self.requirement_content.lower()

        for tech, context_keywords in tech_requirements.items():
            tech_found = tech.lower() in content_lower
            context_score = 0

            if tech_found:
                result["matched_keywords"].append(tech)
                base_score = 1.5  # 基础分

                # 检查上下文关键词
                context_count = sum(
                    1 for kw in context_keywords if kw.lower() in content_lower
                )
                context_score = min(context_count * 0.125, 0.5)  # 上下文最多0.5分

                total_score = base_score + context_score
                result["total_score"] += total_score
                result["context_scores"][tech] = context_score
                result["details"].append(
                    f"✓ 找到技术栈: {tech} (基础分: 1.5, 上下文分: {context_score:.2f})"
                )
            else:
                result["unmatched_keywords"].append(tech)
                result["details"].append(f"✗ 未找到技术栈: {tech}")

        result["total_score"] = round(result["total_score"], 1)
        return result

    def evaluate_ears_compliance(self) -> Dict[str, any]:
        """评估EARS规范遵循度"""
        result = {
            "total_score": 0,
            "max_score": 10,
            "ears_patterns_found": [],
            "details": [],
        }

        # EARS模式
        ears_patterns = {
            "普通需求": r"系统应当|系统必须|系统需要",
            "事件驱动": r"当.*时，系统应当|如果.*，则系统",
            "状态驱动": r"在.*状态下，系统应当|处于.*时",
            "可选特性": r"在.*情况下，系统应当|如果.*可用",
            "复杂需求": r"在.*条件下，当.*时，系统应当",
        }

        for pattern_name, pattern in ears_patterns.items():
            matches = re.findall(pattern, self.requirement_content, re.IGNORECASE)
            if matches:
                result["ears_patterns_found"].extend(matches)
                result["total_score"] += 2
                result["details"].append(f"✓ 找到{pattern_name}模式: {len(matches)}个")
            else:
                result["details"].append(f"✗ 未找到{pattern_name}模式")

        return result

    def generate_evaluation_report(self) -> Dict[str, any]:
        """
        生成完整的评估报告

        Returns:
            Dict: 完整的评估报告
        """
        if not self.load_requirement_file():
            return {"error": "无法加载需求文档文件"}

        # 执行各项评估
        function_coverage = self.evaluate_function_coverage()
        structure_completeness = self.evaluate_structure_completeness()
        description_clarity = self.evaluate_description_clarity()
        tech_requirements = self.evaluate_tech_requirements()
        ears_compliance = self.evaluate_ears_compliance()

        # 计算总分
        total_score = (
            function_coverage["total_score"]
            + structure_completeness["total_score"]
            + description_clarity["total_score"]
            + tech_requirements["total_score"]
            + ears_compliance["total_score"]
        )
        max_total_score = (
            function_coverage["max_score"]
            + structure_completeness["max_score"]
            + description_clarity["max_score"]
            + tech_requirements["max_score"]
            + ears_compliance["max_score"]
        )

        # 生成报告
        report = {
            "evaluation_summary": {
                "total_score": round(total_score, 1),
                "max_total_score": max_total_score,
                "percentage": round((total_score / max_total_score) * 100, 2),
                "evaluation_date": datetime.now().strftime("%Y-%m-%d"),
                "grade": self._calculate_grade(total_score / max_total_score),
            },
            "function_coverage": function_coverage,
            "structure_completeness": structure_completeness,
            "description_clarity": description_clarity,
            "tech_requirements": tech_requirements,
            "ears_compliance": ears_compliance,
            "recommendations": self._generate_recommendations(
                function_coverage,
                structure_completeness,
                description_clarity,
                tech_requirements,
                ears_compliance,
            ),
        }

        return report

    def _calculate_grade(self, percentage: float) -> str:
        """计算等级"""
        if percentage >= 0.9:
            return "优秀 (A)"
        elif percentage >= 0.8:
            return "良好 (B)"
        elif percentage >= 0.7:
            return "中等 (C)"
        elif percentage >= 0.6:
            return "及格 (D)"
        else:
            return "不及格 (F)"

    def _generate_recommendations(
        self,
        function_coverage: Dict,
        structure_completeness: Dict,
        description_clarity: Dict,
        tech_requirements: Dict,
        ears_compliance: Dict,
    ) -> List[str]:
        """
        生成改进建议

        Args:
            function_coverage: 功能点覆盖率结果
            structure_completeness: 需求完整性结果
            description_clarity: 描述清晰度结果
            tech_requirements: 技术要求评估结果
            ears_compliance: EARS规范遵循度结果

        Returns:
            List[str]: 改进建议列表
        """
        recommendations = []

        # 功能点覆盖率建议
        if function_coverage["unmatched_keywords"]:
            high_weight_missing = [
                kw
                for kw in function_coverage["unmatched_keywords"]
                if self.function_keywords.get(kw, 1) >= 1.5
            ]
            if high_weight_missing:
                recommendations.append(
                    f"建议优先添加以下重要功能点: {', '.join(high_weight_missing)}"
                )

            low_weight_missing = [
                kw
                for kw in function_coverage["unmatched_keywords"]
                if self.function_keywords.get(kw, 1) < 1.5
            ]
            if low_weight_missing:
                recommendations.append(
                    f"建议添加以下辅助功能点: {', '.join(low_weight_missing)}"
                )

        # 需求完整性建议
        if structure_completeness["missing_sections"]:
            recommendations.append(
                f"建议在文档中添加以下结构部分: {', '.join(structure_completeness['missing_sections'])}"
            )

        # 描述清晰度建议
        missing_categories = [
            cat
            for cat, count in description_clarity["category_scores"].items()
            if count == 0
        ]
        if missing_categories:
            recommendations.append(
                f"建议添加以下类型的量化指标: {', '.join(missing_categories)}"
            )

        # 技术要求建议
        if tech_requirements["unmatched_keywords"]:
            recommendations.append(
                f"建议在文档中明确指定使用以下技术栈: {', '.join(tech_requirements['unmatched_keywords'])}"
            )

        # EARS规范建议
        if ears_compliance["total_score"] < 6:
            recommendations.append(
                "建议使用更多EARS规范的需求描述模式，如'系统应当'、'当...时，系统应当'等"
            )

        if not recommendations:
            recommendations.append("需求文档质量良好，无需特别改进")

        return recommendations

    def save_report_to_file(self, report: Dict, output_file: str) -> bool:
        """
        保存评估报告到文件

        Args:
            report: 评估报告
            output_file: 输出文件路径

        Returns:
            bool: 是否成功保存
        """
        try:
            # 生成Markdown格式的报告
            markdown_report = self._generate_markdown_report(report)

            with open(output_file, "w", encoding="utf-8") as file:
                file.write(markdown_report)

            print(f"评估报告已保存到: {output_file}")
            return True

        except Exception as e:
            print(f"保存评估报告时发生错误: {e}")
            return False

    def _generate_markdown_report(self, report: Dict) -> str:
        """
        生成Markdown格式的评估报告
        """
        summary = report["evaluation_summary"]

        markdown = f"""# 需求分析评估报告

## 评估概览
- **评估日期**: {summary['evaluation_date']}
- **总分**: {summary['total_score']}/{summary['max_total_score']}
- **得分率**: {summary['percentage']}%

## 1. 功能点覆盖率 ({report['function_coverage']['total_score']}/{report['function_coverage']['max_score']}分)

### 评估标准
检测文档中是否包含校园二手图书交易相关功能点，采用加权评分
核心功能权重2，重要功能权重1.5，辅助功能权重1

### 评估结果
- **已匹配关键词**: {', '.join(report['function_coverage']['matched_keywords']) if report['function_coverage']['matched_keywords'] else '无'}
- **未匹配关键词**: {', '.join(report['function_coverage']['unmatched_keywords']) if report['function_coverage']['unmatched_keywords'] else '无'}

### 详细结果
"""

        for detail in report["function_coverage"]["details"]:
            markdown += f"- {detail}\n"

        markdown += f"""
## 2. 需求完整性 ({report['structure_completeness']['total_score']}/{report['structure_completeness']['max_score']}分)

### 评估标准
检测文档结构完整性和内容质量，包括关键词密度和内容长度
各部分权重：功能需求(5分)、非功能需求(4分)、用户故事(4分)、验收标准(4分)、技术约束(3分)

### 评估结果
- **已找到结构**: {', '.join(report['structure_completeness']['found_sections']) if report['structure_completeness']['found_sections'] else '无'}
- **缺失结构**: {', '.join(report['structure_completeness']['missing_sections']) if report['structure_completeness']['missing_sections'] else '无'}

### 详细结果
"""

        for detail in report["structure_completeness"]["details"]:
            markdown += f"- {detail}\n"

        markdown += f"""
## 3. 描述清晰度 ({report['description_clarity']['total_score']}/{report['description_clarity']['max_score']}分)

### 评估标准
按类别评估量化指标：时间指标、数量指标、性能指标、技术指标
每个类别最多3分，总体表现奖励最多3分

### 评估结果
- **总量化需求数量**: {report['description_clarity']['quantifiable_count']}
- **各类别得分**: {', '.join([f"{k}: {v}" for k, v in report['description_clarity']['category_scores'].items()])}

### 详细结果
"""

        for detail in report["description_clarity"]["details"]:
            markdown += f"- {detail}\n"

        markdown += f"""
## 4. 技术要求 ({report['tech_requirements']['total_score']}/{report['tech_requirements']['max_score']}分)

### 评估标准
检测指定技术栈及其上下文关键词
基础分1.5分，上下文关键词最多加0.5分

### 评估结果
- **已匹配技术栈**: {', '.join(report['tech_requirements']['matched_keywords']) if report['tech_requirements']['matched_keywords'] else '无'}
- **未匹配技术栈**: {', '.join(report['tech_requirements']['unmatched_keywords']) if report['tech_requirements']['unmatched_keywords'] else '无'}

### 详细结果
"""

        for detail in report["tech_requirements"]["details"]:
            markdown += f"- {detail}\n"

        markdown += f"""
## 5. EARS规范遵循度 ({report['ears_compliance']['total_score']}/{report['ears_compliance']['max_score']}分)

### 评估标准
检测EARS规范的需求描述模式
每种模式匹配得2分，最高10分

### 评估结果
- **找到的EARS模式数量**: {len(report['ears_compliance']['ears_patterns_found'])}

### 详细结果
"""

        for detail in report["ears_compliance"]["details"]:
            markdown += f"- {detail}\n"

        markdown += """
## 改进建议

"""

        for i, recommendation in enumerate(report["recommendations"], 1):
            markdown += f"{i}. {recommendation}\n"

        return markdown


def batch_evaluate():
    """
    批量评估output目录下的所有需求文档
    """
    import glob
    
    # 获取output目录下所有需求文档
    output_dir = "output"
    pattern = os.path.join(output_dir, "需求说明_*.md")
    requirement_files = glob.glob(pattern)
    
    if not requirement_files:
        print("错误：在output目录下未找到任何需求文档")
        return
    
    print("=== 需求分析评估器（批量评估模式）===")
    print(f"找到 {len(requirement_files)} 个需求文档进行评估")
    print()
    
    # 存储所有评估结果
    results = []
    
    # 逐个评估需求文档
    for requirement_file in requirement_files:
        print(f"正在评估: {os.path.basename(requirement_file)}")
        
        # 创建评估器实例
        analyzer = RequirementAnalyzer(requirement_file)
        
        # 生成评估报告
        report = analyzer.generate_evaluation_report()
        
        if "error" in report:
            print(f"评估失败: {report['error']}")
            continue
        
        # 提取评估结果
        summary = report["evaluation_summary"]
        filename = os.path.basename(requirement_file).replace("需求说明_", "").replace(".md", "")
        results.append({
            "filename": filename,
            "total_score": summary['total_score'],
            "max_total_score": summary['max_total_score'],
            "percentage": summary['percentage'],
            "grade": summary['grade']
        })
        
        print(f"评估完成: {summary['total_score']}/{summary['max_total_score']} ({summary['percentage']}%) [{summary['grade']}]")
    
    # 按总分从大到小排序
    results.sort(key=lambda x: x['total_score'], reverse=True)
    
    # 以表格形式展示结果
    print()
    print("=" * 80)
    print("评估结果汇总")
    print("=" * 80)
    print(f"{'需求文档':<20} {'总分':<10} {'得分率':<10}")
    print("-" * 80)
    
    total_scores = 0
    max_scores = 0
    
    for result in results:
        print(f"{result['filename']:<20} {result['total_score']:<10} {result['percentage']:<10}")
        total_scores += result['total_score']
        max_scores += result['max_total_score']
    
    # 计算平均分
    if results:
        avg_percentage = (total_scores / max_scores) * 100
        print("-" * 80)
        print(f"{'平均分':<20} {total_scores/len(results):<10.1f} {avg_percentage:<10.2f} {'':<10}")
    
    print("=" * 80)


def main():
    """
    主函数：执行需求分析评估
    """
    import sys

    # 如果提供了命令行参数，则使用单文件评估模式
    if len(sys.argv) > 1:
        requirement_file = sys.argv[1]
        
        if len(sys.argv) > 2:
            output_report_file = sys.argv[2]
        else:
            output_report_file = "output/需求分析评估报告.md"

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_report_file), exist_ok=True)

        print("=== 需求分析评估器 ===")
        print(f"需求文档路径: {requirement_file}")
        print(f"评估报告输出路径: {output_report_file}")
        print()

        # 检查需求文件是否存在
        if not os.path.exists(requirement_file):
            print(f"错误：需求文档文件不存在: {requirement_file}")
            print("请确保需求文档已生成，或使用命令行参数指定需求文档路径")
            print("使用方法: python requirement.py [需求文档路径] [输出报告路径]")
            return

        # 创建评估器实例
        analyzer = RequirementAnalyzer(requirement_file)

        # 生成评估报告
        report = analyzer.generate_evaluation_report()

        if "error" in report:
            print(f"评估失败: {report['error']}")
            return

        # 显示评估结果
        summary = report["evaluation_summary"]
        print(f"评估完成!")
        print(f"总分: {summary['total_score']}/{summary['max_total_score']}")
        print(f"得分率: {summary['percentage']}%")
        print(f"等级: {summary['grade']}")
        print()

        # 保存评估报告
        if analyzer.save_report_to_file(report, output_report_file):
            print("评估报告已成功保存!")
        else:
            print("保存评估报告失败!")
    else:
        # 批量评估模式
        batch_evaluate()


if __name__ == "__main__":
    main()
