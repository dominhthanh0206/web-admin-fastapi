from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import cv2
import numpy as np
from blog.database.database import get_db
from blog.services.camera_service import CameraService
import asyncio
from pathlib import Path

router = APIRouter(prefix="/camera", tags=["camera"])
templates = Jinja2Templates(directory="blog/templates")

@router.get("/")
async def get_camera_page(request: Request):
    return templates.TemplateResponse("camera.html", {"request": request})

async def generate_frames(camera_service: CameraService, request: Request):
    try:
        while True:
            # Check if client is still connected
            if await request.is_disconnected():
                break
                
            frame, name = camera_service.process_frame()
            if frame is None:
                continue
                
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
                
            # Convert to bytes
            frame_bytes = buffer.tobytes()
            
            # Yield frame in MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Add small delay to prevent overwhelming the connection
            await asyncio.sleep(0.1)
            
    except Exception as e:
        print(f"Error in generate_frames: {str(e)}")
    finally:
        camera_service.stop_camera()

@router.get("/stream")
async def video_stream(request: Request, db: Session = Depends(get_db)):
    try:
        camera_service = CameraService(db)
        camera_service.start_camera()
        
        return StreamingResponse(
            generate_frames(camera_service, request),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )
    except Exception as e:
        if 'camera_service' in locals():
            camera_service.stop_camera()
        raise HTTPException(status_code=500, detail=str(e)) 