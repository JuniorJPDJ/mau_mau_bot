FROM python:3.15.2-alpine@sha256:0f9552bb28711333da16915ec146f5e6bb44a7fdac9ced15dc17c2e0206346dd

# renovate: datasource=repology depName=alpine_3_24/gettext versioning=loose
ARG         GETTEXT_VERSION="1.0-r0"

WORKDIR     /app

ADD         requirements.txt .

RUN         --mount=type=cache,sharing=locked,target=/root/.cache,id=home-cache-$TARGETPLATFORM \
            apk add --no-cache \
              gettext=${GETTEXT_VERSION} \
            && \
            pip install -r requirements.txt && \
            chown -R nobody:nogroup /app

COPY        --chown=nobody:nogroup . .

USER        nobody

RUN         cd locales && \
            find . -maxdepth 2 -type d -name 'LC_MESSAGES' -exec ash -c 'msgfmt {}/unobot.po -o {}/unobot.mo' \;

VOLUME      /app/data
ENV         UNO_DB=/app/data/uno.sqlite3

ENTRYPOINT  [ "python", "bot.py" ]
