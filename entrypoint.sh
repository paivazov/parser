#!/bin/bash

# Run alembic migrations on project startup.
cd db && alembic upgrade head
