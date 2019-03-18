import schedule
import time
import os
import get_dussmann
import get_mensa
import ocr_dussmann
import ocr_mensa


def setup_schedule():
    mensadir = os.environ.get('MENSAFOLDER', './data/mensa/')
    dussmanndir = os.environ.get('DUSSMANNFOLDER', './data/dussmann/')
    schedule.every().day.at("10:30").do(get_mensa.getMensa)
    schedule.every().day.at("10:30").do(get_dussmann.getDussmann)
    schedule.every().day.at("10:45").do(
        ocr_dussmann.saveMenuToFile, dussmanndir)
    schedule.every().day.at("10:45").do(
        ocr_mensa.saveMenuToFile, mensadir)

def run_schedule():
    schedule.run_all()
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    setup_schedule()
    run_schedule()