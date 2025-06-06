## End points 
- /sentence-semiotics

## Expected input(s) schema
```json

  {
    "text": [
        "I have the Kelowna coronerâ€™s endorsement ðŸ’— https://t.co/7iS5EA0bYR",
        "With the amount of money Air India loses, it should have been the first Unicorn.",
        "This should be made an actual font! https://t.co/rpHomUr8Yj",
        "Peter Thiel called China a â€œweirdly autisticâ€ country that is â€œprofoundly uncharismaticâ€",
        "Please pray for a frog and his wife with a possible pregnancy problem.",
        "Bill Hwang had $20 billion. He lost it all in two days https://t.co/92YEdnXTqe via @BW",
        "Think beyond yourself. Think in historical terms. Historical cycles unfold at a glacial  pace. Tectonic drift acrossâ€¦ https://t.co/87M9PhZ0ft",
        "Had a mango  a zoom call.  Mentally impossible to go back to 2019 life now.",
        "I realised some time ago itd be perfectly possible to raise children in secret and if its possible its probably being done.",
        "I have the Kelowna coronerâ€™s endorsement ðŸ’— https://t.co/7iS5EA0bYR",
        "With the amount of money Air India loses, it should have been the first Unicorn."],
      "request_id": "123"
  }
```
## Nature of processing
    Note - text preprocessing and cleaning should be done before
    Embeddings are created using these sentence-transformers: LaBSE, clip-ViT-B-32 clip-ViT-B-32-multilingual-v1. Bayesian search with hyperopt package is run to determine optimal UMAP and HDBSCAN parameters. Loss is calculated using HDBSCAN probabilities. Output is the text x,y 2D co-ordinates and cluster label.
   
## Expected output(s) schema
```json
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

```      
    
## How to run the service
1. Build the docker: `docker build -t sentence-semiotics . --build-arg 123`
2. Run the docker:`docker run --name=<container name> -p 8000:8080 <image name> `

## OpenAPI docs
1. http://localhost:8000/docs
2. http://localhost:8000/redoc
