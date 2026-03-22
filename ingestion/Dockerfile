FROM public.ecr.aws/lambda/python:3.14

# Install uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory to Lambda's expected root
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies into the system site-packages
RUN uv pip install --system -r pyproject.toml

# Copy source code
COPY src/ ./src/

# Point to your index.py -> handler function
CMD [ "src.index.handler" ]
