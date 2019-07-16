list dockers containers
```bash
docker container ls
docker container ls -q # for listing also the replicas
```

list dockers images
```bash
docker image ls
```

list dockers services
```bash
docker service ls
```

list dockers stack
```bash
docker stack ps NAMEOFAPP
```






Build a docker image
```bash
docker build -t friendlyhello .
```

Run the docker build and bind port 80 of the docker to our port 4000
```bash
docker run -p 4000:80 friendlyhello
```

Run the docker build in background (detached)
```bash
docker run -d -p 4000:80 friendlyhello
docker container ls
sleep 600
docker container stop 1fa4ab2cf395
```


Run a docker in an app
```bash
docker swarm init
docker stack deploy -c docker-compose.yml getstartedlab
sleep 600
docker stack rm getstartedlab
docker swarm leave --force
```

Single container for a service = a task
