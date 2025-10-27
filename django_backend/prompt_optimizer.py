"""
智能 Prompt 优化系统
提供 Prompt 性能优化和质量提升功能
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import hashlib


@dataclass
class PromptMetrics:
    """Prompt 性能指标"""
    length: int
    complexity: float
    clarity: float
    effectiveness: float
    response_quality: float


@dataclass
class OptimizationResult:
    """优化结果"""
    original_prompt: str
    optimized_prompt: str
    improvements: List[str]
    metrics_before: PromptMetrics
    metrics_after: PromptMetrics
    optimization_score: float


class PromptOptimizer:
    """Prompt 优化器"""
    
    def __init__(self):
        self.optimization_rules = self._initialize_optimization_rules()
        self.quality_indicators = self._initialize_quality_indicators()
        self.performance_patterns = self._initialize_performance_patterns()
    
    def _initialize_optimization_rules(self) -> Dict[str, Dict[str, Any]]:
        """初始化优化规则"""
        return {
            "clarity": {
                "remove_redundancy": True,
                "simplify_language": True,
                "improve_structure": True,
                "add_examples": True
            },
            "effectiveness": {
                "enhance_context": True,
                "improve_instructions": True,
                "add_constraints": True,
                "optimize_format": True
            },
            "performance": {
                "reduce_length": True,
                "optimize_keywords": True,
                "improve_flow": True,
                "enhance_focus": True
            }
        }
    
    def _initialize_quality_indicators(self) -> Dict[str, List[str]]:
        """初始化质量指标"""
        return {
            "positive_indicators": [
                "具体", "明确", "详细", "系统", "结构", "分析", "建议", "解决方案",
                "步骤", "方法", "框架", "模板", "示例", "说明", "解释"
            ],
            "negative_indicators": [
                "模糊", "不清楚", "简单", "基础", "一般", "可能", "大概", "也许",
                "不确定", "不清楚", "需要更多信息"
            ]
        }
    
    def _initialize_performance_patterns(self) -> Dict[str, str]:
        """初始化性能模式"""
        return {
            "high_performance": r"(请|请基于|请按照|请确保|请提供|请分析|请解释|请说明)",
            "structured_analysis": r"(分析框架|分析步骤|分析维度|分析结果)",
            "actionable_output": r"(具体步骤|解决方案|建议措施|改进方案|预防措施)",
            "context_aware": r"(基于.*数据|结合.*信息|根据.*情况|考虑.*因素)"
        }
    
    def analyze_prompt_quality(self, prompt: str) -> PromptMetrics:
        """分析 Prompt 质量"""
        # 计算基本指标
        length = len(prompt)
        
        # 计算复杂度（基于句子数量和词汇多样性）
        sentences = re.split(r'[.!?。！？]', prompt)
        complexity = len(sentences) * 0.3 + len(set(prompt.split())) * 0.7
        
        # 计算清晰度（基于正面指标）
        positive_count = sum(1 for indicator in self.quality_indicators["positive_indicators"] 
                           if indicator in prompt)
        negative_count = sum(1 for indicator in self.quality_indicators["negative_indicators"] 
                           if indicator in prompt)
        clarity = max(0, min(1, (positive_count - negative_count * 0.5) / 10))
        
        # 计算有效性（基于性能模式匹配）
        effectiveness = 0
        for pattern_name, pattern in self.performance_patterns.items():
            if re.search(pattern, prompt):
                effectiveness += 0.25
        effectiveness = min(1, effectiveness)
        
        # 响应质量（基于结构化程度）
        structure_indicators = ["##", "###", "1.", "2.", "3.", "-", "*"]
        structure_count = sum(1 for indicator in structure_indicators if indicator in prompt)
        response_quality = min(1, structure_count / 10)
        
        return PromptMetrics(
            length=length,
            complexity=complexity,
            clarity=clarity,
            effectiveness=effectiveness,
            response_quality=response_quality
        )
    
    def optimize_prompt(self, prompt: str, optimization_type: str = "comprehensive") -> OptimizationResult:
        """优化 Prompt"""
        original_metrics = self.analyze_prompt_quality(prompt)
        optimized_prompt = prompt
        improvements = []
        
        if optimization_type == "comprehensive":
            optimized_prompt, improvements = self._comprehensive_optimization(prompt)
        elif optimization_type == "clarity":
            optimized_prompt, improvements = self._clarity_optimization(prompt)
        elif optimization_type == "effectiveness":
            optimized_prompt, improvements = self._effectiveness_optimization(prompt)
        elif optimization_type == "performance":
            optimized_prompt, improvements = self._performance_optimization(prompt)
        
        optimized_metrics = self.analyze_prompt_quality(optimized_prompt)
        
        # 计算优化分数
        optimization_score = self._calculate_optimization_score(
            original_metrics, optimized_metrics
        )
        
        return OptimizationResult(
            original_prompt=prompt,
            optimized_prompt=optimized_prompt,
            improvements=improvements,
            metrics_before=original_metrics,
            metrics_after=optimized_metrics,
            optimization_score=optimization_score
        )
    
    def _comprehensive_optimization(self, prompt: str) -> Tuple[str, List[str]]:
        """综合优化"""
        optimized = prompt
        improvements = []
        
        # 1. 结构优化
        if not re.search(r'##', optimized):
            optimized = self._add_structure(optimized)
            improvements.append("添加了结构化格式")
        
        # 2. 清晰度优化
        if "请" not in optimized:
            optimized = self._add_clear_instructions(optimized)
            improvements.append("添加了明确的指令")
        
        # 3. 上下文优化
        if not re.search(r'基于.*信息', optimized):
            optimized = self._enhance_context(optimized)
            improvements.append("增强了上下文信息")
        
        # 4. 输出格式优化
        if not re.search(r'请按照.*格式', optimized):
            optimized = self._add_output_format(optimized)
            improvements.append("指定了输出格式")
        
        return optimized, improvements
    
    def _clarity_optimization(self, prompt: str) -> Tuple[str, List[str]]:
        """清晰度优化"""
        optimized = prompt
        improvements = []
        
        # 移除冗余
        optimized = re.sub(r'\s+', ' ', optimized)
        improvements.append("移除了多余空格")
        
        # 简化语言
        if "非常" in optimized:
            optimized = optimized.replace("非常", "很")
            improvements.append("简化了语言表达")
        
        # 添加示例
        if "例如" not in optimized and "比如" not in optimized:
            optimized += "\n\n例如：请提供具体的分析步骤和解决方案。"
            improvements.append("添加了示例说明")
        
        return optimized, improvements
    
    def _effectiveness_optimization(self, prompt: str) -> Tuple[str, List[str]]:
        """有效性优化"""
        optimized = prompt
        improvements = []
        
        # 增强指令
        if "请分析" not in optimized:
            optimized = "请分析以下问题：" + optimized
            improvements.append("添加了分析指令")
        
        # 添加约束
        if "确保" not in optimized:
            optimized += "\n\n请确保分析的具体性和可操作性。"
            improvements.append("添加了质量约束")
        
        return optimized, improvements
    
    def _performance_optimization(self, prompt: str) -> Tuple[str, List[str]]:
        """性能优化"""
        optimized = prompt
        improvements = []
        
        # 减少长度
        if len(optimized) > 1000:
            optimized = self._reduce_length(optimized)
            improvements.append("减少了 Prompt 长度")
        
        # 优化关键词
        optimized = self._optimize_keywords(optimized)
        improvements.append("优化了关键词使用")
        
        return optimized, improvements
    
    def _add_structure(self, prompt: str) -> str:
        """添加结构"""
        return f"""
## 分析任务
{prompt}

## 分析要求
请按照以下结构进行分析：
1. 问题识别
2. 原因分析  
3. 解决方案
4. 预防措施

## 输出格式
请提供结构化的分析报告。
"""
    
    def _add_clear_instructions(self, prompt: str) -> str:
        """添加清晰指令"""
        return f"""
请基于以下信息进行深入分析：

{prompt}

请确保：
1. 分析的系统性和全面性
2. 建议的具体性和可操作性
3. 结论的准确性和实用性
"""
    
    def _enhance_context(self, prompt: str) -> str:
        """增强上下文"""
        return f"""
基于提供的历史数据和上下文信息：

{prompt}

请结合相关数据进行分析，确保分析的准确性和针对性。
"""
    
    def _add_output_format(self, prompt: str) -> str:
        """添加输出格式"""
        return f"""
{prompt}

请按照以下格式输出分析结果：
- 问题描述
- 原因分析
- 解决方案
- 预防建议
"""
    
    def _reduce_length(self, prompt: str) -> str:
        """减少长度"""
        # 简单的长度减少策略
        sentences = prompt.split('。')
        if len(sentences) > 3:
            return '。'.join(sentences[:3]) + '。'
        return prompt
    
    def _optimize_keywords(self, prompt: str) -> str:
        """优化关键词"""
        # 替换低效关键词
        replacements = {
            "可能": "需要确认",
            "大概": "需要验证", 
            "也许": "需要分析",
            "不清楚": "需要调查"
        }
        
        for old, new in replacements.items():
            prompt = prompt.replace(old, new)
        
        return prompt
    
    def _calculate_optimization_score(self, before: PromptMetrics, after: PromptMetrics) -> float:
        """计算优化分数"""
        # 计算各项指标的改进
        clarity_improvement = after.clarity - before.clarity
        effectiveness_improvement = after.effectiveness - before.effectiveness
        response_quality_improvement = after.response_quality - before.response_quality
        
        # 长度优化（减少长度是好的）
        length_improvement = max(0, (before.length - after.length) / before.length) if before.length > 0 else 0
        
        # 综合分数
        total_improvement = (
            clarity_improvement * 0.3 +
            effectiveness_improvement * 0.3 +
            response_quality_improvement * 0.2 +
            length_improvement * 0.2
        )
        
        return max(0, min(1, total_improvement + 0.5))  # 基础分数0.5
    
    def batch_optimize(self, prompts: List[str]) -> List[OptimizationResult]:
        """批量优化"""
        results = []
        for prompt in prompts:
            result = self.optimize_prompt(prompt)
            results.append(result)
        return results
    
    def get_optimization_suggestions(self, prompt: str) -> List[str]:
        """获取优化建议"""
        suggestions = []
        metrics = self.analyze_prompt_quality(prompt)
        
        if metrics.clarity < 0.5:
            suggestions.append("建议提高 Prompt 的清晰度，使用更明确的指令")
        
        if metrics.effectiveness < 0.5:
            suggestions.append("建议增强 Prompt 的有效性，添加具体的分析要求")
        
        if metrics.response_quality < 0.5:
            suggestions.append("建议改善输出质量，指定结构化的输出格式")
        
        if metrics.length > 1000:
            suggestions.append("建议减少 Prompt 长度，提高处理效率")
        
        if metrics.complexity < 10:
            suggestions.append("建议增加 Prompt 的复杂度，提供更详细的分析框架")
        
        return suggestions


# 使用示例
if __name__ == "__main__":
    # 创建 Prompt 优化器
    optimizer = PromptOptimizer()
    
    # 示例 Prompt
    sample_prompt = """
    请分析系统问题。基于日志数据，提供解决方案。
    """
    
    # 分析质量
    metrics = optimizer.analyze_prompt_quality(sample_prompt)
    print(f"Prompt 质量指标: {metrics}")
    
    # 优化 Prompt
    result = optimizer.optimize_prompt(sample_prompt)
    print(f"优化结果: {result.optimization_score}")
    print(f"改进项: {result.improvements}")
    print(f"优化后的 Prompt: {result.optimized_prompt}")
    
    # 获取优化建议
    suggestions = optimizer.get_optimization_suggestions(sample_prompt)
    print(f"优化建议: {suggestions}")
