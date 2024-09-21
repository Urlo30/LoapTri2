from fastapi import FastAPI, HTTPException,Request
from mediaflow_proxy.main import app as mediaflow_app
from importlib import resources



main_app = FastAPI()
static_path = resources.files("mediaflow_proxy").joinpath("static")
main_app.mount("/static", StaticFiles(directory=str(static_path), html=True), name="static")
main_app.router.include_router(mediaflow_app.router)
@app.get("/wow")
async def root():
    return {"message": "This is the main app"}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=8080)
