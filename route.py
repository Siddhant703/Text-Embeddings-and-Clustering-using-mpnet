import uuid
from fastapi import APIRouter, Body, HTTPException
from model import TextInputModel,TextOutputModel
from text_service import TextService

router = APIRouter()
text_service = TextService()


@router.post("/sentence-semiotics", response_description="Sentence Semiotics Completed Successfully",
             response_model=TextOutputModel)
async def cluster_text(input: TextInputModel = Body(...)):
    """ API End point to classify the image with given label(s) list"""
    response_id = uuid.uuid4().hex
    try:
        predictions = text_service.processText(input.text)
        return TextOutputModel(predictions=predictions,request_id=input.request_id,response_id=uuid.uuid4().hex)
    except Exception as error_response:
        raise HTTPException(status_code=500,
                            detail="Error clustering text: "+str(error_response)) from error_response
