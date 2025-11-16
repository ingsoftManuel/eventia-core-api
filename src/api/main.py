from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.application.routes import event_routes, participant_routes, attendance_routes
from src.infrastructure.database.connection import init_db
from src.infrastructure.cache.cache_client import cache_client

# Create FastAPI application
app = FastAPI(
    title="Eventia Core API",
    description="Event management system with participants and attendance tracking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(event_routes.router)
app.include_router(participant_routes.router)
app.include_router(attendance_routes.router)


@app.on_event("startup")
def on_startup():
    """Initialize database and check services on startup"""
    print("=" * 50)
    print("🚀 Starting Eventia Core API...")
    print("=" * 50)
    
    print("\n📊 Initializing database...")
    init_db()
    print("✅ Database initialized successfully!")
    
    # Check cache connection
    print("\n💾 Checking cache system...")
    if cache_client.ping():
        print("✅ Redis cache connected successfully!")
    else:
        print("⚠️  Redis not available - Using in-memory cache")
        print("   (This is fine for development)")
    
    print("\n" + "=" * 50)
    print("✅ Application ready!")
    print("📚 API Docs: http://127.0.0.1:8000/docs")
    print("=" * 50 + "\n")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Eventia Core API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    redis_status = "connected" if cache_client.ping() else "disconnected"
    return {
        "status": "healthy",
        "database": "connected",
        "cache": redis_status
    }