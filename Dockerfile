FROM python:3.12.12-alpine@sha256:d82291d418d5c47f267708393e40599ae836f2260b0519dd38670e9d281657f5

# renovate: datasource=repology depName=alpine_3_22/gettext versioning=loose
ARG         GETTEXT_VERSION="0.24.1-r0"

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
