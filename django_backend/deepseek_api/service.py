# service.py 新增代码（文件顶部）
import os
import json
import logging
import pandas as pd
from typing import Any, Dict, List
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 导入原topklogsystem.py依赖的库（与你的代码一致）
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_ollama import OllamaLLM, OllamaEmbeddings
import chromadb
from llama_index.core import Settings, Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore

# 导入文档感知的 Prompt 系统
try:
    from document_aware_prompt_system import DocumentAwarePromptSystem
    DOCUMENT_AWARE_SYSTEM_AVAILABLE = True
except ImportError:
    DOCUMENT_AWARE_SYSTEM_AVAILABLE = False
    logger.warning("文档感知 Prompt 系统不可用")

# 日志配置（与原代码一致，避免重复配置）
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. 复制完整的TopKLogSystem类（与你topklogsystem.py中的代码完全一致）
class TopKLogSystem:
    def __init__(
            self,
            log_path: str,
            llm: str,
            embedding_model: str,
    ) -> None:
        # 禁用Chroma telemetry（与原代码一致）
        os.environ["ANONYMIZED_TELEMETRY"] = "false"
        os.environ["DISABLE_TELEMETRY"] = "1"
        os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
        
        # 初始化模型（与原代码一致）
        self.embedding_model = OllamaEmbeddings(model=embedding_model)
        self.llm = OllamaLLM(model=llm, temperature=0.1)

        # 全局设置Llama-Index（与原代码一致）
        Settings.llm = self.llm
        Settings.embed_model = self.embedding_model

        self.log_path = log_path
        self.log_index = None
        self.vector_store = None
        self._build_vectorstore()  # 初始化时自动构建向量库

    # 构建向量库（与原代码一致）
    def _build_vectorstore(self):
        vector_store_path = "./data/vector_stores"
        os.makedirs(vector_store_path, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=vector_store_path)
        log_collection = chroma_client.get_or_create_collection("log_collection")

        log_vector_store = ChromaVectorStore(chroma_collection=log_collection)
        log_storage_context = StorageContext.from_defaults(vector_store=log_vector_store)
        if log_documents := self._load_documents(self.log_path):
            self.log_index = VectorStoreIndex.from_documents(
                log_documents,
                storage_context=log_storage_context,
                show_progress=True,
            )
            logger.info(f"日志库索引构建完成，共 {len(log_documents)} 条日志")

    # 加载文档（与原代码一致）
    @staticmethod
    def _load_documents(data_path: str) -> List[Document]:
        if not os.path.exists(data_path):
            logger.warning(f"数据路径不存在: {data_path}")
            return []

        documents = []
        for file in os.listdir(data_path):
            ext = os.path.splitext(file)[1]
            if ext not in [".txt", ".md", ".json", ".jsonl", ".csv"]:
                continue

            file_path = f"{data_path}/{file}"
            try:
                if ext == ".csv":
                    chunk_size = 1000
                    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                        for row in chunk.itertuples(index=False):
                            content = str(row).replace("Pandas", " ")
                            documents.append(Document(text=content))
                else:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        documents.append(Document(text=content))
            except Exception as e:
                logger.error(f"加载文档失败 {file_path}: {e}")
        return documents

    # 检索相关日志（与原代码一致）
    def retrieve_logs(self, query: str, top_k: int = 10) -> List[Dict]:
        if not self.log_index:
            return []
        try:
            retriever = self.log_index.as_retriever(similarity_top_k=top_k)
            results = retriever.retrieve(query)
            formatted_results = [{
                "content": result.text,
                "score": result.score
            } for result in results]
            return formatted_results
        except Exception as e:
            logger.error(f"日志检索失败: {e}")
            return []

    # 生成LLM响应（与原代码一致）
    def generate_response(self, query: str, context: Dict) -> str:
        prompt = self._build_prompt(query, context)
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            logger.error(f"LLM调用失败: {e}")
            return f"生成响应时出错: {str(e)}"

    # 构建Prompt（增强版：支持文档感知的 Prompt 系统）
    def _build_prompt(self, query: str, context: Dict) -> List[Dict]:
        # 优先使用文档感知的 Prompt 系统（如果可用）
        if DOCUMENT_AWARE_SYSTEM_AVAILABLE:
            try:
                document_aware_system = DocumentAwarePromptSystem()
                enhanced_prompt_text = document_aware_system.build_prompt(query, context)
                
                # 将文本Prompt转换为Message格式
                from langchain_core.messages import HumanMessage
                return [HumanMessage(content=enhanced_prompt_text)]
            except Exception as e:
                logger.warning(f"文档感知 Prompt 系统失败，回退到原始系统: {e}")
        
        # 回退到原始 Prompt 系统
        # 补充原代码中缺失的系统消息内容（基于帮助文档"故障日志诊断"需求）
        system_message = SystemMessagePromptTemplate.from_template("""
            你是故障日志诊断专家，需基于提供的历史日志上下文和用户问题，生成详细分析报告。
            报告需包含：1. 故障描述；2. 可能原因；3. 解决方案（分步骤说明）；4. 预防建议。
            分析需结合历史日志中的相似案例，确保建议可落地。
        """)

        # 构建日志上下文（与原代码一致）
        log_context = "## 相关历史日志参考:\n"
        for i, log in enumerate(context, 1):
            log_context += f"日志 {i} : {log['content']}\n"

        # 用户消息模板（与原代码一致）
        user_message = HumanMessagePromptTemplate.from_template("""
            {log_context}
            ## 当前需要分析的问题:
            {query}

            请基于以上信息，提供详细的分析报告:
        """)

        # 组装Prompt（与原代码一致）
        prompt = ChatPromptTemplate.from_messages([system_message, user_message])
        return prompt.format_prompt(log_context=log_context, query=query).to_messages()

    # 执行查询（与原代码一致）
    def query(self, query: str) -> Dict:
        log_results = self.retrieve_logs(query)
        response = self.generate_response(query, log_results)
        return {
            "response": response,
            "retrieval_stats": len(log_results)
        }

# 2. 定义全局实例：初始化TopKLogSystem，参数与原代码一致（关键：实现全局复用）
# 注意：log_path需与你实际的日志路径一致（原代码为./data/log，需确认该路径在django_backend下存在）
topklogsystem = TopKLogSystem(
    log_path="../data/log",  # 因service.py在deepseek_api目录，需用相对路径指向django_backend/data/log
    llm="deepseek-r1:7b",    # 与原代码一致（需确保Ollama已拉取该模型）
    embedding_model="bge-large:latest"  # 与原代码一致（需确保Ollama已拉取该模型）
)
