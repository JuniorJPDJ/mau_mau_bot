FROM python:3.13.0-alpine@sha256:81362dd1ee15848b118895328e56041149e1521310f238ed5b2cdefe674e6dbf

# renovate: datasource=repology depName=alpine_3_20/gettext versioning=loose
ARG         GETTEXT_VERSION="0.22.5-r0"

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
