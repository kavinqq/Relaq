FROM python:3.11-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH=/app

# Install chromium browser and dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install Python packages using uv
COPY relaq/requirements.txt .
RUN uv pip install --system -r requirements.txt

# Copy project files
COPY relaq/ .

# 預設命令
CMD ["tail", "-f", "/dev/null"]