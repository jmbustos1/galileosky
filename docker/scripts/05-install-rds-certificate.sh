# /bin/bash

wget https://s3.amazonaws.com/rds-downloads/rds-ca-2019-root.pem
mkdir -p /certificados
mv rds-ca-2019-root.pem /certificados
