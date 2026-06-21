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

Core Components
Data Strategy (Part 0): Uses 100_Python_Questions_and_Answers.pdf. Documents are chunked by applying a structural split tuned directly to the average token count of individual QA pairs in the document to preserve context integrity.

Vector Indexing (Level 1): Text chunks are vectorized using dense embedding models and indexed locally inside a persistent vector store.

Query Intelligence (Level 2.1): Raw user queries pass through an upstream LLM rewriting node to resolve syntactic mistakes and optimize retrieval matching scores.

🚀 Getting Started
1. Prerequisites & Installation
Ensure you have Python 3.10+ installed. Clone this repository and install the dependencies from the requirements manifest file:

Bash
# Clone the repository
git clone [https://github.com/your-username/intelligent-rag-system.git](https://github.com/your-username/intelligent-rag-system.git)
cd intelligent-rag-system

# Install dependencies
pip install -r requirements.txt
2. Environment Configuration
Create a .env file in the root directory of your project based on the template provided in .env.example:

Bash
cp .env.example .env
Open the .env file and append your API credentials:

Plaintext
OPENAI_API_KEY=your_real_openai_api_key_here
VECTOR_DB_DIR=./chroma_db
3. Ingesting Data
To process the raw PDF document, generate the average-token splits, and populate your vector store index, run your ingestion script or Jupyter Notebook:

Bash
# Execute your vector ingestion step (or open and run data.ipynb)
python data.py
💻 Live Execution Demo
You can execute the end-to-end state machine graph query tool directly using the execution testing script:

Bash
python demo.py
Example Test Trace Output
The following sample traces a user request containing minor syntax errors ("pivote tble"), verifying that both query restructuring and context grounding operate correctly:

Python
test = client.run({
    "query": "how to make pivote tble in pandas?",  
})
print("Rewritten Query:", test.get("rewritten_query"))
print("Response:\n", test.get("response"))
Output:
Plaintext
============================================================
📥 ORIGINAL USER QUERY: 'how to make pivote tble in pandas?'
============================================================

⚙️ Orchestrating execution nodes through LangGraph...

============================================================
📊 PIPELINE RECOGNITION & RESULTS
============================================================
🔄 Rewritten Query:  how to create a pivot table in pandas?
------------------------------------------------------------
🤖 Grounded Answer:
To create a pivot table using numpy, you would typically use pandas library because numpy is primarily used for numerical data manipulation and does not support pivot tables directly. However, if you were to use numpy for such operations, it would involve converting your data into a suitable format first.

Based on the provided context, here's how you can create a pivot table using pandas:

```python
import pandas as pd

data = {
    'Region': ['East', 'West', 'East', 'West', 'East'],
    'Product': ['A', 'B', 'A', 'C', 'B'],
    'Sales': [100, 150, 120, 200, 130]
}
df = pd.DataFrame(data)

# Create a pivot table to show total sales by Region and Product
pivot_table = df.pivot_table(values='Sales', index='Region', columns='Product', aggfunc='sum')

print("Pivot Table (Total Sales by Region and Product):")
print(pivot_table)
This code snippet uses pandas' pivot_table method, which is designed to create pivot tables from a DataFrame. The values parameter specifies the column that should be aggregated, index defines the index of the resulting table, columns define the columns of the resulting table, and aggfunc specifies how the values are aggregated (in this case, summing up the sales).

---

## 📁 Repository Blueprint

```text
├── data/
│   └── 100_Python_Questions_and_Answers.pdf  # Source data file
├── data.ipynb                                # Data processing, chunk calculations & injection
├── models.py                                 # Core LLM model configurations
├── prompts.py                                # System instructions for rewrite/generate nodes
├── agents.py                                 # Node function implementations
├── workflow.py                               # LangGraph compilation & State construction
├── demo.py                                   # End-to-end execution interface
├── requirements.txt                          # Project dependency trees
├── .env.example                              # Shared credential template
└── REPORT.md                                 # Full design analysis report
          ▼
        [End]

