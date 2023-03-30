#!/bin/bash -e
. .env

if [ ! -f openai-models.json ]; then
	curl https://api.openai.com/v1/models \
  	-H "Authorization: Bearer $OPENAI_API_KEY" > openai-models.json
fi

jq -r '.data[].id' openai-models.json | sort | uniq
