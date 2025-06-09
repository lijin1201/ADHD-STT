from fastapi import FastAPI, WebSocket
import os, io
import torchaudio
import whisper

app = FastAPI()
model = whisper.load_model("small")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_json({'message':"Initializing",
                               'mode':'init'})
    
   
    # await websocket.send_text(f"문항 : question")
    while True:
        await websocket.send_json({'message':"Recording", "mode":"record"})
        audio_bytes = await websocket.receive_bytes()

        audio_path = io.BytesIO(audio_bytes)

        waveform, sample_rate = torchaudio.load(audio_path)
        audio_np = waveform.squeeze(0).numpy()
        if sample_rate != 16000:
            resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
            waveform = resampler(waveform)
            audio_np = waveform.squeeze(0).numpy()

        result = model.transcribe(audio_np, language="ko")
        transcript = result["text"].strip()

        data_to_send = {"message": transcript, "mode":"transcript","status": "success"}
        # await websocket.send_text(f"인식된 응답: {transcript}")
        await websocket.send_json(data_to_send)
    # await websocket.close()

        # data = await websocket.receive_text()
        # # Process data
        # response = f"Received: {data}"
        # await websocket.send_text(response)