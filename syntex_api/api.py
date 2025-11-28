from fastapi import FastAPI
import sys
import os
sys.path.append(os.path.dirname(__file__))

from resonance import get_resonance

app = FastAPI()

@app.get("/")
def root():
    return get_resonance()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
