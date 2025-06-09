import whisper
import glob


print(whisper.__file__)

# Define allowed Korean words
# korean_words = ["예", "아니오"]
# block_tokens = createSuppressTokenList(korean_words, language="ko")

# Load Whisper model (base, small, medium, etc.)
model = whisper.load_model("small")  # You can use "medium" or "large" for better accuracy

# Transcribe from local file path
# audio_path = "path/to/your/audio_file.wav"  # Replace with your actual file path

filelist = sorted(glob.glob('stati/audios/*.m4a'))
for audio_path in filelist:
    result = model.transcribe(
        audio_path,
        language="ko",
        # suppress_tokens=[-1] + block_tokens,
        # task="transcribe"
    )

    # Print the Korean output
    print(f"File: {audio_path}", "Result:",result["text"])
