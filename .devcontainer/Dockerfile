# Dev container for ghes-governance — Vertical Slice 1 (Python 3.12+, read-only engine).
# gh CLI and Node arrive via devcontainer features (see devcontainer.json);
# Claude Code is installed in postCreateCommand once Node exists.
FROM mcr.microsoft.com/devcontainers/python:3.12

# jq — used by the issue-tracker conventions (docs/agents/issue-tracker.md)
RUN apt-get update && apt-get install -y --no-install-recommends \
    jq \
    && rm -rf /var/lib/apt/lists/*

# uv — copied from the official image so it sits on PATH for every user
# (an install-script run as root lands in /root/.local/bin, invisible to remoteUser vscode)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/
