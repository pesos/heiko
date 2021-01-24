FROM debian:stable-slim

# install dependencies
RUN apt update && apt upgrade -y
RUN apt install openssh-server vim sudo -y

# set password for root user
RUN echo 'root:yabe' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

# start ssh
RUN service ssh start

# creating user
RUN useradd -rm -d /home/test -s /bin/bash -u 1000 test 

# setting group and GID
RUN sudo groupmod -n test_grp root --gid 1000

# set password for test user
RUN echo 'test:yabe' | chpasswd 

# when run, let user be test
USER test
WORKDIR /home/test