FROM alpine:3.9
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
RUN apk update && apk upgrade --available && apk add --no-cache gcc musl-dev tesseract-ocr tesseract-ocr-data-deu poppler-utils python3 python3-dev libffi libffi-dev jpeg-dev zlib-dev openssl-dev && pip3 install --no-cache-dir --upgrade pip && pip --no-cache-dir install setuptools wheel
WORKDIR /bot
COPY requirements.txt /bot/
COPY *.py /bot/
RUN LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip install -r requirements.txt"
CMD ["python3", "-u", "canteen-bot.py"]
