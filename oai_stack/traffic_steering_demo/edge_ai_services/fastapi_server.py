from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel
from typing import List
from PIL import Image
import io
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection
import uvicorn

# Initialize FastAPI app
app = FastAPI()

# Load the AI model and necessary processor
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")


# Define Pydantic models for request and response
class BoundingBox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float


class DetectedObject(BaseModel):
    label: str
    confidence: float
    bounding_box: BoundingBox


class AIModelOutput(BaseModel):
    detected_objects: List[DetectedObject]


@app.post("/infer", response_model=AIModelOutput)
async def infer(image: UploadFile = File(...)):
    """
    Infer method to handle image uploads and return detected objects.
    """
    try:
        # Read and convert the image to a PIL Image
        image_bytes = await image.read()
        image_pil = Image.open(io.BytesIO(image_bytes))

        # Preprocess the image
        inputs = processor(images=image_pil, return_tensors="pt")

        # Run the model to get predictions
        with torch.no_grad():
            outputs = model(**inputs)

        # Convert outputs (bounding boxes and class logits) to COCO API format
        target_sizes = torch.tensor([image_pil.size[::-1]])  # (height, width)
        results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

        # Prepare the response
        detected_objects = []
        for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
            detected_objects.append(
                DetectedObject(
                    label=model.config.id2label[label.item()],
                    confidence=score.item(),
                    bounding_box=BoundingBox(
                        x_min=box[0].item(),
                        y_min=box[1].item(),
                        x_max=box[2].item(),
                        y_max=box[3].item(),
                    ),
                )
            )

        return AIModelOutput(detected_objects=detected_objects)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)