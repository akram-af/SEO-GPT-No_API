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

C:\python\seo_gpt
│
├── build_db.py
├── app.py
├── chroma_db (will be created after build)
├── seo_docs
│     ├── technical_seo.txt
│     ├── on_page_seo.txt
│
└── .venv
````md
# SEO-GPT (Local RAG, No API)

SEO-GPT is a **local (offline)** ChatGPT-style app specialized for **SEO / AEO**.  
It uses **RAG (Retrieval-Augmented Generation)**:

- Your SEO files in `seo_docs/` are chunked and converted into embeddings (meaning-vectors)
- Embeddings are stored locally in **ChromaDB**
- At question time, relevant chunks are retrieved and sent as **CONTEXT** to a local LLM via **Ollama**
- UI is a chat app built with **Streamlit**

✅ No paid APIs (OpenAI/Anthropic) required.

---

## Table of Contents
- [1) Install Python](#1-install-python)
- [2) Install Ollama + Download a Model](#2-install-ollama--download-a-model)
- [3) Get the Project](#3-get-the-project)
- [4) Create Virtual Environment + Install Dependencies](#4-create-virtual-environment--install-dependencies)
- [5) Add Your SEO Knowledge Files](#5-add-your-seo-knowledge-files)
- [6) Build the RAG Vector Database](#6-build-the-rag-vector-database)
- [7) Run the App](#7-run-the-app)
- [8) Update Knowledge (Rebuild DB)](#8-update-knowledge-rebuild-db)
- [9) Troubleshooting](#9-troubleshooting)
- [10) Deploy on Linux Server (Optional)](#10-deploy-on-linux-server-optional)

---

## 1) Install Python

### Windows (Recommended: Python 3.11)
1. Download Python from the official Python website (Windows installer).
2. During install:
   - ✅ Check **“Add Python to PATH”**
   - Choose **Install Now**
3. Verify installation (PowerShell):
   ```powershell
   python --version
   pip --version
````

If `python` isn’t recognized:

* Re-run installer and ensure **Add Python to PATH** is checked, OR
* Close and reopen PowerShell after installation.

---

### Linux (Ubuntu/Debian)

Install Python + venv:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
python3 --version
pip3 --version
```

---

## 2) Install Ollama + Download a Model

Ollama runs the LLM locally.

### Windows

1. Install Ollama for Windows from the official Ollama website.
2. Verify it works (PowerShell):

   ```powershell
   ollama --version
   ollama list
   ```
3. Download a model (recommended):

   ```powershell
   ollama pull phi3:mini
   ```

   Optional bigger model (needs more RAM, better quality):

   ```powershell
   ollama pull llama3.1:8b
   ```

---

### Linux (Ubuntu/Debian)

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Enable and start Ollama service:

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
```

Download a model:

```bash
ollama pull phi3:mini
# or:
ollama pull llama3.1:8b
```

Verify:

```bash
ollama list
```

---

## 3) Get the Project

### Option A: Clone from GitHub

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd seo_gpt
```

### Option B: Download ZIP

* Download the repo ZIP from GitHub
* Extract it
* Open terminal in the extracted folder

Project should look like:

```
seo_gpt/
  app.py
  build_db.py
  seo_docs/
  (chroma_db/ will be created later)
```

---

## 4) Create Virtual Environment + Install Dependencies

### Windows (PowerShell)

From inside the project folder:

```powershell
cd C:\path\to\seo_gpt
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install chromadb sentence-transformers streamlit ollama pypdf
```

Check that you see `(.venv)` at the start of the terminal line.

---

### Linux

```bash
cd ~/seo_gpt
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install chromadb sentence-transformers streamlit ollama pypdf
```

---

## 5) Add Your SEO Knowledge Files

Put your SEO content in `seo_docs/` as `.txt` or `.md`.

Example structure:

```
seo_docs/
  technical_seo.txt
  on_page_seo.txt
  link_building.txt
  keyword_research.txt
```

✅ Tip: More content = better answers
⚠️ If files are empty, your database will have very few chunks and answers will be weak.

---

## 6) Build the RAG Vector Database

This step reads your files, chunks them, makes embeddings, and saves them into `chroma_db/`.

### Windows / Linux

Make sure your venv is activated, then run:

```bash
python build_db.py
```

Expected output includes:

* `Found X document files`
* `Creating embeddings for Y chunks...`
* `Done! Saved Y chunks into chroma_db`

After success, you will see a new folder:

```
chroma_db/
```

---

## 7) Run the App

### Windows / Linux

Make sure your venv is activated, then:

```bash
streamlit run app.py
```

Open in browser:

* [http://localhost:8501](http://localhost:8501)

---

## 8) Update Knowledge (Rebuild DB)

Whenever you add/change files in `seo_docs/`, rebuild the database:

```bash
python build_db.py
```

Then refresh the Streamlit page (or restart Streamlit).

---

## 9) Troubleshooting

### A) `ModuleNotFoundError: No module named 'chromadb'`

You didn’t install packages in the venv, or venv not activated.

Fix:

* Activate venv
* Reinstall dependencies:

```bash
pip install chromadb sentence-transformers streamlit ollama pypdf
```

---

### B) Ollama error: `Failed to connect to Ollama`

Ollama is not running.

Windows:

```powershell
ollama list
```

If it errors, open Ollama app (or reinstall).

Linux:

```bash
sudo systemctl start ollama
ollama list
```

---

### C) Ollama error: `model "... " not found (404)`

You didn’t download the model.

Fix:

```bash
ollama pull phi3:mini
```

Then ensure `MODEL_NAME` in `app.py` matches:

```python
MODEL_NAME = "phi3:mini"
```

---

### D) `Saved 0 chunks` or many “Skipping empty file”

Your `.txt` files are empty (or unreadable). Add text into them and rebuild:

```bash
python build_db.py
```

---

### E) Streamlit says: `File does not exist: app.py`

You are in the wrong folder.

Fix:

```bash
cd path/to/seo_gpt
dir        # Windows
ls         # Linux
```

Make sure you see `app.py`.

---

### F) Ollama port error: `bind: Only one usage of each socket address`

Ollama is already running. Do **not** run `ollama serve` again.

Just do:

```bash
ollama list
```

---

## 10) Deploy on Linux Server (Optional)

### A) Run Streamlit so other computers can access it

```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

### B) Open firewall port (Ubuntu ufw)

```bash
sudo ufw allow 8501
```

Then visit:

* `http://YOUR_SERVER_IP:8501`

### C) Ensure Ollama is running on the server

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
ollama list
```

---

## Notes / Tips

* If answers are weak: add more content to `seo_docs/` and rebuild DB.
* Smaller model (`phi3:mini`) is faster on low RAM.
* Bigger model (`llama3.1:8b`) gives better reasoning if your server has enough RAM.

---

## License

last commands:
1) pip install fastapi uvicorn langchain openai chromadb tiktoken
2) pip install ollama
3) pip install transformers datasets peft accelerate bitsandbytes
4) python -m venv .venv
.\.venv\Scripts\activate
pip install ollama chromadb sentence-transformers streamlit pypdf
5) python build_db.py
6) streamlit run app.py
