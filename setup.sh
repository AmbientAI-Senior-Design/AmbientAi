# check if user has Python 3.11 or higher installed, error if not
echo 'Checking if Python3 is installed'
type -P python3 >/dev/null 2>&1 && echo Python 3 is installed  || { echo >&2 "Python 3 is required but it's not installed.  Aborting."; exit 1; }
# Check if user has docker installed, error if not
echo 'Checking if Docker is installed'
type -P docker >/dev/null 2>&1 && echo Docker is installed  || { echo >&2 "Docker is required but it's not installed.  Aborting."; exit 1; }
# create MySQL container
echo "Creating MySQL container..."
docker run --name AmbientAi-MySQL -e MYSQL_ROOT_PASSWORD=password -d mysql:latest

# create python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
# activate virtual environment
echo "Activating Python virtual environment..."
source venv/bin/activate
# install requirements from requirements.txt in current directory
echo "Installing requirements..."
pip install -r requirements.txt
# create .env from .env.example
echo "Creating .env file..."
cp .env.example .env


