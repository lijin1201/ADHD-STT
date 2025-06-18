## ADHD 응답에 STT 엔진.

Websocket을 사용하여 `/ws/adhd` 경로에 ADHD 정밤 텍스트만 인식하고, `/ws/general` 경로에 일반 텍스트를 인식합니다.

Setup:
```
pip install openai-whisper fastapi uvicorn[standard] torchaudio
```

Running method:
```
uvicorn sttService1:app --reload --host 0.0.0.0 --port PORT
```

Audio Testing Example for two server routes `/ws/adhd` and `/ws/general` :
```
uvicorn compSTT1:app --reload --host 0.0.0.0 --port PORT
```