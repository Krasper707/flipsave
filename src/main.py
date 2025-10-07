
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .llm_extractor import create_extraction_chain, ExtractedInfo
app = FastAPI(
    title="FlipSave API",
    description="An API to extract and categorize information from financial texts.",
    version="1.0.0",
)

try:
    extraction_chain = create_extraction_chain()
except Exception as e:
    extraction_chain = None
    print(f"Error creating extraction chain on startup: {e}")


class TextInput(BaseModel):
    text: str
@app.post("/process-text/", response_model=ExtractedInfo)
async def process_text(request: TextInput):
    """
    Accepts a raw text string and returns structured financial information.
    
    This endpoint processes the input text using the Gemini-powered extraction chain.
    """
    if extraction_chain is None:
        raise HTTPException(
            status_code=500, 
            detail="Internal Server Error: Extraction chain is not available."
        )

    try:
        result = extraction_chain.invoke({"text_input": request.text})
        return result
    except Exception as e:
        print(f"Error during extraction: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred while processing the text: {e}"
        )

@app.get("/")
def read_root():
    return {"status": "FlipSave API is running"}
