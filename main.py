import start
import models

# check if the database exists
if models.check_database():
    start.run()
else:
    print("Database does not exist")
    print("Please run the db.py file to create the database")
    
models.close()
