# Intelligent RAG System with LangGraph Orchestration

An AI-powered Question-Answering RAG (Retrieval-Augmented Generation) pipeline built for the **Wiyse School AI Engineering Assessment**. The system processes natural language queries over a structured technical QA dataset, dynamically repairs user inputs using an LLM-powered Query Rewriter, extracts context from a vector database, and outputs strictly grounded, hallucination-free answers complete with source validation.

---

## 🛠️ Architecture & Workflow

The entire pipeline is orchestrating explicitly via a **LangGraph** state machine. State information flows across a typed state schema through three distinct operational nodes:

```text
       [Start]
          │
          ▼
   ┌──────────────┐
   │ Query Rewrite│ ──► Dynamically cleans errors (e.g., "pivote tble" -> "pivot table")
   └──────────────┘
          │
          ▼
   ┌──────────────┐
   │ Context Retr.│ ──► Embeds query & searches ChromaDB vector store
   └──────────────┘
          │
          ▼
   ┌──────────────┐
   │ Answer Gener.│ ──► Passes context to LLM for strict grounded generation
   └──────────────┘
          │
          ▼
        [End]

