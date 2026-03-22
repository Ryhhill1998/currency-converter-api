# Stage 1: Get UV
FROM ghcr.io/astral-sh/uv:latest AS uv

# Stage 2: Bundle dependencies
FROM public.ecr.aws/lambda/python:3.14-arm64 AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy

WORKDIR ${LAMBDA_TASK_ROOT}

# Install dependencies into the task root folder directly
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install --no-cache --target "${LAMBDA_TASK_ROOT}" -r pyproject.toml

# Stage 3: Final Runtime
FROM public.ecr.aws/lambda/python:3.14-arm64
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy the pre-installed dependencies from the builder
COPY --from=builder ${LAMBDA_TASK_ROOT} ${LAMBDA_TASK_ROOT}

# Copy your source code
COPY src/ ./src/

# Lambda will look for handler() inside src/index.py
CMD ["src.index.handler"]
