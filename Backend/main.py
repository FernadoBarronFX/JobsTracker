from fastapi import FastAPI

app = FastAPI(title="JobsTaracker")

@app.get("/health")
def health():
    return {"status" : "ok"}