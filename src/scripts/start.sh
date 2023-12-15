#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

uvicorn app:app --host 0.0.0.0 --reload
