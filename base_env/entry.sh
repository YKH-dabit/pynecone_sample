#!/bin/bash
/app/.bun/bin/bun serve static -p 3000 &
python3 -m pynecone.pc run --env prod --no-frontend --port 8000