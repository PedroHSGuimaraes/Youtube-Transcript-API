from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
import re

app = FastAPI(title="API de Transcrição de Vídeo do YouTube")

class HealthCheckResponse(BaseModel):
    status: str

@app.get("/", response_model=HealthCheckResponse)
async def health_check():
    return HealthCheckResponse(status="Healthy")

class TranscriptionRequest(BaseModel):
    url: str
    language: str = "pt"

class TranscriptionResponse(BaseModel):
    transcription: str

def extract_video_id(url: str) -> str:
    """
    Extrai o ID do vídeo da URL do YouTube.
    """
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url)
    if match:
        return match.group(1)
    raise ValueError("ID do vídeo não encontrado na URL.")

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_video(request: TranscriptionRequest):
    try:
        video_id = extract_video_id(request.url)
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[request.language])
        full_text = " ".join([segment["text"] for segment in transcript_data])
        return TranscriptionResponse(transcription=full_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
