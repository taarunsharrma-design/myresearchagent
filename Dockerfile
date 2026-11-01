FROM public.ecr.aws/lambda/python:3.12

COPY pyproject.toml uv.lock ./

# Install exactly what uv.lock pins, prebuilt wheels only (no yum, gcc or Rust needed)
RUN pip install --no-cache-dir uv==0.13.6 && \
    uv export --frozen --no-dev --no-emit-project -o requirements.txt && \
    uv pip install --no-cache --only-binary :all: --target "${LAMBDA_TASK_ROOT}" -r requirements.txt && \
    rm requirements.txt

COPY src/ ${LAMBDA_TASK_ROOT}/src/
COPY config/ ${LAMBDA_TASK_ROOT}/config/
COPY lambda_function/ ${LAMBDA_TASK_ROOT}/lambda_function/

CMD ["lambda_function.handler.lambda_handler"]