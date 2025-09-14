import os
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
import traceback

class QASystem:
    def __init__(self, documents, api_key):
        self.documents = documents
        self.api_key = api_key
        
        self.embeddings = HuggingFaceEmbeddings(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        self.llm = HuggingFaceEndpoint(
            model="google/flan-t5-large",
            huggingfacehub_api_token=api_key,
            task="text2text-generation",
            temperature=0.1,
            max_new_tokens=768,
        )
        local_model = os.getenv("LOCAL_T2T_MODEL", "google/flan-t5-base")
        tokenizer = AutoTokenizer.from_pretrained(local_model)
        try:
            tokenizer.model_max_length = min(getattr(tokenizer, "model_max_length", 1024) or 1024, 1024)
        except Exception:
            pass
        tokenizer.truncation_side = "left"
        model = AutoModelForSeq2SeqLM.from_pretrained(local_model)
        gen_pipe = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=512,
            temperature=0.1,
            truncation=True,
            pad_token_id=tokenizer.eos_token_id if hasattr(tokenizer, "eos_token_id") and tokenizer.eos_token_id is not None else 0,
        )
        self.llm = HuggingFacePipeline(pipeline=gen_pipe)
        
        self.vector_store = self._create_vector_store()
        self.qa_chain = self._create_qa_chain()

    def _create_vector_store(self):
        if not self.documents:
            return None
        texts = [doc['content'] for doc in self.documents]
        metadatas = [dict(doc) for doc in self.documents]
        vector_store = Chroma.from_texts(
            texts, 
            self.embeddings, 
            metadatas=metadatas
        )
        return vector_store

    def _create_qa_chain(self):
        if not self.vector_store:
            return None
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 2})

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are a helpful assistant for answering questions about research papers.\n"
                "Use ONLY the information from the provided context to answer.\n"
                "If the answer isn't in the context, say: I couldn't find that in the provided documents.\n\n"
                "When the question asks for metrics (e.g., accuracy, F1-score, precision, recall),\n"
                "extract the exact numbers and units if present. Be concise.\n\n"
                "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
            ),
        )

        question_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
                "You are a helpful assistant for answering questions about research papers.\n"
                "Use ONLY the information from the provided context to answer.\n"
                "If the answer isn't in the context, say you couldn't find it.\n\n"
                "Context:\n{context}\n\nQuestion: {question}\nConcise answer:"
            ),
        )

        combine_prompt = PromptTemplate(
            input_variables=["summaries", "question"],
            template=(
                "You will receive partial answers from multiple document chunks.\n"
                "Synthesize them into a single, concise answer.\n"
                "If metrics are requested (accuracy, F1-score, etc.), extract exact numbers if present.\n"
                "If the information isn't present, say so clearly.\n\n"
                "Partial answers:\n{summaries}\n\nQuestion: {question}\nFinal answer:"
            ),
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="map_reduce",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={
                "question_prompt": question_prompt,
                "combine_prompt": combine_prompt,
            },
        )
        return qa_chain

    def ask_question(self, query):
        if not self.qa_chain:
            return "QA system not initialized."
        try:
            result = self.qa_chain.invoke({"query": query})
            return result.get("result") or result
        except Exception as e:
            error_trace = traceback.format_exc()
            return f"An error occurred: {e}\n{error_trace}"


