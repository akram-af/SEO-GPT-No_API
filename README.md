# SEO-GPT (Local RAG, No API)
Built in Python: an offline SEO/AEO chatbot using a local LLM via Ollama. 
Implemented a RAG pipeline: chunked SEO documents, embedded with sentence-transformer, stored vectors in ChromaDB.
At query time retrieve top chunks and send them with system prompts and chat history to the model. Streamlit UI includes chat memory and source display. with citations. v1.



SEO-GPT is a **local (offline)** ChatGPT-style app specialized for **SEO / AEO**.
It uses **RAG (Retrieval-Augmented Generation)**:
- Your SEO documents (`seo_docs/`) are embedded with `sentence-transformers`
- Stored in a local vector DB (**ChromaDB**)
- Retrieved as context for a local LLM (**Ollama**) at question time
- UI is a chat app built with **Streamlit**

✅ No OpenAI / paid API required.

---

## Requirements

- Python 3.10+ (3.11 recommended)
- Ollama installed and running
- Enough RAM for your model:
  - `phi3:mini` works on most machines
  - `llama3.1:8b` needs more RAM (recommended 16GB+)

---

## Project Structure

```

seo_gpt/
app.py
build_db.py
seo_docs/
technical_seo.txt
on_page_seo.txt
link_building.txt
keyword_research.txt
chroma_db/           # generated after build

````

---

## 1) Install Ollama + Model

### Windows
1. Install Ollama from the official website
2. Open PowerShell and download a model:

```powershell
ollama pull phi3:mini
# OR (bigger / better quality):
ollama pull llama3.1:8b
````

Check it’s running:

```powershell
ollama list
```

### Linux (Ubuntu/Debian)

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Start service:

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

Download a model:

```bash
ollama pull phi3:mini
# OR:
ollama pull llama3.1:8b
```

Verify:

```bash
ollama list
```

---

## 2) Create Virtual Environment + Install Dependencies

### Windows (PowerShell)

From the project folder:

```powershell
cd C:\python\seo_gpt
python -m venv .venv
.\.venv\Scripts\activate
pip install --upgrade pip
pip install chromadb sentence-transformers streamlit ollama pypdf
```

### Linux / macOS

```bash
cd ~/seo_gpt
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install chromadb sentence-transformers streamlit ollama pypdf
```

---

## 3) Add Your SEO Knowledge Files

Put your content in `seo_docs/` as `.txt` or `.md`.

Example:

```
seo_docs/technical_seo.txt
seo_docs/on_page_seo.txt
seo_docs/link_building.txt
seo_docs/keyword_research.txt
```

> Tip: more content = better answers.

---

## 4) Build the Vector Database (RAG Index)

Run:

### Windows

```powershell
python build_db.py
```

### Linux/macOS

```bash
python build_db.py
```

You should see output like:

* `Found X document files`
* `Creating embeddings for Y chunks...`
* `Done! Saved ... chunks into chroma_db`

---

## 5) Run the App (Streamlit)

### Windows

```powershell
streamlit run app.py
```

### Linux/macOS

```bash
streamlit run app.py
```

Then open in your browser:

* [http://localhost:8501](http://localhost:8501)

---

## 6) Common Errors / Fixes

### “model not found (404)”

You didn’t download the model.

Fix:

```bash
ollama pull phi3:mini
```

### “Failed to connect to Ollama”

Ollama isn’t running.

Windows: Ollama usually runs in background; confirm:

```bash
ollama list
```

Linux:

```bash
sudo systemctl start ollama
```

### “Saved 0 chunks / empty file”

Your `.txt` files are empty. Add SEO content and rebuild:

```bash
python build_db.py
```

---

## 7) Deploy on Linux Server (Optional)

Run Streamlit on all interfaces:

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

Open firewall:

```bash
sudo ufw allow 8501
```

Then access:

* http://SERVER_IP:8501

For production, run Streamlit + Ollama using `systemd` or Docker.

---

## How It Works (RAG Summary)

1. `build_db.py`:

   * reads docs in `seo_docs/`
   * chunks them
   * creates embeddings (vectors)
   * stores in ChromaDB

2. `app.py`:

   * takes user question
   * retrieves top relevant chunks from ChromaDB
   * sends SYSTEM_PROMPT + context + chat history to Ollama
   * displays answer + sources

---

## License

MIT (or choose your own)

```

If you want, I can also generate a `requirements.txt` and a one-command setup script (`setup.ps1` for Windows + `setup.sh` for Linux) so anyone can install it fast.
```

