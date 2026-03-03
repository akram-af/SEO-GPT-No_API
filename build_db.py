import os
import glob
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

DOCS_DIR = "seo_docs"
DB_DIR = "chroma_db"
COLLECTION = "seo_knowledge"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 200):
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    chunks = []
    step = max(1, chunk_size - overlap)
    i = 0
    while i < len(text):
        chunk = text[i:i + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        i += step
    return chunks


def read_txt_md(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def read_pdf(path: str) -> str:
    reader = PdfReader(path)
    pages_text = []
    for i, page in enumerate(reader.pages):
        t = page.extract_text() or ""
        t = t.strip()
        if t:
            pages_text.append(f"\n\n[PAGE {i+1}]\n{t}")
    return "\n".join(pages_text)


def main():
    root = os.getcwd()
    docs_path = os.path.join(root, DOCS_DIR)

    print(f"Project folder: {root}")
    print(f"Looking for docs in: {docs_path}")

    if not os.path.isdir(docs_path):
        raise SystemExit(f"❌ Missing folder: {docs_path}")

    # find txt/md/pdf
    patterns = [
        os.path.join(docs_path, "**", "*.txt"),
        os.path.join(docs_path, "**", "*.md"),
        os.path.join(docs_path, "**", "*.pdf"),
    ]
    files = []
    for p in patterns:
        files.extend(glob.glob(p, recursive=True))
    files = sorted(set(files))

    print(f"Found {len(files)} files:")
    for f in files:
        print(" -", os.path.relpath(f, root))

    if not files:
        raise SystemExit("❌ No .txt/.md/.pdf files found in seo_docs/")

    print("Loading embedding model...")
    embedder = SentenceTransformer(EMBED_MODEL)

    print("Preparing ChromaDB...")
    client = chromadb.PersistentClient(path=DB_DIR)

    # clear old collection safely
    try:
        client.delete_collection(name=COLLECTION)
        print(f"Deleted old collection: {COLLECTION}")
    except Exception:
        pass

    col = client.get_or_create_collection(name=COLLECTION)

    ids, documents, metadatas = [], [], []
    idx = 0

    print("Reading + chunking...")
    for fp in files:
        ext = os.path.splitext(fp)[1].lower()
        base = os.path.basename(fp)

        try:
            if ext in [".txt", ".md"]:
                text = read_txt_md(fp)
            elif ext == ".pdf":
                text = read_pdf(fp)
            else:
                continue
        except Exception as e:
            print(f"⚠️ Failed to read {base}: {e}")
            continue

        chunks = chunk_text(text)
        if not chunks:
            print(f"⚠️ Skipping empty/unreadable file: {base}")
            continue

        for c in chunks:
            ids.append(f"chunk-{idx}")
            documents.append(c)
            metadatas.append({"source": base})
            idx += 1

    if not documents:
        raise SystemExit("❌ No chunks were created. PDFs might be scanned images (no text).")

    print(f"Creating embeddings for {len(documents)} chunks...")
    embeddings = embedder.encode(documents, normalize_embeddings=True).tolist()

    print("Saving to ChromaDB...")
    col.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

    print(f"✅ Done! Saved {len(ids)} chunks into {DB_DIR} (collection: {COLLECTION})")


if __name__ == "__main__":
    main()