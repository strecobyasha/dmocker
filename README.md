<h1> Welcome to dmocker! </h1>

<p>Dmocker is a small terminal tool to interact with remote Docker containers. The use case of this tool is when
you have Docker containers on multiple remote servers and don't use large solutions to monitor and interact with them.
Dmocker allows to execute different commands on the remote devices simultaneously, saving time on manually established
connections.</p>

Currently, the tool has just a few functions:
- list Docker containers on remote servers;
- show logs from the specific container on the remote server.

Behind the scene dmocker uses paramiko library to establish ssh connection with remote servers. To avoid putting
the password every time when use dmocker, it's better to create a key pair and send the public key on each 
remote device that is expected to be used with this tool:
```
ssh-keygen -t ed25519 -f {filename} -C {username}
ssh-copy-id -i {filename} username@remote_host
/usr/bin/ssh-add -K {filename}
```
Also, for each remote device it's better to create a placeholder in ~/.ssh/config file:
```
Host server1
    HostName 192.168.1.X
    User username1
Host server2
    HostName 192.168.1.X
    User username2
```
Now ssh connection may be established with much shorter command:
```
ssh server1
ssh server2
```
Hence, dmocker also can be used with this simplified ssh parameters:
```
dmocker server1 -t ps
```

<h2> Examples </h2>

List containers running on the server
```
dmocker server
```
List containers running on multiple servers
```
dmocker server1 server2... serverN
```
List containers running on multiple servers
```
dmocker server1 server2... serverN -t ps
```
List all containers on multiple servers
```
dmocker server1 server2... serverN -t ps a
```
List containers running on multiple servers, filtered by container_name_filter
```
dmocker server1 server2... serverN -n container_name_filter
```
Show last 10 logs from the container
```
dmocker server -t logs container_id
```
Show last 20 logs from the container
```
dmocker server -t logs container_id 20
```
Show last 10 logs from the container and follow
```
dmocker server -t logs container_id f
```
Show last 20 logs from the container and follow
```
dmocker server -t logs container_id 20 f
```
