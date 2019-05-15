FROM ubuntu 
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends python3-pip python3-wheel python3-setuptools tesseract-ocr tesseract-ocr-deu poppler-utils
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
WORKDIR /bot
COPY requirements.txt /bot/
COPY *.py /bot/
RUN pip install -r requirements.txt
CMD ["python3", "-u", "canteen-bot.py"]
