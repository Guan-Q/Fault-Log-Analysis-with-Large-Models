"""
专业数据分析框架和模板系统
提供多种专业的数据分析框架，提升分析质量和针对性
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
import re
from datetime import datetime, timedelta


class AnalysisFramework(Enum):
    """分析框架类型"""
    SWISS_CHEESE = "swiss_cheese"  # 瑞士奶酪模型
    FISHBONE = "fishbone"  # 鱼骨图分析
    FIVE_WHYS = "five_whys"  # 5个为什么
    PARETO = "pareto"  # 帕累托分析
    ROOT_CAUSE = "root_cause"  # 根因分析
    TREND_ANALYSIS = "trend_analysis"  # 趋势分析
    CORRELATION = "correlation"  # 相关性分析
    PERFORMANCE = "performance"  # 性能分析


@dataclass
class AnalysisResult:
    """分析结果"""
    framework: AnalysisFramework
    findings: List[str]
    recommendations: List[str]
    confidence: float
    metadata: Dict[str, Any]


class ProfessionalAnalysisFrameworks:
    """专业分析框架系统"""
    
    def __init__(self):
        self.frameworks = self._initialize_frameworks()
        self.templates = self._initialize_templates()
    
    def _initialize_frameworks(self) -> Dict[AnalysisFramework, str]:
        """初始化分析框架"""
        return {
            AnalysisFramework.SWISS_CHEESE: """
## 瑞士奶酪模型分析框架

瑞士奶酪模型用于分析系统故障的多层防护失效。每一层防护都像一片瑞士奶酪，有漏洞（孔洞）。
当所有层的漏洞对齐时，故障就会发生。

### 分析步骤：
1. **识别防护层**：列出系统的所有防护层（监控、告警、自动恢复、人工干预等）
2. **分析漏洞**：识别每层防护中的漏洞和薄弱环节
3. **漏洞对齐分析**：分析哪些漏洞的组合导致了故障
4. **改进建议**：针对每层防护提出具体的改进措施

### 输出格式：
- 防护层分析
- 漏洞识别
- 对齐分析
- 改进建议
""",

            AnalysisFramework.FISHBONE: """
## 鱼骨图分析框架（因果分析）

鱼骨图用于系统性地分析问题的根本原因，从多个维度进行深入分析。

### 分析维度：
1. **人员因素**：技能、培训、操作规范、沟通
2. **流程因素**：工作流程、审批流程、应急流程
3. **技术因素**：系统架构、代码质量、技术选型
4. **环境因素**：硬件环境、网络环境、外部依赖
5. **管理因素**：管理制度、资源配置、决策流程
6. **材料因素**：数据质量、配置参数、依赖服务

### 输出格式：
- 问题描述
- 各维度分析
- 根本原因识别
- 解决方案建议
""",

            AnalysisFramework.FIVE_WHYS: """
## 5个为什么分析框架

通过连续问5个"为什么"来深入挖掘问题的根本原因。

### 分析步骤：
1. **问题陈述**：明确描述当前问题
2. **第一层为什么**：为什么会出现这个问题？
3. **第二层为什么**：为什么会出现第一层的原因？
4. **第三层为什么**：为什么会出现第二层的原因？
5. **第四层为什么**：为什么会出现第三层的原因？
6. **第五层为什么**：为什么会出现第四层的原因？
7. **根本原因**：基于5层分析得出的根本原因
8. **解决方案**：针对根本原因的具体解决方案

### 输出格式：
- 问题陈述
- 5层为什么分析
- 根本原因总结
- 解决方案
""",

            AnalysisFramework.PARETO: """
## 帕累托分析框架（80/20法则）

识别导致80%问题的20%关键因素，优先解决最重要的问题。

### 分析步骤：
1. **问题分类**：将问题按类型、严重程度、影响范围分类
2. **频率统计**：统计各类问题的出现频率
3. **影响评估**：评估各类问题对系统的影响
4. **优先级排序**：按频率和影响确定优先级
5. **关键因素识别**：识别导致大部分问题的关键因素
6. **资源分配**：将资源重点投入到关键因素的解决上

### 输出格式：
- 问题分类统计
- 频率分析
- 影响评估
- 优先级排序
- 关键因素识别
- 资源分配建议
""",

            AnalysisFramework.ROOT_CAUSE: """
## 根因分析框架

系统性地分析问题的根本原因，提供结构化的分析方法。

### 分析步骤：
1. **问题定义**：明确问题的具体表现和影响
2. **时间线分析**：构建问题发生的时间线
3. **因果链分析**：分析问题发生的因果链
4. **影响因素识别**：识别所有可能的影响因素
5. **根因定位**：通过排除法定位根本原因
6. **验证分析**：验证根因分析的合理性
7. **解决方案**：基于根因提出解决方案

### 输出格式：
- 问题定义
- 时间线分析
- 因果链分析
- 影响因素分析
- 根因定位
- 解决方案
""",

            AnalysisFramework.TREND_ANALYSIS: """
## 趋势分析框架

分析数据的时间序列特征，识别趋势和模式。

### 分析步骤：
1. **数据收集**：收集相关的时间序列数据
2. **趋势识别**：识别数据的长期趋势
3. **周期性分析**：分析数据的周期性模式
4. **异常检测**：识别数据中的异常点
5. **预测分析**：基于历史数据预测未来趋势
6. **业务影响**：分析趋势对业务的影响

### 输出格式：
- 趋势描述
- 周期性分析
- 异常点识别
- 预测结果
- 业务影响分析
- 建议措施
""",

            AnalysisFramework.CORRELATION: """
## 相关性分析框架

分析不同指标之间的相关性，识别潜在的因果关系。

### 分析步骤：
1. **指标选择**：选择需要分析的相关指标
2. **数据收集**：收集各指标的历史数据
3. **相关性计算**：计算指标间的相关系数
4. **显著性检验**：检验相关性的显著性
5. **因果关系分析**：分析潜在的因果关系
6. **业务解释**：从业务角度解释相关性

### 输出格式：
- 指标相关性矩阵
- 显著性分析
- 因果关系分析
- 业务解释
- 建议措施
""",

            AnalysisFramework.PERFORMANCE: """
## 性能分析框架

专门用于系统性能问题的分析和优化。

### 分析步骤：
1. **性能指标识别**：识别关键性能指标
2. **基准线建立**：建立性能基准线
3. **瓶颈识别**：识别性能瓶颈
4. **资源分析**：分析资源使用情况
5. **优化建议**：提出具体的优化建议
6. **监控策略**：制定性能监控策略

### 输出格式：
- 性能指标分析
- 基准线对比
- 瓶颈识别
- 资源使用分析
- 优化建议
- 监控策略
"""
        }
    
    def _initialize_templates(self) -> Dict[str, str]:
        """初始化分析模板"""
        return {
            "error_diagnosis": """
## 错误诊断分析模板

### 1. 错误现象描述
- **错误类型**：{error_type}
- **发生时间**：{occurrence_time}
- **影响范围**：{impact_scope}
- **严重程度**：{severity_level}

### 2. 错误模式分析
- **错误频率**：{error_frequency}
- **错误模式**：{error_pattern}
- **触发条件**：{trigger_conditions}

### 3. 根因分析
- **直接原因**：{direct_cause}
- **根本原因**：{root_cause}
- **影响因素**：{contributing_factors}

### 4. 解决方案
- **立即措施**：{immediate_actions}
- **长期方案**：{long_term_solutions}
- **预防措施**：{prevention_measures}

### 5. 风险评估
- **业务影响**：{business_impact}
- **技术风险**：{technical_risk}
- **应急计划**：{contingency_plan}
""",

            "performance_analysis": """
## 性能分析模板

### 1. 性能指标概览
- **响应时间**：{response_time}
- **吞吐量**：{throughput}
- **资源利用率**：{resource_utilization}
- **错误率**：{error_rate}

### 2. 瓶颈分析
- **CPU瓶颈**：{cpu_bottleneck}
- **内存瓶颈**：{memory_bottleneck}
- **I/O瓶颈**：{io_bottleneck}
- **网络瓶颈**：{network_bottleneck}

### 3. 优化建议
- **配置优化**：{configuration_optimization}
- **代码优化**：{code_optimization}
- **架构优化**：{architecture_optimization}
- **资源优化**：{resource_optimization}

### 4. 监控策略
- **关键指标**：{key_metrics}
- **告警阈值**：{alert_thresholds}
- **监控频率**：{monitoring_frequency}
""",

            "security_analysis": """
## 安全分析模板

### 1. 安全事件分析
- **事件类型**：{event_type}
- **攻击向量**：{attack_vector}
- **影响范围**：{impact_scope}
- **严重程度**：{severity_level}

### 2. 威胁分析
- **威胁来源**：{threat_source}
- **攻击目标**：{attack_target}
- **攻击手段**：{attack_method}
- **攻击时间**：{attack_timeline}

### 3. 漏洞评估
- **漏洞类型**：{vulnerability_type}
- **利用难度**：{exploit_difficulty}
- **影响程度**：{impact_level}
- **修复优先级**：{fix_priority}

### 4. 防护建议
- **立即措施**：{immediate_actions}
- **安全加固**：{security_hardening}
- **监控增强**：{monitoring_enhancement}
- **培训建议**：{training_recommendations}
"""
        }
    
    def select_framework(self, query: str, context: List[Dict]) -> AnalysisFramework:
        """根据查询和上下文选择合适的分析框架"""
        query_lower = query.lower()
        
        # 基于关键词选择框架
        framework_keywords = {
            AnalysisFramework.SWISS_CHEESE: ["多层", "防护", "失效", "漏洞", "对齐"],
            AnalysisFramework.FISHBONE: ["因果", "原因", "为什么", "分析", "维度"],
            AnalysisFramework.FIVE_WHYS: ["为什么", "根本原因", "深入", "挖掘"],
            AnalysisFramework.PARETO: ["优先级", "重要", "关键", "80/20", "帕累托"],
            AnalysisFramework.ROOT_CAUSE: ["根因", "根本", "原因", "分析"],
            AnalysisFramework.TREND_ANALYSIS: ["趋势", "变化", "预测", "模式", "时间"],
            AnalysisFramework.CORRELATION: ["相关", "关联", "影响", "关系"],
            AnalysisFramework.PERFORMANCE: ["性能", "速度", "响应", "瓶颈", "优化"]
        }
        
        # 计算匹配分数
        scores = {}
        for framework, keywords in framework_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            scores[framework] = score
        
        # 返回得分最高的框架
        if scores:
            return max(scores, key=scores.get)
        
        return AnalysisFramework.ROOT_CAUSE  # 默认使用根因分析
    
    def generate_analysis_prompt(self, framework: AnalysisFramework, query: str, context: List[Dict]) -> str:
        """生成基于框架的分析 Prompt"""
        framework_template = self.frameworks[framework]
        
        # 构建上下文信息
        context_info = self._build_context_info(context)
        
        # 构建分析 Prompt
        analysis_prompt = f"""
{framework_template}

## 分析上下文
{context_info}

## 分析问题
{query}

## 分析要求
请严格按照上述分析框架进行分析，确保：
1. 分析结构化和系统化
2. 充分利用提供的历史数据
3. 提供具体、可操作的建议
4. 确保分析的准确性和实用性

请开始分析：
"""
        return analysis_prompt
    
    def _build_context_info(self, context: List[Dict]) -> str:
        """构建上下文信息"""
        if not context:
            return "无相关历史数据"
        
        info_parts = []
        info_parts.append(f"相关数据数量: {len(context)}")
        
        # 分析数据特征
        error_count = sum(1 for log in context if any(keyword in log.get('content', '').lower() 
                          for keyword in ['error', 'exception', 'failed', 'timeout']))
        warning_count = sum(1 for log in context if any(keyword in log.get('content', '').lower() 
                            for keyword in ['warning', 'warn', 'alert']))
        
        if error_count > 0:
            info_parts.append(f"错误日志数量: {error_count}")
        if warning_count > 0:
            info_parts.append(f"警告日志数量: {warning_count}")
        
        # 时间范围分析
        timestamps = []
        for log in context:
            content = log.get('content', '')
            # 简单的时间戳提取
            import re
            time_matches = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', content)
            timestamps.extend(time_matches)
        
        if timestamps:
            info_parts.append(f"时间范围: {min(timestamps)} 到 {max(timestamps)}")
        
        return "\n".join(info_parts)
    
    def apply_framework_analysis(self, framework: AnalysisFramework, query: str, context: List[Dict]) -> AnalysisResult:
        """应用框架进行分析"""
        # 这里可以集成实际的AI分析逻辑
        # 目前返回模拟结果
        
        findings = [
            f"基于{framework.value}框架的分析结果",
            "识别出关键问题点",
            "提供了结构化的分析视角"
        ]
        
        recommendations = [
            "建议采用系统性的分析方法",
            "重点关注根本原因",
            "制定具体的改进措施"
        ]
        
        return AnalysisResult(
            framework=framework,
            findings=findings,
            recommendations=recommendations,
            confidence=0.85,
            metadata={
                "analysis_time": datetime.now().isoformat(),
                "context_size": len(context),
                "framework_used": framework.value
            }
        )


# 使用示例
if __name__ == "__main__":
    # 创建专业分析框架系统
    analysis_system = ProfessionalAnalysisFrameworks()
    
    # 示例查询
    query = "系统出现性能瓶颈，如何分析根本原因？"
    context = [
        {"content": "2024-01-15 10:30:15 CPU usage 95%", "score": 0.9},
        {"content": "2024-01-15 10:31:22 Memory usage 90%", "score": 0.8}
    ]
    
    # 选择分析框架
    framework = analysis_system.select_framework(query, context)
    print(f"选择的框架: {framework.value}")
    
    # 生成分析 Prompt
    prompt = analysis_system.generate_analysis_prompt(framework, query, context)
    print("分析 Prompt:")
    print(prompt)
    
    # 应用框架分析
    result = analysis_system.apply_framework_analysis(framework, query, context)
    print(f"分析结果: {result}")
