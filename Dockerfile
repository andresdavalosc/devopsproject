FROM python:3
RUN apt-get update
RUN apt install -y mosquitto mosquitto-clients
RUN python -m pip install paho-mqtt
COPY Devops-project-rpi/software/tkinter .
CMD ["echo","mosquitto geinstalleerd"]
CMD ["python3","eerstevenster.py"]

