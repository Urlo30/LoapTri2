# main.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from mediaflow_proxy.main import app as mediaflow_app
from importlib import resources

# Create the main FastAPI app
main_app = FastAPI()

# Serve static files from mediaflow_proxy under /static
static_path = resources.files("mediaflow_proxy").joinpath("static")
main_app.mount("/static", StaticFiles(directory=str(static_path), html=True), name="static")

# Include all routes from mediaflow_proxy
# Here, we'll use the original app as is, avoiding any conflicts with static routes
# This might lead to duplicate static routes, but we'll manage that in the next step
main_app.include_router(mediaflow_app.router)

# Define any additional routes for the main app
@main_app.get("/wow")
async def root():
    return {"message": "This is the main app"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=8080)
