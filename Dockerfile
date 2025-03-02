FROM python:3.13.2-alpine@sha256:323a717dc4a010fee21e3f1aac738ee10bb485de4e7593ce242b36ee48d6b352

# renovate: datasource=repology depName=alpine_3_21/gettext versioning=loose
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
