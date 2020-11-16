# CourseProject

Please fork this repository and paste the github link of your fork on Microsoft CMT. Detailed instructions are on Coursera under Week 1: Course Project Overview/Week 9 Activities.

------
## Installation guide

### Docker installation

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


### Instruction to Build docker image with ElasticSearch and application
   
    After successful installation of Docker, next step is to build the docker container image with ElasticSearch and application

    Command to build the docker image (makesure you are in same path as Dockerfile.amd64 file)
    $ docker build -f Dockerfile.amd64 -t food_recipe_se .    [you can choose your own name instead of "food_recipe_se"]

    It will take some time to build the image. Once done you can check your image on host machine with below command
    $ docker images
   
    Should see something like below
    REPOSITORY                                 TAG                      IMAGE ID            CREATED             SIZE
    food_recipe_se                             latest                   72ab77c2a9b3        35 minutes ago      2.13GB
 

### Run the docker container to trigger search engine

    $docker run --net=host -p 5000:500 food_recipe_se
    
     Expected output:

     Starting Elastic Server
     * Serving Flask app "app" (lazy loading)
     * Environment: development
     * Debug mode: on
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat
     * Debugger is active!
     * Debugger PIN: 271-999-248

### On your host machine open:
    http://127.0.0.1:5000

### Exit condition: Kill the (app) docker container 

    How to kill the container:
       - Open new command terminal 
       - $docker ps -a  (need sudo acccess)
       - Look for docker container with name "food_recipe_se" copy CONTAINER ID)
       - $docker rm <CONTAINER ID>

## TODO: 
     - Kibana shell script for index file generation is not considered currently
     - Once ready will be added to docker image exection
