# Trader bot
This project is a simple trader bot with a simple strategy 
for Deribit.com exchange stock.

### Requirements
- Python 3.8
- Docker SDK for Python 4.4

### Run
1) Go to the project root directory. 
   Create a trader bot docker image from Dockerfile using following commands:
~~~bash
# if you have image named 'traderbot'
docker rmi traderbot

# image building
docker build -t traderbot .
~~~

2) Rewrite ```config.yaml``` according to your wishes. 
   Also, it is necessary to add your authentication data.

3) ```main.py``` from ```src``` launches a docker container with your 
   trader bot. Run ```main.py``` using following command:
~~~bash
poetry run python src/main.py config.yaml
~~~

4) Press **Ctrl+C** and wait for shutting down the running docker container.

5) Also```run.sh``` contains commands for 1 and 3 steps .