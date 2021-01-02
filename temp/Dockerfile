FROM debian:stable-slim
RUN apt update && apt upgrade -y
RUN apt install openssh-server vim -y
RUN echo 'root:yabe' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
ENTRYPOINT service ssh start && bash
