import os
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    ToxicityMetric,
    BiasMetric,
    # RoleAdherenceMetric,  # Uncomment if DeepEval is updated
    # SummarizationMetric,  # Optional
    # TaskCompletionMetric, # Optional
)
from deepeval.test_case import LLMTestCase

# ─── Setup ───────────────────────────────────────────────────────
load_dotenv()
API_URL  = os.getenv("API_URL")
API_KEY  = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # optional

st.set_page_config(page_title="Nexus QA Metrics", layout="wide")

# ─── Explanation Generator ───────────────────────────────────────
def generate_explanation(metric_name, score):
    if score == "⚠️" or score is None:
        return "⚠️ Metric could not be evaluated."
    
    score = float(score)

    if metric_name == "AnswerRelevancy":
        return "Answer was relevant." if score >= 0.7 else "Answer was off-topic or too vague."
    elif metric_name == "Faithfulness":
        return "Answer sticks to the context." if score >= 0.6 else "Answer may include hallucinated content."
    elif metric_name == "ContextualRecall":
        return "Answer covers key points from the context." if score >= 0.7 else "Answer misses some important details."
    elif metric_name == "ContextualPrecision":
        return "Answer is sharp and well-supported by the context." if score >= 0.7 else "Answer includes unsupported or extra content."
    elif metric_name == "Toxicity":
        return "✅ No toxic language detected." if score == 0 else "⚠️ Some potentially toxic language detected."
    elif metric_name == "Bias":
        return "✅ No bias detected." if score == 0 else "⚠️ Potential bias detected in the answer."
    elif metric_name == "Summarization":
        return "Answer summarizes the content well." if score >= 0.7 else "Summary lacks clarity or misses details."
    elif metric_name == "TaskCompletion":
        return "The task was completed as expected." if score >= 0.7 else "Answer did not fully complete the requested task."
    elif metric_name == "RoleAdherence":
        return "Agent stayed in role." if score >= 0.8 else "Agent deviated from its defined persona."
    else:
        return "No explanation available for this metric."

# ─── Sidebar inputs ───────────────────────────────────────────────
st.sidebar.header("Test Configuration")
question = st.sidebar.text_input("Question", "Is ServiceFabric available at JFK10?")
context  = st.sidebar.text_area(
    "Context",
    """
ServiceFabric is available at JFK10…
– Location: 111 8th Avenue, New York, NY
– Deployment Type: Colo & Scale
– 100G Port Availability: Yes
"""
)
expected = st.sidebar.text_area(
    "Expected output",
    """Yes, ServiceFabric is available at JFK10 (operational site code for NYC2, also called JFK010). The site is "SF Enabled," indicating that digital connectivity via ServiceFabric is supported. Key details include:
Location: 111 8th Avenue, New York, NY
Deployment Type: Colo & Scale
Platform Diversity: Metro Connect links primary location (32 Avenue of the Americas) and redundant location (60 Hudson Street)
Availability of 100G Ports: Yes
This means clients at JFK10 can leverage ServiceFabric for virtual network interconnectivity alongside physical and metro connect options.
Would you like me to walk you through the best-fit Digital Realty offering for leveraging ServiceFabric at JFK10 or explore connectivity options there?"""
)
run = st.sidebar.button("Run Test")

# ─── Main UI ──────────────────────────────────────────────────────
st.title("Nexus Agent QA → DeepEval Metrics")

if run:
    # Call the agent
    conv_id = str(uuid.uuid4())
    headers = {"x-functions-key": API_KEY, "Content-Type": "application/json"}
    payload = {"conversation": question, "conversation_id": conv_id}
    resp = requests.post(API_URL, json=payload, headers=headers)

    if resp.status_code != 200:
        st.error(f"Agent API error {resp.status_code}: {resp.text}")
    else:
        agent_answer = resp.json().get("answer") or resp.text

        # Build test case
        test_case = LLMTestCase(
            input=question,
            actual_output=agent_answer,
            expected_output=expected,
            retrieval_context=[context]
        )

        # Define metrics
        metrics = [
            AnswerRelevancyMetric(threshold=0.7),
            FaithfulnessMetric(threshold=0.6),
            ContextualRecallMetric(threshold=0.7),
            ContextualPrecisionMetric(threshold=0.7),
            ToxicityMetric(threshold=0.1),
            BiasMetric(threshold=0.1),
            # RoleAdherenceMetric(threshold=0.8, role="AI Sales Assistant"),
            # SummarizationMetric(threshold=0.7),
            # TaskCompletionMetric(threshold=0.7, tools_called=["sf_lookup"]),
        ]

        # Run and collect results
        results = []
        for m in metrics:
            try:
                score = m.measure(test_case)
                metric_name = m.__class__.__name__.replace("Metric", "")
                results.append({
                    "Metric": metric_name,
                    "Score": f"{score:.2f}",
                    "Passed": "✅" if score >= m.threshold else "❌",
                    "Threshold": m.threshold,
                    "What It Means": generate_explanation(metric_name, score)
                })
            except Exception as e:
                metric_name = m.__class__.__name__.replace("Metric", "")
                results.append({
                    "Metric": metric_name,
                    "Score": "⚠️",
                    "Passed": "⚠️",
                    "Threshold": m.threshold,
                    "What It Means": generate_explanation(metric_name, None)
                })
                st.warning(f"⚠️ {metric_name} failed: {e}")

        # Display results
        st.subheader("Agent’s Answer")
        st.write(agent_answer)

        st.subheader("DeepEval Results")
        st.table(results)