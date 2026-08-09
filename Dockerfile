FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked

COPY . .

# Changed the path to point directly to your app.py inside the 05-monitoring folder
CMD ["uv", "run", "streamlit", "run", "05-monitoring/app.py", "--server.port=8501", "--server.address=0.0.0.0"]