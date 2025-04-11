from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders import YoutubeLoader

app = FastAPI(title="API de Transcrição de Vídeo do YouTube")

class TranscriptionRequest(BaseModel):
    url: str
    language: str = "pt"

class TranscriptionResponse(BaseModel):
    transcription: str

@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_video(request: TranscriptionRequest):
    """
    Rota que recebe a URL de um vídeo do YouTube e um código de idioma.
    Retorna a transcrição completa do vídeo.
    """
    try:
        loader = YoutubeLoader.from_youtube_url(request.url, language=request.language)
        documents = loader.load()
        
        if not documents:
            raise HTTPException(status_code=404, detail="Transcrição não encontrada para este vídeo.")

        transcript = " ".join([doc.page_content for doc in documents])
        return TranscriptionResponse(transcription=transcript)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
