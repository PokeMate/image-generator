FROM python:3.7

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

CMD ["pip3 install --upgrade pip3"]
CMD [ "python3", "./api/main.py" ]