"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Portfolio-specific schemas

class Project(BaseModel):
    """
    Freelance/project portfolio items
    Collection: "project"
    """
    title: str = Field(..., description="Project title")
    description: str = Field(..., description="Short summary")
    tags: List[str] = Field(default_factory=list, description="Tech used")
    link: Optional[HttpUrl] = Field(None, description="Live URL or repo")
    image: Optional[HttpUrl] = Field(None, description="Thumbnail image URL")
    featured: bool = Field(False, description="Show on homepage")

class BlogPost(BaseModel):
    """
    Simple blog posts
    Collection: "blogpost"
    """
    title: str = Field(..., description="Post title")
    excerpt: str = Field(..., description="Short excerpt for cards")
    content: str = Field(..., description="Markdown or HTML content")
    cover_image: Optional[HttpUrl] = Field(None, description="Hero image URL")
    author: str = Field(..., description="Author name")
    slug: str = Field(..., description="URL slug")
    published: bool = Field(True, description="Is published")
