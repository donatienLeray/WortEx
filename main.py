'''
The main File only checks if the database was initalised correctly
and if all dependencys are installed correctly. if so it will start the game with an animation and than 
call the main menu.
'''
import subprocess
import start
import models

# check if the dependencies are installed
def check_dependencies():
    requirements_file='requirements.txt'
    try:
        subprocess.run(['pip', 'check', '-r', requirements_file], check=True)
        print("All dependencies are satisfied.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return False

# try to install the dependencies  
def install_dependencies(requirements_file='requirements.txt'):
    try:
        subprocess.run(['pip', 'install', '-r', requirements_file], check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
# check if the database exists
if not models.check_database():
    # if not exit the program
    raise SystemExit("Database not found.")
else:
    #check if the dependencies are installed
    if check_dependencies():
        # if yes start the game
        start()
    else:
        # try to install the dependencies
        install_dependencies()
        # check again if the dependencies are installed
        if check_dependencies():
            start()
        # if still not installed exit the program
        else:
            raise SystemExit("Could not install dependencies.")
   
