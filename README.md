# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

------
## Installation guide

    Scroll down for Mac instructions. Windows not supported.

### (Linux) Docker installation

    Follow instructions from https://docs.docker.com/get-docker/ select download based on your host machine OS 

    Check if docker daemon is running on host machine (Ex: Output from Ubuntu 16.04 host machine): 
    $docker
      # docker

      Usage:	docker [OPTIONS] COMMAND

      A self-sufficient runtime for containers

      Options:
            --config string      Location of client config files (default "/home/psakamoori/.docker")
        -c, --context string     Name of the context to use to connect to the daemon (overrides DOCKER_HOST env var and default context set with "docker context use")
        -D, --debug              Enable debug mode
        -H, --host list          Daemon socket(s) to connect to
        -l, --log-level string   Set the logging level ("debug"|"info"|"warn"|"error"|"fatal") (default "info")
            --tls                Use TLS; implied by --tlsverify
            --tlscacert string   Trust certs signed only by this CA (default "/home/psakamoori/.docker/ca.pem")
            --tlscert string     Path to TLS certificate file (default "/home/psakamoori/.docker/cert.pem")
            --tlskey string      Path to TLS key file (default "/home/psakamoori/.docker/key.pem")
            --tlsverify          Use TLS and verify the remote
        -v, --version            Print version information and quit


### (Linux) Instruction to Build docker image with ElasticSearch and application
   
    After successful installation of Docker, next step is to build the docker container image with ElasticSearch and application

    Command to build the docker image (makesure you are in same path as Dockerfile.amd64 file)
    $ docker build -f Dockerfile.amd64 -t food_recipe_se .    [you can choose your own name instead of "food_recipe_se"]

    It will take some time to build the image. Once done you can check your image on host machine with below command
    $ docker images
   
    Should see something like below
    REPOSITORY                                 TAG                      IMAGE ID            CREATED             SIZE
    food_recipe_se                             latest                   72ab77c2a9b3        35 minutes ago      2.13GB

    Troubleshooting "docker build" failure:
     - Change Folder & File access permissions of project recipes-search-engine$ chmod -R 777 *
     - Check if docker daemon is running https://docs.docker.com/config/daemon/
 
 ### (Linux) Run the docker container to trigger search engine

     $docker run --net=host -p 5000:5000 -p 9200:9200 food_recipe_se
    
     Expected output:

     Starting Elastic Server
     * Serving Flask app "app" (lazy loading)
     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 271-999-248

### (Linux) Launch ingest script:

    TODO: @Pradeep please verify this is the correct command

    Open a new terminal window
        $docker ps -a  (need sudo acccess)
        
        Identify and copy <container ID> for food_recipe_se, then run
        $ docker run <container ID> bash

    In the container shell run:
        $ python /app/batch/es_data_loader.py  

        NOTE: If you receive connection error, retry again in 30-60 seconds 

    Expected output (may take several minutes to complete ingestion):

        ****Load begins****
        **Loading now: /app/dataset/recipes_raw_nosource_ar.json
                * 1000 documents successfully indexed in recipes_id index.
                ...
                ...
        39802 documents successfully indexed in recipes_idx index.

### (Linux) On your host machine open:
    http://127.0.0.1:5000

    Paste url into browser to begin testing the application

### (Mac) Docker Desktop for Mac download instructions and configurations

    Install the latest edge release from Docker (v2.5.1.0 or later): 
        https://docs.docker.com/docker-for-mac/edge-release-notes/

    Install jq. Options: 
        $brew install jq
        $port install jq
        Or: https://stedolan.github.io/jq/download/

    Setup jq to work with Docker SOCKS server:
        $cd ~/Library/Group\ Containers/group.com.docker/
        $mv settings.json settings.json.backup
        $cat settings.json.backup | jq '.["socksProxyPort"]=8888' > settings.json

    Enable SOCKS proxy:
        System Preferences -> Network -> Advanced -> Proxies  
        Select the box next to ‘SOCKS proxy’
        Ensure SOCKS Proxy server reads ‘local host:8888’
        Ensure Bypass settings reads ‘*.local, 169.254.0.0/16, *.io’
        If Unselected, Select the box next to ‘Use Passive FTP Mode’
        Select “OK” then “APPLY”

        NOTE: 
        Internet access may be disabled while you running your proxy server. 
        To restore your settings after testing the application:
            * Deselect the box next to ‘SOCKS Proxy’ in your Network settings
            * Select “OK” and “Apply”

    Start Docker Desktop for Mac application:
        'commmand' + 'space' and type 'Docker.app' then launch
        The blue whale Docker icon should appear in the apple menu bar
            * Select the icon and ensure green status: 'Docker Desktop is Running'

    Verify Expiramental features in Docker Desktop for Mac:
        Docker.app -> Preferences -> Expiramental Features
            * Ensure all features are enabled

### (Mac) Build the Docker image

    Navigate to project directory 'recipes-search-engine' in terminal.
    Enter command to build the Docker image:
        $ docker build -f Dockerfile.amd64 -t food_recipe_se .

        Expected output (may take a few minutes to complete):
            Building ...
            ...
            ...
            naming to docker.io/library/food_recipe_se

### (Mac) Run the Docker image

    Run the Docker image:
        $docker run -p 5000:5000 food_recipe_se

        Expected output:
            Starting Elastic Server
             * Serving Flask app "app" (lazy loading)
             * Environment: development
             * Debug mode: on
             * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
             * Restarting with stat
             * Debugger is active!
             * Debugger PIN: 544-260-012

### (Mac) Launch ingest script:

    Docker.app -> Dashboard -> Containers/Apps
        Next to the running food_recipe_se image, select "CLI" icon.
        
    This will open a terminal window fromn inside the Docker image. 
        
    Recommend closing unused applications to speed up ingestion

    In the container shell:
        $python /app/batch/es_data_loader.py

        NOTE: If you receive connection error, retry again in 30-60 seconds 

    Expected output (may take several minutes to complete ingestion):

        ****Load begins****
        **Loading now: /app/dataset/recipes_raw_nosource_ar.json
                * 1000 documents successfully indexed in recipes_id index.
                ...
                * 65000 documents indexed.
        65125 documents successfully indexed in recipes_idx index.


### (Mac) On your host machine open:
    http://0.0.0.0:5000/

    Paste url into browser to begin testing the application

### (Linux/Mac) Exit condition: Kill the (app) docker container 

    How to kill the container:
       - Open new command terminal 
       - $docker ps -a  (need sudo acccess)
       - Look for docker container with name "food_recipe_se" copy CONTAINER ID)
       - $docker stop <CONTAINER ID>
       - $docker rm <CONTAINER ID>
