import whisper
import glob

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
korean_words = ["예", "아니오"]
block_tokens = createSuppressTokenList(korean_words, language="ko")

# Load Whisper model (base, small, medium, etc.)
model = whisper.load_model("small")  # You can use "medium" or "large" for better accuracy

print ("device: ",model.device)
# Transcribe from local file path
# audio_path = "path/to/your/audio_file.wav"  # Replace with your actual file path

filelist = sorted(glob.glob('sounds/*.m4a'))
for audio_path in filelist:
    result = model.transcribe(
        audio_path,
        language="ko",
        suppress_tokens=[-1] + block_tokens,
        task="transcribe"
    )

    # Print the Korean output
    print(f"File: {audio_path}", "Result:",result["text"])
