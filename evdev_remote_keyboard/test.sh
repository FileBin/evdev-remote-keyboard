#!/usr/bin/env bash

cat ./test-events.txt | while read line
do
    echo $line
    sleep 1
done