FROM python:3.8-alpine
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev automake libtool python3-dev make
COPY . .
RUN pip install -r requirements.txt
RUN python3 setup.py install
COPY . .
WORKDIR src/raiden_paywall
