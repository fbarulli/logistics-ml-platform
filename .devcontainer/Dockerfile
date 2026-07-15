# syntax=docker/dockerfile:1.7

FROM ghcr.io/astral-sh/uv:latest AS uv

FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm

ENV DEBIAN_FRONTEND=noninteractive

############################################################
# Base packages
############################################################

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-17-jdk \
        git \
        curl \
        wget \
        unzip \
        jq \
        vim \
        make \
        build-essential \
        ca-certificates \
        gnupg \
        lsb-release \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

############################################################
# uv
############################################################

COPY --from=uv /uv /usr/local/bin/uv
COPY --from=uv /uvx /usr/local/bin/uvx

############################################################
# kubectl
############################################################

RUN ARCH=$(dpkg --print-architecture) && \
    curl -fsSL -o /usr/local/bin/kubectl \
    "https://dl.k8s.io/release/$(curl -fsSL https://dl.k8s.io/release/stable.txt)/bin/linux/${ARCH}/kubectl" && \
    chmod +x /usr/local/bin/kubectl

############################################################
# Helm
############################################################

RUN curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

############################################################
# Kind
############################################################

RUN ARCH=$(dpkg --print-architecture) && \
    curl -fsSL -o /usr/local/bin/kind \
    "https://kind.sigs.k8s.io/dl/latest/kind-linux-${ARCH}" && \
    chmod +x /usr/local/bin/kind

############################################################
# Java
############################################################

RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "arm64" ]; then \
        echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64" >/etc/profile.d/java.sh; \
    else \
        echo "export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64" >/etc/profile.d/java.sh; \
    fi

############################################################
# Workspace
############################################################

WORKDIR /workspace

############################################################
# Verify tools
############################################################

RUN python --version && \
    uv --version && \
    kubectl version --client && \
    helm version --short && \
    kind version && \
    java -version