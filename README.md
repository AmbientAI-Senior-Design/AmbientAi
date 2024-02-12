# AmbientAi Documentation

## Installation
To run the setup script, run the following command:
```bash
$ ./setup.sh
```
This script will install the necessary dependencies for the project.


## Testing Deployment 
To deploy the app locally, run the `Dockerfile` located in the root directory of the project. 
```bash
$ docker build -t ambientai .
$ docker run -p 80:80 ambientai
```

