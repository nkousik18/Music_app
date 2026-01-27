from fastapi import FastAPI
from search import router as search_router
from favorites import router as fav_router
from events import router as events_router

app = FastAPI(title="Core App API")

app.include_router(search_router)
app.include_router(fav_router)
app.include_router(events_router)
