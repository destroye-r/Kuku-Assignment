import json

SYSTEM_GUARDRAIL = """You are NyayMitra, an AI Legal Triage Assistant for everyday citizens in India.
STRICT GROUND RULES:
1. NEVER invent or cite any Act, Section, or past Supreme Court/High Court case that is NOT explicitly provided in the VERIFIED STATUTES context below.
2. If the user cites a fake or non-existent law, explicitly correct them politely and state that no such provision exists in your verified database.
3. If the issue involves criminal violence, arrest/bail, property title litigation, or claims > Rs 10 Lakhs, set requires_human_lawyer = true and advise contacting a licensed Advocate or NALSA (15100).
4. Respond in the same language/script comfort level as the user (English, Hindi, or Hinglish).
"""

def analyze_case(llm, rag_docs: list, user_story: str) -> dict:
    context_str = json.dumps(rag_docs, indent=2)
    prompt = f"""VERIFIED STATUTES:
{context_str}

USER PROBLEM:
{user_story}

Return a valid JSON object with the exact keys:
- "detected_language": string
- "dispute_category": string
- "requires_human_lawyer": boolean
- "escalation_reason": string (why they do or do not need a human lawyer right now)
- "structured_case": {{
    "what_happened": string,
    "timeline_events": list of strings,
    "amount_at_stake_inr": string,
    "proof_user_has": list of strings,
    "missing_info_or_proof_needed": list of strings
  }}
- "plain_language_standing": string (explain where they stand using ONLY the VERIFIED STATUTES)
- "step_by_step_options": list of strings (practical next steps including official portals)
- "draft_legal_notice": string (a ready-to-send formal Legal Notice / Grievance Email with placeholders for missing details)
"""
    raw = llm.generate(SYSTEM_GUARDRAIL, prompt, json_mode=True)
    return json.loads(raw)

def roleplay_opponent(llm, case_summary: str, chat_history: list, user_reply: str) -> str:
    sys_prompt = f"""You are playing the OTHER SIDE (the stubborn landlord, unresponsive HR manager, or customer support lead) in a realistic negotiation practice session for an Indian citizen.
Case context: {case_summary}
Push back with realistic excuses (e.g., 'maintenance charges', 'company policy', 'no refund window') for 2-3 turns, then after each reply add a short '[COACH TIP]' in brackets telling the user how to counter your excuse using their evidence and statutory notice."""
    history_str = "\n".join([f"{m['role']}: {m['content']}" for m in chat_history])
    return llm.generate(sys_prompt, f"{history_str}\nUser: {user_reply}", json_mode=False)