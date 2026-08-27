**THIS IS VIBECODE**

# 👁️ Horus Vision

**Horus Vision** is a career intelligence experiment designed to conduct a comprehensive reality check on job listings and contracts.

This was built for a Gemini AI Hackathon based in Tokyo.   It was more an exercise on how to use Google AI tools.  It mostly works, but is horribly inefficient with tokens.  AI Agents are shoehorned into something that could have and should have been done with relatively simple python, firecrawl and database. I might revisit this.

### 🌟 What is Horus?
In Egyptian mythology, the **Eye of Horus** is a powerful symbol of clear perception, royal protection, and absolute truth. 


It is built with **FastAPI**, **Jinja2**, **HTMX**, **TailwindCSS (via CDN)**, and powered by **Gemini 3.5 Flash** (using the `google-genai` SDK) and client-side **Gemini Nano** (`window.ai`).

---

## ✨ Features

- **Stage 1: Multi-modal Ingestion**: Extract role metadata, salary details, work hours, and deeptech/aerospace tags from raw text, PDFs, or image uploads using Gemini 3.5 Flash.
- **Stage 2: Contract Forensic Audit**: Scans listings for contract manipulation, overtime patterns, and PTO definitions.
- **Stage 3: Fuzzy Ethical Lockout Gate**: Uses `rapidfuzz` to block pipeline runs if they fuzzy-match unethical target entities (e.g. *Anduril*, *Palantir*, *Shield AI*).
- **Stage 4: Live OSINT reputation Grounding**: Queries Google Search live grounding to check founded years, lawsuit records, unprofitability traps, and competitors.
- **Stage 5: Asymmetric Math Engine**: Strictly calculates true effective wage and discretionary margins in pure Python (no probabilistic math).
- **Stage 6: Multi-Agent Report Compilation**: Compiles narratives, wage metrics, life indexes, and OSINT findings into an executive report.
- **Chrome Gemini Nano Pre-Screening**: Intercepts pasted job details instantly in-browser using Chrome Prompt API (`window.ai`) for immediate risk warnings.

---

## 🛠️ Local Development & Setup

### 1. Prerequisites
- Python 3.10+
- An API key for Gemini. Get one from [Google AI Studio](https://aistudio.google.com/app/api-keys).

### 2. Installation
Clone or navigate to the project directory, then initialize your virtual environment and install dependencies:

```bash
# Navigate to the workspace
cd /Users/jon/.gemini/antigravity/scratch/careershield

# Create virtual environment (if not already done)
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Setting Environment Variables
You must set your `GEMINI_API_KEY` before starting the application:

```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 4. Running the Dev Server
Run the FastAPI development server with reload enabled:

```bash
uvicorn app.main:app --reload --port 8000
```
Then open [http://localhost:8000](http://localhost:8000) in Google Chrome (to enable the Gemini Nano local pre-screen).

---

## 🧪 Testing

Run the full automated test suite to verify mathematics models, Pydantic validation, and the fuzzy-matching ethical database:

```bash
pytest tests/
```

---

## 🚀 Deploying to Google Cloud Run

Horus Vision is pre-configured for deployment to your Google Cloud project `career-shield-500702` using the included Dockerfile (which dynamically handles Cloud Run's `$PORT` binding).

### Steps to Deploy:

1. **Verify Google Cloud Project and Authentication**
   Ensure your local gcloud CLI is connected and authenticated as `jon@saigou.io`:
   ```bash
   gcloud config set project career-shield-500702
   ```

2. **Deploy directly with Cloud Run**
   Run the single-command build and deploy script. Note that you must pass your `GEMINI_API_KEY` as an environment variable to the container:
   ```bash
   gcloud run deploy horus-vision \
     --source . \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GEMINI_API_KEY="your_api_key_here"
   ```

3. **Production URL**
   Once deployment completes, the terminal will print your secure live production URL.

---

*Developed with ❤️ as part of the Google Cloud & Antigravity Agent Hackathon.*
