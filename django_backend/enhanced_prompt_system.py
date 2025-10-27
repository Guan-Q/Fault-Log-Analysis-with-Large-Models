"""
增强型 Prompt 系统 - 智能数据分析
提供更科学、精准的 Prompt 设计，提升大模型数据分析能力
"""

import re
import json
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

# 导入专业分析框架和优化器
try:
    from analysis_frameworks import ProfessionalAnalysisFrameworks, AnalysisFramework
    from prompt_optimizer import PromptOptimizer
    from technical_error_analyzer import TechnicalErrorAnalyzer
    ADVANCED_FEATURES_AVAILABLE = True
except ImportError:
    ADVANCED_FEATURES_AVAILABLE = False


class AnalysisType(Enum):
    """分析类型枚举"""
    ERROR_DIAGNOSIS = "error_diagnosis"  # 错误诊断
    PERFORMANCE_ANALYSIS = "performance_analysis"  # 性能分析
    SECURITY_ANALYSIS = "security_analysis"  # 安全分析
    TREND_ANALYSIS = "trend_analysis"  # 趋势分析
    ROOT_CAUSE_ANALYSIS = "root_cause_analysis"  # 根因分析
    CAPACITY_PLANNING = "capacity_planning"  # 容量规划
    TECHNICAL_ERROR_ANALYSIS = "technical_error_analysis"  # 技术错误分析
    GENERAL_ANALYSIS = "general_analysis"  # 通用分析


class LogSeverity(Enum):
    """日志严重程度"""
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


@dataclass
class AnalysisContext:
    """分析上下文"""
    query: str
    log_context: List[Dict]
    analysis_type: AnalysisType
    log_severity: Optional[LogSeverity] = None
    time_range: Optional[str] = None
    system_components: Optional[List[str]] = None


class EnhancedPromptSystem:
    """增强型 Prompt 系统"""
    
    def __init__(self):
        self.analysis_templates = self._initialize_analysis_templates()
        self.context_patterns = self._initialize_context_patterns()
        
        # 初始化高级功能
        if ADVANCED_FEATURES_AVAILABLE:
            self.analysis_frameworks = ProfessionalAnalysisFrameworks()
            self.prompt_optimizer = PromptOptimizer()
            self.technical_error_analyzer = TechnicalErrorAnalyzer()
        else:
            self.analysis_frameworks = None
            self.prompt_optimizer = None
            self.technical_error_analyzer = None
    
    def _initialize_analysis_templates(self) -> Dict[AnalysisType, str]:
        """初始化分析模板"""
        return {
            AnalysisType.ERROR_DIAGNOSIS: """
你是资深的系统故障诊断专家，具备10年以上的运维和故障排查经验。你的任务是基于历史日志数据，对系统故障进行深度分析和诊断。

## 分析框架
请按照以下结构进行分析：

### 1. 故障现象描述
- 明确描述当前故障的具体表现
- 识别故障的影响范围和严重程度
- 分析故障的时间特征和频率

### 2. 日志模式分析
- 分析相关日志中的错误模式
- 识别异常的时间序列特征
- 提取关键的错误信息和异常指标

### 3. 根因分析
- 基于日志数据推断可能的根本原因
- 分析故障的传播路径
- 识别触发故障的关键因素

### 4. 解决方案
- 提供具体的修复步骤
- 建议预防措施
- 制定监控和预警策略

### 5. 风险评估
- 评估故障的潜在影响
- 分析业务连续性风险
- 提供应急处理建议
""",

            AnalysisType.PERFORMANCE_ANALYSIS: """
你是专业的系统性能分析专家，专注于性能优化和容量规划。你的任务是分析系统性能数据，识别性能瓶颈并提供优化建议。

## 分析框架
请按照以下结构进行分析：

### 1. 性能指标分析
- 分析关键性能指标（CPU、内存、磁盘、网络）
- 识别性能异常和瓶颈点
- 评估性能趋势和变化

### 2. 资源利用率分析
- 分析系统资源使用情况
- 识别资源浪费和过度使用
- 评估资源分配效率

### 3. 性能瓶颈识别
- 定位具体的性能瓶颈
- 分析瓶颈的根本原因
- 评估瓶颈对系统的影响

### 4. 优化建议
- 提供具体的性能优化方案
- 建议系统配置调整
- 制定性能监控策略

### 5. 容量规划
- 基于历史数据预测未来需求
- 提供扩容建议
- 制定性能基准和SLA
""",

            AnalysisType.SECURITY_ANALYSIS: """
你是网络安全专家，专注于系统安全分析和威胁检测。你的任务是分析安全日志，识别潜在的安全威胁并提供防护建议。

## 分析框架
请按照以下结构进行分析：

### 1. 安全事件识别
- 识别可疑的安全事件和异常行为
- 分析攻击模式和威胁类型
- 评估安全事件的严重程度

### 2. 威胁分析
- 分析潜在的安全威胁
- 识别攻击者的意图和手段
- 评估威胁的影响范围

### 3. 漏洞评估
- 识别系统中的安全漏洞
- 分析漏洞的利用可能性
- 评估漏洞的潜在影响

### 4. 防护建议
- 提供具体的安全防护措施
- 建议安全配置优化
- 制定安全监控策略

### 5. 应急响应
- 提供安全事件响应流程
- 建议安全加固措施
- 制定安全培训计划
""",

            AnalysisType.TREND_ANALYSIS: """
你是数据分析专家，专注于系统运行趋势分析和预测。你的任务是分析历史数据，识别系统运行趋势并提供预测建议。

## 分析框架
请按照以下结构进行分析：

### 1. 趋势识别
- 识别系统运行的关键趋势
- 分析趋势的变化规律
- 评估趋势的稳定性

### 2. 模式分析
- 分析数据中的周期性模式
- 识别异常模式和异常点
- 评估模式的可靠性

### 3. 预测分析
- 基于历史数据预测未来趋势
- 评估预测的准确性
- 识别潜在的风险点

### 4. 业务影响分析
- 分析趋势对业务的影响
- 评估业务风险
- 提供业务优化建议

### 5. 监控建议
- 建议关键监控指标
- 制定预警阈值
- 提供数据收集策略
""",

            AnalysisType.ROOT_CAUSE_ANALYSIS: """
你是系统架构专家，专注于复杂问题的根因分析。你的任务是深入分析系统问题，找到根本原因并提供系统性解决方案。

## 分析框架
请按照以下结构进行分析：

### 1. 问题现象分析
- 详细描述问题的具体表现
- 分析问题的影响范围
- 识别问题的关键特征

### 2. 因果链分析
- 构建问题的因果链
- 分析各因素之间的关系
- 识别关键的影响因素

### 3. 根因定位
- 通过排除法定位根本原因
- 分析根因的触发条件
- 评估根因的复现可能性

### 4. 系统性解决方案
- 提供根本性的解决方案
- 建议系统架构优化
- 制定长期改进计划

### 5. 预防措施
- 设计预防机制
- 建议监控和预警
- 制定应急响应流程
""",

            AnalysisType.CAPACITY_PLANNING: """
你是容量规划专家，专注于系统容量分析和规划。你的任务是分析系统容量需求，制定容量规划策略。

## 分析框架
请按照以下结构进行分析：

### 1. 容量现状分析
- 分析当前系统容量使用情况
- 识别容量瓶颈和限制
- 评估容量利用效率

### 2. 需求预测
- 基于历史数据预测未来需求
- 分析业务增长对容量的影响
- 评估季节性变化和峰值需求

### 3. 容量规划
- 制定容量扩展计划
- 建议资源配置策略
- 设计弹性扩容方案

### 4. 成本优化
- 分析容量成本结构
- 建议成本优化方案
- 制定预算规划

### 5. 监控和调整
- 设计容量监控指标
- 制定容量调整策略
- 提供容量管理流程
""",

            AnalysisType.TECHNICAL_ERROR_ANALYSIS: """
你是资深的技术错误分析专家，具备深厚的编译原理和系统分析经验。你的任务是基于编译错误信息，进行精准的技术分析。

## BROKE 分析框架
请严格按照以下结构进行分析：

### 1. Bug 识别 (Bug Identification)
- **错误类型**: 准确识别错误类型（词法错误、语法错误、语义错误等）
- **编程语言**: 精确识别编程语言类型（C--、C++、Java、Python等）
- **错误位置**: 精确定位错误位置（文件名、行号、列号）
- **错误上下文**: 分析错误发生的代码上下文

### 2. Root Cause 分析 (Root Cause Analysis)
- **编译原理分析**: 基于词法分析、语法分析、语义分析等编译原理
- **Token 分析**: 分析 tokenization 过程中的具体问题
- **语法规则**: 分析违反的具体语法规则
- **语言特性**: 分析编程语言的特定语法要求

### 3. Observation 观察 (Observation)
- **错误信息解析**: 逐字解析错误信息中的关键信息
- **代码模式识别**: 识别问题代码的模式和特征
- **环境因素**: 分析编译环境、工具链等因素
- **历史模式**: 分析类似错误的模式

### 4. Knowledge 知识应用 (Knowledge Application)
- **技术标准**: 应用相关的技术标准和规范
- **最佳实践**: 应用行业最佳实践
- **工具链**: 推荐相关的工具和配置
- **文档参考**: 提供相关的技术文档

### 5. Execution 执行方案 (Execution Plan)
- **具体修复代码**: 提供可直接执行的修复代码
- **工具配置**: 提供具体的工具配置步骤
- **验证方法**: 提供验证修复效果的方法
- **预防措施**: 提供防止类似问题的具体措施

## 技术要求
1. **精确性**: 必须准确对应报错中的每个技术细节
2. **专业性**: 基于编译原理和语言规范进行分析
3. **可操作性**: 提供可直接执行的解决方案
4. **验证性**: 提供验证修复效果的具体方法
""",

            AnalysisType.GENERAL_ANALYSIS: """
你是系统分析专家，具备全面的技术分析能力。你的任务是基于提供的数据，进行全面的系统分析。

## 分析框架
请按照以下结构进行分析：

### 1. 数据概览
- 总结分析的关键数据
- 识别数据中的关键信息
- 评估数据的完整性和可靠性

### 2. 问题识别
- 识别数据中的问题和异常
- 分析问题的严重程度
- 评估问题的影响范围

### 3. 深度分析
- 深入分析问题的原因
- 探索数据中的模式和规律
- 识别关键的影响因素

### 4. 解决方案
- 提供具体的解决方案
- 建议预防措施和改进方案
- 制定监控和预警策略

### 5. 总结和建议
- 总结分析结果
- 提供关键建议
- 制定后续行动计划
"""
        }
    
    def _initialize_context_patterns(self) -> Dict[str, AnalysisType]:
        """初始化上下文模式识别"""
        return {
            r"(错误|故障|异常|报错|失败|崩溃)": AnalysisType.ERROR_DIAGNOSIS,
            r"(性能|速度|响应|延迟|吞吐|瓶颈)": AnalysisType.PERFORMANCE_ANALYSIS,
            r"(安全|攻击|威胁|漏洞|入侵|恶意)": AnalysisType.SECURITY_ANALYSIS,
            r"(趋势|预测|变化|增长|下降|模式)": AnalysisType.TREND_ANALYSIS,
            r"(根因|原因|为什么|为什么|根本)": AnalysisType.ROOT_CAUSE_ANALYSIS,
            r"(容量|资源|内存|CPU|存储|扩展)": AnalysisType.CAPACITY_PLANNING,
            r"(编译错误|语法错误|词法错误|tokenization|lexical|syntax|compilation|编译器|编译失败)": AnalysisType.TECHNICAL_ERROR_ANALYSIS,
        }
    
    def detect_analysis_type(self, query: str) -> AnalysisType:
        """检测分析类型"""
        query_lower = query.lower()
        
        for pattern, analysis_type in self.context_patterns.items():
            if re.search(pattern, query_lower):
                return analysis_type
        
        return AnalysisType.GENERAL_ANALYSIS
    
    def extract_log_severity(self, logs: List[Dict]) -> Optional[LogSeverity]:
        """提取日志严重程度"""
        severity_keywords = {
            LogSeverity.CRITICAL: ["critical", "fatal", "emergency", "panic"],
            LogSeverity.ERROR: ["error", "err", "exception", "failed"],
            LogSeverity.WARNING: ["warning", "warn", "caution", "alert"],
            LogSeverity.INFO: ["info", "information"],
            LogSeverity.DEBUG: ["debug", "trace", "verbose"]
        }
        
        for log in logs:
            content = log.get('content', '').lower()
            for severity, keywords in severity_keywords.items():
                if any(keyword in content for keyword in keywords):
                    return severity
        
        return None
    
    def extract_system_components(self, logs: List[Dict]) -> List[str]:
        """提取系统组件"""
        components = set()
        
        # 常见的系统组件关键词
        component_keywords = [
            "database", "db", "mysql", "postgresql", "redis", "mongodb",
            "api", "service", "microservice", "gateway", "load balancer",
            "cache", "queue", "message", "kafka", "rabbitmq",
            "web", "frontend", "backend", "nginx", "apache",
            "docker", "kubernetes", "container", "pod"
        ]
        
        for log in logs:
            content = log.get('content', '').lower()
            for keyword in component_keywords:
                if keyword in content:
                    components.add(keyword)
        
        return list(components)
    
    def build_enhanced_prompt(self, query: str, context: List[Dict]) -> str:
        """构建增强型 Prompt"""
        # 创建分析上下文
        analysis_context = AnalysisContext(
            query=query,
            log_context=context,
            analysis_type=self.detect_analysis_type(query),
            log_severity=self.extract_log_severity(context),
            system_components=self.extract_system_components(context)
        )
        
        # 获取对应的分析模板
        template = self.analysis_templates[analysis_context.analysis_type]
        
        # 构建日志上下文
        log_context = self._build_log_context(context)
        
        # 构建增强的用户消息
        user_message = self._build_user_message(analysis_context, log_context)
        
        # 基础 Prompt
        base_prompt = f"{template}\n\n{user_message}"
        
        # 如果高级功能可用，进行进一步优化
        if ADVANCED_FEATURES_AVAILABLE and self.analysis_frameworks and self.prompt_optimizer:
            # 检查是否是技术错误分析
            if analysis_context.analysis_type == AnalysisType.TECHNICAL_ERROR_ANALYSIS and self.technical_error_analyzer:
                # 使用技术错误分析器
                technical_analysis = self.technical_error_analyzer.analyze_error(query)
                
                # 构建技术错误分析 Prompt
                technical_prompt = self._build_technical_error_prompt(technical_analysis, context)
                enhanced_prompt = f"{base_prompt}\n\n{technical_prompt}"
            else:
                # 选择专业分析框架
                framework = self.analysis_frameworks.select_framework(query, context)
                framework_prompt = self.analysis_frameworks.generate_analysis_prompt(framework, query, context)
                
                # 合并基础模板和专业框架
                enhanced_prompt = f"{base_prompt}\n\n{framework_prompt}"
            
            # 优化 Prompt
            optimization_result = self.prompt_optimizer.optimize_prompt(enhanced_prompt)
            
            return optimization_result.optimized_prompt
        
        return base_prompt
    
    def _build_log_context(self, context: List[Dict]) -> str:
        """构建日志上下文"""
        if not context:
            return "## 相关历史日志参考:\n暂无相关日志数据"
        
        log_context = "## 相关历史日志参考:\n"
        for i, log in enumerate(context, 1):
            score = log.get('score', 0)
            content = log.get('content', '')
            log_context += f"### 日志 {i} (相似度: {score:.3f})\n"
            log_context += f"{content}\n\n"
        
        return log_context
    
    def _build_user_message(self, analysis_context: AnalysisContext, log_context: str) -> str:
        """构建用户消息"""
        # 构建分析上下文信息
        context_info = self._build_context_info(analysis_context)
        
        user_message = f"""
{log_context}

## 分析上下文信息
{context_info}

## 当前需要分析的问题
{analysis_context.query}

## 分析要求
请基于以上信息，按照指定的分析框架进行深入分析。分析应该：
1. 充分利用提供的历史日志数据
2. 结合分析上下文信息
3. 提供具体、可操作的建议
4. 确保分析的准确性和实用性

请开始分析：
"""
        return user_message
    
    def _build_context_info(self, analysis_context: AnalysisContext) -> str:
        """构建上下文信息"""
        info_parts = []
        
        if analysis_context.log_severity:
            info_parts.append(f"日志严重程度: {analysis_context.log_severity.value}")
        
        if analysis_context.system_components:
            info_parts.append(f"涉及系统组件: {', '.join(analysis_context.system_components)}")
        
        if analysis_context.time_range:
            info_parts.append(f"时间范围: {analysis_context.time_range}")
        
        info_parts.append(f"分析类型: {analysis_context.analysis_type.value}")
        info_parts.append(f"相关日志数量: {len(analysis_context.log_context)}")
        
        return "\n".join(info_parts) if info_parts else "无特殊上下文信息"
    
    def _build_technical_error_prompt(self, technical_analysis, context: List[Dict]) -> str:
        """构建技术错误分析 Prompt"""
        prompt = f"""
## 技术错误分析结果

### 错误基本信息
- **错误类型**: {technical_analysis.error_type.value}
- **编程语言**: {technical_analysis.programming_language.value}
- **编译阶段**: {technical_analysis.technical_details.get('compilation_phase', '未知')}
- **错误位置**: 第 {technical_analysis.location.line_number} 行，第 {technical_analysis.location.column_number} 列

### 根本原因分析
{technical_analysis.root_cause}

### 技术细节
- **Tokenization 状态**: {technical_analysis.technical_details.get('tokenization_status', '未知')}
- **语言规范**: {technical_analysis.technical_details.get('identifier_rules', '无')}
- **语法要求**: {technical_analysis.technical_details.get('syntax_requirements', '无')}

### 修复代码
```{technical_analysis.programming_language.value.lower()}
{technical_analysis.fix_code}
```

### 验证步骤
{chr(10).join(f"{step}" for step in technical_analysis.verification_steps)}

### 预防措施
{chr(10).join(f"{measure}" for measure in technical_analysis.prevention_measures)}

## 分析要求
请基于以上技术分析结果，严格按照 BROKE 框架进行深入分析：
1. **Bug 识别**: 确认错误类型、语言、位置
2. **Root Cause**: 分析编译原理层面的根本原因
3. **Observation**: 观察错误模式和特征
4. **Knowledge**: 应用相关技术标准和最佳实践
5. **Execution**: 提供具体的修复和验证方案

请确保分析的精确性、专业性和可操作性。
"""
        return prompt


# 使用示例
if __name__ == "__main__":
    # 创建增强型 Prompt 系统
    prompt_system = EnhancedPromptSystem()
    
    # 示例查询和上下文
    query = "系统出现数据库连接超时错误，如何解决？"
    context = [
        {
            "content": "2024-01-15 10:30:15 ERROR Database connection timeout after 30 seconds",
            "score": 0.95
        },
        {
            "content": "2024-01-15 10:31:22 WARNING Connection pool exhausted, creating new connection",
            "score": 0.87
        }
    ]
    
    # 生成增强型 Prompt
    enhanced_prompt = prompt_system.build_enhanced_prompt(query, context)
    print("增强型 Prompt:")
    print(enhanced_prompt)
