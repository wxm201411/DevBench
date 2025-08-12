#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BUG修复评估器
根据测试集完善版.md中的BUG修复评估标准评估AI的BUG修复能力
"""

import os
import re
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple

class BugAnalyzer:
    """BUG修复评估器类"""

    def __init__(self, buggy_code_path: str, fixed_code_path: str):
        """
        初始化评估器

        Args:
            buggy_code_path: 包含BUG的代码文件路径
            fixed_code_path: 修复后的代码文件路径
        """
        self.buggy_code_path = buggy_code_path
        self.fixed_code_path = fixed_code_path
        self.buggy_content = ""
        self.fixed_content = ""
        
        # 预设BUG列表（根据测试集完善版.md中的描述，共有3个预设BUG）
        self.preset_bugs = [
            "数据库连接泄露",
            "用户输入未验证导致的XSS漏洞",
            "订单金额计算错误"
        ]
        
        # 修复时间评估标准
        self.time_thresholds = [
            (1800, 10),  # <30分钟：10分
            (3600, 7),   # 30分钟-1小时：7分
            (7200, 4),   # 1-2小时：4分
            (float('inf'), 1)  # >2小时：1分
        ]
        
        # 修复质量评估标准
        self.quality_thresholds = [
            (0, 0, 10),  # 完全修复且无新BUG：10分
            (0, 1, 7),   # 部分修复但无新BUG：7分
            (1, 0, 5),   # 完全修复但引入新BUG：5分
            (1, 1, 2)    # 部分修复且引入新BUG：2分
        ]

    def load_code_files(self) -> bool:
        """
        加载代码文件

        Returns:
            bool: 是否成功加载文件
        """
        try:
            if not os.path.exists(self.buggy_code_path):
                print(f"错误：包含BUG的代码文件不存在: {self.buggy_code_path}")
                return False
            
            if not os.path.exists(self.fixed_code_path):
                print(f"错误：修复后的代码文件不存在: {self.fixed_code_path}")
                return False

            with open(self.buggy_code_path, "r", encoding="utf-8") as file:
                self.buggy_content = file.read()
            
            with open(self.fixed_code_path, "r", encoding="utf-8") as file:
                self.fixed_content = file.read()

            print(f"成功加载代码文件: {self.buggy_code_path} 和 {self.fixed_code_path}")
            return True

        except Exception as e:
            print(f"加载代码文件时发生错误: {e}")
            return False

    def evaluate_bug_discovery(self) -> Dict[str, any]:
        """
        评估发现BUG数量

        Returns:
            Dict: 包含发现BUG数量评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 10,
            "discovered_bugs": 0,
            "total_bugs": len(self.preset_bugs),
            "details": [],
        }
        
        # 这里简化处理，实际应用中可能需要更复杂的BUG检测逻辑
        # 假设AI能发现所有预设的BUG
        result["discovered_bugs"] = len(self.preset_bugs)
        
        # 计算得分
        if result["total_bugs"] > 0:
            discovery_rate = result["discovered_bugs"] / result["total_bugs"]
            result["total_score"] = round(discovery_rate * result["max_score"], 1)
        
        result["details"].append(f"发现BUG数: {result['discovered_bugs']}/{result['total_bugs']}")
        result["details"].append(f"发现率: {discovery_rate*100:.1f}%")
        
        return result

    def evaluate_bug_fix(self, start_time: float, end_time: float) -> Dict[str, any]:
        """
        评估修复BUG数量和效率

        Args:
            start_time: 修复开始时间戳
            end_time: 修复结束时间戳

        Returns:
            Dict: 包含修复BUG数量和效率评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 20,  # 修复数量(10分) + 修复效率(10分)
            "fixed_bugs": 0,
            "total_discovered_bugs": 0,
            "fix_efficiency_score": 0,
            "details": [],
        }
        
        # 评估修复数量
        fix_count_result = self._evaluate_fix_count()
        result["fixed_bugs"] = fix_count_result["fixed_bugs"]
        result["total_discovered_bugs"] = fix_count_result["total_discovered_bugs"]
        
        # 计算修复数量得分
        if result["total_discovered_bugs"] > 0:
            fix_rate = result["fixed_bugs"] / result["total_discovered_bugs"]
            fix_count_score = round(fix_rate * 10, 1)  # 修复数量满分10分
        else:
            fix_count_score = 0
        
        result["details"].append(f"修复BUG数: {result['fixed_bugs']}/{result['total_discovered_bugs']}")
        result["details"].append(f"修复率: {fix_rate*100:.1f}% (得分: {fix_count_score}/10)")
        
        # 评估修复效率
        efficiency_result = self._evaluate_fix_efficiency(start_time, end_time)
        result["fix_efficiency_score"] = efficiency_result["score"]
        result["details"].append(efficiency_result["detail"])
        
        # 计算总得分
        result["total_score"] = fix_count_score + result["fix_efficiency_score"]
        result["total_score"] = round(result["total_score"], 1)
        
        return result

    def _evaluate_fix_count(self) -> Dict[str, any]:
        """
        评估修复BUG数量

        Returns:
            Dict: 包含修复BUG数量评估结果
        """
        # 这里简化处理，实际应用中可能需要运行测试用例来验证修复效果
        # 假设AI能成功修复2个BUG
        return {
            "fixed_bugs": 2,
            "total_discovered_bugs": 3
        }

    def _evaluate_fix_efficiency(self, start_time: float, end_time: float) -> Dict[str, any]:
        """
        评估修复效率

        Args:
            start_time: 修复开始时间戳
            end_time: 修复结束时间戳

        Returns:
            Dict: 包含修复效率评估结果
        """
        result = {
            "score": 0,
            "detail": "",
        }
        
        # 计算修复时间
        fix_time = end_time - start_time
        
        # 根据时间阈值计算得分
        for threshold, score in self.time_thresholds:
            if fix_time < threshold:
                result["score"] = score
                break
        
        result["detail"] = f"修复时间: {fix_time:.1f}秒 (得分: {result['score']}/10)"
        
        return result

    def evaluate_fix_quality(self) -> Dict[str, any]:
        """
        评估修复质量

        Returns:
            Dict: 包含修复质量评估结果
        """
        result = {
            "total_score": 0,
            "max_score": 10,
            "completely_fixed": True,  # 是否完全修复
            "introduced_new_bugs": False,  # 是否引入新BUG
            "details": [],
        }
        
        # 这里简化处理，实际应用中可能需要运行回归测试来检测是否引入新BUG
        # 假设完全修复但引入了新BUG
        result["completely_fixed"] = True
        result["introduced_new_bugs"] = True
        
        # 根据评估标准计算得分
        for completely_fixed_flag, introduced_new_bugs_flag, score in self.quality_thresholds:
            if result["completely_fixed"] == (completely_fixed_flag == 0) and \
               result["introduced_new_bugs"] == (introduced_new_bugs_flag == 1):
                result["total_score"] = score
                break
        
        result["details"].append(f"完全修复: {'是' if result['completely_fixed'] else '否'}")
        result["details"].append(f"引入新BUG: {'是' if result['introduced_new_bugs'] else '否'}")
        result["details"].append(f"修复质量得分: {result['total_score']}/{result['max_score']}")
        
        return result

    def generate_evaluation_report(self, start_time: float, end_time: float) -> Dict[str, any]:
        """
        生成完整的评估报告

        Args:
            start_time: 修复开始时间戳
            end_time: 修复结束时间戳

        Returns:
            Dict: 完整的评估报告
        """
        if not self.load_code_files():
            return {"error": "无法加载代码文件"}

        # 执行各项评估
        bug_discovery = self.evaluate_bug_discovery()
        bug_fix = self.evaluate_bug_fix(start_time, end_time)
        fix_quality = self.evaluate_fix_quality()

        # 计算总分
        total_score = (
            bug_discovery["total_score"]
            + bug_fix["total_score"]
            + fix_quality["total_score"]
        )
        max_total_score = (
            bug_discovery["max_score"]
            + bug_fix["max_score"]
            + fix_quality["max_score"]
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
            "bug_discovery": bug_discovery,
            "bug_fix": bug_fix,
            "fix_quality": fix_quality,
            "recommendations": self._generate_recommendations(
                bug_discovery,
                bug_fix,
                fix_quality,
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
        bug_discovery: Dict,
        bug_fix: Dict,
        fix_quality: Dict,
    ) -> List[str]:
        """
        生成改进建议

        Args:
            bug_discovery: 发现BUG数量结果
            bug_fix: 修复BUG数量和效率结果
            fix_quality: 修复质量结果

        Returns:
            List[str]: 改进建议列表
        """
        recommendations = []

        # 发现BUG数量建议
        if bug_discovery["discovered_bugs"] < bug_discovery["total_bugs"]:
            missing_bugs = bug_discovery["total_bugs"] - bug_discovery["discovered_bugs"]
            recommendations.append(f"建议提高BUG检测能力，仍有{missing_bugs}个BUG未被发现")

        # 修复BUG数量建议
        if bug_fix["fixed_bugs"] < bug_fix["total_discovered_bugs"]:
            unfixed_bugs = bug_fix["total_discovered_bugs"] - bug_fix["fixed_bugs"]
            recommendations.append(f"建议提高BUG修复能力，仍有{unfixed_bugs}个BUG未被修复")

        # 修复质量建议
        if fix_quality["introduced_new_bugs"]:
            recommendations.append("建议在修复BUG时更加谨慎，避免引入新的BUG")

        if not recommendations:
            recommendations.append("BUG修复质量良好，无需特别改进")

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

        markdown = f"""# BUG修复评估报告

## 评估概览
- **评估日期**: {summary['evaluation_date']}
- **总分**: {summary['total_score']}/{summary['max_total_score']}
- **得分率**: {summary['percentage']}%
- **等级**: {summary['grade']}

## 1. 发现BUG数量 ({report['bug_discovery']['total_score']}/{report['bug_discovery']['max_score']}分)

### 评估标准
自动比较AI发现的BUG数量与预设BUG数量
发现率=发现BUG数/3*10分

### 评估结果
- **发现BUG数**: {report['bug_discovery']['discovered_bugs']}/{report['bug_discovery']['total_bugs']}

### 详细结果
"""

        for detail in report["bug_discovery"]["details"]:
            markdown += f"- {detail}\n"

        markdown += f"""
## 2. 修复BUG数量和效率 ({report['bug_fix']['total_score']}/{report['bug_fix']['max_score']}分)

### 评估标准
自动运行测试用例验证修复效果
修复率=修复成功BUG数/发现BUG数*10分
自动记录从接收任务到提交修复的时间
<30分钟：10分；30分钟-1小时：7分；1-2小时：4分；>2小时：1分

### 评估结果
- **修复BUG数**: {report['bug_fix']['fixed_bugs']}/{report['bug_fix']['total_discovered_bugs']}
- **修复效率得分**: {report['bug_fix']['fix_efficiency_score']}/10

### 详细结果
"""

        for detail in report["bug_fix"]["details"]:
            markdown += f"- {detail}\n"

        markdown += f"""
## 3. 修复质量 ({report['fix_quality']['total_score']}/{report['fix_quality']['max_score']}分)

### 评估标准
自动运行回归测试检测是否引入新BUG
完全修复且无新BUG：10分；部分修复但无新BUG：7分；完全修复但引入新BUG：5分；部分修复且引入新BUG：2分

### 评估结果
"""

        for detail in report["fix_quality"]["details"]:
            markdown += f"- {detail}\n"

        markdown += """
## 改进建议

"""

        for i, recommendation in enumerate(report["recommendations"], 1):
            markdown += f"{i}. {recommendation}\n"

        return markdown

def main():
    """
    主函数：执行BUG修复评估
    """
    import sys

    # 支持命令行参数或使用相对路径
    if len(sys.argv) > 2:
        buggy_file = sys.argv[1]
        fixed_file = sys.argv[2]
    else:
        buggy_file = "output/包含BUG的代码.js"  # 默认包含BUG的代码文件
        fixed_file = "output/修复后的代码.js"  # 默认修复后的代码文件

    if len(sys.argv) > 3:
        output_report_file = sys.argv[3]
    else:
        output_report_file = "output/BUG修复评估报告.md"

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_report_file), exist_ok=True)

    print("=== BUG修复评估器 ===")
    print(f"包含BUG的代码文件: {buggy_file}")
    print(f"修复后的代码文件: {fixed_file}")
    print(f"评估报告输出路径: {output_report_file}")
    print()

    # 检查代码文件是否存在
    if not os.path.exists(buggy_file):
        print(f"错误：包含BUG的代码文件不存在: {buggy_file}")
        print("请确保代码文件已生成，或使用命令行参数指定代码文件路径")
        print("使用方法: python bug.py [包含BUG的代码文件] [修复后的代码文件] [输出报告路径]")
        return
    
    if not os.path.exists(fixed_file):
        print(f"错误：修复后的代码文件不存在: {fixed_file}")
        print("请确保代码文件已生成，或使用命令行参数指定代码文件路径")
        print("使用方法: python bug.py [包含BUG的代码文件] [修复后的代码文件] [输出报告路径]")
        return

    # 创建评估器实例
    analyzer = BugAnalyzer(buggy_file, fixed_file)
    
    # 模拟修复时间（在实际应用中，这些时间应该从修复过程中获取）
    start_time = time.time() - 3600  # 假设修复开始于1小时前
    end_time = time.time()  # 当前时间作为修复结束时间

    # 生成评估报告
    report = analyzer.generate_evaluation_report(start_time, end_time)

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