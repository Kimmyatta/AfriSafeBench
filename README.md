# AfriSafeBench

**Regional Tracks:** Track 4: Open  
**Project type:** Evaluation + Tool  
**Focus:** African healthcare AI deployment risk assessment

AfriSafeBench is a benchmark and governance-support tool for evaluating whether large language models can identify AI safety and governance risks in African healthcare AI deployment scenarios.

**Live prototype (frontend):** https://afrisafebench-ai-safety.vercel.app

**Note:** The frontend prototype is deployed on Vercel. Live scenario evaluation requires the FastAPI backend, which can be run locally or deployed using the instructions below. Full deployment instructions for both frontend and backend are provided in this repository.

The project includes:

- 25 African healthcare AI deployment scenarios
- 10 AI safety and governance risk categories
- benchmark scoring for model-detected versus expected risks
- rescored review files with human-review flags
- framework-guided recommendations using WHO, NIST, UNESCO, OECD, and African Union guidance
- result figures and a hackathon submission report

## Screenshots

### Scenario Browser

![Scenario Browser](docs/figures/screenshot_browser.png)

### Evaluation Results

![Evaluation Results](docs/figures/screenshot_results.png)

### Risk Scoring Detail

![Risk Scoring](docs/figures/screenshot_scoring.png)

### Framework Guidance Report

![Framework Report](docs/figures/screenshot_report.png)

![Framework Report Sources](docs/figures/screenshot_report2.png)

## Repository Structure

```text
backend/
  ai_safety/                  Core benchmark, scoring, report, and framework guidance services
  app/                        Minimal FastAPI app for AfriSafeBench
data/
  afrisafebench_scenarios.json
  afrisafebench_frameworks.json
  afrisafebench/results/      Benchmark and framework-guidance outputs
  afrisafebench/frameworks/   Framework PDFs, chunks, embeddings, and FAISS index
docs/
  figures/                    Result visuals
  reports/                    Submission report drafts
frontend/
  src/pages/AiSafetyEvaluation.tsx
scripts/                      Result compilation, rescoring, figure, and report generation scripts
```

## Risk Categories

- Bias and Fairness
- Human Oversight
- Transparency and Explainability
- Safety and Reliability
- Data Governance and Privacy
- Monitoring and Incident Reporting
- Distribution Shift and Local Validation
- Vendor Dependency
- Resource-Constrained Deployment
- Misinformation or Unsafe Medical Advice

## Models Evaluated

- `llama-3.1-8b-instant`
- `llama-3.3-70b-versatile`
- `openai/gpt-oss-20b`

## How Scenarios Are Evaluated

Each model receives the same scenario text and is asked to identify AI safety and governance risks, explain why each risk is present using scenario-specific evidence, assign severity, and return structured JSON.

Expected risk categories are compared with model-detected categories using a 0/1/2 rubric:

- `2`: risk identified with scenario-specific explanation
- `1`: risk identified, but explanation is generic or partial
- `0`: risk missed or incorrectly identified

Because models often describe the same risk using different wording, AfriSafeBench includes semantic rescoring and human-review flags when rescoring changes a category.

## Run The Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd ..
copy .env.example .env
# Add your GROQ_API_KEY to .env
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

## Run The Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL, usually:

```text
http://127.0.0.1:5173
```

## Deploy The Frontend On Vercel

The frontend can be deployed to Vercel from this GitHub repository.

Use these Vercel settings:

- Framework preset: Vite
- Build command: `cd frontend && npm ci && npm run build`
- Output directory: `frontend/dist`
- Environment variable: `VITE_API_BASE_URL=<your deployed backend API URL>`

Important: Vercel hosts the webpage. To make live evaluations work, the backend must also run on a public URL, and that URL must be added to `VITE_API_BASE_URL`.

## Deploy The Backend On Render

The frontend will show `API offline` until the FastAPI backend is deployed.

Use these Render settings:

- Service type: Web Service
- Repository: `Kimmyatta/AfriSafeBench`
- Build command: `pip install -r backend/requirements.txt`
- Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
- Environment variables:
  - `GROQ_API_KEY=<your Groq API key>`
  - `CORS_ORIGINS=https://afrisafebench-ai-safety.vercel.app`

After Render gives you a backend URL, set this in Vercel:

```text
VITE_API_BASE_URL=https://your-render-backend-url
```

## Result Files

- Benchmark CSV: `data/afrisafebench/results/benchmark_results.csv`
- Benchmark summary: `data/afrisafebench/results/benchmark_summary.json`
- Framework guidance CSV: `data/afrisafebench/results/framework_guidance_results.csv`
- Submission report: `docs/reports/AfriSafeBench_Official_Template_4Page_Draft_v3.docx`

## Limitations and Dual-Use Considerations

AfriSafeBench is an early benchmark, not a clinical or legal decision system. The scenarios are English-language, researcher-defined, and should be expanded and validated with African healthcare, legal, and policy experts.

The benchmark could be misused to train models to repeat expected category labels without improving real safety reasoning. Mitigations include requiring scenario-specific explanations, preserving missed-risk outputs, showing framework sources, and keeping human-review flags visible.
