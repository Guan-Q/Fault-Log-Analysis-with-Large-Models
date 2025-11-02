"""
技术错误分析框架
专门用于分析编译错误、语法错误等技术问题
"""

import re
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass


class ErrorType(Enum):
    """错误类型枚举"""
    LEXICAL_ERROR = "lexical_error"  # 词法错误
    SYNTAX_ERROR = "syntax_error"    # 语法错误
    SEMANTIC_ERROR = "semantic_error"  # 语义错误
    RUNTIME_ERROR = "runtime_error"  # 运行时错误
    LINKING_ERROR = "linking_error"  # 链接错误


class ProgrammingLanguage(Enum):
    """编程语言枚举"""
    C_MINUS_MINUS = "C--"  # C--
    C_PLUS_PLUS = "C++"   # C++
    JAVA = "Java"         # Java
    PYTHON = "Python"     # Python
    JAVASCRIPT = "JavaScript"  # JavaScript
    GO = "Go"             # Go
    RUST = "Rust"         # Rust


@dataclass
class ErrorLocation:
    """错误位置信息"""
    file_name: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    context: Optional[str] = None


@dataclass
class TechnicalErrorAnalysis:
    """技术错误分析结果"""
    error_type: ErrorType
    programming_language: ProgrammingLanguage
    location: ErrorLocation
    root_cause: str
    technical_details: Dict[str, Any]
    fix_code: str
    verification_steps: List[str]
    prevention_measures: List[str]


class TechnicalErrorAnalyzer:
    """技术错误分析器"""
    
    def __init__(self):
        self.language_patterns = self._initialize_language_patterns()
        self.error_patterns = self._initialize_error_patterns()
        self.fix_templates = self._initialize_fix_templates()
    
    def _initialize_language_patterns(self) -> Dict[str, ProgrammingLanguage]:
        """初始化语言识别模式"""
        return {
            r"C--": ProgrammingLanguage.C_MINUS_MINUS,
            r"C\+\+": ProgrammingLanguage.C_PLUS_PLUS,
            r"Java": ProgrammingLanguage.JAVA,
            r"Python": ProgrammingLanguage.PYTHON,
            r"JavaScript": ProgrammingLanguage.JAVASCRIPT,
            r"Go": ProgrammingLanguage.GO,
            r"Rust": ProgrammingLanguage.RUST,
        }
    
    def _initialize_error_patterns(self) -> Dict[str, ErrorType]:
        """初始化错误类型识别模式"""
        return {
            r"Lexical Analysis Failed": ErrorType.LEXICAL_ERROR,
            r"Tokenization aborted": ErrorType.LEXICAL_ERROR,
            r"Unexpected token": ErrorType.LEXICAL_ERROR,
            r"Syntax Error": ErrorType.SYNTAX_ERROR,
            r"Parse Error": ErrorType.SYNTAX_ERROR,
            r"Semantic Error": ErrorType.SEMANTIC_ERROR,
            r"Type Error": ErrorType.SEMANTIC_ERROR,
            r"Runtime Error": ErrorType.RUNTIME_ERROR,
            r"Segmentation Fault": ErrorType.RUNTIME_ERROR,
            r"Linking Error": ErrorType.LINKING_ERROR,
            r"Undefined Reference": ErrorType.LINKING_ERROR,
        }
    
    def _initialize_fix_templates(self) -> Dict[str, str]:
        """初始化修复模板"""
        return {
            "invalid_identifier": """
// 修复前
int $count = 42;

// 修复后
int count = 42;
// 或者
int _count = 42;
""",
            "unexpected_token": """
// 修复前
int count = 42; // 错误的语法

// 修复后
int count = 42; // 正确的语法
""",
            "missing_semicolon": """
// 修复前
int count = 42

// 修复后
int count = 42;
""",
        }
    
    def analyze_error(self, error_message: str) -> TechnicalErrorAnalysis:
        """分析技术错误"""
        # 识别编程语言
        language = self._detect_language(error_message)
        
        # 识别错误类型
        error_type = self._detect_error_type(error_message)
        
        # 提取错误位置
        location = self._extract_location(error_message)
        
        # 分析根本原因
        root_cause = self._analyze_root_cause(error_message, error_type, language)
        
        # 生成技术细节
        technical_details = self._generate_technical_details(error_message, error_type, language)
        
        # 生成修复代码
        fix_code = self._generate_fix_code(error_message, error_type, language)
        
        # 生成验证步骤
        verification_steps = self._generate_verification_steps(error_type, language)
        
        # 生成预防措施
        prevention_measures = self._generate_prevention_measures(error_type, language)
        
        return TechnicalErrorAnalysis(
            error_type=error_type,
            programming_language=language,
            location=location,
            root_cause=root_cause,
            technical_details=technical_details,
            fix_code=fix_code,
            verification_steps=verification_steps,
            prevention_measures=prevention_measures
        )
    
    def _detect_language(self, error_message: str) -> ProgrammingLanguage:
        """检测编程语言"""
        for pattern, language in self.language_patterns.items():
            if re.search(pattern, error_message):
                return language
        
        # 默认返回 C--
        return ProgrammingLanguage.C_MINUS_MINUS
    
    def _detect_error_type(self, error_message: str) -> ErrorType:
        """检测错误类型"""
        for pattern, error_type in self.error_patterns.items():
            if re.search(pattern, error_message, re.IGNORECASE):
                return error_type
        
        # 默认返回词法错误
        return ErrorType.LEXICAL_ERROR
    
    def _extract_location(self, error_message: str) -> ErrorLocation:
        """提取错误位置"""
        location = ErrorLocation()
        
        # 提取行号
        line_match = re.search(r"Line (\d+)", error_message)
        if line_match:
            location.line_number = int(line_match.group(1))
        
        # 提取列号
        column_match = re.search(r"Column (\d+)", error_message)
        if column_match:
            location.column_number = int(column_match.group(1))
        
        # 提取上下文
        context_match = re.search(r"Nearby source: \"([^\"]+)\"", error_message)
        if context_match:
            location.context = context_match.group(1)
        
        return location
    
    def _analyze_root_cause(self, error_message: str, error_type: ErrorType, language: ProgrammingLanguage) -> str:
        """分析根本原因"""
        if error_type == ErrorType.LEXICAL_ERROR:
            if "Unexpected token" in error_message:
                return "词法分析器在解析输入流时遇到了不符合语言规范的 token"
            elif "Invalid character" in error_message:
                return "变量名中包含了该编程语言不允许的字符"
            else:
                return "词法分析阶段失败，输入流无法正确 tokenize"
        
        elif error_type == ErrorType.SYNTAX_ERROR:
            return "语法分析阶段失败，代码结构不符合语言语法规范"
        
        elif error_type == ErrorType.SEMANTIC_ERROR:
            return "语义分析阶段失败，代码逻辑或类型使用有误"
        
        else:
            return "编译过程中发生了未预期的错误"
    
    def _generate_technical_details(self, error_message: str, error_type: ErrorType, language: ProgrammingLanguage) -> Dict[str, Any]:
        """生成技术细节"""
        details = {
            "error_message": error_message,
            "error_type": error_type.value,
            "programming_language": language.value,
            "compilation_phase": self._get_compilation_phase(error_type),
            "tokenization_status": "Failed" if error_type == ErrorType.LEXICAL_ERROR else "Success",
        }
        
        # 添加语言特定的技术细节
        if language == ProgrammingLanguage.C_MINUS_MINUS:
            details["identifier_rules"] = "C-- 语言要求标识符以字母或下划线开头，不能包含特殊字符如 $"
            details["syntax_requirements"] = "C-- 语言遵循 C 语言的基本语法结构"
        
        return details
    
    def _get_compilation_phase(self, error_type: ErrorType) -> str:
        """获取编译阶段"""
        phase_map = {
            ErrorType.LEXICAL_ERROR: "词法分析 (Lexical Analysis)",
            ErrorType.SYNTAX_ERROR: "语法分析 (Syntax Analysis)",
            ErrorType.SEMANTIC_ERROR: "语义分析 (Semantic Analysis)",
            ErrorType.RUNTIME_ERROR: "运行时 (Runtime)",
            ErrorType.LINKING_ERROR: "链接 (Linking)",
        }
        return phase_map.get(error_type, "未知阶段")
    
    def _generate_fix_code(self, error_message: str, error_type: ErrorType, language: ProgrammingLanguage) -> str:
        """生成修复代码"""
        if "Invalid character '$'" in error_message:
            return self.fix_templates["invalid_identifier"]
        elif "Unexpected token" in error_message:
            return self.fix_templates["unexpected_token"]
        else:
            return "// 需要根据具体错误信息进行修复"
    
    def _generate_verification_steps(self, error_type: ErrorType, language: ProgrammingLanguage) -> List[str]:
        """生成验证步骤"""
        steps = [
            f"1. 使用 {language.value} 编译器重新编译代码",
            "2. 检查编译输出，确认错误已解决",
            "3. 运行代码，验证功能正常",
        ]
        
        if error_type == ErrorType.LEXICAL_ERROR:
            steps.insert(1, "1.5. 检查变量名是否符合语言规范")
        
        return steps
    
    def _generate_prevention_measures(self, error_type: ErrorType, language: ProgrammingLanguage) -> List[str]:
        """生成预防措施"""
        measures = [
            f"1. 使用支持 {language.value} 语法高亮的编辑器",
            "2. 配置编译器的实时错误检查",
            "3. 遵循编程语言的命名规范",
            "4. 定期进行代码审查",
        ]
        
        if error_type == ErrorType.LEXICAL_ERROR:
            measures.extend([
                "5. 避免在标识符中使用特殊字符",
                "6. 使用代码格式化工具自动检查语法",
            ])
        
        return measures


# 使用示例
if __name__ == "__main__":
    analyzer = TechnicalErrorAnalyzer()
    
    # 示例错误信息
    error_msg = """
    [ERROR] Lexical Analysis Failed (Line 14, Column 8): Unexpected token '#' detected in input stream. 
    Tokenization aborted: - Current context: parsing variable declaration statement (expected identifier/keyword after 'int') 
    - Nearby source: "int $count = 42;" 
    - Diagnostic: Invalid character '$' in identifier (C-- syntax requires identifiers to start with [a-zA-Z_]) 
    - Suggested fix: Replace '$' with a valid starting character (e.g., 'count' or '_count')
    """
    
    # 分析错误
    analysis = analyzer.analyze_error(error_msg)
    
    print(f"错误类型: {analysis.error_type.value}")
    print(f"编程语言: {analysis.programming_language.value}")
    print(f"根本原因: {analysis.root_cause}")
    print(f"修复代码:\n{analysis.fix_code}")
    print(f"验证步骤: {analysis.verification_steps}")
    print(f"预防措施: {analysis.prevention_measures}")
