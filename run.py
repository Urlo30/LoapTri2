from fastapi import FastAPI, APIRouter
from mediaflow_proxy.main import app as mediaflow_app
FastAPI = main_app()
main_app.router.include_router(mediaflow_app.router)

# Define any additional routes for the main app
@main_app.get("/wow")
async def root():
    return {"message": "This is the main app"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=8080)
