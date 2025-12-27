FROM python:3.12.7-slim-bookworm

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

USER root

RUN apt-get update && apt-get install -y \
    && apt-get clean
USER user

COPY --chown=user . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
