FROM frolvlad/alpine-miniconda3:latest
MAINTAINER Nilav Ghosh "nilavghosh@gmail.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]
