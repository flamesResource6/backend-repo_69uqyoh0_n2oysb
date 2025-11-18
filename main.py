import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Project, BlogPost

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Portfolio Backend Running"}


# Helper to convert Mongo docs
class MongoEncoder(BaseModel):
    @staticmethod
    def encode(doc: dict):
        if not doc:
            return doc
        d = dict(doc)
        if "_id" in d:
            d["id"] = str(d.pop("_id"))
        # Convert any ObjectId nested values if needed
        for k, v in list(d.items()):
            if isinstance(v, ObjectId):
                d[k] = str(v)
        return d


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response


# Portfolio Endpoints

@app.get("/api/projects")
def list_projects(featured: Optional[bool] = None):
    flt = {}
    if featured is not None:
        flt["featured"] = featured
    docs = get_documents("project", flt, limit=50)
    return [MongoEncoder.encode(d) for d in docs]


@app.post("/api/projects")
def create_project(p: Project):
    try:
        inserted_id = create_document("project", p)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/blogs")
def list_blogs(published: Optional[bool] = True):
    flt = {}
    if published is not None:
        flt["published"] = published
    docs = get_documents("blogpost", flt, limit=20)
    return [MongoEncoder.encode(d) for d in docs]


@app.post("/api/blogs")
def create_blog(post: BlogPost):
    try:
        inserted_id = create_document("blogpost", post)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
