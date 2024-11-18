from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Mount the "static" folder to serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Define a route that serves the index.html file
@app.get("/")
async def read_index():
    return FileResponse("templates/index.html")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
