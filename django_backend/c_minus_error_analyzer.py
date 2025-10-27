"""
C-- 词法错误分析和 RAG 问题分析专用模块
严格按照文档 1 规则进行精准分析
"""

import re
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass


class ErrorCategory(Enum):
    """错误类别"""
    LEXICAL_ERROR = "lexical_error"  # 词法错误
    RAG_RETRIEVAL_ERROR = "rag_retrieval_error"  # RAG检索错误


class TokenType(Enum):
    """词法分析 Token 类型（基于文档 1）"""
    IDN = "IDN"  # 标识符
    KW_INT = "KW_INT"  # 关键字 int (1)
    KW_VOID = "KW_VOID"  # 关键字 void (2)
    KW_RETURN = "KW_RETURN"  # 关键字 return (3)
    KW_CONST = "KW_CONST"  # 关键字 const (4)
    KW_MAIN = "KW_MAIN"  # 关键字 main (5)
    KW_FLOAT = "KW_FLOAT"  # 关键字 float (6)
    KW_IF = "KW_IF"  # 关键字 if (7)
    KW_ELSE = "KW_ELSE"  # 关键字 else (8)
    INT = "INT"  # 整数
    FLOAT = "FLOAT"  # 浮点数
    OP = "OP"  # 运算符
    SE = "SE"  # 界符
    ILLEGAL = "ILLEGAL"  # 非法符号


@dataclass
class LexicalErrorAnalysis:
    """词法错误分析结果"""
    error_type: str
    violated_rule: str  # 违反的文档条款
    error_location: str  # 错误位置（行号+列号）
    rule_category: str  # 数据类型/符号类型
    fix_suggestion: str  # 修复建议（需对应条款）
    verification_steps: List[str]  # 验证步骤（文档 1 标准操作）


@dataclass
class RAGErrorAnalysis:
    """RAG 检索错误分析结果"""
    fault_chain: List[str]  # 故障链路
    violated_rules: List[str]  # 每环节违反的文档规则
    fix_steps: List[str]  # 分步修复（文档 1 标准操作）
    prevention_measures: List[str]  # 预防措施


class CMinusErrorAnalyzer:
    """C-- 词法错误分析器（严格基于文档 1 规则）"""
    
    def __init__(self):
        self.token_patterns = self._initialize_token_patterns()
        self.rag_rules = self._initialize_rag_rules()
    
    def _initialize_token_patterns(self) -> Dict[str, dict]:
        """初始化 C-- Token 模式（基于文档 1）"""
        return {
            # 关键字模式（8个关键字，不区分大小写）
            "keywords": {
                r"int\b": (TokenType.KW_INT, "keyword int (1)"),
                r"void\b": (TokenType.KW_VOID, "keyword void (2)"),
                r"return\b": (TokenType.KW_RETURN, "keyword return (3)"),
                r"const\b": (TokenType.KW_CONST, "keyword const (4)"),
                r"main\b": (TokenType.KW_MAIN, "keyword main (5)"),
                r"float\b": (TokenType.KW_FLOAT, "keyword float (6)"),
                r"if\b": (TokenType.KW_IF, "keyword if (7)"),
                r"else\b": (TokenType.KW_ELSE, "keyword else (8)"),
            },
            # 标识符模式（文档 1.1）
            "identifier": {
                "rule": r"^[a-zA-Z_][a-zA-Z0-9_]*$",
                "description": "标识符（IDN）：由字母/下划线开头，后接字母/数字/下划线，禁止包含$、#等特殊字符"
            },
            # 运算符模式（22个运算符，长匹配优先）
            "operators": {
                r"==": (TokenType.OP, "operator == (17)"),
                r"&&": (TokenType.OP, "operator && (21)"),
                # ... 更多运算符
            },
            # 整数模式（文档 1.1）
            "integer": {
                "rule": r"^\d+$",
                "description": "整数（INT）：纯数字序列，如 123、0"
            },
            # 浮点数模式（文档 1.1）
            "float": {
                "rule": r"^\d+\.\d+$",  # 必须前后都有数字
                "description": "浮点数（FLOAT）：必须包含且仅包含1个小数点，小数点前后均需有数字"
            },
        }
    
    def _initialize_rag_rules(self) -> Dict[str, str]:
        """初始化 RAG 模块规则（基于文档 1）"""
        return {
            "log_file_format": "仅支持.txt、.md、.json、.jsonl、.csv格式",
            "log_file_path": "存储路径默认../data/log（因service.py在deepseek_api目录）",
            "vector_store_path": "Chroma向量库持久化路径为./data/vector_stores",
            "collection_name": "collection名称固定为log_collection",
            "csv_chunk_size": "CSV文件需分块读取（默认1000行/块）",
            "retrieve_top_k": "retrieve_logs()方法默认top_k=10（返回Top10相似日志）",
            "build_vectorstore_method": "需调用_build_vectorstore()重建向量库"
        }
    
    def analyze_error(self, error_message: str) -> Dict[str, Any]:
        """分析错误（自动识别词法错误或RAG错误）"""
        # 检测错误类型
        if "Lexical Analysis Failed" in error_message or "lexical_error" in error_message.lower():
            return self._analyze_lexical_error(error_message)
        elif "RAG Retrieval Failed" in error_message or "vector store" in error_message.lower():
            return self._analyze_rag_error(error_message)
        else:
            return {"error": "无法识别的错误类型"}
    
    def _analyze_lexical_error(self, error_message: str) -> Dict[str, Any]:
        """分析词法错误（严格基于文档 1.1 C--词法规则）"""
        analysis = {
            "error_category": ErrorCategory.LEXICAL_ERROR.value,
            "document_rules": [],
            "analysis_layers": {},
            "fix_code": "",
            "verification": []
        }
        
        # 提取错误位置
        line_match = re.search(r"Line (\d+)", error_message)
        col_match = re.search(r"Column (\d+)", error_message)
        line_num = line_match.group(1) if line_match else "未知"
        col_num = col_match.group(1) if col_match else "未知"
        
        # 提取错误上下文
        context_match = re.search(r'Nearby source: "([^"]+)"', error_message)
        error_context = context_match.group(1) if context_match else ""
        
        # 分析错误类型并关联文档规则
        if "float" in error_message.lower() or "FLOAT" in error_message:
            # 浮点数格式错误
            analysis["error_type"] = "浮点数格式错误"
            analysis["document_rules"] = [
                "违反浮点数（FLOAT）规则：文档 1.1 要求浮点数必须包含且仅包含1个小数点，小数点前后均有数字",
                "错误示例：36.（无小数部分）、.6（无整数部分）均为非法格式"
            ]
            analysis["rule_category"] = "FLOAT（浮点数类型）"
            
            # 生成修复建议
            if "36." in error_context:
                analysis["fix_code"] = '// 修复前：float temp = 36.;\n// 修复后：float temp = 36.0;  // 或 float temp = 36.;改为float temp = 36.0;'
            
            # 验证步骤
            analysis["verification"] = [
                "1. 修改源代码中的浮点数格式",
                "2. 执行 flex lexer.l && gcc lex.yy.c -o lexer",
                "3. 执行 ./lexer test_fix.c-- 验证，确保无<ERROR>输出"
            ]
        
        elif "$" in error_message or "Invalid character" in error_message:
            # 标识符非法字符错误
            analysis["error_type"] = "标识符非法字符错误"
            analysis["document_rules"] = [
                "违反标识符（IDN）规则：文档 1.1 要求标识符由字母/下划线开头，后接字母/数字/下划线",
                "禁止包含$、#等特殊字符（C--无预处理指令）"
            ]
            analysis["rule_category"] = "IDN（标识符类型）"
            
            # 生成修复建议
            if "$" in error_context:
                analysis["fix_code"] = '// 修复前：int $count = 42;\n// 修复后：int count = 42;  // 或 int _count = 42;'
            
            # 验证步骤
            analysis["verification"] = [
                "1. 将变量名中的$替换为字母或下划线",
                "2. 执行 flex lexer.l && gcc lex.yy.c -o lexer",
                "3. 执行 ./lexer test_fix.c-- 验证，确保无<ERROR>输出"
            ]
        
        else:
            # 其他词法错误
            analysis["error_type"] = "其他词法错误"
            analysis["document_rules"] = [
                "违反 C-- 词法规则（文档 1.1）：需按长匹配优先原则识别，如==优先于=、&&优先于&"
            ]
            analysis["rule_category"] = "词法分析"
        
        # 构建分析层级（用于 Prompt 生成）
        analysis["analysis_layers"] = {
            "错误位置": f"第 {line_num} 行，第 {col_num} 列"
        }
        
        return analysis
    
    def _analyze_rag_error(self, error_message: str) -> Dict[str, Any]:
        """分析 RAG 检索错误（严格基于文档 1.2 RAG模块规则）"""
        analysis = {
            "error_category": ErrorCategory.RAG_RETRIEVAL_ERROR.value,
            "document_rules": [],
            "fault_chain": [],
            "fix_steps": [],
            "prevention": []
        }
        
        # 构建故障链路
        if "Empty vector store" in error_message or "vector store collection" in error_message:
            analysis["fault_chain"] = [
                "日志文件缺失或加载失败 → 向量库为空 → 检索失败"
            ]
            analysis["document_rules"] = [
                "违反文档 1.2 RAG 模块规则：日志文件路径应为../data/log（service.py所在目录）",
                "违反文档 1.2 RAG 模块规则：仅支持.txt、.md、.json、.jsonl、.csv格式",
                "违反文档 1.2 RAG 模块规则：需通过_build_vectorstore()构建向量库"
            ]
            
            # 分步修复
            analysis["fix_steps"] = [
                "1. 检查日志文件路径：ls ../data/log（验证文件存在性）",
                "2. 验证日志文件内容：cat ../data/log/test.log",
                "3. 重建向量库：在Python交互环境中执行：",
                "   from deepseek_api.service import topklogsystem",
                "   topklogsystem._build_vectorstore()",
                "4. 验证检索：通过API调用验证检索功能正常"
            ]
            
            analysis["prevention"] = [
                "启动后端前检查日志文件是否存在",
                "确保日志文件格式符合文档要求（.txt、.md、.json、.jsonl、.csv）",
                "初始化TopKLogSystem时自动调用_build_vectorstore()构建索引",
                "定期检查向量库状态，避免空集合"
            ]
        
        # 构建分析层级
        analysis["analysis_layers"] = {
            "故障链路": analysis["fault_chain"],
            "每环节违反的文档规则": analysis["document_rules"],
            "分步修复": analysis["fix_steps"],
            "预防措施": analysis["prevention"]
        }
        
        return analysis
    
    def build_prompt(self, error_message: str) -> str:
        """构建基于文档规则的精准分析 Prompt"""
        analysis = self.analyze_error(error_message)
        
        if analysis["error_category"] == ErrorCategory.LEXICAL_ERROR.value:
            return self._build_lexical_prompt(analysis)
        else:
            return self._build_rag_prompt(analysis)
    
    def _build_lexical_prompt(self, analysis: Dict[str, Any]) -> str:
        """构建词法错误分析 Prompt（强制关联文档 1）"""
        prompt = f"""你是 C-- 词法分析专家，精通编译原理和《智能数据分析任务书》文档 1.1 章节的 C-- 词法规则。

## 错误分析要求
必须严格按照以下分析逻辑，强制关联文档 1 中的 C-- 词法规则：

### 错误类型
{analysis.get('error_type', '词法错误')}

### 文档规则关联（强制）
**必须引用文档 1.1 的具体条款：**
{chr(10).join(f"- {rule}" for rule in analysis.get('document_rules', []))}

**规则类别**：{analysis.get('rule_category', '未知')}

### 错误位置
{analysis.get('analysis_layers', {}).get('错误位置', '未知')}

### 修复方案（绑定实验流程）
必须使用文档 1 中的标准操作：

```bash
# 修复源代码后
flex lexer.l
gcc lex.yy.c -o lexer
./lexer test_fix.c--  # 验证无<ERROR>输出
```

{chr(10).join(f"**步骤{i+1}**：{step}" for i, step in enumerate(analysis.get('verification', []), 0))}

## 输出格式（Markdown 三级标题）
必须使用以下格式输出分析结果：

### 错误类型
[详细描述错误类型]

### 文档规则关联
[引用文档 1.1 的具体条款，标注规则类型]

### 修复方案
[提供可直接执行的修复代码和验证步骤]

## 禁止事项
- 禁止泛化建议（如"使用语法检查工具"），必须明确为"使用文档1中的flex+gcc编译词法分析器"
- 禁止脱离文档规则进行分析
- 必须提供可直接按文档流程执行的修复方案
"""
        return prompt
    
    def _build_rag_prompt(self, analysis: Dict[str, Any]) -> str:
        """构建 RAG 错误分析 Prompt（强制关联文档 1）"""
        prompt = f"""你是 RAG 系统专家，精通《智能数据分析任务书》文档 1.2 章节的 RAG 模块规则。

## 错误分析要求
必须严格按照以下分析逻辑，强制关联文档 1.2 RAG 模块规则：

### 错误类型
RAG 检索失败

### 文档规则关联（强制）
**必须引用文档 1.2 的具体条款：**
{chr(10).join(f"- {rule}" for rule in analysis.get('document_rules', []))}

### 故障链路（分层引导）
{chr(10).join(f"- {step}" for step in analysis.get('fault_chain', []))}

### 修复方案（绑定实验流程）
必须使用文档 1.2 中的标准方法：

{chr(10).join(f"**步骤{i+1}**：{step}" for i, step in enumerate(analysis.get('fix_steps', []), 0))}

## 输出格式（Markdown 三级标题）
必须使用以下格式输出分析结果：

### 错误类型
[描述 RAG 检索失败的类型]

### 文档规则关联
[引用文档 1.2 RAG 模块的具体规则]

### 修复方案
[提供分步修复，每一步必须对应文档 1.2 的标准操作]

### 预防措施
[提供启动前的检查清单]

## 禁止事项
- 禁止泛化建议（如"检查向量库"），必须明确为"执行 topklogsystem._build_vectorstore()"
- 禁止脱离文档规则进行分析
- 必须提供可直接按文档流程执行的修复命令
"""
        return prompt


# 使用示例
if __name__ == "__main__":
    analyzer = CMinusErrorAnalyzer()
    
    # 示例1：词法错误
    error1 = '[ERROR] Lexical Analysis Failed (Line 8, Column 12): Mismatched float literal format detected. Nearby source: "float temp = 36.;" Diagnostic: Float literal "36." violates C-- syntax'
    
    # 示例2：RAG错误
    error2 = '[ERROR] RAG Retrieval Failed (Line 45, Function: retrieve_logs): Empty vector store collection "log_collection" detected. Nearby source: "related_logs = topklogsystem.retrieve_logs(query)"'
    
    print("=== 词法错误分析 ===")
    result1 = analyzer.analyze_error(error1)
    print(result1)
    
    print("\n=== RAG 错误分析 ===")
    result2 = analyzer.analyze_error(error2)
    print(result2)
