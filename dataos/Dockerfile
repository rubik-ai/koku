FROM registry.access.redhat.com/ubi8/python-38:latest

ARG PIPENV_DEV=False
ARG USER_ID=1000

# needed for successful collectstatic
ARG PROMETHEUS_MULTIPROC_DIR=/tmp

ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    PIP_NO_CACHE_DIR=off \
    ENABLE_PIPENV=true \
    PIN_PIPENV_VERSION="2018.11.26" \
    APP_HOME="/opt/app-root/src/koku" \
    APP_MODULE="koku.wsgi" \
    APP_CONFIG="gunicorn_conf.py" \
    DISABLE_MIGRATE=true \
    DJANGO_READ_DOT_ENV_FILE=false \
    SUMMARY="caretaker-cloud-kernel-cost is the caretaker cloud kernel cost visibility processor" \
    DESCRIPTION="caretaker-cloud-kernel-cost is the caretaker cloud kernel cost visibility processor"

LABEL summary="$SUMMARY" \
    description="$DESCRIPTION" \
    name="caretaker-cloud-kernel-cost" \
    version="1" \
    maintainer="TMDC"

USER root

# Get latest packages
RUN dnf -y upgrade
COPY ./.s2i/bin/ $STI_SCRIPTS_PATH

# Copy application files to the image.
COPY . /tmp/src/.

RUN \
    ls -la /tmp/src/ && \
    /usr/bin/fix-permissions /tmp/src && \
    chmod 755 $STI_SCRIPTS_PATH/assemble $STI_SCRIPTS_PATH/run && \
    groupadd -g ${USER_ID} caretaker && \
    useradd -m -s /bin/bash -g ${USER_ID} -u ${USER_ID} -G root caretaker && \
    chmod g+rwx /opt

USER caretaker

RUN umask u=rwx,g=rwx,o=rx && \
    $STI_SCRIPTS_PATH/assemble && \
    mv /opt/app-root/src/dataos/Makefile /opt/app-root/src/Makefile && \
    ls -la /opt/app-root/src && \
    ls -la /opt/app-root/src/koku

EXPOSE 8000

WORKDIR /opt/app-root/src

CMD $STI_SCRIPTS_PATH/run
