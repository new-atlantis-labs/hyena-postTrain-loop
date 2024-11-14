#!/bin/bash

if [ ! -f /home/ec2-user/mount-s3.rpm ]; then
    wget https://s3.amazonaws.com/mountpoint-s3-release/latest/x86_64/mount-s3.rpm -O /home/ec2-user/mount-s3.rpm
fi


if ! rpm -q mount-s3; then
    sudo yum install /home/ec2-user/mount-s3.rpm -y
fi


mkdir -p /home/ec2-user/SageMaker/s3/newatlantis-raw-veba-db-prod/


mount-s3 newatlantis-raw-veba-db-prod /home/ec2-user/SageMaker/s3/newatlantis-raw-veba-db-prod/
