FROM debian:stable-slim

# install dependencies
RUN apt update && apt upgrade -y
RUN apt install openssh-server vim sudo -y

# set password for root user
RUN echo 'root:yabe' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

# start ssh service
# create a test user which is not root
# set password for test user
# switch user
ENTRYPOINT  echo yabe | sudo -S service ssh restart && \
            useradd -rm -d /home/test -s /bin/bash -u 1000 test && \
            echo 'test:yabe' | chpasswd && \
            su test && \
            bash
