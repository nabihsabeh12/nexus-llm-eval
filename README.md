
# Nexus DeepEval

This project provides a QA and evaluation interface for the Digital Nexus Agent using [DeepEval](https://deepeval.com) metrics. It allows you to test your agent’s responses, assess their quality, and visualize evaluation results directly from a Streamlit UI.

---

## Features

- Live integration with Nexus agent via API
- DeepEval metrics (faithfulness, relevancy, hallucination detection, etc.)
- Dynamic explanations for each score
- Graceful error handling and real-time feedback
- Streamlit interface for technical and non-technical stakeholders

---

## Project Structure

```
deepeval_nexus_test/
│
├── app.py              # Streamlit UI for evaluation
├── test_agent.py       # CLI-based test runner
├── .env.example        # Sample environment config (safe for sharing)
├── venv/               # Virtual environment (ignored)
└── README.md           # This file
```

---

## Setup Instructions

### 1. Clone this repo (or download locally)

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist yet, manually install:

```bash
pip install streamlit deepeval openai python-dotenv requests
```

### 4. Configure environment variables

Create a `.env` file using the `.env.example` template:

```bash
cp .env.example .env
```

Then fill in your actual credentials:

```env
API_URL=https://your-nexus-api.azurewebsites.net/api/aisearch
API_KEY=your-api-key-here
OPENAI_API_KEY=your-openai-api-key-here  # Optional for advanced metrics
```

---

## Run the Streamlit App

```bash
streamlit run app.py
```

Then open your browser to: `http://localhost:8501`

---

## Metrics Evaluated

| Metric                | Description                                                                |
|-----------------------|-----------------------------------------------------------------------------|
| Answer Relevancy      | Checks if the agent's answer stays focused and relevant to the question     |
| Faithfulness           | Evaluates whether the answer sticks to the context or hallucinates          |
| Contextual Recall      | Measures if key points from the context are included                       |
| Contextual Precision   | Ensures no extra, unsupported info is added                                |
| Toxicity               | Flags unsafe or offensive language                                          |
| Bias                   | Detects gender/racial bias                                                  |
| (Optional) Role Adherence | Checks if the agent stays in its persona (e.g., Sales Assistant)     |
| (Optional) Summarization   | Evaluates summary quality                                              |
| (Optional) Task Completion | Checks if the response finishes the intended task                    |

---

## Use Cases

- QA team reviewing LLM answers before production
- Engineering teams monitoring LLM performance over time
- Business/solution teams verifying message clarity and compliance

---

## Notes

- This is optimized for evaluating Nexus AI Agent with context-aware questions and expected answers.
- You can run tests manually via `test_agent.py` or use the Streamlit UI.

---

## Contact

Built by Nabih and the Nexus AI Engineering team  

