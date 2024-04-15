#!/bin/bash

if psql -h localhost -U postgres -W -t -c '\du' | cut -d \| -f 1 | grep -qw jm; then
    echo "user exists"
    # $? is 0
else
    psql -h localhost -U postgres -W -c "CREATE ROLE $USER_NAME WITH LOGIN SUPERUSER PASSWORD '$PASSWORD';"
fi
