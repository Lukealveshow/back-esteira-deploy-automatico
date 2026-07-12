from fastapi import FastAPI

app = FastAPI(title="Esteira de Deploy - EBOP")


@app.get("/health")
def root():
    return {"status": "online", "servico": "esteira-deploy"}
