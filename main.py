from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
from search_engine import SearchEngine
from assistant import ConversationalAssistant
from cart_manager import CartManager
import uvicorn
import json
import logging
import webbrowser
from contextlib import asynccontextmanager

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ShopAI")

# Initialize core components
search_engine = SearchEngine()
assistant = ConversationalAssistant()
cart_manager = CartManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize databases on startup
    await assistant.init_db()
    await cart_manager.init_db()
    yield

app = FastAPI(title="ShopAI: Premium Ecommerce Assistant", lifespan=lifespan)

# --- API ROUTES (Defined First) ---

class QueryRequest(BaseModel):
    query: str
    session_id: Optional[str] = "default"

class CartAddRequest(BaseModel):
    session_id: str
    product: dict

@app.post("/chat")
async def chat_with_assistant(request: QueryRequest):
    logger.info(f"Chat request received for session: {request.session_id}")
    if not search_engine or not assistant:
        raise HTTPException(status_code=500, detail="Assistant components not initialized")
    
    products = await search_engine.search(request.query)
    
    async def event_generator():
        yield f"DATA:PRODUCTS:{json.dumps(products)}\n\n"
        async for chunk in assistant.generate_streaming_response(request.query, products, session_id=request.session_id):
            yield f"DATA:TEXT:{chunk}\n\n"

    return StreamingResponse(event_generator(), media_type="text/plain")

@app.post("/cart/add")
async def add_to_cart(request: CartAddRequest):
    logger.info(f"Adding product to cart for session: {request.session_id}")
    await cart_manager.add_to_cart(request.session_id, request.product)
    return {"status": "success"}

@app.get("/cart/{session_id}")
async def get_cart(session_id: str):
    return await cart_manager.get_cart(session_id)

@app.delete("/cart/{session_id}")
async def clear_cart(session_id: str):
    await cart_manager.clear_cart(session_id)
    return {"status": "cleared"}

@app.get("/products", response_model=List[dict])
async def list_products():
    if not search_engine:
        raise HTTPException(status_code=500, detail="Search engine not initialized")
    return search_engine.products_df.to_dict(orient='records')

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/sessions")
async def get_sessions():
    return await assistant.get_all_sessions()

@app.get("/sessions/{session_id}")
async def get_session_history(session_id: str):
    return await assistant.get_session_history(session_id)

# --- FRONTEND ROUTES (Defined Last) ---

@app.get("/")
async def get_frontend():
    return FileResponse("index.html")

@app.get("/style.css")
async def get_css():
    return FileResponse("style.css")

@app.get("/app.js")
async def get_js():
    return FileResponse("app.js")

# In case images are needed from the root (like logo.png if it existed)
# But we won't do a greedy mount for security reasons.

if __name__ == "__main__":
    # Open browser on main start
    webbrowser.open("http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
