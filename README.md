# Azure AI Support Desk

An IT support desk solution powered by Azure AI Projects and Azure Functions. It uses multi-agent orchestration to classify incoming IT support issues and provide actionable troubleshooting guidance.

## Architecture & Features

- **Issue Classifier Agent**: Analyzes reported IT issues, categorizes them, and assigns appropriate priority levels (Low, Medium, High).
- **Solution Agent**: Generates practical, step-by-step troubleshooting recommendations based on the issue description and classification.
- **Azure Functions HTTP API**: Exposes a `/api/solve` endpoint to invoke the multi-agent workflow via HTTP POST requests.
- **Standalone CLI**: A local script (`main.py`) for defining the prompt agents and testing interactive queries in the terminal.

## Prerequisites

- Python 3.10+
- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) logged in (`az login`)
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- Azure AI Foundry project with a deployed language model (e.g., `gpt-4o-mini` or `gpt-5-mini`)

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd azure-ai-support-desk
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows (PowerShell)
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment settings**:
   Copy `local.settings.example.json` to `local.settings.json` and update `FOUNDRY_PROJECT_ENDPOINT` with your Azure AI Foundry project endpoint.
   ```bash
   cp local.settings.example.json local.settings.json
   ```

## Running the Application

### Option 1: Standalone Script
```bash
python main.py
```

### Option 2: Azure Functions Local Server
```bash
func start
```
Test the `/api/solve` endpoint:
```bash
curl -X POST http://localhost:7071/api/solve \
  -H "Content-Type: application/json" \
  -d '{"issue": "Cannot connect to company VPN"}'
```
