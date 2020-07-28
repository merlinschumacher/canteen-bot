FROM ubuntu 
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends python3-pip python3-wheel python3-setuptools tesseract-ocr tesseract-ocr-deu poppler-utils build-essential libpoppler-cpp-dev pkg-config python3-dev
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
WORKDIR /bot
COPY requirements.txt /bot/
COPY *.py /bot/
RUN pip3 install -r requirements.txt
CMD ["python3", "-u", "canteen-bot.py"]
