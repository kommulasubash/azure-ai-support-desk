
import json
import os
import logging

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

app = func.FunctionApp()

@app.route(
    route="solve",
    methods=["POST"],
    auth_level=func.AuthLevel.FUNCTION
)
def solve_issue(req: func.HttpRequest) -> func.HttpResponse:

    try:
        data = req.get_json()
        issue = data.get("issue", "").strip()

        if not issue:
            return func.HttpResponse(
                json.dumps({"error": "Issue is required"}),
                status_code=400,
                mimetype="application/json"
            )

        project = AIProjectClient(
            endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            credential=DefaultAzureCredential()
        )

        # Agent 1 - Classifier
        classifier = project.get_openai_client(
            agent_name="issue-classifier"
        )

        result1 = classifier.responses.create(
            input=issue
        )

        # Agent 2 - Solution Agent
        solver = project.get_openai_client(
            agent_name="solution-agent"
        )

        result2 = solver.responses.create(
            input=f"""
            Issue: {issue}

            Classification:
            {result1.output_text}

            Provide troubleshooting steps.
            """
        )

        response = {
            "issue": issue,
            "classification": result1.output_text,
            "solution": result2.output_text
        }

        return func.HttpResponse(
            json.dumps(response),
            status_code=200,
            mimetype="application/json"
        )

    except (ValueError, AttributeError):
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON request"}),
            status_code=400,
            mimetype="application/json"
        )

    except Exception:
        logging.exception("Agent execution failed")
        return func.HttpResponse(
            json.dumps({"error": "Agent execution failed"}),
            status_code=500,
            mimetype="application/json"
        )
