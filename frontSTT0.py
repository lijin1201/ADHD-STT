from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import whisper
import os

app = FastAPI()

# Whisper base 모델 로드 (GPU 사용)
model = whisper.load_model("base", device="cuda:0")

# ADHD 간이 문항 (2개)
QUESTIONS = [
    "당신은 주의가 산만하다는 말을 자주 듣습니까?",
    "가만히 앉아 있는 것이 어렵다고 느끼나요?"
]

@app.get("/")
def home():
    return HTMLResponse("""
    <html>
    <head>
      <title>ADHD 음성 진단</title>
    </head>
    <body>
      <h2><b>ADHD</b> 음성 진단 테스트 (2문항)</h2>
      <button onclick="startWebSocket()">진단 시작</button>
      <div id="messages"></div>
      <div id="status" style="margin-top: 10px; font-weight: bold; color: darkred;"></div>

      <script>
        let socket;
        let mediaRecorder;
        let audioChunks = [];
        
        function startWebSocket() {
          const host = 'localhost:10181';
          
          const statusDiv = document.getElementById("status");
          statusDiv.textContent = "🎙️ 1 녹음 준비....";
          setTimeout(()=>{},5000);
          socket = new WebSocket(`ws://${host}/ws`);


          socket.onmessage = async function(event) {
            const msg = event.data;
            const messagesDiv = document.getElementById("messages");
        
            const message = document.createElement("p");
            const cont = JSON.parse(msg);
            if (cont.mode == 'record') {
              statusDiv.textContent = "🎙️ 녹음 중... 응답을 말씀해 주세요.";
            } else if (cont.mode=='transcript') {
              const message = document.createElement("p");
              message.textContent = '응답 내용 : '+ cont.transcript;
              messagesDiv.appendChild(message);
              statusDiv.textContent = "";
            }
            
            // messagesDiv.appendChild(message);
        
            if (cont.mode =='record') {
              //statusDiv.textContent = "🎙️ 녹음 준비... 응답을 말씀해 주세요.";
        
              // 마이크 녹음 시작
              const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
              audioChunks = [];
              mediaRecorder = new MediaRecorder(stream);
        
              mediaRecorder.ondataavailable = e => {
                audioChunks.push(e.data);
              };
        
              mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
                const arrayBuffer = await audioBlob.arrayBuffer();
                socket.send(arrayBuffer);
              };
        
              mediaRecorder.start();
        
              // 3초 뒤 자동 종료 및 전송
              setTimeout(() => {
                mediaRecorder.stop();
              }, 3000);
            }
          };
        
          socket.onclose = function() {
            const message = document.createElement("p");
            message.textContent = "진단이 종료되었습니다.";
            document.getElementById("messages").appendChild(message);
            document.getElementById("status").textContent = "";
          };
        }
      </script>
    </body>
    </html>
    """)

