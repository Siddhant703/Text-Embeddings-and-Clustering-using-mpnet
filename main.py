from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.datastructures import CommaSeparatedStrings
from route import router as CLIPRouter
from model import RootModel

app = FastAPI(title="SENTENCE SEMIOTICS",
              description="""REST API for text embedding and clustering.""",
              version="1.0",
              openapi_url="/api/v1/openapi.json")



app.add_middleware(
    CORSMiddleware,
    allow_origins=CommaSeparatedStrings("*"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(CLIPRouter)

@app.get("/", tags=["Root"], response_model=RootModel)
async def read_root():
    """ Root End Point to Describe the API"""
    return RootModel(
        message="""SENTENCE SEMIOTICS: This REST API will embed and cluster text""")
