from datetime import datetime

def my_scheduled_job():
    myFile = open('append.txt', 'a') 
    myFile.write('\nAccessed on ' + str(datetime.now()))
    pass