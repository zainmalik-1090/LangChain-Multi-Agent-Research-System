Markdown
# 🔬 Multi-Agent Autonomous Deep Research System

An autonomous, multi-agent deep research assistant built with **LangChain**, **LangGraph**, and **Google Gemini**. The system investigates complex topics by searching the web in real-time, extracting clean text from authoritative sources, drafting structured Markdown reports, and providing critical quality assessments—all through an interactive **Streamlit** dashboard.

---

## 🏗️ Architecture & Pipeline Flow

The system orchestrates specialized agents and chains in a sequential pipeline to mimic a professional research and editorial workflow:

[ User Query ]
│
▼
┌─────────────┐
│ Search Agent│ ──▶ Searches real-time web sources (Tavily API)
└─────────────┘
│
▼
┌─────────────┐
│ Reader Agent│ ──▶ Selects top URLs & scrapes clean body text
└─────────────┘     (Trafilatura / Readability / BeautifulSoup)
│
▼
┌─────────────┐
│ Writer Chain│ ──▶ Synthesizes research into a structured markdown report
└─────────────┘
│
▼
┌─────────────┐
│ Critic Chain│ ──▶ Evaluates report quality, assigns a score, and lists critiques
└─────────────┘
│
▼
[ Streamlit UI Dashboard ]


### Components:
* **Search Agent (`build_search_agent`)**: Uses LangGraph's ReAct agent pattern to discover recent, relevant URLs and context for the user's research topic.
* **Reader Agent (`build_reader_agent`)**: Evaluates retrieved links, selects the most relevant page, and performs deep extraction while stripping navigation bars, ads, and scripts.
* **Writer Chain (`writer_chain`)**: Compiles raw snippets and deep-scraped content into a structured research report containing an Introduction, Key Findings, Conclusions, and Source citations.
* **Critic Chain (`critic_chain`)**: Reviews the completed draft against editorial standards, scoring it out of 10 and noting explicit strengths and areas for improvement.

---

## 🛠️ Technologies Used

* **Language**: Python 3.11+
* **LLM Core**: Google Gemini (`langchain-google-genai`)
* **Agentic Framework**: LangChain & LangGraph
* **Search Engine**: Tavily API (`tavily-python`)
* **Web Scraping & Extraction**:
  * Trafilatura
  * Readability-lxml
  * BeautifulSoup4
  * Requests
* **User Interface**: Streamlit
* **Configuration**: `python-dotenv`

---

## 📂 Project Structure

```text
LangChain-Multi-Agent-Research-System/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agents.py          # Search/Reader agents, Writer/Critic chains
│   ├── pipelines/
│   │   ├── __init__.py
│   │   └── pipeline.py        # Sequential multi-agent pipeline logic
│   └── tools/
│       ├── __init__.py
│       └── tools.py           # Tavily search & resilient scraping tools
├── .env                       # API keys (ignored by Git)
├── .gitignore
├── app.py                     # Streamlit frontend application
├── main.py                    # CLI entry point for testing
├── README.md                  # Project documentation
└── requirements.txt           # Project dependencies
🚀 Getting Started
1. Clone the Repository
Bash
git clone [https://github.com/your-username/LangChain-Multi-Agent-Research-System.git](https://github.com/your-username/LangChain-Multi-Agent-Research-System.git)
cd LangChain-Multi-Agent-Research-System
2. Set Up a Virtual Environment
Bash
# Windows
python -m venv langagent
langagent\Scripts\activate

# macOS / Linux
python3 -m venv langagent
source langagent/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
(If creating requirements.txt from scratch, include: langchain, langgraph, langchain-google-genai, tavily-python, trafilatura, readability-lxml, beautifulsoup4, requests, python-dotenv, and streamlit).

4. Configure Environment Variables
Create a .env file in the project root:

Code snippet
GOOGLE_API_KEY=your_google_ai_studio_api_key
TAVILY_API_KEY=your_tavily_search_api_key
💻 Usage
Run via Web Interface (Streamlit)
Launch the interactive dashboard:

Bash
streamlit run app.py
Open http://localhost:8501 in your browser, enter any research query, and watch the agents work through each step in real time.

Run via Command Line Interface (CLI)
To run a direct test without the web UI:

Bash
python main.py
📄 License
Distributed under the MIT License. See LICENSE for more information.