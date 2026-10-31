#!/bin/sh
# usage: sh q01_cli.sh  (starts moto_server on 8501, runs the aws CLI with fake keys, stops it)
export AWS_ACCESS_KEY_ID=testing AWS_SECRET_ACCESS_KEY=testing AWS_DEFAULT_REGION=us-east-1
V=/tmp/claude-0/b10p10/v/bin
$V/moto_server -p 8501 >/tmp/claude-0/b10_q01_10/moto.log 2>&1 &
PID=$!
for i in 1 2 3 4 5 6 7 8 9 10; do curl -s -o /dev/null http://127.0.0.1:8501/ && break; sleep 1; done
E="--endpoint-url http://127.0.0.1:8501"
$V/aws $E s3 mb s3://ml-lake-cli
$V/aws $E s3api put-bucket-lifecycle-configuration --bucket ml-lake-cli --lifecycle-configuration file://lifecycle.json
$V/aws $E s3api get-bucket-lifecycle-configuration --bucket ml-lake-cli --query 'Rules[0].[ID,Filter.Prefix,Transitions[0].StorageClass,AbortIncompleteMultipartUpload.DaysAfterInitiation]' --output text
kill $PID
