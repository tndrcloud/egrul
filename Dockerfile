FROM python:3.11-slim

RUN mkdir ./egrul
COPY . ./egrul
WORKDIR /egrul/app
RUN python3 -m pip install -r ../requirements.txt

CMD ["python", "main.py"]