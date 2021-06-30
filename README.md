# 2020Spring-6440Project

AWS Based Chat Sticker Maker Web Application
>Graduate student project of 6440 Cloud Computing course

This repository contains:

emotion-detection-master: guide about training the Deep Learning emotion detection model
sticker_api: emotion predict api using the model we get from folder emotion-detection-master
sticker_client: python version client to test server
sticker_server: server using api 

## Table of Contents

- [Demo](#demo)
- [Setup](#setup)
- [Reference](#reference)

## Demo
https://youtu.be/dVVOON9T3zc

## Setup

You can deploy it on your Ubuntu.

1. Download repository

```sh
$ git clone https://github.com/cyxlily/2020Spring-6440Project.git
$ cd 2020Spring-6440Project 
```
 2. Setup API
 
```sh
$ docker pull cyxlily/sticker_api 
$ docker run -it -p 5000:5000 -p 5001:5001 -v $PWD:/home/lily cyxlily/sticker_api
```
Test: On your Ubuntu browser, enter http://localhost:5000/, and you will see the API document.

3. Setup server
Open a new terminal on Ubuntu.

```sh
$ docker ps
```
Remember the docker id number you run in Step 2.
```sh
$ docker exec -it your_docker_id_number /bin/bash 
```
In docker, run server.
```sh
$ cd /home/lily/sticker_server 
$ python no_database_app.py
```
Test: On your Ubuntu browser, enter http://localhost:5001/, and you will see the Sticker Maker web page. Upload your photo and get your sticker.


Also, you can deploy it onto Cloud.


## Reference
https://github.com/elzisiou/K-means

https://towardsdatascience.com/deploy-a-machine-learning-model-as-an-api-on-aws-43e92d08d05b


