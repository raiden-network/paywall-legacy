FROM python:3.8-alpine
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev automake libtool python3-dev make
COPY . .
RUN pip install -r requirements.txt
RUN python3 setup.py install
EXPOSE 5000
COPY . .
WORKDIR src/raiden_paywall
#ENV FLASK_APP=main.py
#ENV FLASK_RUN_HOST=0.0.0.0
#ENV RAIDEN_PAYWALL_SETTINGS=default.cfg
#CMD ["gunicorn", "-w", "4", "-b", "localhost:5000", "-c", "config.py", "raiden_paywall.main:app"]
