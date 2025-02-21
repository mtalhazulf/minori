#!/bin/sh
ROOT_DIR=.

set_env() {
  ENV_NAME=$1
  ENV="$(eval echo \$$ENV_NAME)"

  for file in "$ROOT_DIR/js/"*.js* "$ROOT_DIR/index.html"; do
    sed -i "s|%%%$ENV_NAME%%%|$ENV|g" "$file"
  done
}

set_env APP_API_BASE_URL
set_env APP_REPORT_URL
