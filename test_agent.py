import sys
import os
import requests
from dotenv import load_dotenv
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
    ToxicityMetric,
    BiasMetric,
    RoleAdherenceMetric,
    SummarizationMetric,
    TaskCompletionMetric,
)

# Handle Unicode in terminal (Mac compatibility)
sys.stdout.reconfigure(encoding="utf-8")

# Load environment variables from .env
load_dotenv()
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

# Sanity check: Print loaded keys
print("✅ API_URL =", API_URL)
print("✅ API_KEY loaded =", bool(API_KEY))

# Define test input
question = "Is ServiceFabric available at JFK10?"
conversation_id = "test_conversation_123"

# Call your LLM agent
headers = {
    "x-functions-key": API_KEY,
    "Content-Type": "application/json",
}
payload = {
    "conversation": question,
    "conversation_id": conversation_id
}

response = requests.post(API_URL, json=payload, headers=headers)

if response.status_code == 200:
    agent_answer = response.json().get("answer") or response.text
else:
    print(f"❌ API Error {response.status_code}: {response.text}")
    sys.exit(1)

# Define context and expected output
context = (
    "ServiceFabric is available at JFK10 (operational site code NYC2, also called JFK010). "
    "The site is 'SF Enabled,' supporting digital connectivity via ServiceFabric. Key details include:\n"
    "- Location: 111 8th Avenue, New York, NY\n"
    "- Deployment Type: Colo & Scale\n"
    "- Platform Diversity: Metro Connect links primary and redundant locations\n"
    "- 100G Port Availability: Yes\n"
    "Clients at JFK10 can leverage ServiceFabric for virtual interconnectivity."
)

expected_output = (
    "Yes, ServiceFabric is available at JFK10 (also known as JFK010, site code NYC2). "
    "The site supports digital connectivity via ServiceFabric. Key details:\n"
    "- Location: 111 8th Avenue, New York, NY\n"
    "- Deployment Type: Colo & Scale\n"
    "- Metro Connect: links to primary and redundant sites\n"
    "- 100G Ports: Available\n"
    "This enables clients to use ServiceFabric for virtual and physical interconnection."
)

# Debug output
print("\n🔎 DEBUG:")
print("  ➤ Question:", repr(question))
print("  ➤ Agent Answer:", repr(agent_answer))
print("  ➤ Expected Output:", repr(expected_output))
print("  ➤ Context:", repr(context))

# Create test case for evaluation
test_case = LLMTestCase(
    input=question,
    actual_output=agent_answer,
    expected_output=expected_output,
    retrieval_context=[context]
)

# List of metrics to evaluate
metrics = [
    AnswerRelevancyMetric(threshold=0.7),
    FaithfulnessMetric(threshold=0.6),
    ContextualRecallMetric(threshold=0.7),
    ContextualPrecisionMetric(threshold=0.7),
    ToxicityMetric(threshold=0.9),
    BiasMetric(threshold=0.9),
    # RoleAdherenceMetric(threshold=0.8),  # optional
    SummarizationMetric(threshold=0.7),
    TaskCompletionMetric(threshold=0.7)
]

# Evaluate and print results
print("\n📊 Evaluation Results:")
for metric in metrics:
    try:
        score = metric.measure(test_case)
        passed = score >= metric.threshold
        print(f"{'✅' if passed else '❌'} {metric.__class__.__name__}: {score:.2f} (Threshold: {metric.threshold})")
    except Exception as e:
        print(f"⚠️ Error running {metric.__class__.__name__}: {e}")