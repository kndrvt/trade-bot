FROM python:3.8

COPY . .

RUN pip install poetry
RUN poetry update

CMD ["poetry", "run", "python", "src/TradeBot.py", "/conf/config.yaml"]