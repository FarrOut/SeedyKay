#!/bin/bash -xe
yum update -y
yum install -y aws-cfn-bootstrap
yum install -y java-1.8.0-openjdk
yum install -y unzip
# Install the files and packages from the metadata
/opt/aws/bin/cfn-init -v --stack ${AWS::StackName} --resource Apollo11 --configsets install --region ${AWS::Region}