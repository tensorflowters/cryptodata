ARG PYTHON_VERSION=3.11.7

FROM python:${PYTHON_VERSION}-slim-bookworm

RUN apt update && apt upgrade -y && \
    apt install -y \
    sshpass \
    expect && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -r --gid 1000 ansible-controller && \
    useradd -r -g ansible-controller --uid 1000 ansible-controller && \
    mkdir -p /home/ansible-controller && \
    chown -R ansible-controller:ansible-controller /home/ansible-controller

WORKDIR /home/ansible-controller

ENV PATH="/home/ansible-controller/.local/bin:$PATH"

COPY --chown=1000 --chmod=755 . ./ansible-deployment/

USER ansible-controller

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --user pipx && \
    python3 -m pipx ensurepath && \
    python3 -m pip install --user --upgrade pipx && \
    pipx install --include-deps ansible && \
    pipx upgrade --include-injected ansible && \
    pipx inject --include-apps ansible argcomplete && \
    ansible-galaxy install geerlingguy.security && \
    ansible-galaxy install l3d.no_sleep

ENTRYPOINT [ "./ansible-deployment/entrypoint.sh" ]