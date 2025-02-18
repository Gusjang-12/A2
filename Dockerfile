FROM python:3.9

WORKDIR /A2

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE  224

CMD [ "python","app1.py" ]

