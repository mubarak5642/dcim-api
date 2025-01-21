FROM python

LABEL image for dcim-api

WORKDIR /docker-flask

ADD . /docker-flask

RUN pip3 install -r requirements.txt

EXPOSE 443
#EXPOSE 8086
ENV FLASK_APP=api.py

RUN pip3 install pandas
RUN pip3 install pyopenssl

CMD ["flask", "run", "-h", "0.0.0.0", "-p", "443", "--cert=adhoc"]
#CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8086"]
