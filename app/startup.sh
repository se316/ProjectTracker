#!/bin/bash

# create tables if they don't exist then start the server
python3 create_sql_tables.py && \
python3 main.py
