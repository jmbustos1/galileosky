# /bin/bash

apt-get update
apt-get install python3.9 python3-virtualenv \
                libpq5 gdal-bin wget \
                --no-install-recommends --assume-yes
apt-get clean
