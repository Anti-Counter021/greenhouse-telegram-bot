FROM python:3.8

WORKDIR /home/counter/programming_projects/greenhouses/bot

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["sh", "/home/counter/programming_projects/greenhouses/bot/entrypoint.sh"]
