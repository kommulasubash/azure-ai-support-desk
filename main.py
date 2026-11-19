
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

# Replace with your actual Foundry project endpoint
ENDPOINT = "https://azure-ai-support-desk-resource.services.ai.azure.com/api/projects/azure-ai-support-desk"

# Use your deployed model name
MODEL = "gpt-5-mini"

project = AIProjectClient(
    endpoint=ENDPOINT,
    credential=DefaultAzureCredential()
)

# Agent 1: IT issue classifier
project.agents.create_version(
    agent_name="issue-classifier",
    definition=PromptAgentDefinition(
        model=MODEL,
        instructions=(
            "You are an IT support classification agent. "
            "Classify the issue into a category and assign "
            "Low, Medium, or High priority. "
            "Explain your decision briefly."
        ),
    ),
)

# Agent 2: IT troubleshooting specialist
project.agents.create_version(
    agent_name="solution-agent",
    definition=PromptAgentDefinition(
        model=MODEL,
        instructions=(
            "You are an IT support specialist. "
            "Use the issue and classification provided. "
            "Suggest three safe, practical troubleshooting "
            "steps. Do not claim to have fixed the problem."
        ),
    ),
)

issue = input("Enter your IT issue: ")

# Run first agent
classifier = project.get_openai_client(
    agent_name="issue-classifier"
)

result1 = classifier.responses.create(input=issue)

print("\nCLASSIFICATION:")
print(result1.output_text)

# Pass the first agent's result to the second agent
solver = project.get_openai_client(
    agent_name="solution-agent"
)

result2 = solver.responses.create(
    input=(
        f"Original issue: {issue}\n"
        f"Classification: {result1.output_text}"
    )
)

print("\nSUGGESTED SOLUTION:")
print(result2.output_text)
