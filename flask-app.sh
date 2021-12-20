#!/bin/bash
./upgrade.sh
gunicorn --log-level info -w 3 -b 0.0.0.0:8000 brackend:app
