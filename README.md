
---

# LLM Zoomcamp Portfolio

## Overview

This repository serves as a comprehensive workspace documenting the end-to-end implementation of Large Language Model (LLM) applications and Retrieval-Augmented Generation (RAG) pipelines. Developed in alignment with the DataTalksClub LLM Zoomcamp curriculum, this project focuses on modern AI engineering practices, data orchestration, and the deployment of autonomous AI agents.

## Repository Structure

The repository is organized into progressive modules, each focusing on a core aspect of LLM engineering:

* **`01-agentic-rag/` & `01-ollama-practice/**`
* Contains the foundational implementations of RAG architectures.
* Includes local LLM deployment strategies (utilizing Ollama) and the development of initial agentic loops for contextual data retrieval.


* **`02-vector-search/`**
* Focuses on advanced search methodologies.
* Implements core vector search algorithms, embedding generation, and hybrid search architectures leveraging Reciprocal Rank Fusion (RRF) to optimize retrieval accuracy.


* **`03-orchestration/`**
* Covers AI workflow automation and multi-agent collaboration.
* Utilizes Kestra and Docker to design, automate, and orchestrate complex LLM pipelines, including web-researching agents and multi-agent systems.


* **`homeworks/`**
* Contains the completed practical assignments, evaluations, and module-specific deliverables.



## Tech Stack & Tooling

* **Languages:** Python, Jupyter Notebook
* **Environment & Package Management:** Managed via `uv` (`pyproject.toml` and `uv.lock`) and `.python-version`. Designed for compatibility with WSL/Linux environments.
* **Orchestration & Containerization:** Kestra, Docker, Docker Compose
* **AI Models & APIs:** Google Gemini, local models via Ollama, Tavily (Web Search API)
* **Core Concepts:** RAG, Vector Databases, Hybrid Search, Autonomous Agents, Workflow Orchestration

## Getting Started

### Prerequisites

Ensure you have Python installed (version specified in `.python-version`) along with `uv` for dependency management. Docker and Docker Compose are required for the orchestration module.

### Installation

Clone the repository and install the project dependencies:

```bash
git clone <your-repository-url>
cd <repository-directory>
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

## Author

**Ömer Yaslıtaş**