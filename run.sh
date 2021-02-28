docker rmi tradebot
docker build -t tradebot .
docker run \
  --name tradebot \
  --mount type=bind,src=$PWD/conf,dst=/conf \
  --rm \
  tradebot
