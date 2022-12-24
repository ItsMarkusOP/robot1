FROM jokerhacker/zerotwo-python:latest

RUN  git clone https://github.com/Black-Bulls-Bots/Cutiepii_Robot -b main  /root/zerotwo
RUN  mkdir  /root/zerotwo/bin/
WORKDIR /root/zerotwo/

COPY  ./Cutiepii_Robot/elevated_users.json* ./Cutiepii_Robot/config.py* /root/zerotwo/Cutiepii_Robot/
RUN pip3 install -r requirements.txt

CMD ["python3", "-m", "Cutiepii_Robot"]
