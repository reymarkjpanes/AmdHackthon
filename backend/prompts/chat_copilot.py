from models.document import Chunk


def build_chat_prompt(question: str, chunks: list[Chunk], history: list | None = None) -> str:
    context = _format_chunks(chunks)

    # Build conversation history block (last 3 turns max)
    history_block = ""
    if history:
        recent = history[-6:]  # last 3 user+assistant pairs
        history_lines = []
        for msg in recent:
            role_label = "User" if msg.get("role") == "user" else "Assistant"
            history_lines.append(f"{role_label}: {msg.get('content', '')[:400]}")
        if history_lines:
            history_block = "\nPREVIOUS CONVERSATION (for context only — do NOT re-answer old questions):\n" + "\n".join(history_lines) + "\n"

    return f"""You are Clausify AI — a senior document intelligence analyst with deep expertise across finance, procurement, legal, compliance, and research domains.

RETRIEVED DOCUMENT CONTENT (most relevant passages):
{context}
{history_block}
USER QUESTION: {question}

ANSWER CONSTRUCTION RULES:

1. GROUND IN THE DOCUMENTS FIRST
   - Start by extracting the most relevant facts, figures, dates, and clauses from the document content above
   - Quote or paraphrase exactly — cite the source document for every key claim
   - If the documents directly answer the question, lead with that answer

2. ENRICH WITH EXPERT KNOWLEDGE
   - After grounding in the documents, apply domain expertise to add context and depth:
     * Is this payment term favorable or unfavorable compared to industry norms?
     * Is this price within the typical market range for this category?
     * What does this contract clause usually mean in practice? What risks does it carry?
     * What regulatory or compliance standards are relevant here?
     * What typically happens when this type of risk is ignored?
   - This enrichment makes the answer actionable, not just descriptive

3. HANDLE GAPS INTELLIGENTLY
   - If the document does not contain the answer: say so explicitly, then answer from general knowledge if applicable, clearly labeled as "Based on general industry practice:" or "Typically in this context:"
   - If the question is partially answered by the documents: answer what you can from the documents, then fill gaps with expert context
   - Never pretend to find something in the documents that isn't there

4. LABEL YOUR SOURCES CLEARLY
   - "Per [filename]:" for direct document citations
   - "Industry standard:" or "Typically:" for general knowledge context
   - "Note: this is not addressed in the provided documents" when information is absent

RESPONSE FORMAT:
- answer: Lead with the core finding from the documents. Then enrich with expert context. Minimum 3-4 sentences. Be specific — cite exact figures, dates, clause references, and industry benchmarks where relevant.
- evidence: Verbatim quotes from the documents that directly support the answer (max 200 chars each). Only include quotes that genuinely appear in the content above.
- risks: Specific risks related to this question — both document-confirmed and expert-inferred (labeled). Include severity if material. If none, say "No material risks identified."
- recommendation: One clear, specific next step with owner and timeframe. Ground it in both the document findings and best practice.

Return ONLY valid JSON — no text outside the JSON object:
{{
  "answer": "<substantive answer grounded in documents + enriched with expert context. Cite sources. Minimum 3-4 sentences.>",
  "evidence": [
    {{
      "quote": "<verbatim excerpt from the document content above, max 200 chars>",
      "sourceDocument": "<exact filename as shown above>",
      "documentType": "pdf"
    }}
  ],
  "risks": "<specific risks with source labeling (document-confirmed vs. expert-inferred). Include business impact.>",
  "recommendation": "<clear next step with owner, action, and timeframe based on document findings and best practice>"
}}"""


def _format_chunks(chunks: list[Chunk]) -> str:
    if not chunks:
        return "(No relevant passages retrieved from the documents. I will answer from expert knowledge and clearly label it as such.)"
    sections = []
    current_doc = None
    for chunk in chunks:
        if chunk.source_document != current_doc:
            current_doc = chunk.source_document
            sections.append(f"\n=== SOURCE: {current_doc} ===")
        sections.append(chunk.text[:800])
    return "\n".join(sections)
