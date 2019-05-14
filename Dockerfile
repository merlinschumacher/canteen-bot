FROM alpine
ENV PYTHONUNBUFFERED=1
ENV LC_ALL=C.UTF-8
RUN apk update && apk upgrade --available && apk add --no-cache gcc musl-dev tesseract-ocr tesseract-ocr-data-deu poppler-utils python3 python3-dev libffi libffi-dev && pip3 install --no-cache-dir --upgrade pip && pip --no-cache-dir install setuptools wheel
WORKDIR /bot
COPY requirements.txt /bot/
COPY *.py /bot/
RUN pip3 install -r  requirements.txt
CMD ["python3", "-u", "canteen-bot.py"]
