import os

# chroma 不上传数据
os.environ["ANONYMIZED_TELEMETRY"] = "false"
os.environ["DISABLE_TELEMETRY"] = "1"
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

import json
import logging
import pandas as pd
from typing import Any, Dict, List, Tuple
import re
import numpy as np

# langchain
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_ollama import OllamaLLM, OllamaEmbeddings

# llama-index & chroma
import chromadb
from llama_index.core import Settings
from llama_index.core import Document
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

# 日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdvancedRAGSystem:
    """高级RAG系统 - 使用现有依赖包实现"""
    
    def __init__(self):
        self.query_analyzer = QueryAnalyzer()
        self.prompt_optimizer = PromptOptimizer()
        
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """深度查询分析"""
        return self.query_analyzer.analyze(query)
    
    def build_enhanced_prompt(self, query: str, context: str, intent: str) -> str:
        """构建增强的Prompt"""
        return self.prompt_optimizer.build_prompt(query, context, intent)


class QueryAnalyzer:
    """查询理解模块"""
    
    def __init__(self):
        self.error_patterns = {
            'error_code': r'ERROR\s+\d+|error\s+code\s+\d+',
            'timeout': r'timeout|time\s+out|响应超时|连接超时',
            'connection': r'connection|connect|连接|链接',
            'memory': r'memory|内存|OOM|out of memory',
            'database': r'database|db|mysql|oracle|数据库',
            'network': r'network|网络|ping|telnet'
        }
        
    def analyze(self, query: str) -> Dict[str, Any]:
        """分析查询意图和特征"""
        return {
            'original_query': query,
            'technical_terms': self._extract_technical_terms(query),
            'query_type': self._classify_query_type(query),
            'complexity': self._assess_complexity(query),
            'expanded_queries': self._query_expansion(query)
        }
    
    def _extract_technical_terms(self, query: str) -> List[str]:
        """提取技术术语"""
        terms = []
        for category, pattern in self.error_patterns.items():
            matches = re.findall(pattern, query, re.IGNORECASE)
            terms.extend(matches)
        return terms
    
    def _classify_query_type(self, query: str) -> str:
        """分类查询类型"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['怎么', '如何', '解决', '修复']):
            return "solution"
        elif any(word in query_lower for word in ['原因', '为什么', '为何']):
            return "diagnosis" 
        elif any(word in query_lower for word in ['是什么', '解释', '说明']):
            return "explanation"
        else:
            return "general"
    
    def _assess_complexity(self, query: str) -> str:
        """评估问题复杂度"""
        terms_count = len(self._extract_technical_terms(query))
        if terms_count >= 3:
            return "high"
        elif terms_count >= 1:
            return "medium"
        else:
            return "low"
    
    def _query_expansion(self, query: str) -> List[str]:
        """查询扩展"""
        expanded = [query]
        
        # 同义词扩展
        synonyms = {
            'timeout': ['响应超时', '连接超时', '执行超时'],
            'error': ['错误', '异常', '故障'],
            'memory': ['内存', 'RAM'],
            'database': ['数据库', 'DB']
        }
        
        for original, synonym_list in synonyms.items():
            if original in query.lower():
                for synonym in synonym_list:
                    expanded_query = query.replace(original, synonym)
                    expanded.append(expanded_query)
        
        return list(set(expanded))


class EnhancedRetriever:
    """增强检索器 - 仅使用现有依赖包"""
    
    def __init__(self, vector_index, documents: List[str]):
        self.vector_index = vector_index
        self.documents = documents
    
    def multi_query_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """多查询检索 - 使用查询扩展"""
        query_analyzer = QueryAnalyzer()
        query_analysis = query_analyzer.analyze(query)
        
        all_results = []
        
        # 对每个扩展查询进行检索
        for expanded_query in query_analysis['expanded_queries']:
            results = self.vector_search(expanded_query, top_k * 2)
            all_results.extend(results)
        
        # 去重和重排序
        unique_results = self._deduplicate_results(all_results)
        reranked_results = self._rerank_with_custom_rules(query, unique_results)
        
        return reranked_results[:top_k]
    
    def vector_search(self, query: str, top_k: int = 10) -> List[Dict]:
        """向量检索"""
        try:
            retriever = self.vector_index.as_retriever(similarity_top_k=top_k)
            results = retriever.retrieve(query)
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content": result.text,
                    "score": result.score,
                    "type": "vector"
                })
            return formatted_results
        except Exception as e:
            logger.error(f"向量检索失败: {e}")
            return []
    
    def _deduplicate_results(self, results: List[Dict]) -> List[Dict]:
        """结果去重"""
        seen_content = set()
        unique_results = []
        
        for result in results:
            # 使用内容的前100个字符作为去重依据
            content_preview = result["content"][:100]
            if content_preview not in seen_content:
                seen_content.add(content_preview)
                unique_results.append(result)
        
        return unique_results
    
    def _rerank_with_custom_rules(self, query: str, results: List[Dict]) -> List[Dict]:
        """使用自定义规则重排序"""
        if not results:
            return []
        
        query_terms = set(query.lower().split())
        
        for result in results:
            content = result["content"].lower()
            
            # 1. 基于向量相似度的基础分数
            base_score = result.get("score", 0)
            
            # 2. 查询术语匹配奖励
            content_terms = set(content.split())
            term_overlap = len(query_terms.intersection(content_terms))
            term_bonus = min(0.3, term_overlap * 0.1)  # 最多30%奖励
            
            # 3. 内容长度惩罚（避免过长的文档）
            content_length = len(result["content"])
            length_penalty = 1.0
            if content_length > 1000:
                length_penalty = 0.8  # 长文档惩罚
            elif content_length < 100:
                length_penalty = 0.9  # 过短文档惩罚
            
            # 4. 技术术语匹配额外奖励
            technical_terms = QueryAnalyzer()._extract_technical_terms(query)
            tech_bonus = 0.0
            for term in technical_terms:
                if term.lower() in content:
                    tech_bonus += 0.05  # 每个技术术语5%奖励
            
            # 计算最终重排序分数
            result["rerank_score"] = base_score * (1 + term_bonus + tech_bonus) * length_penalty
        
        # 按重排序分数降序排列
        return sorted(results, key=lambda x: x["rerank_score"], reverse=True)


class PromptOptimizer:
    """Prompt优化器 - 实现思维链和结构化输出"""
    
    def __init__(self):
        self.templates = {
            "diagnosis": """
你是一个资深系统故障诊断专家。请按照以下步骤分析问题：

## 故障信息
{query}

## 相关技术背景
{context}

## 分析步骤
请按以下结构思考：

### 第一步：现象理解
- 故障的具体表现是什么？
- 影响哪些系统组件？
- 紧急程度如何评估？

### 第二步：原因推理  
- 基于技术文档，可能的原因有哪些？
- 按可能性从高到低排序
- 技术依据是什么？

### 第三步：解决方案
- 立即采取的应急措施
- 根本解决方案
- 验证方法

### 第四步：预防建议
- 如何避免类似问题？
- 监控和预警机制

请基于以上分析给出最终报告。
""",
            "solution": """
你是一个经验丰富的技术专家。请提供具体可行的解决方案：

问题：{query}

参考方案：
{context}

请提供：
1. **问题分析** - 简要说明问题本质
2. **具体步骤** - 详细的操作指南
3. **命令示例** - 需要执行的命令或代码
4. **验证方法** - 如何确认问题解决
5. **注意事项** - 可能遇到的坑和解决方法

确保方案具体、可操作、有针对性。
""",
            "general": """
基于以下信息回答问题：

问题：{query}

相关背景：
{context}

请提供专业、准确的分析。
"""
        }
    
    def build_prompt(self, query: str, context: str, intent: str) -> str:
        """构建优化后的Prompt"""
        template = self.templates.get(intent, self.templates["general"])
        return template.format(query=query, context=context)


class TopKLogSystem:
    def __init__(
            self,
            log_path: str,
            llm: str,
            embedding_model: str,
    ) -> None:
        # init models
        self.embedding_model = OllamaEmbeddings(model=embedding_model)
        self.llm = OllamaLLM(model=llm, temperature=0.1)

        # init advanced RAG components
        self.advanced_rag = AdvancedRAGSystem()
        
        # init database
        Settings.llm = self.llm
        Settings.embed_model = self.embedding_model

        self.log_path = log_path
        self.log_index = None
        self.enhanced_retriever = None
        self.documents_cache = []  # 缓存文档内容
        
        self._build_enhanced_vectorstore()

    def _build_enhanced_vectorstore(self):
        """构建增强的向量存储和检索系统"""
        vector_store_path = "./data/vector_stores"
        os.makedirs(vector_store_path, exist_ok=True)

        chroma_client = chromadb.PersistentClient(path=vector_store_path)
        log_collection = chroma_client.get_or_create_collection("log_collection")

        # 构建向量存储
        log_vector_store = ChromaVectorStore(chroma_collection=log_collection)
        log_storage_context = StorageContext.from_defaults(vector_store=log_vector_store)
        
        # 加载文档
        log_documents = self._load_documents_with_chunking(self.log_path)
        if log_documents:
            self.log_index = VectorStoreIndex.from_documents(
                log_documents,
                storage_context=log_storage_context,
                show_progress=True,
            )
            
            # 缓存文档内容
            self.documents_cache = [doc.text for doc in log_documents]
            
            # 初始化增强检索器
            self.enhanced_retriever = EnhancedRetriever(self.log_index, self.documents_cache)
            
            logger.info(f"增强索引构建完成，共 {len(log_documents)} 个文档块")

    def _load_documents_with_chunking(self, data_path: str) -> List[Document]:
        """使用智能分块加载文档"""
        if not os.path.exists(data_path):
            logger.warning(f"数据路径不存在: {data_path}")
            return []

        all_documents = []
        
        for file in os.listdir(data_path):
            ext = os.path.splitext(file)[1]
            if ext not in [".txt", ".md", ".json", ".jsonl", ".csv"]:
                continue

            file_path = f"{data_path}/{file}"
            try:
                if ext == ".csv":
                    # CSV文件分块处理
                    chunks = self._process_csv_file(file_path)
                    for chunk in chunks:
                        all_documents.append(Document(text=chunk))
                else:
                    # 文本文件智能分块
                    chunks = self._process_text_file(file_path)
                    for chunk in chunks:
                        all_documents.append(Document(text=chunk))
                        
            except Exception as e:
                logger.error(f"加载文档失败 {file_path}: {e}")
                
        return all_documents

    def _process_csv_file(self, file_path: str) -> List[str]:
        """处理CSV文件并分块"""
        chunks = []
        try:
            # 分块读取大型CSV
            chunk_size = 500
            for chunk_df in pd.read_csv(file_path, chunksize=chunk_size):
                for row in chunk_df.itertuples(index=False):
                    # 将每行转换为有意义的文本
                    row_text = " | ".join([f"{col}: {val}" for col, val in zip(chunk_df.columns, row)])
                    chunks.append(f"日志记录: {row_text}")
        except Exception as e:
            logger.error(f"处理CSV文件失败 {file_path}: {e}")
            
        return chunks

    def _process_text_file(self, file_path: str, chunk_size: int = 500) -> List[str]:
        """处理文本文件并分块"""
        chunks = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 简单的按段落分块
            paragraphs = content.split('\n\n')
            current_chunk = ""
            
            for paragraph in paragraphs:
                if len(current_chunk) + len(paragraph) <= chunk_size:
                    current_chunk += paragraph + "\n\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph + "\n\n"
                    
            if current_chunk:
                chunks.append(current_chunk.strip())
                
        except Exception as e:
            logger.error(f"处理文本文件失败 {file_path}: {e}")
            
        return chunks

    def retrieve_logs(self, query: str, top_k: int = 10) -> List[Dict]:
        """增强的检索方法 - 使用多查询检索"""
        if not self.enhanced_retriever:
            return []

        try:
            # 使用多查询检索
            results = self.enhanced_retriever.multi_query_search(query, top_k)
            return results
        except Exception as e:
            logger.error(f"增强检索失败: {e}")
            # 降级到基础向量检索
            return self._fallback_vector_search(query, top_k)

    def _fallback_vector_search(self, query: str, top_k: int) -> List[Dict]:
        """降级检索方法"""
        try:
            retriever = self.log_index.as_retriever(similarity_top_k=top_k)
            results = retriever.retrieve(query)
            
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "content": result.text,
                    "score": result.score
                })
            return formatted_results
        except Exception as e:
            logger.error(f"降级检索失败: {e}")
            return []

    def generate_response(self, query: str, context_docs: List[Dict]) -> str:
        """增强的响应生成 - 使用高级Prompt工程"""
        try:
            # 查询分析
            query_analysis = self.advanced_rag.analyze_query(query)
            
            # 构建上下文
            context = self._build_structured_context(context_docs, query_analysis)
            
            # 构建优化Prompt
            prompt = self.advanced_rag.build_enhanced_prompt(
                query, context, query_analysis['query_type']
            )
            
            # 生成响应
            response = self.llm.invoke(prompt)
            return response
            
        except Exception as e:
            logger.error(f"增强响应生成失败: {e}")
            return f"生成响应时出错: {str(e)}"

    def _build_structured_context(self, docs: List[Dict], analysis: Dict) -> str:
        """构建结构化的上下文"""
        if not docs:
            return "暂无相关技术文档"
        
        context_parts = []
        
        # 根据查询类型选择不同的上下文组织方式
        if analysis['query_type'] == 'diagnosis':
            # 对于诊断类问题，优先包含错误模式和原因分析
            context_parts.append("## 相关错误模式和原因分析")
        elif analysis['query_type'] == 'solution':
            # 对于解决方案类问题，优先包含操作指南
            context_parts.append("## 相关解决方案和操作指南")
        else:
            context_parts.append("## 相关技术文档")
        
        # 添加检索到的文档
        for i, doc in enumerate(docs[:5], 1):  # 限制前5个最相关的
            score = doc.get('rerank_score', doc.get('score', 0))
            context_parts.append(f"文档 {i} (相关度: {score:.3f}):")
            context_parts.append(doc['content'])
            context_parts.append("")  # 空行分隔
        
        return "\n".join(context_parts)

    def query(self, query: str) -> Dict:
        """增强的查询方法"""
        # 1. 增强检索
        retrieved_docs = self.retrieve_logs(query)
        
        # 2. 查询分析
        query_analysis = self.advanced_rag.analyze_query(query)
        
        # 3. 生成响应
        response = self.generate_response(query, retrieved_docs)
        
        return {
            "response": response,
            "retrieval_stats": {
                "total_retrieved": len(retrieved_docs),
                "query_analysis": query_analysis,
                "top_docs": retrieved_docs[:3] if retrieved_docs else []
            }
        }


# 示例使用
if __name__ == "__main__":
    # 初始化增强系统
    system = TopKLogSystem(
        log_path="./data/log",
        llm="deepseek-r1:7b",
        embedding_model="bge-large:latest"
    )

    # 测试查询
    query = "如何解决数据库连接池耗尽的问题？"
    result = system.query(query)

    print(f"查询: {query}")
    print(f"响应: {result['response']}")
    print(f"检索统计: {result['retrieval_stats']['total_retrieved']} 个相关文档")
    print(f"查询类型: {result['retrieval_stats']['query_analysis']['query_type']}")
    print(f"复杂度: {result['retrieval_stats']['query_analysis']['complexity']}")
