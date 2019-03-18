import bot
import scheduler
import threading
import get_dussmann
import get_mensa
import ocr_dussmann
import ocr_mensa


def main():
    scheduler.setup_schedule()
    threading.Thread(target=scheduler.run_schedule).start()
    bot.main()

if __name__ == "__main__":
    main()