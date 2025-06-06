from typing import List
from pydantic import BaseModel, Field


class TextInputModel(BaseModel):
    """ Input Model for the Sentence Semiotics"""
    text: List[str]
    request_id: str = Field(...)

    class Config:
        """ Sample Config"""
        schema_extra = {
            "example": {
                "text": ["hello world","this is a test"],
                "request_id": "60cedb6868b7ae0275a96ee4"

            }
        }


class TextPrediction(BaseModel):
    """ Model for Output Predictions"""
    x: float
    y: float
    labels: int
    docs: str


class TextOutputModel(BaseModel):
    """Output Model for Sentence Semiotics"""
    predictions: List[TextPrediction]
    request_id: str
    response_id: str
    message: str = "Text Clustered Successfully"

    class Config:
        """Sample Config"""
        schema_extra = {
            "example": {
                "predictions": [
                    {
                        "x": 0.99,
                        "y": 1.23,
                        "labels": 4,
                        "docs": "hello world"
                    },
                    {
                        "x": 0.91,
                        "y": 1.25,
                        "labels": 3,
                        "docs": "this is a test"
                    }
                ],
                "request_id": "60cedb6868b7ae0275a96ee4",
                "response_id": "62f8a029656c471f8e07c2dc78837d2d",
                "message": "Text Clustered Successfully"
            }
        }


class RootModel(BaseModel):
    """ Root Model"""
    message: str

    class Config:
        """ Sample Config"""
        schema_extra = {
            "example": {
                "message": "This REST API will embed and cluster text."
            }
        }
