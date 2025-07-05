from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import os
import tempfile
import shutil
from process_voice import process_voice
import uvicorn

app = FastAPI(
    title="OpenVoice API",
    description="API for processing voice files and extracting voice features",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "OpenVoice API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/process-voice")
async def process_voice_api(file: UploadFile = File(...)):
    """
    Process a voice file and return the voice features (.pt file)
    """
    # Check if file is an audio file
    if not file.content_type or not file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="File must be an audio file")
    
    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded file
        input_path = os.path.join(temp_dir, file.filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process the voice
        try:
            output_path = process_voice(input_path, temp_dir)
            
            # Return the processed file
            return FileResponse(
                output_path,
                media_type='application/octet-stream',
                filename='voice.pt'
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing voice: {str(e)}")

@app.post("/process-voice-url")
async def process_voice_url(url: str):
    """
    Process a voice file from URL and return the voice features (.pt file)
    """
    import requests
    
    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Download file from URL
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Determine filename from URL or use default
            filename = url.split('/')[-1] if '/' in url else 'audio.mp3'
            input_path = os.path.join(temp_dir, filename)
            
            with open(input_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # Process the voice
            output_path = process_voice(input_path, temp_dir)
            
            # Return the processed file
            return FileResponse(
                output_path,
                media_type='application/octet-stream',
                filename='voice.pt'
            )
            
        except requests.RequestException as e:
            raise HTTPException(status_code=400, detail=f"Error downloading file: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing voice: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 