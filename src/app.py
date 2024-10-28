from fastapi import FastAPI, UploadFile, File
from prometheus_client import Summary, generate_latest, REGISTRY, Histogram, Counter
from PIL import Image
from transformers import AutoModelForImageClassification, AutoFeatureExtractor
import torch
from starlette.responses import Response
from time import time

# Initialize FastAPI
app = FastAPI()

# Prometheus errors!
# Create a metric to track request duration
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

# Track model inference time
INFERENCE_TIME = Summary('model_inference_seconds', 'Time spent in model inference')

# Count the number of requests to the prediction endpoint
PREDICTION_REQUESTS = Counter('prediction_requests_total', 'Total number of prediction requests')

# Histogram to track upload file sizes in bytes
UPLOAD_FILE_SIZE = Histogram('upload_file_size_bytes', 'Size of uploaded files in bytes', buckets=[1000, 5000, 10000, 50000, 100000, 500000])

# Counter for errors
ERROR_COUNT = Counter('prediction_errors_total', 'Total number of prediction errors')

# Load the model and feature extractor at startup
model = AutoModelForImageClassification.from_pretrained("./deit-base-distilled-patch16-224")
extractor = AutoFeatureExtractor.from_pretrained("./deit-base-distilled-patch16-224")

@app.post("/image/predict/")
async def predict(file: UploadFile = File(...)):
    start_time = time()  # Record start time
    PREDICTION_REQUESTS.inc()
    
    # Observe file size
    file_size = len(await file.read())
    UPLOAD_FILE_SIZE.observe(file_size)
    file.file.seek(0)  # Reset file pointer after reading

    try:
        with INFERENCE_TIME.time():
            # Load the image from the upload
            image = Image.open(file.file)
            
            # Ensure the image is in RGB format
            if image.mode != "RGB":
                image = image.convert("RGB")

            # Preprocess the image
            inputs = extractor(images=image, return_tensors="pt")
            
            # Perform inference
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
                predicted_class = logits.argmax(-1).item()
        
            # Get the label from the model configuration
            labels = model.config.id2label
            return {"predicted_class": labels[predicted_class]}
    except Exception as e:
        ERROR_COUNT.inc()  # Increment error count on exception
        raise e

    finally:
        elapsed_time = time() - start_time  # Calculate elapsed time
        REQUEST_TIME.observe(elapsed_time)  # Manually observe the duration
    
# Expose Prometheus metrics
@app.get("/info/metrics")
async def metrics():
    # Generate metrics data for Prometheus
    return Response(generate_latest(REGISTRY), media_type="text/plain")