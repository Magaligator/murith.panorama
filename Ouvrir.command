#!/bin/bash
cd "$(dirname "$0")"
(sleep 1.5; open http://localhost:3010/) &
node dev-server.mjs 3010
