FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Default: CPU-only torch (~200MB, fast build). Set TORCH_GPU=1 for full torch+LoRA on GPU.
# Example GPU build: docker compose build --build-arg TORCH_GPU=1
ARG TORCH_GPU=0
RUN if [ "$TORCH_GPU" = "1" ]; then \
      pip install --no-cache-dir torch && pip install --no-cache-dir -r requirements.txt; \
    else \
      pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu && \
      pip install --no-cache-dir -r requirements.txt; \
    fi

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
