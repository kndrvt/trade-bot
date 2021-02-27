docker rmi tradebot
docker build -t tradebot .
docker run -d \
  --name tradebot \
  --rm \
  tradebot