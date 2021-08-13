FROM python:3.7.11-stretch

WORKDIR /home/parking

ENV http_proxy="http://icache:80"
ENV https_proxy="http://icache:80"

RUN apt-get update && apt-get -y update
RUN pip3 -q install pip --upgrade
RUN pip3 install jupyter
RUN git clone https://github.com/johnStrong23/parking_test_v1.git ./

COPY . /home/parking

ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

