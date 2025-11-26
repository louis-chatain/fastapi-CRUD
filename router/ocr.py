import httpx
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from starlette.responses import JSONResponse

# Create the router instance
router = APIRouter(prefix="/process-image", tags=["OCR Forwarding"])

# Configuration for the target OCR service (running on port 8001)
OCR_SERVICE_URL = "http://localhost:8001/ocr"


# We inject the 'Request' object to access the main app's state (request.app.state)
@router.post("/", summary="Uploads image and forwards it to the OCR service")
async def process_image_for_ocr(
    request: Request,
    image: UploadFile = File(..., description="Image file to process.")
):
    """
    Receives an image, forwards it to the OCR service running on port 8001,
    and returns the extracted text.
    """
    if not image.content_type or not image.content_type.startswith('image/'):
         raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    try:
        # Access the shared httpx.AsyncClient from the main app's state
        http_client = request.app.state.http_client
        
        # 1. Read the entire file content asynchronously
        file_content = await image.read()
        
        # 2. Create the files payload
        files_payload = {
            # Note: The field name "image" must match the expected FastAPI parameter name 
            # in the target service (port 8001).
            "image": (image.filename, file_content, image.content_type)
        }
        
        # 3. Use the shared AsyncClient instance to make the POST request
        response = await http_client.post(
            OCR_SERVICE_URL,
            files=files_payload,
            timeout=30.0
        )

        # 4. Handle service response status
        if response.status_code == 200:
            # Successfully received OCR data
            return JSONResponse(response.json())
        
        elif response.status_code == 400:
            # OCR service rejected the file
            raise HTTPException(status_code=400, detail=f"OCR Service Error: {response.json().get('detail', 'Bad Request')}")
        
        else:
            # Handle other server-side errors
            raise HTTPException(status_code=503, detail=f"OCR Service failed with status code {response.status_code}")

    except httpx.ConnectError:
        # This occurs if the OCR service (on port 8001) is not running
        raise HTTPException(status_code=503, detail="Cannot connect to the OCR service on port 8001. Is it running?")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred while processing the request.")