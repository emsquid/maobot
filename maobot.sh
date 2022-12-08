#!/bin/bash

configfolder=$HOME/.config/maobot
logfile=$configfolder/maobot.log
pidfile=$configfolder/maobot.pid
pythonfile="$(dirname "${BASH_SOURCE[0]}")"/main.py

function store_pid() {
    echo "$1" >"$pidfile"
}

function kill_previous_process() {
    if test -f "$pidfile"; then
        pid=$(cat "$pidfile" 2>/dev/null)
        kill "$pid" &>/dev/null
        rm "$pidfile" 2>/dev/null
    fi
}

function start() {
    mkdir -p "$configfolder"
    kill_previous_process
    nohup python3 "$pythonfile" >>"$logfile" 2>/dev/null &
    store_pid "$!"
}

command=$1

if [[ $command == "start" ]]; then
    echo "Bot started"
    start
elif [[ $command == "stop" ]]; then
    echo "Bot stopped"
    kill_previous_process
fi
