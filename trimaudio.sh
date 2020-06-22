#!/bin/bash

input=$1
output=$2
start_time=$3
end_time=$4

ffmpeg -i $input -ss $start_time -to $end_time -c copy $output
# e.g. ./trimaudio.sh ./audio/david-cooper-aud.wav ./audio/david-cooper-17-20.wav 17 20
