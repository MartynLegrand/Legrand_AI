# 🏗️ Legrand 3D - Technical Architecture

## Overview

Legrand 3D is a modern 3D software that combines a clean, intuitive UI with the power of Blender's core engine. This document provides a deep dive into the technical architecture and design decisions.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Browser                          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Node Editor  │  │ 3D Viewport   │  │  Properties     │  │
│  │  (React)     │  │  (Three.js)   │  │   (React)       │  │
│  └──────┬───────┘  └──────┬────────┘  └────────┬────────┘  │
│         │                 │                     │           │
│         └─────────────────┴─────────────────────┘           │
│                           │                                 │
│                   React State Management                    │
└───────────────────────────┼─────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              │    WebSocket/REST API     │
              └─────────────┬─────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│                     Backend Server                          │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              FastAPI Application                      │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │  REST Routes │  │  WebSocket   │  │  CORS      │ │  │
│  │  └──────┬───────┘  └──────┬───────┘  └────────────┘ │  │
│  └─────────┼──────────────────┼──────────────────────────┘  │
│            │                  │                             │
│  ┌─────────▼──────────────────▼──────────┐                  │
│  │    Blender Core Wrapper (bpy)         │                  │
│  │  ┌───────────────┐  ┌──────────────┐ │                  │
│  │  │ Geometry Ops  │  │  Modifiers   │ │                  │
│  │  └───────────────┘  └──────────────┘ │                  │
│  │  ┌───────────────┐  ┌──────────────┐ │                  │
│  │  │  Transform    │  │  GLB Export  │ │                  │
│  │  └───────────────┘  └──────────────┘ │                  │
│  └──────────────────────────────────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

## Component Deep Dive

### Frontend Components

#### 1. Node Editor Component

**Purpose**: Provides a node-based interface for creating and modifying 3D objects.

**Key Features**:
- Primitive creation (Cube, Sphere, Cylinder, Cone, Torus, Plane)
- Modifier application (Subdivision, Bevel, Array)
- Scene object list
- Parameter controls

**Technologies**:
- React for UI rendering
- CSS Grid for layout
- Event-driven updates

**Data Flow**:
```javascript
User clicks primitive → 
  onCreatePrimitive() → 
    POST /api/primitive → 
      Blender creates object → 
        Export GLB → 
          WebSocket broadcast → 
            UI updates
```

#### 2. Viewport3D Component

**Purpose**: Real-time 3D preview using WebGL.

**Key Features**:
- Three.js scene management
- GLTFLoader for model loading
- OrbitControls for camera interaction
- Grid and axes helpers
- Lighting setup

**Rendering Pipeline**:
```
Initialize Scene →
  Setup Camera & Lights →
    Add Helpers (Grid, Axes) →
      Load GLB Model →
        Render Loop →
          OrbitControls Update →
            Render Scene
```

**Performance Considerations**:
- Reuses Three.js scene
- Removes old models before loading new ones
- Uses requestAnimationFrame for smooth rendering
- OrbitControls damping for smooth camera movement

#### 3. Properties Component

**Purpose**: Display and edit object properties.

**Key Features**:
- Object information display
- Transform controls (Location, Rotation, Scale)
- Apply changes button

**State Management**:
- Local state for transform values
- Sync with selected object
- Apply changes on user action

### Backend Components

#### 1. FastAPI Server (api_server.py)

**Purpose**: HTTP/WebSocket server for handling client requests.

**Endpoints**:
- `GET /api/health`: Health check
- `GET /api/scene`: Get scene information
- `POST /api/scene/clear`: Clear scene
- `POST /api/primitive`: Create primitive
- `POST /api/modifier`: Apply modifier
- `POST /api/transform`: Update transform
- `GET /api/preview/{filename}`: Serve GLB files
- `WS /ws`: WebSocket connection

**WebSocket Manager**:
```python
class ConnectionManager:
    - connect(websocket)      # Accept new connection
    - disconnect(websocket)   # Remove connection
    - broadcast(message)      # Send to all clients
```

**CORS Configuration**:
```python
allow_origins=["http://localhost:3000", "http://localhost:5173"]
allow_methods=["*"]
allow_headers=["*"]
```

#### 2. Blender Core Wrapper (blender_core.py)

**Purpose**: Abstraction layer over Blender Python API.

**Key Methods**:

1. **clear_scene()**
   - Removes all objects
   - Clears mesh data
   - Resets scene state

2. **create_primitive(type, name, location, scale)**
   - Creates primitive objects
   - Supports: cube, sphere, cylinder, cone, torus, plane
   - Sets transform properties

3. **apply_modifier(object_name, modifier_type, params)**
   - Adds modifiers to objects
   - Supports: subdivision, bevel, array
   - Configurable parameters

4. **export_scene(filename)**
   - Exports scene to GLB format
   - Returns file info (path, size, URL)
   - Uses GLTF 2.0 binary format

5. **get_scene_info()**
   - Returns object list
   - Includes transform data
   - Object count

6. **update_object_transform()**
   - Modifies object transforms
   - Supports location, rotation, scale
   - Returns updated values

## Data Flow

### Creating a Primitive Object

```
1. User clicks "Cube" in Node Editor
   ↓
2. NodeEditor.jsx → onCreatePrimitive('cube')
   ↓
3. App.jsx → handleCreatePrimitive('cube')
   ↓
4. axios.post('/api/primitive', { type: 'cube', ... })
   ↓
5. api_server.py → create_primitive()
   ↓
6. blender_core.py → bpy.ops.mesh.primitive_cube_add()
   ↓
7. blender_core.py → export_scene()
   ↓
8. GLB file created in exports/
   ↓
9. WebSocket broadcast: { type: 'primitive_created', data: {...} }
   ↓
10. App.jsx receives WebSocket message
   ↓
11. setPreviewUrl(data.export.url)
   ↓
12. Viewport3D.jsx → GLTFLoader loads model
   ↓
13. Three.js renders model
   ↓
14. User sees 3D object in viewport ✅
```

### Real-Time Updates via WebSocket

```
WebSocket Connection Flow:
1. App.jsx useEffect → new WebSocket('ws://localhost:8000/ws')
2. Server accepts connection
3. Server sends initial scene state
4. Connection stays open

Update Flow:
1. Backend operation completes
2. manager.broadcast({ type: '...', data: {...} })
3. All connected clients receive message
4. Clients update UI accordingly
```

## Technology Stack

### Frontend

| Technology | Purpose | Version |
|------------|---------|---------|
| React | UI Framework | 18.2.0 |
| Three.js | 3D Rendering | 0.159.0 |
| Vite | Build Tool | 5.0.8 |
| Axios | HTTP Client | 1.6.2 |

### Backend

| Technology | Purpose | Version |
|------------|---------|---------|
| FastAPI | API Framework | 0.104.1 |
| Uvicorn | ASGI Server | 0.24.0 |
| Blender (bpy) | 3D Engine | 4.0.0 |
| WebSockets | Real-time Comm | 12.0 |

### DevOps

| Technology | Purpose |
|------------|---------|
| Docker | Containerization |
| Docker Compose | Orchestration |

## File Formats

### GLB (GL Transmission Format Binary)

**Why GLB?**
- Binary format (smaller file size)
- Fast loading
- Supports geometry, materials, textures
- Industry standard
- Three.js native support

**Export Configuration**:
```python
bpy.ops.export_scene.gltf(
    filepath=filepath,
    export_format='GLB',          # Binary format
    export_texcoords=True,        # UV coordinates
    export_normals=True,          # Normal vectors
    export_materials='EXPORT',    # Material data
    export_colors=True,           # Vertex colors
    use_selection=False,          # Export all
    export_cameras=False,         # Skip cameras
    export_lights=False           # Skip lights
)
```

## Performance Considerations

### Frontend Optimization

1. **Three.js Scene Reuse**
   - Single scene instance
   - Reuse renderer and camera
   - Remove old models instead of recreating scene

2. **WebSocket Connection Management**
   - Auto-reconnect on disconnect
   - Connection status indicator
   - Graceful error handling

3. **Efficient State Updates**
   - Minimal re-renders
   - Local state for form inputs
   - Apply changes on user action

### Backend Optimization

1. **Blender Core Instance**
   - Singleton instance
   - Reuse scene
   - Clear instead of recreating

2. **File Caching**
   - Single export file (preview.glb)
   - Overwrite instead of creating new files
   - Cache busting with timestamps

3. **Async Operations**
   - FastAPI async endpoints
   - WebSocket async broadcasting
   - Non-blocking operations

## Security Considerations

1. **CORS Configuration**
   - Whitelist specific origins
   - Development: localhost:3000, localhost:5173
   - Production: Set environment-specific origins

2. **Input Validation**
   - Pydantic models for request validation
   - Type checking
   - Parameter constraints

3. **File Serving**
   - Serve only from exports directory
   - Check file existence
   - Return 404 for missing files

## Future Enhancements

### Phase 2 (Next Steps)

1. **Material System**
   - Material editor UI
   - Texture support
   - PBR materials

2. **Advanced Viewport**
   - Object selection in 3D view
   - Multi-viewport layouts
   - Camera presets

3. **Performance**
   - Web Workers for heavy operations
   - Progressive loading
   - LOD (Level of Detail) system

### Phase 3 (Advanced)

1. **Collaboration**
   - Multi-user editing
   - Change synchronization
   - User presence indicators

2. **Rendering**
   - Cloud rendering
   - Render queue
   - Render presets

3. **Animation**
   - Keyframe animation
   - Timeline editor
   - Animation preview

## Deployment

### Development

```bash
# Backend
cd backend
pip install -r requirements.txt
python bridge/api_server.py

# Frontend
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up -d
```

### Production Considerations

1. **Environment Variables**
   - API URLs
   - CORS origins
   - Database connections

2. **Scaling**
   - Load balancer
   - Multiple backend instances
   - Shared file storage

3. **Monitoring**
   - Logging
   - Error tracking
   - Performance metrics

---

This architecture provides a solid foundation for a modern 3D software application with room for growth and enhancement.
