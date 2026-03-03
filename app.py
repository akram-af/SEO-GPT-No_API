import chromadb
import ollama
from sentence_transformers import SentenceTransformer
import streamlit as st

DB_DIR = "chroma_db"
COLLECTION = "seo_knowledge"
MODEL_NAME = "phi3:mini"  # or "llama3.1:8b" if you have enough RAM

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

SYSTEM_PROMPT = """You are SEO-GPT, a specialist assistant for SEO and AEO.

Allowed scope:
- SEO: technical SEO (crawling, indexing, robots.txt, sitemaps, canonical, redirects, Core Web Vitals)
- SEO: on-page SEO (titles, meta descriptions, headings, internal linking, image alt text)
- SEO: keyword research (intent, clustering, SERP analysis)
- SEO: content strategy (topical authority, content briefs, E-E-A-T)
- SEO: link building (safe strategies, outreach, digital PR)
- SEO: SEO analytics (Search Console, GA4 insights as they relate to SEO)
- AEO (Answer Engine Optimization): optimizing content for answer engines and AI/generative search results,
  including featured snippets, entity coverage, structured data, question-answer formatting, and intent matching.

Rules:
- If the question is fully unrelated to SEO/AEO, reply briefly:
  "I can help with SEO/AEO. Please ask a question about search optimization."
- If the question is partially related, answer ONLY the SEO/AEO part and ignore unrelated parts.
- Use the provided CONTEXT as your main source of truth.
- If the context is missing key info, say what you know, then list what’s missing and what to check next.
- Keep answers practical: steps, checklists, examples.
- When helpful, include a short section: "Next actions".
"""


@st.cache_resource
def load_embedder():
    return SentenceTransformer(EMBED_MODEL)


@st.cache_resource
def load_chroma_collection():
    client = chromadb.PersistentClient(path=DB_DIR)
    return client.get_or_create_collection(name=COLLECTION)


def retrieve(query: str, k: int = 5):
    embedder = load_embedder()
    col = load_chroma_collection()

    q_emb = embedder.encode([query], normalize_embeddings=True).tolist()[0]
    res = col.query(query_embeddings=[q_emb], n_results=k, include=["documents", "metadatas"])

    docs = res["documents"][0] if res.get("documents") else []
    metas = res["metadatas"][0] if res.get("metadatas") else []
    return list(zip(docs, metas))


def build_context_and_sources(hits):
    if not hits:
        return "NO CONTEXT FOUND", []

    blocks = []
    sources = []
    for i, (doc, meta) in enumerate(hits, start=1):
        src = (meta or {}).get("source", "unknown")
        sources.append(src)
        blocks.append(f"[{i}] (source: {src})\n{doc}")

    # de-duplicate sources while preserving order
    seen = set()
    unique_sources = []
    for s in sources:
        if s not in seen:
            seen.add(s)
            unique_sources.append(s)

    return "\n\n".join(blocks), unique_sources


def main():
    st.set_page_config(page_title="SEO-GPT (Local)", layout="centered")
    st.title("SEO-GPT (Local, No API)")
    st.caption("Tip: Run `python build_db.py` anytime you add or change files in seo_docs/")

    # Reset button
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Reset chat"):
            st.session_state.messages = []
            st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render chat history
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    user_q = st.chat_input("Ask an SEO/AEO question…")
    if not user_q:
        return

    # Save + show user message
    st.session_state.messages.append({"role": "user", "content": user_q})
    with st.chat_message("user"):
        st.markdown(user_q)

    # Retrieve context
    hits = retrieve(user_q, k=5)
    context, sources = build_context_and_sources(hits)

    # Build messages for Ollama (multi-turn chat)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # keep last N turns for memory
    history = st.session_state.messages[-10:]
    for m in history:
        messages.append({"role": m["role"], "content": m["content"]})

    # Provide RAG context
    messages.append({"role": "system", "content": f"CONTEXT:\n{context}"})

    try:
        resp = ollama.chat(model=MODEL_NAME, messages=messages)
        answer = (resp.get("message") or {}).get("content", "").strip()
        if not answer:
            answer = "I couldn't generate a response. Make sure Ollama is running and the model is installed."
    except Exception as e:
        answer = f"Error talking to Ollama: {e}"

    # Save + show assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

        # Show sources
        with st.expander("Sources used"):
            if sources:
                for s in sources:
                    st.write(f"- {s}")
            else:
                st.write("No sources (no matching context found).")


if __name__ == "__main__":
    main()