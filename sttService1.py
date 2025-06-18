import io
# import numpy as np
import torchaudio
import whisper
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once
model = whisper.load_model("small",device="cuda:1")  # You can choose tiny, small, medium, etc.

def createSuppressTokenList(words_to_remain, language="ko"):
    # Load tokenizer for Korean
    tokenizer = whisper.tokenizer.get_tokenizer(multilingual=True, language=language, task="transcribe")

    # Token IDs to keep (tokens for " 예" and " 아니오")
    keep_tokens = []
    for word in words_to_remain:
        tokens = tokenizer.encode(" " + word)  # Leading space matters
        keep_tokens.extend(tokens)

    # Suppress all tokens except the ones to keep
    block_tokens = [i for i in range(tokenizer.eot) if i not in keep_tokens]
    return block_tokens

# Define allowed Korean words
korean_words = ["전혀 그렇지 않다", "1번","일번","1전","일전",
                "약간 그렇다", "2번","이번","2전","이전",
                "꽤 그렇다","3번","삼번","3전","삼전",
                "아주 많이 그렇다","4번","사번","4전","사전",
                ]

block_tokens = createSuppressTokenList(korean_words, language="ko")

@app.websocket("/ws/adhd")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            # Load waveform
            waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))

            print("Waveform shape:", waveform.shape)
            print("Sample rate:", sample_rate)

            if waveform.shape[0] > 1:
                waveform = waveform.mean(dim=0, keepdim=True)
            # Resample if needed
            if sample_rate != 16000:
                resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
                waveform = resampler(waveform)

            audio_np = waveform.squeeze(0).numpy()

            # Transcribe
            result = model.transcribe(audio_np, language="ko",
                                      suppress_tokens=[-1] + block_tokens,
                                      task="transcribe")
            transcript = result["text"].strip()

            await websocket.send_text(transcript)
    except WebSocketDisconnect:
        print("WebSocket disconnected")


@app.websocket("/ws/general")
async def websocket_general(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            # Load waveform
            waveform, sample_rate = torchaudio.load(io.BytesIO(audio_bytes))
            if waveform.shape[0] > 1:
                waveform = waveform.mean(dim=0, keepdim=True)
            # Resample if needed
            if sample_rate != 16000:
                resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
                waveform = resampler(waveform)

            audio_np = waveform.squeeze(0).numpy()

            # Transcribe
            result = model.transcribe(audio_np, language="ko")
            transcript = result["text"].strip()

            await websocket.send_text(transcript)
    except WebSocketDisconnect:
        print("WebSocket disconnected")