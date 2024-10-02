from fastapi import FastAPI, Response,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import random
import json
import time
from services.regions_service import RegionService
from services.dto import RegionDTO
from models import Database
import io
import uvicorn
from imageio import v3 as iio
from dotenv import load_dotenv
import os
import traceback

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

database = Database(os.getenv('DATABASE_URL'))
region_service = RegionService(database)
# cam = Reconnecting_CamGear(cam_address=int(0))

@app.get('/')
def index():
    return "Hello, João Gabriel Develop this!!"


@app.get('/video')
async def video():
    '''streaming video from .mp4 file'''
    cap = cv2.VideoCapture('video.mp4')
    while True:
        frame,_ = cap.read()
        if not frame:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n')
        yield (b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

@app.get('/cam_frame')
async def cam_frame():
    # Capture a single frame
    frame = cam.get_frame()
    if frame is None or frame.size == 0:
        return Response(status_code=404, content="Camera frame could not be captured")

    # Flip and convert to grayscale (optional)
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
   
    # Convert to bytes and return the response
    print("Returning frame")
    with io.BytesIO() as buf:
        iio.imwrite(buf, frame, plugin="pillow", format="JPEG")
        im_bytes = buf.getvalue()
    headers = {'Content-Disposition': 'inline; filename="image.jpeg"'}
    return Response(im_bytes, headers=headers, media_type='image/jpeg')


@app.get('/background_kr/')
def background_kr():
    image = cv2.imread('img/background.png')
    _, buffer = cv2.imencode('.jpg', image)
    frame = buffer.tobytes()
    return StreamingResponse(io.BytesIO(frame), media_type='image/jpeg')


@app.get('/OnMouseEvent')
def OnMouseEvent():
    raise NotImplementedError

# @app.get('/video')
# def video():
#     # # Capture a single frame
#     # frame = cam.get_frame()
#     # if frame is None or frame.size == 0:
#     #     return Response(status_code=404, content="Camera frame could not be captured")

#     # # Flip and convert to grayscale (optional)
#     # frame = cv2.flip(frame, 1)
#     # frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
   
#     # # Convert to bytes and return the response
#     # print("Returning frame")
#     # with io.BytesIO() as buf:
#     #     iio.imwrite(buf, frame, plugin="pillow", format="JPEG")
#     #     im_bytes = buf.getvalue()
#     # headers = {'Content-Disposition': 'inline; filename="image.jpeg"'}
#     # return Response(im_bytes, headers=headers, media_type='image/jpeg')


@app.get('/grafico')
async def chart_data():
    raise NotImplementedError
    
@app.get('/remove_region')
def remove_region():
    try:
        region_service.delete_region(1)
        return {'status': 'success'}
    except Exception as e:
        return {'error': str(e)}

@app.post('/save_region')
async def save_region(request: Request):
    values = await request.json()  # Read JSON body from request
    regions = values.get('polygon')  # Adjust according to how your data is structured
    name = values.get('feature_id')
    
    entry = RegionDTO(
        name=name,
        polygon=regions
    )
    
    try:
        region_service.update_region(id=1, data=entry)
        return {'status': 'success'}
    except Exception as e:
        traceback.print_exc()
        return {'error': str(e)}

@app.get('/get_regions')
def get_regions():
    try:
        regions = region_service.list_regions()
        region = regions[0]
        return region
    except Exception as e:
        return {'error': str(e)}
    
@app.post('/init_corrida')
def init_corrida():
    # process frame and save the recording on database
    ## to be implemented
    return {'status': 'success'}

@app.post('/end_corrida')
def end_corrida():
    # process frame and save the recording on database
    ## to be implemented
    return {'status': 'success'}

@app.post('/save_frame')
def save_frame():    
    # process frame and save the recording on database
    ## to be implemented
    return {'status': 'success'}

@app.post('/init_recording')
def init_recording():
    # process frame and save the recording on database
    ## to be implemented
    return {'status': 'success'}

@app.post('/end_recording')
def end_recording():
    # process frame and save the recording on database
    ## to be implemented
    return {'status': 'success'}

if __name__ == "__main__":
    print("=== API IS RUNNING ===")
    uvicorn_app = f"{os.path.basename(__file__).removesuffix('.py')}:app"
    uvicorn.run(uvicorn_app, host="0.0.0.0", port=5050, reload=False)
