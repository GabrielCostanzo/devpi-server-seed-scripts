#!/bin/bash
DOMAIN="todo-remove-domain"
DOMAIN_OWNER="730335357252"
REPO="todo-remove-repo"
REGION="us-east-1"

devpi login cache --password 123

CODEARTIFACT_AUTH_TOKEN=$(aws codeartifact get-authorization-token \
    --domain "$DOMAIN" \
    --domain-owner "$DOMAIN_OWNER" \
    --region "$REGION" \
    --query authorizationToken \
    --output text)

export CODEARTIFACT_AUTH_TOKEN=$CODEARTIFACT_AUTH_TOKEN
export CODEARTIFACT_UPLOAD_URL=`aws codeartifact get-repository-endpoint --domain $DOMAIN --domain-owner $DOMAIN_OWNER --repository $REPO --region $REGION --format pypi --query repositoryEndpoint --output text`

export CODEARTIFACT_INDEX_URL=https://aws:$CODEARTIFACT_AUTH_TOKEN@$DOMAIN-$DOMAIN_OWNER.d.codeartifact.$REGION.amazonaws.com/pypi/$REPO/simple/

export PROD_MIRROR_INDEX_URL=http://localhost:4040/cache/prod_mirror
export DEV_INDEX_URL=http://localhost:4040/costanga/dev

pip install -v \
    --index-url $PROD_MIRROR_INDEX_URL \
    --extra-index-url $CODEARTIFACT_INDEX_URL \
    --extra-index-url $DEV_INDEX_URL \
    prettytable

uv pip install -v \
    --dry-run \
    --no-cache \
    --index-strategy first-index \
    --default-index $PROD_MIRROR_INDEX_URL \
    --index $CODEARTIFACT_INDEX_URL \
    --index $DEV_INDEX_URL \
    prettytable
    

uv pip install -v \
    --dry-run \
    --no-cache \
    --index-strategy first-index \
    --default-index $PROD_MIRROR_INDEX_URL \
    todo-remove-cognito-testing

uv pip install -v \
    --dry-run \
    --no-cache \
    --no-deps \
    --index-strategy unsafe-first-match \
    --default-index $DEV_INDEX_URL \
    --index $CODEARTIFACT_INDEX_URL \
    --index $PROD_MIRROR_INDEX_URL \
    todo-remove-cognito-testing


uv pip install -v \
    --dry-run \
    --no-cache \
    --no-deps \
    todo-remove-cognito-testing