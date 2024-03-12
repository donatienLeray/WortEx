'''
The main File only checks if the database was initalised correctly
and if all dependencys are installed correctly. if so it will start the game with an animation and than 
call the main menu.
'''
import subprocess
import start
import models

def check_dependencies():
    # check if the dependencies are installed
    requirements_file='requirements.txt'
    try:
        subprocess.run(['pip', 'check', '-r', requirements_file], check=True)
        print("All dependencies are satisfied.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        
# check if the database exists
if models.check_database():
    #check if the dependencies are installed
    if check_dependencies():
        start()
