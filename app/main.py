from fastapi import FastAPI, HTTPException
 
from app.services.build import buildar_modulo
from app.config import MODULOS_VALIDOS

app = FastAPI(title="Esteira de Deploy - EBOP")


@app.get("/health")
def root():
    return {"status": "online", "servico": "esteira-deploy"}

@app.post("/build/{modulo}")
def buildar(modulo: str, branch: str = "main"):
    if modulo not in MODULOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Módulo inválido. Válidos: {MODULOS_VALIDOS}"
        )
    resultado = buildar_modulo(modulo, branch=branch)
    if not resultado.sucesso:
        raise HTTPException(
            status_code=500,
            detail={"erro": "Build falhou", "log": resultado.log},
        )
    
    return{
        "sucesso": True,
        "modulo": modulo,
        "branch": branch,
        "war_gerado": str(resultado.caminho_war),
        "log":resultado.log, 
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)