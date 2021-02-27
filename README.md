# Trade bot
This project is a simple trade bot with a simple strategy 
for Deribit.com exchange stock.

### Requirements

- Python 3.8
- Docker SDK for Python 4.4

### Run

1) Move to the project root directory. 
   Rewrite ```config.yaml``` according to your wishes. 
   Also, it is necessary to add your authentication data.
   
2) You can launch ```run.sh``` for quick start. 
   It contains commands for 3 and 4 steps.
   
3) Create a trade bot docker image from Dockerfile using following commands:
~~~bash
# if you have image named 'tradebot'
docker rmi tradebot

# image building
docker build -t tradebot .
~~~

4) Launch a docker container with your 
   trade bot using following command:
~~~bash
docker run --name tradebot --rm tradebot
~~~
