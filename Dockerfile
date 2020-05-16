FROM python:3
RUN apt-get update
RUN apt install -y mosquitto mosquitto-clients
#RUN apt install python-tk
RUN pip3 install paho-mqtt python-etcd
COPY spel.py /spel.py
COPY img /img
CMD ["echo","mosquitto geinstalleerd"]
CMD ["python3","spel.py"]

