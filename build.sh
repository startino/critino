#!/usr/bin/env bash

(cd web && nixpacks build . -o . --build-cmd "" --start-cmd "pnpm dev --host 0.0.0.0")

docker compose build
