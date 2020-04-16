#!/bin/bash

# download the code
mv mape-data-importer/ kafka-influx/
find ./kafka-influx -type d -exec sudo chmod -R 755 {} \;
find ./kafka-influx -type f -exec sudo chmod 664 {} \;
chmod a+x ./kafka-influx/deployment/run.sh ./kafka-influx/deployment/clean.sh
cp ./kafka-influx/deployment/Dockerfile .
sudo docker build -t kafka-influx .
source ./kafka-influx/deployment/clean.sh