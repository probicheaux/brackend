#!/bin/bash
docker-compose run brackend python brackend/delete_everything.py
docker-compose run brackend python brackend/delete_firebase_users.py
