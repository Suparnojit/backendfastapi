from fastapi import FastAPI, UploadFile, File, FileResponse, StreamingResponse 
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse
import os
import subprocess
import uuid

app = FastAPI(debug=True)

@app.post("/upload-video")
async def upload_video(video: UploadFile = File(...)):
    try:
        if video.content_type != "video/mp4":
            return HTTPException(status_code=400, detail="Only MP4 videos are allowed")
        filename = f"{str(uuid.uuid4())}.mp4"
        with open(f"uploads/{filename}", "wb") as f:
            f.write(await video.read())
        return {"filename": filename}
    except Exception as e:
        return {"error": str(e)}
    subprocess.call(["python", "videoDehaze.py", f"uploads/{filename}"])
    
@app.get("/download-video")
async def download_video():
    file_path = "path/to/processed_video.mp4"
    file = open(file_path, "rb")

    return StreamingResponse(file, media_type="video/mp4", filename="processed_video.mp4")    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
