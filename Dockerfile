FROM almalinux:9
RUN yum install -y python3 python3-requests python3-pip && pip install python-kasa && pip install ambient-api
COPY pondHeater.py /
ENTRYPOINT [ "/usr/bin/env", "python3", "pondHeater.py" ]