
---

# LLM Zoomcamp Portfolio

## Overview

This repository serves as a comprehensive workspace documenting the end-to-end implementation of Large Language Model (LLM) applications and Retrieval-Augmented Generation (RAG) pipelines. Developed in alignment with the DataTalksClub LLM Zoomcamp curriculum, this project focuses on modern AI engineering practices, data orchestration, and the deployment of autonomous AI agents.

## Repository Structure

The repository is organized into progressive modules, each focusing on a core aspect of LLM engineering:

* **`01-agentic-rag/`** & **`01-ollama-practice/`**
* Contains the foundational implementations of RAG architectures.
* Includes local LLM deployment strategies (utilizing Ollama) and the development of initial agentic loops for contextual data retrieval.


* **`02-vector-search/`**
* Focuses on advanced search methodologies.
* Implements core vector search algorithms, embedding generation, and hybrid search architectures leveraging Reciprocal Rank Fusion (RRF) to optimize retrieval accuracy.


* **`03-orchestration/`**
* Covers AI workflow automation and multi-agent collaboration.
* Utilizes Kestra and Docker to design, automate, and orchestrate complex LLM pipelines, including web-researching agents and multi-agent systems.


* **`05-monitoring/`**
* Implements a complete monitoring and observability stack for RAG applications.
* Containerizes a Streamlit web interface alongside PostgreSQL for conversation/feedback storage and Grafana for real-time dashboard visualization.
* Includes infrastructure-as-code deployments via Docker Compose and scripts for simulating live user data.


* **`homeworks/`**
* Contains the completed practical assignments, evaluations, and module-specific deliverables.



## Tech Stack & Tooling

* **Languages & Frameworks:** Python, Jupyter Notebook, Streamlit
* **Environment & Package Management:** Managed via `uv` (`pyproject.toml` and `uv.lock`) and `.python-version`. Designed for compatibility with WSL/Linux environments.
* **Orchestration, Containerization & Databases:** Kestra, Docker, Docker Compose, PostgreSQL
* **Observability & Monitoring:** Grafana
* **AI Models & APIs:** Google Gemini, local models via Ollama, Tavily (Web Search API)
* **Core Concepts:** RAG, Vector Databases, Hybrid Search, Autonomous Agents, Workflow Orchestration, LLM Evaluation & Monitoring

## Getting Started

### Prerequisites

Ensure you have Python installed (version specified in `.python-version`) along with `uv` for dependency management. Docker and Docker Compose are required for the orchestration and monitoring modules.

### Installation

Clone the repository and install the project dependencies:

```bash
git clone https://github.com/yaslitasomer/intro-to-RAG
cd intro-to-RAG
uv sync

```

### Module Execution

Each directory contains specific instructions and codebases for its respective module.

* For standard Python scripts and Jupyter Notebooks (Modules 1 and 2), navigate to the specific directory and execute the files within the configured virtual environment.
* For the orchestration workflows (Module 3), navigate to `03-orchestration/` and initialize the Docker containers:
```bash
cd 03-orchestration
docker compose up -d

```


* For the complete monitoring and UI stack (Module 5), run the following from the root directory to build and start the Streamlit, PostgreSQL, and Grafana containers:
```bash
docker-compose up -d --build

```


*(Note: For the initial setup, you need to build the database tables by running `POSTGRES_HOST=localhost uv run python 05-monitoring/db_init.py` before generating mock data).*

## Author

**Ömer Yaslıtaş**