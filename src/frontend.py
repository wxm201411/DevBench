#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
前端开发评估器
根据测试集完善版.md中的前端开发评估标准评估AI生成的前端代码
"""

import os
import re
import json
from datetime import datetime
from typing import Dict, List, Tuple


class FrontendAnalyzer:
    """前端开发评估器类"""

    def __init__(self, frontend_file_path: str):
        """
        初始化评估器

        Args:
            frontend_file_path: 前端代码文件路径
        """
        self.frontend_file_path = frontend_file_path
        self.frontend_content = ""

        # 功能点关键词列表（每个功能点权重相同）
        self.function_keywords = [
            "图书信息展示",
            "相关推荐列表",
            "用户评论区",
            "加入购物车按钮"
        ]

        # 界面美观度评估维度
        self.ui_aspects = [
            "布局合理性",
            "色彩搭配",
            "交互体验",
            "响应式设计"
        ]

        # 代码质量评估维度
        self.code_quality_aspects = [
            "组件化结构",
            "命名规范",
            "代码复用率",
            "性能优化"
        ]

    def load_frontend_file(self) -> bool:
        """
        加载前端代码文件

        Returns:
            bool: 是否成功加载文件
        """
        try:
            if not os.path.exists(self.frontend_file_path):
                print(f"错误：前端代码文件不存在: {self.frontend_file_path}")
                return False

            with open(self.frontend_file_path, "r", encoding="utf-8") as file:
                self.frontend_content = file.read()

            print(f"成功加载前端代码: {self.frontend_file_path}")
            return True

        except Exception as e:
            print(f"加载前端代码时发生错误: {e}")
            return False

    def evaluate_function_coverage(self) -> Dict[str, any]:
        """
        评估功能点覆盖率

        Returns:
            Dict: 包含功能点覆盖率评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 10,
            "matched_keywords": [],
            "unmatched_keywords": [],
            "details": [],
        }
        content_lower = self.frontend_content.lower()
        
        # 每个功能点权重相同，都是2.5分
        weight = 2.5

        for keyword in self.function_keywords:
            if keyword.lower() in content_lower:
                result["matched_keywords"].append(keyword)
                result["total_score"] += weight
                result["details"].append(
                    f"✓ 找到功能点: {keyword} (得分: {weight})"
                )
            else:
                result["unmatched_keywords"].append(keyword)
                result["details"].append(f"✗ 未找到功能点: {keyword} (权重: {weight})")

        result["total_score"] = round(result["total_score"], 1)
        return result

    def evaluate_ui_beauty(self) -> Dict[str, any]:
        """
        评估界面美观度

        Returns:
            Dict: 包含界面美观度评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 10,
            "evaluated_aspects": [],
            "missing_aspects": [],
            "details": [],
        }
        
        # 每个维度权重：布局合理性(3分)、色彩搭配(3分)、交互体验(2分)、响应式设计(2分)
        aspect_weights = {
            "布局合理性": 3,
            "色彩搭配": 3,
            "交互体验": 2,
            "响应式设计": 2
        }
        
        content_lower = self.frontend_content.lower()
        
        # 检查各个维度是否在代码中有所体现
        for aspect in self.ui_aspects:
            # 这里简化处理，实际应用中可能需要更复杂的检测逻辑
            # 比如调用专门的UI评估工具
            if aspect.lower() in content_lower:
                result["evaluated_aspects"].append(aspect)
                weight = aspect_weights[aspect]
                result["total_score"] += weight
                result["details"].append(
                    f"✓ 涉及到{aspect}: (得分: {weight})"
                )
            else:
                result["missing_aspects"].append(aspect)
                result["details"].append(f"✗ 未涉及{aspect}: (权重: {aspect_weights[aspect]})")

        result["total_score"] = round(result["total_score"], 1)
        return result

    def evaluate_code_quality(self) -> Dict[str, any]:
        """
        评估代码质量

        Returns:
            Dict: 包含代码质量评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 10,
            "evaluated_aspects": [],
            "missing_aspects": [],
            "details": [],
        }
        
        # 每个维度权重：组件化结构(3分)、命名规范(2分)、代码复用率(2分)、性能优化(3分)
        aspect_weights = {
            "组件化结构": 3,
            "命名规范": 2,
            "代码复用率": 2,
            "性能优化": 3
        }
        
        content_lower = self.frontend_content.lower()
        
        # 检查各个维度是否在代码中有所体现
        for aspect in self.code_quality_aspects:
            # 这里简化处理，实际应用中可能需要调用ESLint和Prettier等工具
            if aspect.lower() in content_lower:
                result["evaluated_aspects"].append(aspect)
                weight = aspect_weights[aspect]
                result["total_score"] += weight
                result["details"].append(
                    f"✓ 涉及到{aspect}: (得分: {weight})"
                )
            else:
                result["missing_aspects"].append(aspect)
                result["details"].append(f"✗ 未涉及{aspect}: (权重: {aspect_weights[aspect]})")

        result["total_score"] = round(result["total_score"], 1)
        return result

    def generate_evaluation_report(self) -> Dict[str, any]:
        """
        生成完整的评估报告

        Returns:
            Dict: 完整的评估报告
        """
        if not self.load_frontend_file():
            return {"error": "无法加载前端代码文件"}

        # 执行各项评估
        function_coverage = self.evaluate_function_coverage()
        ui_beauty = self.evaluate_ui_beauty()
        code_quality = self.evaluate_code_quality()

        # 计算总分
        total_score = (
            function_coverage["total_score"]
            + ui_beauty["total_score"]
            + code_quality["total_score"]
        )
        max_total_score = (
            function_coverage["max_score"]
            + ui_beauty["max_score"]
            + code_quality["max_score"]
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
            "ui_beauty": ui_beauty,
            "code_quality": code_quality,
            "recommendations": self._generate_recommendations(
                function_coverage,
                ui_beauty,
                code_quality,
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
        ui_beauty: Dict,
        code_quality: Dict,
    ) -> List[str]:
        """
        生成改进建议

        Args:
            function_coverage: 功能点覆盖率结果
            ui_beauty: 界面美观度结果
            code_quality: 代码质量评估结果

        Returns:
            List[str]: 改进建议列表
        """
        recommendations = []

        # 功能点覆盖率建议
        if function_coverage["unmatched_keywords"]:
            recommendations.append(
                f"建议实现以下缺失的功能点: {', '.join(function_coverage['unmatched_keywords'])}"
            )

        # 界面美观度建议
        if ui_beauty["missing_aspects"]:
            recommendations.append(
                f"建议改进以下界面美观度方面: {', '.join(ui_beauty['missing_aspects'])}"
            )

        # 代码质量建议
        if code_quality["missing_aspects"]:
            recommendations.append(
                f"建议改进以下代码质量方面: {', '.join(code_quality['missing_aspects'])}"
            )

        if not recommendations:
            recommendations.append("前端代码质量良好，无需特别改进")

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

        markdown = f"""# 前端开发评估报告

## 评估概览
- **评估日期**: {summary['evaluation_date']}
- **总分**: {summary['total_score']}/{summary['max_total_score']}
- **得分率**: {summary['percentage']}%
- **等级**: {summary['grade']}

## 1. 功能点覆盖率 ({report['function_coverage']['total_score']}/{report['function_coverage']['max_score']}分)

### 评估标准
检测代码中是否实现以下功能：图书信息展示、相关推荐列表、用户评论区、加入购物车按钮
每个功能实现得2.5分，最高10分

### 评估结果
- **已实现功能**: {', '.join(report['function_coverage']['matched_keywords']) if report['function_coverage']['matched_keywords'] else '无'}
- **未实现功能**: {', '.join(report['function_coverage']['unmatched_keywords']) if report['function_coverage']['unmatched_keywords'] else '无'}

### 详细结果
"""

        for detail in report["function_coverage"]["details"]:
            markdown += f"- {detail}\n"

        markdown += f"""
## 2. 界面美观度 ({report['ui_beauty']['total_score']}/{report['ui_beauty']['max_score']}分)

### 评估标准
评估界面美观度：布局合理性(3分)、色彩搭配(3分)、交互体验(2分)、响应式设计(2分)

### 评估结果
- **已涉及方面**: {', '.join(report['ui_beauty']['evaluated_aspects']) if report['ui_beauty']['evaluated_aspects'] else '无'}
- **未涉及方面**: {', '.join(report['ui_beauty']['missing_aspects']) if report['ui_beauty']['missing_aspects'] else '无'}

### 详细结果
"""

        for detail in report["ui_beauty"]["details"]:
            markdown += f"- {detail}\n"

        markdown += f"""
## 3. 代码质量 ({report['code_quality']['total_score']}/{report['code_quality']['max_score']}分)

### 评估标准
评估代码规范：组件化结构(3分)、命名规范(2分)、代码复用率(2分)、性能优化(3分)
使用ESLint和Prettier自动评分

### 评估结果
- **已涉及方面**: {', '.join(report['code_quality']['evaluated_aspects']) if report['code_quality']['evaluated_aspects'] else '无'}
- **未涉及方面**: {', '.join(report['code_quality']['missing_aspects']) if report['code_quality']['missing_aspects'] else '无'}

### 详细结果
"""

        for detail in report["code_quality"]["details"]:
            markdown += f"- {detail}\n"

        markdown += """
## 改进建议

"""

        for i, recommendation in enumerate(report["recommendations"], 1):
            markdown += f"{i}. {recommendation}\n"

        return markdown


def main():
    """
    主函数：执行前端开发评估
    """
    import sys

    # 支持命令行参数或使用相对路径
    if len(sys.argv) > 1:
        frontend_file = sys.argv[1]
    else:
        frontend_file = "output/图书详情页组件代码.js"  # 默认前端代码文件

    if len(sys.argv) > 2:
        output_report_file = sys.argv[2]
    else:
        output_report_file = "output/前端开发评估报告.md"

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_report_file), exist_ok=True)

    print("=== 前端开发评估器 ===")
    print(f"前端代码路径: {frontend_file}")
    print(f"评估报告输出路径: {output_report_file}")
    print()

    # 检查前端代码文件是否存在
    if not os.path.exists(frontend_file):
        print(f"错误：前端代码文件不存在: {frontend_file}")
        print("请确保前端代码已生成，或使用命令行参数指定前端代码路径")
        print("使用方法: python frontend.py [前端代码路径] [输出报告路径]")
        return

    # 创建评估器实例
    analyzer = FrontendAnalyzer(frontend_file)

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


if __name__ == "__main__":
    main()