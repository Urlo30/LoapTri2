from fastapi import FastAPI, APIRouter
from mediaflow_proxy.main import app as mediaflow_app
main_app = FastAPI()

main_app.router.include_router(mediaflow_app.router)

# Define any additional routes for the main app
@main_app.get("/wow")
async def root():
    return {"message": "This is the main app"}
@main_app.get('/huhu/{id}')
async def huhu(id:str):
    async with httpx.AsyncClient() as client:
        response = client.get(f"https://huhu.to/play/{id}/index.m3u8")
        return response.url

@main_app.get('/mixdrop/{id}')
async def mixdrop(id:str):
    print(f"Received ID: {id}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.10; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(id, headers=headers, follow_redirects=True,timeout = 30)
        [s1, s2] = re.search(r"\}\('(.+)',.+,'(.+)'\.split", response.text).group(1, 2)
        schema = s1.split(";")[2][5:-1]
        terms = s2.split("|")
        charset = string.digits + string.ascii_letters
        d = dict()
        for i in range(len(terms)):
            d[charset[i]] = terms[i] or charset[i]
        s = 'https:'
        for c in schema:
            s += d[c] if c in d else c
        return s

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(main_app, host="0.0.0.0", port=8080)
