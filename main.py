from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount the "static" directory as a static file directory
app.mount("/web", StaticFiles(directory="web"), name="web")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # You can use Python's open() function to read the HTML file
    with open("web/index.html", "r") as file:
        html_content = file.read()
    
    return HTMLResponse(content=html_content)