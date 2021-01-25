FROM debian:stable-slim

# install dependencies
RUN apt update && apt upgrade -y
RUN apt install openssh-server vim sudo -y

# set password for root user
RUN echo 'root:yabe' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config

# creating user
RUN useradd -rm -d /home/test -s /bin/bash -u 1000 -G sudo test 

# set password for test user
RUN echo 'test:yabe' | chpasswd 

# when run, let user be test
USER test
WORKDIR /home/test

# start ssh service
# change group of user
# remove user from group of sudoers
ENTRYPOINT  echo yabe | sudo -S service ssh restart && \
            echo yabe | sudo -S groupmod -n test_grp root --gid 1000 && \
            echo yabe | sudo -S deluser test sudo && \
            bash
