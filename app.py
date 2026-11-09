import streamlit as st
import json
from src.rag_pipeline import LegalRAGPipeline
from src.llm_provider import SwappableLLM
from src.legal_workflows import analyze_case, roleplay_opponent

st.set_page_config(page_title="NyayMitra — Everyday AI Lawyer", layout="wide")

@st.cache_resource
def load_rag():
    return LegalRAGPipeline()

rag = load_rag()

# Sidebar: Model Swapper (Kuku Requirement: "a solution where the model is easy to swap will shine")
with st.sidebar:
    st.header("⚙️ Model & Config")
    provider = st.selectbox("LLM Provider", ["gemini", "groq", "ollama"])
    default_model = "gemini-2.5-flash" if provider == "gemini" else ("llama-3.3-70b-versatile" if provider == "groq" else "llama3.1")
    model_name = st.text_input("Model Name", value=default_model)
    api_key = st.text_input("API Key (optional if set in .env)", type="password")
    st.caption("Architecture inspired by FAISS + CrossEncoder RAG (`ipc_legal_chatbot`), adapted for everyday Indian civil disputes.")

llm = SwappableLLM(provider=provider, model_name=model_name, api_key=api_key if api_key else None)

st.title("⚖️ NyayMitra: Everyday Legal Triage & Action Assistant")
st.write("Describe your problem in **English, Hindi, or Hinglish** (e.g., withheld rent deposit, unpaid salary, stalled refund, or a notice you received).")

user_story = st.text_area("What happened?", height=120, placeholder="Mere landlord ne 50,000 security deposit rok liya hai flat khali karne ke 2 mahine baad bhi...")

if st.button("🔍 Build My Case & Options", type="primary") and user_story.strip():
    with st.spinner("Retrieving verified statutes via FAISS + Cross-Encoder & structuring your case..."):
        retrieved_docs = rag.retrieve(user_story, top_k=2)
        result = analyze_case(llm, retrieved_docs, user_story)
        citation_check = rag.verify_citations(json.dumps(result), retrieved_docs)
        st.session_state["current_result"] = result
        st.session_state["retrieved_docs"] = retrieved_docs
        st.session_state["citation_check"] = citation_check
        st.session_state["roleplay_history"] = []

if "current_result" in st.session_state:
    res = st.session_state["current_result"]
    check = st.session_state["citation_check"]

    if res.get("requires_human_lawyer"):
        st.error(f"🚨 **Human Lawyer Recommended:** {res.get('escalation_reason')}")
    else:
        st.success(f"✅ **Self-Help Triage Eligible ({res.get('dispute_category')})** | Guardrail Check: Verified against {', '.join(check['allowed_sources'])}")

    tab1, tab2, tab3, tab4 = st.tabs([
        "1️⃣ Case Summary & Missing Proof",
        "2️⃣ Where You Stand & Options",
        "3️⃣ Ready-to-Send Legal Notice",
        "4️⃣ Practice Arguing (Roleplay)"
    ])

    with tab1:
        sc = res.get("structured_case", {})
        st.subheader("What Happened")
        st.write(sc.get("what_happened"))
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Timeline of Events**")
            for ev in sc.get("timeline_events", []):
                st.markdown(f"- {ev}")
            st.markdown(f"**Amount at Stake:** {sc.get('amount_at_stake_inr')}")
        with col2:
            st.markdown("**Proof You Already Have**")
            for p in sc.get("proof_user_has", []):
                st.markdown(f"- ✅ {p}")
            st.markdown("** Clarifying Questions / Proof Needed**")
            for m in sc.get("missing_info_or_proof_needed", []):
                st.markdown(f"- ❓ {m}")

    with tab2:
        st.subheader("Where You Stand (Plain Language)")
        st.write(res.get("plain_language_standing"))
        st.subheader("Your Action Plan")
        for idx, step in enumerate(res.get("step_by_step_options", []), 1):
            st.markdown(f"**Step {idx}:** {step}")
        with st.expander("📚 View Exact Retrieved Statutory Grounding (FAISS + CrossEncoder)"):
            st.json(st.session_state["retrieved_docs"])

    with tab3:
        st.subheader("Draft Legal Notice / Formal Complaint")
        notice_text = st.text_area("Edit before downloading:", value=res.get("draft_legal_notice", ""), height=300)
        st.download_button("⬇️ Download Notice (.txt)", data=notice_text, file_name="legal_notice_draft.txt")

    with tab4:
        st.subheader("Practice with the Other Side")
        for msg in st.session_state.get("roleplay_history", []):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        reply = st.chat_input("Practice what you will say to your landlord / HR / support...")
        if reply:
            st.session_state["roleplay_history"].append({"role": "user", "content": reply})
            opp_resp = roleplay_opponent(llm, res.get("plain_language_standing", ""), st.session_state["roleplay_history"], reply)
            st.session_state["roleplay_history"].append({"role": "assistant", "content": opp_resp})
            st.rerun()

    st.divider()
    st.download_button(
        "📦 Download Raw Output JSON (For Kuku Submission Pack)",
        data=json.dumps({"input": user_story, "retrieved_statutes": st.session_state["retrieved_docs"], "citation_verification": check, "output": res}, indent=2, ensure_ascii=False),
        file_name="test_case_output.json",
        mime="application/json"
    )