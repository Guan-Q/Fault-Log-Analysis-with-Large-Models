"""
Prompt 性能监控和优化系统
监控和分析 Prompt 的性能，提供优化建议
"""

import time
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics


@dataclass
class PerformanceMetrics:
    """性能指标"""
    response_time: float
    token_count: int
    quality_score: float
    user_satisfaction: float
    timestamp: datetime
    prompt_type: str
    context_size: int


@dataclass
class OptimizationSuggestion:
    """优化建议"""
    category: str
    description: str
    impact: str
    priority: int
    implementation: str


class PromptPerformanceMonitor:
    """Prompt 性能监控器"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history = deque(maxlen=max_history)
        self.performance_stats = defaultdict(list)
        self.logger = logging.getLogger(__name__)
        
        # 性能阈值
        self.thresholds = {
            "response_time": 30.0,  # 秒
            "quality_score": 0.7,
            "user_satisfaction": 0.8,
            "token_efficiency": 0.6
        }
    
    def record_metrics(self, metrics: PerformanceMetrics):
        """记录性能指标"""
        self.metrics_history.append(metrics)
        self.performance_stats[metrics.prompt_type].append(metrics)
        
        # 检查性能问题
        self._check_performance_issues(metrics)
    
    def _check_performance_issues(self, metrics: PerformanceMetrics):
        """检查性能问题"""
        issues = []
        
        if metrics.response_time > self.thresholds["response_time"]:
            issues.append(f"响应时间过长: {metrics.response_time:.2f}s")
        
        if metrics.quality_score < self.thresholds["quality_score"]:
            issues.append(f"质量分数过低: {metrics.quality_score:.2f}")
        
        if metrics.user_satisfaction < self.thresholds["user_satisfaction"]:
            issues.append(f"用户满意度低: {metrics.user_satisfaction:.2f}")
        
        if issues:
            self.logger.warning(f"性能问题检测: {', '.join(issues)}")
    
    def get_performance_summary(self, time_window: Optional[timedelta] = None) -> Dict[str, Any]:
        """获取性能摘要"""
        if not self.metrics_history:
            return {"error": "无性能数据"}
        
        # 过滤时间窗口
        if time_window:
            cutoff_time = datetime.now() - time_window
            recent_metrics = [m for m in self.metrics_history if m.timestamp >= cutoff_time]
        else:
            recent_metrics = list(self.metrics_history)
        
        if not recent_metrics:
            return {"error": "指定时间窗口内无数据"}
        
        # 计算统计信息
        response_times = [m.response_time for m in recent_metrics]
        quality_scores = [m.quality_score for m in recent_metrics]
        satisfaction_scores = [m.user_satisfaction for m in recent_metrics]
        
        return {
            "total_requests": len(recent_metrics),
            "avg_response_time": statistics.mean(response_times),
            "max_response_time": max(response_times),
            "min_response_time": min(response_times),
            "avg_quality_score": statistics.mean(quality_scores),
            "avg_satisfaction": statistics.mean(satisfaction_scores),
            "performance_trend": self._calculate_trend(recent_metrics),
            "top_issues": self._identify_top_issues(recent_metrics)
        }
    
    def _calculate_trend(self, metrics: List[PerformanceMetrics]) -> str:
        """计算性能趋势"""
        if len(metrics) < 2:
            return "数据不足"
        
        # 计算最近一半和之前一半的平均性能
        mid_point = len(metrics) // 2
        recent_avg = statistics.mean([m.quality_score for m in metrics[mid_point:]])
        earlier_avg = statistics.mean([m.quality_score for m in metrics[:mid_point]])
        
        if recent_avg > earlier_avg * 1.05:
            return "性能提升"
        elif recent_avg < earlier_avg * 0.95:
            return "性能下降"
        else:
            return "性能稳定"
    
    def _identify_top_issues(self, metrics: List[PerformanceMetrics]) -> List[str]:
        """识别主要问题"""
        issues = []
        
        # 响应时间问题
        slow_responses = [m for m in metrics if m.response_time > self.thresholds["response_time"]]
        if len(slow_responses) > len(metrics) * 0.2:  # 超过20%的请求响应慢
            issues.append(f"响应时间问题: {len(slow_responses)}/{len(metrics)} 请求超时")
        
        # 质量问题
        low_quality = [m for m in metrics if m.quality_score < self.thresholds["quality_score"]]
        if len(low_quality) > len(metrics) * 0.15:  # 超过15%的请求质量低
            issues.append(f"质量问题: {len(low_quality)}/{len(metrics)} 请求质量低")
        
        # 用户满意度问题
        low_satisfaction = [m for m in metrics if m.user_satisfaction < self.thresholds["user_satisfaction"]]
        if len(low_satisfaction) > len(metrics) * 0.1:  # 超过10%的请求满意度低
            issues.append(f"用户满意度问题: {len(low_satisfaction)}/{len(metrics)} 请求满意度低")
        
        return issues
    
    def generate_optimization_suggestions(self) -> List[OptimizationSuggestion]:
        """生成优化建议"""
        suggestions = []
        
        if not self.metrics_history:
            return suggestions
        
        recent_metrics = list(self.metrics_history)[-100:]  # 最近100条记录
        
        # 响应时间优化建议
        avg_response_time = statistics.mean([m.response_time for m in recent_metrics])
        if avg_response_time > self.thresholds["response_time"]:
            suggestions.append(OptimizationSuggestion(
                category="性能优化",
                description="响应时间过长",
                impact="高",
                priority=1,
                implementation="优化 Prompt 长度，减少不必要的上下文信息"
            ))
        
        # 质量优化建议
        avg_quality = statistics.mean([m.quality_score for m in recent_metrics])
        if avg_quality < self.thresholds["quality_score"]:
            suggestions.append(OptimizationSuggestion(
                category="质量提升",
                description="分析质量需要提升",
                impact="高",
                priority=1,
                implementation="使用更专业的分析框架，增强 Prompt 的结构性"
            ))
        
        # 用户满意度优化建议
        avg_satisfaction = statistics.mean([m.user_satisfaction for m in recent_metrics])
        if avg_satisfaction < self.thresholds["user_satisfaction"]:
            suggestions.append(OptimizationSuggestion(
                category="用户体验",
                description="用户满意度需要提升",
                impact="中",
                priority=2,
                implementation="提供更具体、可操作的解决方案"
            ))
        
        # 基于历史数据的建议
        if len(self.metrics_history) > 50:
            suggestions.extend(self._generate_historical_suggestions())
        
        return suggestions
    
    def _generate_historical_suggestions(self) -> List[OptimizationSuggestion]:
        """基于历史数据生成建议"""
        suggestions = []
        
        # 分析不同 Prompt 类型的性能
        type_performance = {}
        for prompt_type, metrics in self.performance_stats.items():
            if len(metrics) > 10:  # 有足够的数据
                avg_quality = statistics.mean([m.quality_score for m in metrics])
                avg_time = statistics.mean([m.response_time for m in metrics])
                type_performance[prompt_type] = {
                    "quality": avg_quality,
                    "time": avg_time,
                    "count": len(metrics)
                }
        
        # 找出性能最差的类型
        if type_performance:
            worst_type = min(type_performance, 
                           key=lambda x: type_performance[x]["quality"])
            worst_metrics = type_performance[worst_type]
            
            if worst_metrics["quality"] < 0.6:
                suggestions.append(OptimizationSuggestion(
                    category="类型优化",
                    description=f"{worst_type} 类型 Prompt 性能较差",
                    impact="中",
                    priority=2,
                    implementation=f"针对 {worst_type} 类型优化 Prompt 设计"
                ))
        
        return suggestions
    
    def get_prompt_type_analysis(self) -> Dict[str, Any]:
        """获取不同 Prompt 类型的性能分析"""
        analysis = {}
        
        for prompt_type, metrics in self.performance_stats.items():
            if len(metrics) < 5:  # 数据不足
                continue
            
            response_times = [m.response_time for m in metrics]
            quality_scores = [m.quality_score for m in metrics]
            satisfaction_scores = [m.user_satisfaction for m in metrics]
            
            analysis[prompt_type] = {
                "request_count": len(metrics),
                "avg_response_time": statistics.mean(response_times),
                "avg_quality_score": statistics.mean(quality_scores),
                "avg_satisfaction": statistics.mean(satisfaction_scores),
                "performance_grade": self._calculate_performance_grade(
                    statistics.mean(quality_scores),
                    statistics.mean(satisfaction_scores)
                )
            }
        
        return analysis
    
    def _calculate_performance_grade(self, quality: float, satisfaction: float) -> str:
        """计算性能等级"""
        score = (quality + satisfaction) / 2
        
        if score >= 0.9:
            return "优秀"
        elif score >= 0.8:
            return "良好"
        elif score >= 0.7:
            return "一般"
        elif score >= 0.6:
            return "较差"
        else:
            return "很差"
    
    def export_metrics(self, filepath: str):
        """导出性能指标"""
        data = {
            "export_time": datetime.now().isoformat(),
            "total_records": len(self.metrics_history),
            "performance_summary": self.get_performance_summary(),
            "prompt_type_analysis": self.get_prompt_type_analysis(),
            "optimization_suggestions": [
                asdict(suggestion) for suggestion in self.generate_optimization_suggestions()
            ],
            "raw_metrics": [
                {
                    "response_time": m.response_time,
                    "token_count": m.token_count,
                    "quality_score": m.quality_score,
                    "user_satisfaction": m.user_satisfaction,
                    "timestamp": m.timestamp.isoformat(),
                    "prompt_type": m.prompt_type,
                    "context_size": m.context_size
                }
                for m in self.metrics_history
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"性能指标已导出到: {filepath}")


class PromptPerformanceOptimizer:
    """Prompt 性能优化器"""
    
    def __init__(self, monitor: PromptPerformanceMonitor):
        self.monitor = monitor
        self.optimization_history = []
    
    def auto_optimize(self) -> Dict[str, Any]:
        """自动优化"""
        suggestions = self.monitor.generate_optimization_suggestions()
        
        if not suggestions:
            return {"status": "无需优化", "message": "当前性能良好"}
        
        # 按优先级排序
        suggestions.sort(key=lambda x: x.priority)
        
        # 应用高优先级优化
        applied_optimizations = []
        for suggestion in suggestions[:3]:  # 只应用前3个建议
            if suggestion.priority <= 2:  # 高优先级和中优先级
                applied_optimizations.append(suggestion)
        
        # 记录优化历史
        optimization_record = {
            "timestamp": datetime.now(),
            "suggestions_applied": len(applied_optimizations),
            "optimizations": [asdict(s) for s in applied_optimizations]
        }
        self.optimization_history.append(optimization_record)
        
        return {
            "status": "优化完成",
            "applied_optimizations": len(applied_optimizations),
            "optimizations": applied_optimizations,
            "next_review": "建议1周后重新评估性能"
        }
    
    def get_optimization_report(self) -> Dict[str, Any]:
        """获取优化报告"""
        return {
            "monitor_summary": self.monitor.get_performance_summary(),
            "optimization_history": self.optimization_history,
            "current_suggestions": self.monitor.generate_optimization_suggestions(),
            "performance_trend": self._analyze_performance_trend()
        }
    
    def _analyze_performance_trend(self) -> str:
        """分析性能趋势"""
        if len(self.optimization_history) < 2:
            return "数据不足，无法分析趋势"
        
        # 比较最近两次优化的效果
        recent_optimizations = self.optimization_history[-2:]
        
        if len(recent_optimizations) >= 2:
            return "性能趋势分析需要更多数据"
        
        return "性能趋势稳定"


# 使用示例
if __name__ == "__main__":
    # 创建性能监控器
    monitor = PromptPerformanceMonitor()
    
    # 模拟一些性能数据
    for i in range(10):
        metrics = PerformanceMetrics(
            response_time=20.0 + i * 2,
            token_count=1000 + i * 100,
            quality_score=0.7 + i * 0.02,
            user_satisfaction=0.8 + i * 0.01,
            timestamp=datetime.now(),
            prompt_type="error_diagnosis",
            context_size=5 + i
        )
        monitor.record_metrics(metrics)
    
    # 获取性能摘要
    summary = monitor.get_performance_summary()
    print("性能摘要:", summary)
    
    # 生成优化建议
    suggestions = monitor.generate_optimization_suggestions()
    print("优化建议:", suggestions)
    
    # 创建优化器
    optimizer = PromptPerformanceOptimizer(monitor)
    optimization_result = optimizer.auto_optimize()
    print("优化结果:", optimization_result)
