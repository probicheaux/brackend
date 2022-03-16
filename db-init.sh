#!/bin/bash
#PGPASSWORD=postgres
psql -s -p 5438 -h localhost postgres postgres -c "CREATE DATABASE brackend;"