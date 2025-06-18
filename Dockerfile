FROM python:3.10-slim
WORKDIR /app
COPY . /app

RUN pip install openai-whisper fastapi uvicorn[standard] torchaudio 
RUN apt-get -y update && apt-get -y upgrade && apt-get install -y --no-install-recommends ffmpeg
RUN whisper static/audios/Ya.m4a --model small --language ko

#CMD ["uvicorn", "sttService1:app", "--reload", "--host", "0.0.0.0", "--port", "10181"]
#docker build .  -t backend2
#docker run -d -p 10181:10181 --gpus all --restart unless-stopped backend2 \
#uvicorn sttService1:app --reload --host 0.0.0.0 --port 10181