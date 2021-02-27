CONFIG="config.yaml"

docker rmi tradebot
docker build -t tradebot .
docker run -d --name tradebot --rm tradebot poetry run python src/TradeBot.py $CONFIG