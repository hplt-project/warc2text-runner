#!/bin/bash
RPATH=$1
LPATH=$2

NAME=$(basename $RPATH)
FIFO=${NAME}.fifo


# rclone will write messages about files downloaded (among others) to the pipe
rclone copy --log-level INFO --log-file $FIFO --transfers 16 -P $RPATH $LPATH/$NAME
