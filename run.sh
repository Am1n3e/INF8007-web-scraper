#!/bin/bash
#
# Clone and run a node webserver, then run the crawler on it

#######################################
# Print error message with the missing args and exits with 1.
# Arguments:
#   arg_name: Missing argument name
#######################################
function report_missing_arg() {
    echo "Error: Missing $1"
    exit 1
}

#######################################
# Check the requirements for the scripts 
# Arguments:
#   arg_name: Missing argument name
#######################################
function check_requirements() {
    git_exits=
    npm_exits=1
    echo "Checking requirements"

     
    git_found=$(which git)
    [ -z "$git_found" ] && echo "git ... Not found!" || echo "git ... Found!"
    npm_found=$(which npm)
    [ -z "$npm_found" ] && echo "npm ... Not found!" || echo "npm ... Found!"

    if [ -z "$git_found" ] || [ -z "$npm_found" ]; then
        echo "Checking requirements ... Fail!"
        exit 1
    else
        echo "Checking requirements ... OK!"
    fi
}

# Get command line arguments
[ -z "$1" ] && report_missing_arg "node webserver git repository" || node_webserver_git_repo=$1
[ -z "$2" ] && report_missing_arg "node webserver port" || node_webserver_port=$2

check_requirements
