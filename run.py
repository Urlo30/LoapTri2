from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from mediaflow_proxy.main import app as mediaflow_app
from importlib import resources
from fastapi.routing import APIRoute

# Create the main FastAPI app
main_app = FastAPI()

# Serve static files from mediaflow_proxy under /static
static_path = resources.files("mediaflow_proxy").joinpath("static")
main_app.mount("/static", StaticFiles(directory=str(static_path), html=True), name="static")

# Create a new router for mediaflow_proxy excluding the static route
proxy_router = APIRouter()

# Manually include all routes from mediaflow_proxy except the static routes
for route in mediaflow_app.router.routes:
    if isinstance(route, APIRoute):  # Check if the route is an API route
        proxy_router.add_route(route.path, route.endpoint, methods=route.methods, name=route.name)

# Include the new router in the main app
main_app.include_router(proxy_router)

# Define any additional routes for the main app
@main_app.get("/wow")
async def root():
    return {"message": "This is the main app"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=8080)
