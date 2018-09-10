FROM python:3.7.0

ADD requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

ADD webconsole.py /

# Add Tini
ENV TINI_VERSION v0.18.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

RUN useradd webapp
USER webapp
EXPOSE 5000
ENV FLASK_APP=/webconsole.py
CMD ["flask", "run", "-h", "0.0.0.0"]
