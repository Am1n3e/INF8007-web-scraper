#!/bin/bash
#
# Clone and run a node webserver, then run the crawler on it

REQUIRED_APPS=(git npm lsof curl)

#######################################
# Prints header (For better output) 
# Arguments:
#   header_text: The header text (title)
#######################################
function print_header() {
    echo "#************************************************************"
    echo "# $1"
    echo "#************************************************************"
}

#######################################
# Prints footer (For better output) 
# Arguments:
#   None
#######################################
function print_footer() {
    echo "#------------------------------------------------------------"
    echo ""
    echo ""
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

    print_header "Command line arguments"

    echo "node_webserver_git_repo = $node_webserver_git_repo"
    echo "node_webserver_port     = $node_webserver_port"
    echo "git_clone_dest          = $git_clone_dest"

    print_footer
}

#######################################
# Prints the usage
# Arguments:
#   None
#######################################
display_usage() { 
	echo -e "\nUsage: run.sh node_webserver_git_repo node_webserver_port [git_clone_dest]\n" 
    echo -e "positional arguments"
    echo -e "\tnode_webserver_git_repo: The node webserver git repository"
    echo -e "\tnode_webserver_port: The port to start the node webserver"
    echo -e "\tgit_clone_dest: Set the destination for git clone. Optional default to pwd"
}

#######################################
# Print error message with the missing args and exits with 1.
# Arguments:
#   arg_name: Missing argument name
#######################################
function report_missing_arg() {
    echo "Error: Missing $1 argument"
    display_usage
    exit 1
}

#######################################
# Check the requirements for the scripts 
# Arguments:
#   None
#######################################
function check_requirements() {
    print_header "Check requirements"

    requirements_ok=1
    for app in "${REQUIRED_APPS[@]}"; do
        app_found=$(which $app)
        if [ -z "$app_found" ]; then 
            echo "$app ... Not found :("
            requirements_ok=0
        else
            echo "$app ... Found"
        fi
    done

    # We chose not block on this since the user can install the packages in the global python
    [ -z "$VIRTUAL_ENV" ] && echo "Python env ... Not enabled!" || echo "Python env ... enabled!"

    if [[ $requirements_ok -eq 0 ]]; then
        echo "Checking requirements ... Fail!"
        exit 1
    else
        echo "Checking requirements ... OK!"
    fi

    print_footer
}

#######################################
# Clones, install and start the node webserver 
# Arguments:
#   node_webserver_git_repo: The git repository 
#   node_webserver_port: The port to start the server
#   git_clone_dest: The destination for the git clone
#######################################
function setup_webserver() {
    print_header "Setup webserver"

    echo ">>> Cloning $1"
    if [ -d "$3" ]; then
        echo "$3 directory exits already. Do you want to delete and re-clone [y/N] ? "
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
    npm start & # & to start in the back ground 
    cd -

    echo ">>> Waiting for server to start ..."
    # When the curl exit code is 0, that means that server is started
    # The output of the curl is redirected to /dev/null to not polute the output
    until $(curl --output /dev/null --silent --head --fail http://localhost:$PORT); do
        echo '.'
        sleep 1
        # This can create an infinite loop if the server is not working
        # But we assume that server we are using is working 
        # The user will need to hit CTRL+C to terminate
    done

    print_footer
}

#######################################
# Runs the crawler 
# Arguments:
#   node_webserver_port: The port to start the server
#######################################
function run_crawler() {
    print_header "Running the crawler"

    python main.py --verbose url "http://localhost:$1"

    print_footer
}

#######################################
# Clean up all artifacts created by this script 
# Arguments:
#   node_webserver_port: The port to start the server
#######################################
function clean_up() {
    print_header "Clean up"

    # Terminating the server since it was started by this script 
    echo ">>> Terminating the server"
    # If the server started successfully, we can safely assume that pid returned by the lsof command
    # Is the PID of the server we started

    # The lsof command will return the PID of the process listening at the provided port
    # the kill -9 sill send a SIGKILL to the process
    kill -9 `lsof -i:$node_webserver_port -t`

    print_footer
}


###################################Main####################################

# Get command line arguments
[ -z "$1" ] && report_missing_arg "node webserver git repository" || node_webserver_git_repo=$1
[ -z "$2" ] && report_missing_arg "node webserver port" || node_webserver_port=$2
[ -z "$3" ] && git_clone_dest=$(pwd) || git_clone_dest=$3 # Added this argument in order to  choose where to clone

print_cmd_args

check_requirements

setup_webserver $node_webserver_git_repo $node_webserver_port $git_clone_dest

run_crawler $node_webserver_port

clean_up $node_webserver_port
