#!/bin/bash
#
# Clone and run a node webserver, then run the crawler on it

#######################################
# Print error message with the missing args and exits with 1.
# Arguments:
#   arg_name: Missing argument name
#######################################
function report_missing_arg() {
    echo "Error: Missing $1 argument"
    echo "Usage: run.sh node_webserver_git_repo node_webserver_port <git_clone_dest>"
    exit 1
}

#######################################
# Check the requirements for the scripts 
# Arguments:
#   None
#######################################
function check_requirements() {
    git_exits=
    npm_exits=1
    echo ">>> Checking requirements"

    git_found=$(which git)
    [ -z "$git_found" ] && echo "git ... Not found!" || echo "git ... Found!"
    npm_found=$(which npm)
    [ -z "$npm_found" ] && echo "npm ... Not found!" || echo "npm ... Found!"
    lsof_found=$(which lsof)
    [ -z "$lsof_found" ] && echo "lsof ... not found!" || echo "lsof ... found!"

    # We chose not block on this since the user can install the packages in the global python
    [ -z "$VIRTUAL_ENV" ] && echo "Python env ... Not enabled!" || echo "Python env ... enabled!"

    if [ -z "$git_found" ] || [ -z "$npm_found" ] || [ -z "$lsof_found" ]; then
        echo "Checking requirements ... Fail!"
        exit 1
    else
        echo "Checking requirements ... OK!"
    fi
    echo "**********************************"
}

#######################################
# Clones, install and start the node webserver 
# Arguments:
#   node_webserver_git_repo: The git repository 
#   node_webserver_port: The port to start the server
#   git_clone_dest: The destination for the git clone
#######################################
function setup_webserver() {
    echo ">>> Cloning $1"
    if [ -d "$3" ]; then
        echo "$3 directory exits alread. Do you want to delete and re-clone [y/N] ? "
        read del_dir
        if [ "$del_dir" == "y" ]; then
            rm -rf $3
            # --depth 1: Since we are cloning the default branch no need to clone all the branches
            # || exit 1 so the script exit with one if this command fails
            git clone $1 --depth 1 $3 || exit 1
        fi
    else
        git clone $1 --depth 1 $3 || exit 1
    fi


    echo ">>> Installing npm package"
    npm install || exit 1

    echo ">>> Running the web server"
    export PORT=$2

    cd $3 # Changing directory so all the relative paths in the webserver work
    npm start &  # We hide the output to not mess up the crawler output
    cd -
    echo "Waiting for server to start"
    sleep 10 # Give the server time to start

    echo "**********************************"
}

#######################################
# Runs the crawler 
# Arguments:
#   node_webserver_port: The port to start the server
#######################################
function run_crawler() {
    echo ">>> Running the crawler"
    python main.py --verbose url "http://localhost:$1"  

    echo "**********************************"
}

#######################################
# Clean up all artifacts created by this script 
# Arguments:
#   node_webserver_port: The port to start the server
#######################################
function clean_up() {
    # Terminating the server since it was started by this script 
    echo "Terminating the server"
    # If the server started successfully, we can safely assume that pid returned by the lsof command
    # Is the PID of the server we started

    # The lsof command will return the PID of the process listening at the provided port
    # the kill -9 sill send a SIGKILL to the process
    kill -9 `lsof -i:$node_webserver_port -t`

    echo "**********************************"
}

#######################################
# Prints the command line arguments 
# Arguments:
#   node_webserver_git_repo: The git repository 
#   node_webserver_port: The port to start the server
#   git_clone_dest: The destination for the git clone
#######################################
function print_cmd_args() {
    # This is usefull for automation since using the log we can see the 
    # command line arguments that we used
    echo ">>> Command line arguments"
    echo "node_webserver_git_repo = $node_webserver_git_repo"
    echo "node_webserver_port     = $node_webserver_port"
    echo "git_clone_dest          = $git_clone_dest"
    echo "**********************************"
}

# Get command line arguments
[ -z "$1" ] && report_missing_arg "node webserver git repository" || node_webserver_git_repo=$1
[ -z "$2" ] && report_missing_arg "node webserver port" || node_webserver_port=$2
[ -z "$3" ] && git_clone_dest=$(pwd) || git_clone_dest=$3 # Added this argument in order to  choose where to clone


check_requirements

setup_webserver $node_webserver_git_repo $node_webserver_port $git_clone_dest

run_crawler $node_webserver_port

clean_up $node_webserver_port
