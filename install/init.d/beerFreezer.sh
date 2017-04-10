#!/bin/bash

py="/usr/bin/python2"
dr="/home/pi/beerFreezer/"
bf="beerFreezer.py"

pid=$(ps -ef | grep $bf | grep -v grep | awk '{ print $2 }')

start() {
    if [[ "${pid}" -gt 0 ]]; then
        echo "beerFreezer already started. PID: ${pid}"
        exit 1
    else
        echo "Starting beerFreezer"
        cd $dr
        $py $bf &
    fi
}
 
stop() {
    if [[ "${pid}" -gt 0 ]]; then
        echo "Stopping PID: ${pid}"
        kill $pid
        sleep 2
        echo "beerFreezer stopped."
    else
        echo "beerFreezer not started"
        exit 1
    fi
}
 
case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  *)
    echo "Usage: /etc/init.d/beerFreezer {start|stop}"
    exit 1
esac
exit 0
