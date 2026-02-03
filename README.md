# ShopAI: Premium Agentic E-commerce Assistant

**ShopAI** is a state-of-the-art conversational shopping platform that unifies local inventory management with the unlimited scope of the open web. By leveraging a **Hybrid RAG (Retrieval-Augmented Generation)** architecture, it delivers a shopping experience that is intuitive, visual, and highly intelligent.

---

## ✨ Core Functionalities

### 1. 🤖 Contextual Conversational AI
*   **Natural Language Understanding**: Users can speak naturally (e.g., *"I need a quiet mechanical keyboard under $100"*). The AI understands attributes like price constraints, categories, and features without rigid keywords.
*   **Session Memory**: The assistant remembers previous interactions within a session, allowing for follow-up questions like *"Does it show products from the previous search?"*.
*   **Personality**: Tuned to be a helpful, witty, and knowledgeable shopping expert.

### 2. 🔍 Hybrid Search Engine (The Brain)
ShopAI employs a dual-strategy search system to ensure zero dead-ends:
*   **Local Semantic Search**: Prioritizes your own inventory. It understands that "joggers" and "running pants" are semantically related.
*   **Automated Web Fallback**: If a product is not found locally, the agent autonomously agents out to the internet to find real-world products, prices, and images.

### 3. 🛍️ Dynamic Shopping Interface
*   **Rich Product Cards**: Products are displayed with images, ratings, and prices directly in the chat stream.
*   **Two-Way Interaction**:
    *   **Local Items**: One-click **"Add to Cart"** functionality with a persistent shopping cart.
    *   **Web Items**: Direct **"Check Website"** deep links for external products.
*   **Glassmorphism UI**: A modern, responsive frontend built with Vanilla JS and CSS variables for a premium feel.

---

## 🧠 Model Procedure & Architecture

The intelligence of ShopAI is driven by a sophisticated pipeline of three distinct AI technologies:

### Step 1: Query Embedding (Sentence-Transformers)
*   **Model**: `all-MiniLM-L6-v2`
*   **Procedure**: When a user types a query, it is converted into a 384-dimensional vector embedding. This allows the system to match products based on *meaning* rather than just text overlap.

### Step 2: Vector Retrieval (FAISS)
*   **Technology**: Facebook AI Similarity Search (FAISS)
*   **Procedure**: The query vector is compared against the pre-computed index of local product descriptions.
*   **Logic**: If semantic similarity scores are high, local products are retrieved and ranked.

### Step 3: Web Reinforcement (DuckDuckGo)
*   **Fallback Trigger**: If local results are sparse or irrelevant.
*   **Procedure**: The system executes a live search (targeting Images and Shopping results) to fetch real-time metadata (Title, Image URL, Price, Link) from the web.
*   **Stock Logic**: Web items are automatically tagged as "Available Online".

### Step 4: Response Generation (OpenAI GPT-4o-mini)
*   **Role**: The Synthesizer.
*   **Procedure**: The LLM receives the user's chat history and the structured list of found products (Local + Web) as context. It generates a streaming, human-like response that explains *why* these products fit the user's needs.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python, FastAPI | High-performance, async REST API |
| **Vector DB** | FAISS | Efficient similarity search for dense vectors |
| **Embeddings** | all-MiniLM-L6-v2 | State-of-the-art sentence embeddings |
| **LLM** | OpenAI GPT-4o-mini | Conversational logic and reasoning |
| **Web Search** | DuckDuckGo (ddgs) | Privacy-preserving web scraping |
| **Database** | AioSQLite | Async SQL storage for sessions and carts |
| **Frontend** | JavaScript, HTML5 | Lightweight, framework-free UI |

---

## 🚀 Installation & Usage

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Environment Setup**:
    Create a `.env` file with your OpenAI API key:
    ```env
    OPENAI_API_KEY=sk-your-key-here
    ```
3.  **Run the Server**:
    ```bash
    python main.py
    ```
    The application will launch at `http://localhost:8000`.

---
*Built for the future of Agentic Commerce.*
