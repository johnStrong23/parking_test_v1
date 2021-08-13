FROM python:3.7.11-stretch

WORKDIR /home/parking

ENV http_proxy="http://icache:80"
ENV https_proxy="http://icache:80"

RUN apt-get update && apt-get -y update
RUN pip3 -q install pip --upgrade
RUN pip3 install jupyter
RUN git clone https://github.com/johnStrong23/parking_test_v1.git ./
RUN git config --global user.email "vibm@intracom-telecom.com"
RUN git config --global user.name "johnStrong23"

COPY . /home/parking

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

#for when you want to push use this command only after u have committed your changes
#git push origin HEAD:main

#This command for when ou wanna run the notebook on jupyter but you have run the container with bash
#jupyter notebook --port=8888 --no-browser --ip=0.0.0.0 --allow-root
