import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import analysis

app = FastAPI(title="Horus Vision", description="Elite Career Intelligence Ledger — Audit the actual human cost of career decisions.")

# Setup static files directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "templates", "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.include_router(analysis.router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")



if __name__ == "__main__":
    import uvicorn
    # Cloud Run injects PORT env variable, so we run on that port if present
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
