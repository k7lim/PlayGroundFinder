import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from common.models import Base, PlaygroundImageOrm, PlaygroundOrm, HostLocationOrm, AddressOrm, LocationOrm, AgeRangeOrm, PlaygroundFeatureOrm
import os
from common.utils.process_playground_image import process_playground_image
from common.schemas import PlaygroundImage, Playground

# Create an engine and bind it to the Base
engine = create_engine('sqlite:///playgrounds.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads/')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No file selected")
    if file.filename.rsplit('.', 1)[1].lower() not in {'png', 'jpg', 'jpeg', 'gif', 'webp'}:
        raise HTTPException(status_code=400, detail="File type not allowed")

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    # Process the uploaded image
    processed_file_path, playground_image = process_playground_image(filepath)

    # Persist the playground image and related objects
    new_playground_image = PlaygroundImageOrm(
        url=playground_image.url,
        taken_at=playground_image.taken_at,
        children_detected=playground_image.children_detected,
        needs_face_blurring=playground_image.needs_face_blurring,
        estimated_age_range=AgeRangeOrm(min_age=playground_image.estimated_age_range.min_age, max_age=playground_image.estimated_age_range.max_age)
    )
    session.add(new_playground_image)
    session.commit()

    return {"filename": file.filename, "processed_file_path": processed_file_path}

@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    return FileResponse(os.path.join(UPLOAD_FOLDER, filename))

@app.get("/playground_images/")
async def get_playground_images():
    images = session.query(PlaygroundImageOrm).all()
    return {"images": [PlaygroundImage.model_validate(image) for image in images]}

@app.get("/playground_images/{image_id}")
async def get_playground_image(image_id: int):
    image = session.query(PlaygroundImageOrm).filter(PlaygroundImageOrm.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"image": PlaygroundImage.model_validate(image)}

@app.put("/playground_images/{image_id}")
async def update_playground_image(image_id: int, playground_image: PlaygroundImage):
    image = session.query(PlaygroundImageOrm).filter(PlaygroundImageOrm.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    for key, value in playground_image.dict().items():
        setattr(image, key, value)
    session.commit()
    return {"image": PlaygroundImage.model_validate(image)}

@app.delete("/playground_images/{image_id}")
async def delete_playground_image(image_id: int):
    image = session.query(PlaygroundImageOrm).filter(PlaygroundImageOrm.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    session.delete(image)
    session.commit()
    return {"message": "Image deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from common.models import Base, PlaygroundImageOrm, PlaygroundOrm, HostLocationOrm, AddressOrm, LocationOrm, AgeRangeOrm, PlaygroundFeatureOrm
import os
from common.utils.process_playground_image import process_playground_image
from common.schemas import PlaygroundImage, Playground

# Create an engine and bind it to the Base
engine = create_engine('sqlite:///playgrounds.db')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

app = FastAPI()

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads/')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No file selected")
    if file.filename.rsplit('.', 1)[1].lower() not in {'png', 'jpg', 'jpeg', 'gif', 'webp'}:
        raise HTTPException(status_code=400, detail="File type not allowed")

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    # Process the uploaded image
    processed_file_path, playground_image = process_playground_image(filepath)

    # Persist the playground image and related objects
    new_playground_image = PlaygroundImageOrm(
        url=playground_image.url,
        taken_at=playground_image.taken_at,
        children_detected=playground_image.children_detected,
        needs_face_blurring=playground_image.needs_face_blurring,
        estimated_age_range=AgeRangeOrm(min_age=playground_image.estimated_age_range.min_age, max_age=playground_image.estimated_age_range.max_age)
    )
    session.add(new_playground_image)
    session.commit()

    return {"filename": file.filename, "processed_file_path": processed_file_path}

@app.get("/uploads/{filename}")
async def get_uploaded_file(filename: str):
    return FileResponse(os.path.join(UPLOAD_FOLDER, filename))

@app.get("/playground_images/")
async def get_playground_images():
    images = session.query(PlaygroundImageOrm).all()
    return {"images": [PlaygroundImage.model_validate(image) for image in images]}

@app.get("/playground_images/{image_id}")
async def get_playground_image(image_id: int):
    image = session.query(PlaygroundImageOrm).filter(PlaygroundImageOrm.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"image": PlaygroundImage.model_validate(image)}

@app.put("/playground_images/{image_id}")
async def update_playground_image(image_id: int, playground_image: PlaygroundImage):
    image = session.query(PlaygroundImageOrm).filter(PlaygroundImageOrm.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    for key, value in playground_image.dict().items():
        setattr(image, key, value)
    session.commit()
    return {"image": PlaygroundImage.model_validate(image)}

@app.delete("/playground_images/{image_id}")
async def delete_playground_image(image_id: int):
    image = session.query(PlaygroundImageOrm).filter(PlaygroundImageOrm.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    session.delete(image)
    session.commit()
    return {"message": "Image deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
