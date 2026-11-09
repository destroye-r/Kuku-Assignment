# ⚖️ NyayMitra: Everyday AI Legal Triage & Action Assistant

**Submission for Kuku AI Generalist Assignment — Problem 2: Build an AI Lawyer**

NyayMitra is a multilingual (English, Hindi, and Hinglish) legal triage and self-help action assistant designed for everyday citizens in India. Instead of acting as a generic legal Q&A chatbot that risks hallucinating laws, NyayMitra combines a **two-stage Retrieval-Augmented Generation (RAG) pipeline** (`FAISS` + `Cross-Encoder` re-ranking) with **deterministic citation guardrails** and a **4-step action workflow** covering everyday civil and consumer disputes.

---

## 🎯 Problem Scope & What It Covers

Most citizens give up on everyday legal disputes because lawyers feel too expensive, paperwork is intimidating, and procedures are unclear. NyayMitra focuses in depth on **8 high-frequency everyday civil/consumer dispute categories** while enforcing a hard escalation boundary for criminal and complex litigation matters:

### ✅ In-Scope (Self-Help Triage & Document Generation)
1. **Landlord & Security Deposit Disputes:** Unlawful withholding of rent deposits, arbitrary painting/cleaning deductions, and unlawful eviction notices (*Transfer of Property Act, 1882; Indian Contract Act, 1872; Model Tenancy Act, 2021*).
2. **Consumer Refunds & Defective Goods:** E-commerce refund refusals, unfair EdTech/gym subscription contracts, and flight cancellation compensation (*Consumer Protection Act, 2019; E-Commerce Rules, 2020; DGCA CAR*).
3. **Unpaid Salary & Full and Final (FnF) Settlement:** Delayed monthly wages, withheld relieving letters, and unremitted PF/TDS deductions (*Payment of Wages Act, 1936; Contract Act Sec 27; EPF Act*).
4. **Legal Notices & Recovery Harassment:** Decoding pre-litigation civil notices, Section 138 NI Act cheque bounce timelines, and RBI guidelines against recovery agent harassment.
5. **Banking, UPI Fraud & CIBIL Disputes:** RBI Zero-Liability unauthorized electronic transaction rules (1930 helpline workflow) and ₹100/day statutory compensation for delayed credit bureau rectification.
6. **Traffic E-Challans, Insurance Rejections, Telecom & RTI:** Contesting faulty camera challans on Virtual Courts, Insurance Ombudsman escalations, and filing Section 6(1) RTI applications.

### 🚨 Out-of-Scope (Hard Escalation to Human Lawyer)
* **Criminal Offences, Physical Assault, Police FIRs & Bail:** Covered under *Bharatiya Nyaya Sanhita (BNS), 2023* and *Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023*.
* **Contested Matrimonial, Child Custody, Ancestral Property Partition, or High-Value Claims (> ₹10 Lakhs).**
* *Behavior:* When a query triggers these boundaries, NyayMitra displays a red **Human Lawyer Required** alert and directs the user to Emergency 112, a licensed Advocate, or the **NALSA Free Legal Aid Helpline (15100)**.

---

## 🛡️ Architecture: How We Avoid Invented Laws & Hallucinations

| Layer | Handled By | Purpose |
| :--- | :--- | :--- |
| **1. Curated Statutory Knowledge Base** | `data/legal_data.jsonl` | Stores verified Indian statutory sections, remedies, and official government portals (`e-Jagriti`, `SAMADHAN`, `RBI CMS`, `1930`). |
| **2. Bi-Encoder Vector Search** | `all-MiniLM-L6-v2` + `FAISS` (`IndexFlatIP`) | Retrieves top candidate statutory records using normalized cosine similarity. |
| **3. Cross-Encoder Re-Ranking** | `cross-encoder/ms-marco-MiniLM-L-6-v2` | Re-scores candidate pairs `(user_query, statute)` to select the top verified provisions before LLM generation. |
| **4. Strict Context Lock & Trap Detection** | System Prompt Guardrail (`src/legal_workflows.py`) | Prohibits citing any Act, Section, or case law outside the retrieved JSON context and explicitly corrects fake laws injected by the user. |
| **5. Deterministic Citation Sanitizer** | Regex Verifier (`verify_citations` in `src/rag_pipeline.py`) | Parses all `Section X` references in the LLM output and cross-checks them against the retrieved statute metadata. |
| **6. Swappable LLM Wrapper** | `SwappableLLM` (`src/llm_provider.py`) | Supports seamless switching between **Gemini (`gemini-3.8-flash`)**, **Groq (`llama-3.3-70b-versatile`)**, and local **Ollama (`llama3.1`)** via the UI sidebar or `.env`. |

---

## 📂 Project Structure

```text
ipc_legal_chatbot/
├── app.py                      # Main Streamlit application (4 Action Tabs + Model Swapper Sidebar)
├── src/
│   ├── __init__.py
│   ├── config.py               # Environment & default model configuration
│   ├── rag_pipeline.py         # Self-healing dataset loader, FAISS indexer, Cross-Encoder & Regex Citation Verifier
│   ├── llm_provider.py         # Unified model-agnostic wrapper (Gemini, Groq, Ollama)
│   └── legal_workflows.py      # Structured JSON case builder, notice drafter & adversarial roleplay coach
├── data/
│   ├── legal_data.jsonl        # 20 verified everyday Indian legal & escalation records
│   ├── faiss.index             # Auto-generated FAISS vector index cache
│   └── metadata.json           # Auto-generated statutory metadata cache
├── raw_outputs/                # Unedited JSON outputs across 5 diverse evaluation test cases
├── generate_raw_outputs.py     # Batch runner to reproduce all 5 raw test case outputs
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
🚀 Quickstart: How to Run Locally
1. Clone & Set Up Virtual Environment
Bash
git clone <your-repo-url>
cd ipc_legal_chatbot

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
2. Install Dependencies
Bash
pip install -r requirements.txt
(Or directly: pip install streamlit faiss-cpu sentence-transformers google-genai python-dotenv requests numpy)

3. Configure API Keys (.env or UI Sidebar)
Create a .env file in the project root (or enter your key directly in the Streamlit sidebar at runtime):

Code snippet
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_optional_groq_api_key_here
4. Launch the Application
Bash
streamlit run app.py
Open http://localhost:8501 in your browser.

Note on First Run: On initial startup, SentenceTransformer and CrossEncoder will build and cache data/faiss.index and data/metadata.json automatically (~10–15 seconds). Subsequent runs load instantaneously from cache.

🔄 Swapping Models During Evaluation
This project is built so evaluators can test new inputs or swap models in seconds:

Via the UI Sidebar: Select gemini (default: gemini-3.8-flash), groq (default: llama-3.3-70b-versatile), or ollama (default: llama3.1), type any model identifier in the Model Name box, and paste an API key.

Via Code (src/llm_provider.py): Instantiate SwappableLLM(provider="...", model_name="...", api_key="...").

🧪 Reproducing the Test Cases (raw_outputs/)
Five end-to-end test cases are included to evaluate multilingual parsing, missing-evidence detection, escalation boundaries, and adversarial hallucination resistance:

test_1_hinglish_landlord_deposit.json — Hinglish security deposit dispute with arbitrary painting deductions.

test_2_ecommerce_defective_refund.json — Defective television delivery with closed support ticket.

test_3_unpaid_salary_fnf.json — Withheld 2 months' salary and relieving letter after serving full notice period.

test_4_out_of_scope_criminal_escalation.json — Physical assault & police detention query triggering the Hard Stop Human Lawyer guardrail.

test_5_adversarial_fake_law_trap.json — Prompt injecting a fabricated law ("Section 999 of the Indian Tenant Revenge Act, 2022") to verify that the system corrects the user rather than agreeing with false premises.

To regenerate all 5 raw outputs from scratch:

Bash
python generate_raw_outputs.py