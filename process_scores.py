#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
需求文档评分处理脚本
用于合并两个表格中相同需求文档的得分，并按总分排序输出
"""

def parse_table(lines):
    """
    解析表格数据
    :param lines: 表格行列表
    :return: 字典，键为需求文档名称，值为(总分, 得分率)元组
    """
    scores = {}
    for line in lines:
        # 跳过表头和分隔线
        if line.startswith("需求文档") or line.startswith("==") or line.startswith("--") or line.strip() == "":
            continue
        
        # 分割行数据
        parts = line.split()
        if len(parts) >= 3:
            name = parts[0]
            total_score = float(parts[1])
            score_rate = float(parts[2])
            scores[name] = (total_score, score_rate)
    
    return scores

def merge_scores(scores1, scores2):
    """
    合并两个评分字典
    :param scores1: 第一个评分字典
    :param scores2: 第二个评分字典
    :return: 合并后的评分字典
    """
    merged = {}
    
    # 合并所有需求文档
    all_names = set(scores1.keys()) | set(scores2.keys())
    
    for name in all_names:
        score1 = scores1.get(name, (0, 0))
        score2 = scores2.get(name, (0, 0))
        
        # 总分相加，得分率也相加
        total_score = score1[0] + score2[0]
        # 得分率也相加
        score_rate = score1[1] + score2[1]
            
        merged[name] = (total_score, score_rate)
    
    return merged

def print_sorted_scores(scores):
    """
    按总分排序并打印结果
    :param scores: 评分字典
    """
    # 按总分降序排序
    sorted_scores = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)
    
    # 打印表头
    print("需求文档                 总分         得分率")
    print("--------------------------------------------------------------------------------")
    
    # 打印数据
    for name, (total_score, score_rate) in sorted_scores:
        print(f"{name:<20} {total_score:>6.1f}       {score_rate:>6.2f}")

def main():
    # 第一个表格数据
    table1_lines = [
        "GLM-4.5              40.6       54.13",
        "Kimi-k2              38.1       50.8",
        "Qwen-3-Coder         31.5       42.0",
        "Doubao-Seek-1.6      28.6       38.13",
        "DeepSeek-V3-0324     27.5       36.67",
        "Doubao-1.5-thinking-pro 24.3       32.4",
        "DeepSeek-Reason      19.4       25.87",
        "Doubao-1.5-pro       14.0       18.67"
    ]
    
    # 第二个表格数据
    table2_lines = [
        "Doubao-Seek-1.6      56.5       75.33",
        "Kimi-k2              53.6       71.47",
        "GLM-4.5              49.0       65.33",
        "Qwen-3-Coder         46.1       61.47",
        "Doubao-1.5-pro       42.5       56.67",
        "DeepSeek-V3-0324     41.3       55.07",
        "Doubao-1.5-thinking-pro 40.6       54.13",
        "DeepSeek-Reason      25.3       33.73"
    ]
    
    # 解析表格
    scores1 = parse_table(table1_lines)
    scores2 = parse_table(table2_lines)
    
    # 合并评分
    merged_scores = merge_scores(scores1, scores2)
    
    # 输出结果
    print_sorted_scores(merged_scores)

if __name__ == "__main__":
    main()