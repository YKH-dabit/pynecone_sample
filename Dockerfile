FROM python:3.11-slim as base

RUN adduser --disabled-password pynecone

RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_19.x | bash - \
    && apt-get update && apt-get install -y \
    nodejs \
    unzip \
    && rm -rf /var/lib/apt/lists/*
ENV PATH="/app/venv/bin:$PATH"


FROM base as build


ENV VIRTUAL_ENV=/app/venv
WORKDIR /app
RUN chown pynecone:pynecone /app
USER pynecone
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY base_env .

RUN pip install -r requirements.txt
ENV BUN_INSTALL="/app/.bun"

FROM build as init

WORKDIR /app

COPY --chown=pynecone pcconfig.py /app/
COPY --chown=pynecone pynecone_sample/ /app/pynecone_sample/
RUN pc init && cd .web && npm install\
            && cd ..   && pc export --no-zip \
            && /app/.bun/bin/bun install serve
RUN /app/.bun/bin/bun install serve


FROM build as runtime

WORKDIR /app
COPY --chown=pynecone assets/ /app/assets/
COPY --chown=pynecone pcconfig.py /app/
COPY --chown=pynecone pynecone_sample/ /app/pynecone_sample/
COPY --chown=pynecone --from=init /app/.web/_static /app/static/
COPY --chown=pynecone --from=init /app/.bun/ /app/.bun/
COPY --chown=pynecone --from=init /app/bun.lockb /app/
COPY --chown=pynecone --from=init /app/node_modules/ /app/node_modules/
RUN pc init

ENTRYPOINT [ "/app/entry.sh" ]