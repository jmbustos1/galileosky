# /bin/bash

apt-get update
apt-get install python3.9 python3.9-dev python3-virtualenv \
                git libpq-dev build-essential wget \
                --no-install-recommends --assume-yes
apt-get clean
