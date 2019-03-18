FROM ubuntu 
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends python3-pip python3-wheel python3-setuptools tesseract-ocr tesseract-ocr-deu poppler-utils
COPY requirements.txt /bot/
WORKDIR /bot
RUN pip3 install -r  requirements.txt
COPY *.py /bot/
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
CMD ["python3", "-u", "canteen-bot.py"]
