from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from urllib3 import disable_warnings
from routers import network, provision, notification, platform
import uvicorn

# supress warnings
disable_warnings()

# server
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(network.router)
app.include_router(provision.router)
app.include_router(notification.router)
app.include_router(platform.router)


@app.get("/")
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>FastAPI HTML Response</title>
    </head>
    <body>
        <h1>Welcome to VM Automation Server</h1>
        <p>This is a FastAPI server designed for virtual machines provisioning including IPAM.</p>
    </body>
    </html>
    """
    return Response(content=html_content, status_code=200)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
