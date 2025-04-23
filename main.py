from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, select
from pydantic import BaseModel, HttpUrl
import string, random

# ----------------- Database Config -----------------
DATABASE_URL = "sqlite+aiosqlite:///./shortener.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# ----------------- FastAPI App -----------------
app = FastAPI()

# ----------------- Models -----------------
class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    target_url = Column(String)

# ----------------- Schemas -----------------
class URLBase(BaseModel):
    target_url: HttpUrl

# ----------------- Utility -----------------
def generate_key(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

# ----------------- Dependency -----------------
async def get_db():
    async with async_session() as session:
        yield session

# ----------------- Routes -----------------
@app.post("/shorten/")
async def shorten_url(payload: URLBase, session: AsyncSession = Depends(get_db)):
    try:
        key = generate_key()

        # Check if URL already exists
        result = await session.execute(select(URL).where(URL.target_url == payload.target_url))
        existing_url = result.scalar_one_or_none()
        if existing_url:
            return {"shortened_url": f"http://127.0.0.1:8000/{existing_url.key}"}

        # Create new shortened URL
        new_url = URL(key=key, target_url=payload.target_url)
        session.add(new_url)
        await session.commit()

        return {"shortened_url": f"http://127.0.0.1:8000/{key}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/{url_key}")
async def forward_to_target_url(url_key: str, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(URL).where(URL.key == url_key))
    db_url = result.scalar_one_or_none()

    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    return RedirectResponse(db_url.target_url)
