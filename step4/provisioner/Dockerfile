FROM python:3.7

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

ADD provisioner.py /
ADD job-template.yaml /

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini

RUN useradd webapp
USER webapp

ENTRYPOINT ["/tini", "--", "python", "/provisioner.py"]
