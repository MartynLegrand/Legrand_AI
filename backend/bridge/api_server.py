"""
FastAPI Server for Legrand 3D
Provides REST API and WebSocket endpoints for Blender Core
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import uvicorn
import asyncio
import json
import os
from blender_core import BlenderCore


app = FastAPI(title="Legrand 3D API", version="1.0.0")

# CORS configuration - allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Blender Core
blender = BlenderCore()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()


# Pydantic models for request validation
class PrimitiveCreate(BaseModel):
    type: str
    name: Optional[str] = None
    location: Optional[List[float]] = [0, 0, 0]
    scale: Optional[List[float]] = [1, 1, 1]


class ModifierApply(BaseModel):
    object_name: str
    modifier_type: str
    params: Optional[Dict[str, Any]] = None


class TransformUpdate(BaseModel):
    object_name: str
    location: Optional[List[float]] = None
    rotation: Optional[List[float]] = None
    scale: Optional[List[float]] = None


# REST API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Legrand 3D API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "blender": "ready"}


@app.get("/api/scene")
async def get_scene():
    """Get current scene information"""
    result = blender.get_scene_info()
    return result


@app.post("/api/scene/clear")
async def clear_scene():
    """Clear the scene"""
    result = blender.clear_scene()
    await manager.broadcast({
        "type": "scene_cleared",
        "data": result
    })
    return result


@app.post("/api/primitive")
async def create_primitive(primitive: PrimitiveCreate):
    """Create a primitive object"""
    result = blender.create_primitive(
        primitive_type=primitive.type,
        name=primitive.name,
        location=tuple(primitive.location),
        scale=tuple(primitive.scale)
    )
    
    if result["status"] == "success":
        # Export scene after creating object
        export_result = blender.export_scene()
        result["export"] = export_result
        
        # Broadcast to all connected WebSocket clients
        await manager.broadcast({
            "type": "primitive_created",
            "data": result
        })
    
    return result


@app.post("/api/modifier")
async def apply_modifier(modifier: ModifierApply):
    """Apply a modifier to an object"""
    result = blender.apply_modifier(
        object_name=modifier.object_name,
        modifier_type=modifier.modifier_type,
        params=modifier.params
    )
    
    if result["status"] == "success":
        # Export scene after applying modifier
        export_result = blender.export_scene()
        result["export"] = export_result
        
        # Broadcast update
        await manager.broadcast({
            "type": "modifier_applied",
            "data": result
        })
    
    return result


@app.post("/api/transform")
async def update_transform(transform: TransformUpdate):
    """Update object transformation"""
    result = blender.update_object_transform(
        object_name=transform.object_name,
        location=tuple(transform.location) if transform.location else None,
        rotation=tuple(transform.rotation) if transform.rotation else None,
        scale=tuple(transform.scale) if transform.scale else None
    )
    
    if result["status"] == "success":
        # Export scene after transform
        export_result = blender.export_scene()
        result["export"] = export_result
        
        # Broadcast update
        await manager.broadcast({
            "type": "transform_updated",
            "data": result
        })
    
    return result


@app.post("/api/export")
async def export_scene(filename: str = "preview.glb"):
    """Export the scene to GLB"""
    result = blender.export_scene(filename)
    return result


@app.get("/api/preview/{filename}")
async def get_preview_file(filename: str):
    """Serve exported GLB files"""
    filepath = os.path.join(blender.export_dir, filename)
    
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=filepath,
        media_type="model/gltf-binary",
        filename=filename
    )


# WebSocket endpoint for real-time updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket connection for real-time updates"""
    await manager.connect(websocket)
    
    try:
        # Send initial scene state
        scene_info = blender.get_scene_info()
        await websocket.send_json({
            "type": "connected",
            "data": scene_info
        })
        
        # Keep connection alive and listen for messages
        while True:
            data = await websocket.receive_json()
            
            # Handle different message types
            if data.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)


if __name__ == "__main__":
    print("🚀 Starting Legrand 3D API Server...")
    print("📍 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
