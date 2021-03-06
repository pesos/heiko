FROM debian:stable-slim

# install dependencies
RUN apt update && apt upgrade -y
RUN apt install openssh-server vim sudo -y

# set password for root user
RUN echo 'root:yabe' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

RUN useradd -rm -d /home/test -s /bin/bash -u 1000 -G sudo test

RUN echo 'test:yabe' | chpasswd

# change user to test
USER test
WORKDIR /home/test

# install rsync
RUN echo yabe | sudo -S apt-get install rsync -y

# start ssh service
ENTRYPOINT  echo yabe | sudo -S service ssh restart && bash
