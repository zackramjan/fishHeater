FROM centos:latest

RUN yum install -y git python3 python3-requests python3-pip && pip install python-kasa && pip install ambient-api
RUN git clone https://github.com/zackramjan/restartHeater.git
WORKDIR /restartHeater
ENTRYPOINT [ "/usr/bin/env", "bash", "entrypoint.sh" ]