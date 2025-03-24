## Setup & Installation

### Setup a virtual environment
```
sudo apt update && sudo apt upgrade -y
sudo apt-get install python3-venv -y
cd ~/plc_gui
python3 -m venv .venv
chmod -R 777 ./
```

### Active virtual environment
```
source .venv/bin/activate
```

### Install Dependencies
```cmd
sudo apt-get install python3-pip -y
pip3 install -r requirements.txt
```

### Create the user
```cmd
python3 add_user.py
```

### Run the application
```cmd
python3 run.py
```
