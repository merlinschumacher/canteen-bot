import schedule
import time
import os
from helpers import with_logging
import get_dussmann
import get_mensa
import ocr_dussmann
import ocr_mensa

start_time = "09:30"
start_time_list = list(start_time)
start_time_list[4] = "2"
start_time2 = str().join(start_time_list)

print("Running Jobs at: " + start_time + " and " + start_time2)

def setup_schedule():
    mensadir = os.environ.get('MENSAFOLDER', './data/mensa/')
    dussmanndir = os.environ.get('DUSSMANNFOLDER', './data/dussmann/')
    
    schedule.every().day.at(start_time).do(get_mensa.getMensa)
    schedule.every().day.at(start_time).do(get_dussmann.getDussmann)
    
    schedule.every().day.at(start_time2).do(
        ocr_dussmann.saveMenuToFile, dussmanndir)
    schedule.every().day.at(start_time2).do(
        ocr_mensa.saveMenuToFile, mensadir)

def run_schedule():
    schedule.run_all()
    while True:
        schedule.run_pending()
        print("Ran scheduler")
        time.sleep(1)

if __name__ == "__main__":
    setup_schedule()
    run_schedule()
