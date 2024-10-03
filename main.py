from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import spacy
from typing import List, Optional

app = FastAPI(
    title="Spacy Entity Extraction API",
    description="API for extracting entities from text using Spacy, with optional noun and noun chunk extraction.",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "Entity Extraction",
            "description": "Operations related to entity extraction using Spacy",
        },
    ],
)

# Check if the model is downloaded, if not, download it
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading the Spacy model. This may take a while...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

class EntityExtractionRequest(BaseModel):
    text: str = Field(..., description="The input text to extract entities from")
    extract_nouns: bool = Field(False, description="Whether to extract nouns from the text")
    extract_noun_chunks: bool = Field(False, description="Whether to extract noun chunks from the text")

class Entity(BaseModel):
    text: str = Field(..., description="The extracted entity text")
    label: str = Field(..., description="The label of the extracted entity")

class EntityExtractionResponse(BaseModel):
    entities: List[Entity] = Field(..., description="List of extracted entities")
    nouns: Optional[List[str]] = Field(None, description="List of extracted nouns (if requested)")
    noun_chunks: Optional[List[str]] = Field(None, description="List of extracted noun chunks (if requested)")

@app.post("/extract_entities", response_model=EntityExtractionResponse, tags=["Entity Extraction"])
async def extract_entities(request: EntityExtractionRequest):
    """
    Extract entities from the given text using Spacy.

    This endpoint processes the input text and returns:
    - A list of extracted entities with their labels
    - Optionally, a list of nouns (if extract_nouns is True)
    - Optionally, a list of noun chunks (if extract_noun_chunks is True)

    Args:
        request (EntityExtractionRequest): The request body containing the text and extraction options

    Returns:
        EntityExtractionResponse: The response containing extracted information

    Raises:
        HTTPException: If there's an error during processing
    """
    try:
        doc = nlp(request.text)
        
        result = EntityExtractionResponse(entities=[])
        
        # Extract entities
        for ent in doc.ents:
            result.entities.append(Entity(text=ent.text, label=ent.label_))
        
        # Extract nouns if requested
        if request.extract_nouns:
            result.nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        
        # Extract noun chunks if requested
        if request.extract_noun_chunks:
            result.noun_chunks = [chunk.text for chunk in doc.noun_chunks]
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)