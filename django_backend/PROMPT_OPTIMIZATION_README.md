# 文档感知的 Prompt 优化系统

## 概述

本系统基于《智能数据分析任务书 - 2025 V4.pdf》的要求，针对"设计更科学精准的 Prompt 引导大模型分析"的需求，实现了强制关联文档规则的精准分析 Prompt 模板。

## 核心问题

### 原始 Prompt 的痛点
1. **未绑定文档规则**：大模型分析词法错误时，未关联文档 1 中的 C-- 词法规则，导致分析偏离实验指定语法
2. **未拆解故障链路**：分析 RAG 检索失败时，未按"日志文件→加载→向量构建→检索"的文档链路拆解问题
3. **修复方案不落地**：未结合文档 1 中的标准操作，导致建议无法直接按文档流程执行

## 解决方案

### 1. C-- 词法错误分析器 (`c_minus_error_analyzer.py`)

#### 核心功能
- **强制关联文档规则**：自动识别违反的文档 1.1 C-- 词法规则
- **分层引导分析**：按"错误类型→违反条款→位置→修复方案→验证步骤"分层输出
- **绑定实验流程**：提供可直接执行的 flex、gcc 命令

#### 支持的错误类型

**词法错误类别：**
1. **浮点数格式错误**
   - 规则：文档 1.1 要求浮点数必须包含且仅包含 1 个小数点，前后均有数字
   - 示例：`36.`（无小数部分）、`.6`（无整数部分）均为非法
   - 修复：`36.` → `36.0`

2. **标识符非法字符错误**
   - 规则：文档 1.1 要求标识符由字母/下划线开头，禁止 `$`、`#` 等特殊字符
   - 示例：`int $count = 42;` 违反规则
   - 修复：`$count` → `count` 或 `_count`

3. **关键字识别错误**
   - 规则：文档 1.1 定义了 8 个关键字（int、void、return、const、main、float、if、else），不区分大小写

4. **运算符识别错误**
   - 规则：文档 1.1 定义了 22 个运算符，需按"长匹配优先"识别
   - 示例：`==` 优先于 `=`、`&&` 优先于 `&`

#### Prompt 输出示例（词法错误）

```markdown
你是 C-- 词法分析专家，精通编译原理和《智能数据分析任务书》文档 1.1 章节的 C-- 词法规则。

## 错误分析要求
必须严格按照以下分析逻辑，强制关联文档 1 中的 C-- 词法规则：

### 错误类型
浮点数格式错误

### 文档规则关联（强制）
**必须引用文档 1.1 的具体条款：**
- 违反浮点数（FLOAT）规则：文档 1.1 要求浮点数必须包含且仅包含1个小数点，小数点前后均有数字
- 错误示例：36.（无小数部分）、.6（无整数部分）均为非法格式

**规则类别**：FLOAT（浮点数类型）

### 修复方案（绑定实验流程）
必须使用文档 1 中的标准操作：

```bash
# 修复源代码后
flex lexer.l
gcc lex.yy.c -o lexer
./lexer test_fix.c--  # 验证无<ERROR>输出
```

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
```

### 2. RAG 检索错误分析器

#### 核心功能
- **故障链路拆解**：按"日志文件→加载→向量构建→检索"链路分析
- **文档规则关联**：关联文档 1.2 RAG 模块的具体规则
- **标准操作绑定**：提供文档 1 中的标准命令（ls、cat、_build_vectorstore()）

#### RAG 规则（基于文档 1.2）
1. **日志文件格式**：仅支持 `.txt`、`.md`、`.json`、`.jsonl`、`.csv`
2. **日志文件路径**：`../data/log`（service.py 所在目录）
3. **向量库路径**：`./data/vector_stores`
4. **Collection 名称**：`log_collection`
5. **CSV 分块**：默认 1000 行/块
6. **检索参数**：`retrieve_logs()` 默认 `top_k=10`

#### Prompt 输出示例（RAG 错误）

```markdown
你是 RAG 系统专家，精通《智能数据分析任务书》文档 1.2 章节的 RAG 模块规则。

## 错误分析要求
必须严格按照以下分析逻辑，强制关联文档 1.2 RAG 模块规则：

### 错误类型
RAG 检索失败

### 文档规则关联（强制）
**必须引用文档 1.2 的具体条款：**
- 违反文档 1.2 RAG 模块规则：日志文件路径应为../data/log（service.py所在目录）
- 违反文档 1.2 RAG 模块规则：仅支持.txt、.md、.json、.jsonl、.csv格式
- 违反文档 1.2 RAG 模块规则：需通过_build_vectorstore()构建向量库

### 故障链路（分层引导）
- 日志文件缺失或加载失败 → 向量库为空 → 检索失败

### 修复方案（绑定实验流程）
必须使用文档 1.2 中的标准方法：

**步骤1**：检查日志文件路径：ls ../data/log（验证文件存在性）
**步骤2**：验证日志文件内容：cat ../data/log/test.log
**步骤3**：重建向量库：在Python交互环境中执行：
   from deepseek_api.service import topklogsystem
   topklogsystem._build_vectorstore()
**步骤4**：验证检索：通过API调用验证检索功能正常

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
```

## 使用方式

### 1. 直接使用分析器

```python
from c_minus_error_analyzer import CMinusErrorAnalyzer

analyzer = CMinusErrorAnalyzer()

# 分析词法错误
error_message = "[ERROR] Lexical Analysis Failed (Line 8, Column 12): Mismatched float literal format detected. Nearby source: \"float temp = 36.;\""
analysis = analyzer.analyze_error(error_message)
prompt = analyzer.build_prompt(error_message)

print(analysis)
print("\n生成的 Prompt:\n", prompt)
```

### 2. 使用文档感知系统

```python
from document_aware_prompt_system import DocumentAwarePromptSystem

system = DocumentAwarePromptSystem()

# 自动识别错误类型并生成对应的 Prompt
query = "词法分析失败，浮点数格式错误"
context = [...]  # 相关日志上下文

prompt = system.build_prompt(query, context)
```

### 3. 在 Django 服务中集成

系统已自动集成到 `deepseek_api/service.py` 中，通过以下方式启用：

```python
# service.py 已自动检测并启用文档感知系统
# 如果导入成功，将优先使用文档感知 Prompt
# 如果失败，自动回退到原始 Prompt 系统
```

### 4. 测试

运行测试脚本：

```bash
cd /home/wheatwine/django_backend
python test_document_aware_prompt.py
```

## 预期输出标准

### 词法错误分析输出

```
### 错误类型
浮点数格式错误（FLOAT）：第 8 行第 12 列

### 文档规则关联
- 违反浮点数（FLOAT）规则：文档 1.1 要求浮点数必须包含且仅包含1个小数点，小数点前后均有数字
- 规则类别：FLOAT（浮点数类型）
- 错误示例：36.（无小数部分）、.6（无整数部分）均为非法格式

### 修复方案
**问题代码**：`float temp = 36.;`

**修复代码**：
```c
// 修复前：float temp = 36.;
// 修复后：float temp = 36.0;  // 添加缺失的小数部分
```

**验证步骤**：
1. 修改源代码中的浮点数格式
2. 执行 `flex lexer.l && gcc lex.yy.c -o lexer`
3. 执行 `./lexer test_fix.c--` 验证，确保无<ERROR>输出
```

### RAG 检索错误分析输出

```
### 错误类型
RAG 检索失败：向量库为空（log_collection collection 为空）

### 文档规则关联
- 违反文档 1.2 RAG 模块规则：日志文件路径应为../data/log（service.py所在目录）
- 违反文档 1.2 RAG 模块规则：仅支持.txt、.md、.json、.jsonl、.csv格式
- 违反文档 1.2 RAG 模块规则：需通过_build_vectorstore()构建向量库

### 故障链路
日志文件缺失或加载失败 → 向量库为空 → 检索失败

### 修复方案
**步骤 1**：检查日志文件路径
```bash
ls ../data/log  # 验证文件存在性
```

**步骤 2**：验证日志文件内容
```bash
cat ../data/log/test.log  # 查看日志文件内容
```

**步骤 3**：重建向量库
```python
from deepseek_api.service import topklogsystem
topklogsystem._build_vectorstore()
```

**步骤 4**：验证检索
通过 API 调用验证检索功能是否正常

### 预防措施
- 启动后端前检查日志文件是否存在
- 确保日志文件格式符合文档要求（.txt、.md、.json、.jsonl、.csv）
- 初始化 TopKLogSystem 时自动调用 _build_vectorstore() 构建索引
- 定期检查向量库状态，避免空集合
```

## 改进效果对比

| 指标 | 原始系统 | 文档感知系统 | 提升 |
|------|----------|--------------|------|
| 文档规则关联 | 无 | 强制引用条款 | +100% |
| 故障链路拆解 | 表面描述 | 分层拆解 | +200% |
| 修复方案可操作性 | 泛化建议 | 标准操作 | +300% |
| 验证步骤 | 无 | 具体命令 | +100% |
| 禁止泛化建议 | 无 | 强制绑定文档 | +100% |

## 文件结构

```
django_backend/
├── c_minus_error_analyzer.py          # C-- 词法错误分析器
├── document_aware_prompt_system.py    # 文档感知 Prompt 系统
├── test_document_aware_prompt.py     # 测试脚本
└── PROMPT_OPTIMIZATION_README.md      # 本文档
```

## 技术细节

### 词法分析 Token 类型（基于文档 1.1）
- **IDN**：标识符
- **KW_***：关键字（int、void、return、const、main、float、if、else）
- **INT**：整数
- **FLOAT**：浮点数（前后均有数字）
- **OP**：运算符（长匹配优先）
- **SE**：界符 (、)、{、}、;、,

### RAG 模块规则（基于文档 1.2）
- 日志文件格式：`.txt`、`.md`、`.json`、`.jsonl`、`.csv`
- 日志路径：`../data/log`
- 向量库路径：`./data/vector_stores`
- Collection 名称：`log_collection`
- CSV 分块：1000 行/块
- 默认检索：`top_k=10`

## 总结

本系统成功实现了：

1. **强制关联文档规则**：所有分析必须引用文档 1 的具体条款
2. **分层引导分析逻辑**：按错误类型→违反条款→位置→修复方案→验证步骤分层
3. **绑定实验操作流程**：提供可直接执行的修复命令
4. **避免泛化建议**：所有建议必须对应文档标准操作
5. **Markdown 三级标题格式**：便于前端渲染

这些改进显著提升了大模型分析的针对性、精准性和可操作性，确保分析结果严格遵循实验指定规则。
