# 🚀 Getting Started with Legrand 3D

This guide will help you get Legrand 3D up and running on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

### For Local Development

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Blender 3.0+** (or bpy module) - [Download Blender](https://www.blender.org/download/)

### For Docker Setup

- **Docker** - [Download Docker](https://www.docker.com/products/docker-desktop)
- **Docker Compose** - Usually comes with Docker Desktop

## Installation Methods

### Method 1: Docker (Easiest - Recommended)

This is the easiest way to get started. Docker will handle all dependencies for you.

1. **Clone the repository**
   ```bash
   git clone https://github.com/MartynLegrand/Legrand_AI.git
   cd Legrand_AI
   ```

2. **Start the application**
   ```bash
   docker-compose up -d
   ```

   This will:
   - Build the backend container with Python, Blender, and all dependencies
   - Start the frontend container with Node.js
   - Set up networking between containers
   - Expose ports 3000 (frontend) and 8000 (backend)

3. **Check the logs** (optional)
   ```bash
   docker-compose logs -f
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

5. **Stop the application**
   ```bash
   docker-compose down
   ```

### Method 2: Local Development

If you prefer to run the application without Docker:

#### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   **Note**: Installing `bpy` (Blender as a Python module) can be tricky. If you encounter issues:
   
   - Option A: Install Blender system-wide and use its Python
   - Option B: Use `pip install bpy==4.0.0` (may require specific system dependencies)
   - Option C: Follow [Blender's official guide](https://wiki.blender.org/wiki/Building_Blender/Other/BlenderAsPyModule)

4. **Run the backend server**
   ```bash
   python bridge/api_server.py
   ```

   You should see:
   ```
   🚀 Starting Legrand 3D API Server...
   📍 Server: http://localhost:8000
   📚 Docs: http://localhost:8000/docs
   🔌 WebSocket: ws://localhost:8000/ws
   ```

#### Frontend Setup

1. **Open a new terminal** and navigate to frontend directory
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

   You should see:
   ```
   VITE v5.0.8  ready in 500 ms
   ➜  Local:   http://localhost:3000/
   ```

4. **Open your browser**
   Navigate to http://localhost:3000

## First Steps

### 1. Verify Connection

When you open the application, you should see:
- A green status indicator in the header showing "Connected"
- The Node Editor panel on the left
- The 3D Viewport in the center
- The Properties panel on the right

### 2. Create Your First Object

1. In the **Node Editor** (left panel), make sure the **Primitives** tab is selected
2. Click on the **Cube** button
3. Watch the 3D Viewport update with your cube!

**What's happening behind the scenes:**
- Frontend sends a request to the backend
- Backend uses Blender to create a cube
- Blender exports the cube as a GLB file
- Frontend loads and displays the GLB in the 3D viewport

### 3. Explore the Viewport

Try these interactions in the 3D Viewport:
- **Rotate**: Left-click and drag
- **Pan**: Right-click and drag
- **Zoom**: Scroll with your mouse wheel

### 4. Apply a Modifier

1. Switch to the **Modifiers** tab in the Node Editor
2. Select your cube from the dropdown (it should be named something like "cube_1234567890")
3. Click on **Subdivision** to smooth out your cube
4. Adjust the **Levels** parameter (default is 2)
5. Click the modifier button again to apply

### 5. Transform Your Object

1. With an object selected, look at the **Properties** panel (right side)
2. Try changing the **Location** values (X, Y, Z)
3. Click **Apply Transform**
4. Watch your object move in the viewport!

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'bpy'`

**Solution**: 
- Make sure Blender is installed
- Try `pip install bpy==4.0.0`
- If that fails, use Blender's built-in Python: `/path/to/blender --background --python bridge/api_server.py`

**Problem**: `Port 8000 is already in use`

**Solution**: 
- Stop any other process using port 8000
- Or change the port in `api_server.py`: `uvicorn.run(app, host="0.0.0.0", port=8001)`

### Frontend Issues

**Problem**: `Failed to connect to WebSocket`

**Solution**:
- Make sure the backend is running on port 8000
- Check the browser console for error messages
- Verify CORS settings in `api_server.py`

**Problem**: `npm install` fails

**Solution**:
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again

**Problem**: Preview not showing

**Solution**:
- Check browser console for errors
- Verify the GLB file was created in `backend/exports/`
- Make sure Three.js dependencies are installed

### Docker Issues

**Problem**: `docker-compose up` fails

**Solution**:
- Make sure Docker is running
- Try `docker-compose down` then `docker-compose up --build`
- Check logs: `docker-compose logs`

**Problem**: Containers are running but can't access the app

**Solution**:
- Check if ports 3000 and 8000 are available
- Try accessing `http://localhost:3000` in an incognito window
- Restart Docker: `docker-compose restart`

## Development Workflow

### Making Changes

1. **Backend changes**: Edit files in `backend/`, the server will need to be restarted
2. **Frontend changes**: Edit files in `frontend/src/`, Vite will hot-reload automatically

### Testing the API

Access the interactive API documentation at http://localhost:8000/docs

You can test all endpoints directly from this interface.

### Debugging

**Backend**:
- Add `print()` statements in Python code
- Check terminal output where `api_server.py` is running

**Frontend**:
- Open browser DevTools (F12)
- Check Console tab for JavaScript errors
- Check Network tab for API requests
- Use React DevTools extension

## Next Steps

Now that you have Legrand 3D running:

1. **Explore all primitives**: Try creating spheres, cylinders, cones, torus, and planes
2. **Experiment with modifiers**: Apply multiple modifiers to the same object
3. **Create complex scenes**: Combine multiple objects
4. **Check the API docs**: Understand the available endpoints
5. **Read the architecture docs**: Learn how everything works together

## Getting Help

- **Documentation**: Check the `docs/` folder for detailed information
- **API Reference**: http://localhost:8000/docs (when running)
- **Issues**: Open an issue on GitHub if you encounter problems

## Contributing

Want to contribute? Great! Here's how:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test thoroughly
5. Commit: `git commit -m "Add my feature"`
6. Push: `git push origin feature/my-feature`
7. Open a Pull Request

---

Happy creating! 🎨✨
