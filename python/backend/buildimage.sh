#!/bin/bash

# Check if two arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <image>:<tag> <stage> <container>"
    exit 1
fi

# Extract arguments
image=$1
stage=$2
container=$3

# Check stage
if [[ "$stage" != "test" && "$stage" != "production" ]]; then
    echo "Invalid stage. Please provide 'test' or 'production'."
    exit 1
fi

# Function to remove old image and build new image with a specified network bridge
build_image() {
    docker rmi "$image" --force >/dev/null 2>&1
    docker build --file Dockerfile --tag "$image" .
}

# Function to run containers
run_container() {
    local ports=()    
    local count

    if [[ "$stage" == "test" ]]; then
        count=1   
        ports=(8080)     
    else
        count=3
        ports=(8080 8081 8082)
    fi

    docker network inspect pyservernetbridge &>/dev/null || docker network create --driver=bridge pyservernetbridge
    
    for ((i = 0; i < count; i++)); do
        container_name="$container$i"
        docker stop "$container_name" >/dev/null 2>&1
        docker rm "$container_name" >/dev/null 2>&1
        docker run -d --name "$container_name" --restart always -p "${ports[i]}:8000" --net pyservernetbridge "$image"
    done
}

# Call functions
build_image
run_container
