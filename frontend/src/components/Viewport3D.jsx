import React, { useEffect, useRef, useState } from 'react'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import './Viewport3D.css'

function Viewport3D({ previewUrl, onSelectObject }) {
  const containerRef = useRef(null)
  const sceneRef = useRef(null)
  const rendererRef = useRef(null)
  const cameraRef = useRef(null)
  const controlsRef = useRef(null)
  const loadedModelRef = useRef(null)
  const [isLoading, setIsLoading] = useState(false)

  // Initialize Three.js scene
  useEffect(() => {
    if (!containerRef.current) return

    // Create scene
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0x1a1a1a)
    sceneRef.current = scene

    // Create camera
    const camera = new THREE.PerspectiveCamera(
      75,
      containerRef.current.clientWidth / containerRef.current.clientHeight,
      0.1,
      1000
    )
    camera.position.set(5, 5, 5)
    camera.lookAt(0, 0, 0)
    cameraRef.current = camera

    // Create renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(containerRef.current.clientWidth, containerRef.current.clientHeight)
    renderer.setPixelRatio(window.devicePixelRatio)
    containerRef.current.appendChild(renderer.domElement)
    rendererRef.current = renderer

    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(10, 10, 10)
    scene.add(directionalLight)

    // Add grid helper
    const gridHelper = new THREE.GridHelper(10, 10, 0x444444, 0x222222)
    scene.add(gridHelper)

    // Add axes helper
    const axesHelper = new THREE.AxesHelper(5)
    scene.add(axesHelper)

    // Add orbit controls
    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true
    controls.dampingFactor = 0.05
    controlsRef.current = controls

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate)
      controls.update()
      renderer.render(scene, camera)
    }
    animate()

    // Handle window resize
    const handleResize = () => {
      if (!containerRef.current) return
      const width = containerRef.current.clientWidth
      const height = containerRef.current.clientHeight
      camera.aspect = width / height
      camera.updateProjectionMatrix()
      renderer.setSize(width, height)
    }
    window.addEventListener('resize', handleResize)

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
      if (containerRef.current && renderer.domElement) {
        containerRef.current.removeChild(renderer.domElement)
      }
      renderer.dispose()
    }
  }, [])

  // Load GLB model when preview URL changes
  useEffect(() => {
    if (!previewUrl || !sceneRef.current) return

    setIsLoading(true)

    // Remove previous model
    if (loadedModelRef.current) {
      sceneRef.current.remove(loadedModelRef.current)
      loadedModelRef.current = null
    }

    // Load new model
    const loader = new GLTFLoader()
    loader.load(
      `http://localhost:8000${previewUrl}`,
      (gltf) => {
        const model = gltf.scene
        sceneRef.current.add(model)
        loadedModelRef.current = model

        // Center the model
        const box = new THREE.Box3().setFromObject(model)
        const center = box.getCenter(new THREE.Vector3())
        model.position.sub(center)

        setIsLoading(false)
        console.log('✅ Model loaded successfully')
      },
      (progress) => {
        const percent = (progress.loaded / progress.total) * 100
        console.log(`Loading: ${percent.toFixed(0)}%`)
      },
      (error) => {
        console.error('❌ Error loading model:', error)
        setIsLoading(false)
      }
    )
  }, [previewUrl])

  return (
    <div className="viewport-3d panel">
      <div className="viewport-header">
        <h2>🎬 3D Viewport</h2>
        {isLoading && <span className="loading-indicator">Loading...</span>}
      </div>
      <div className="viewport-container" ref={containerRef}>
        {!previewUrl && (
          <div className="viewport-placeholder">
            <div className="placeholder-content">
              <span className="placeholder-icon">🎨</span>
              <h3>Welcome to Legrand 3D</h3>
              <p>Create a primitive object to see the preview</p>
            </div>
          </div>
        )}
      </div>
      <div className="viewport-controls">
        <div className="control-hint">
          <span>🖱️ Left click + drag: Rotate</span>
          <span>🖱️ Right click + drag: Pan</span>
          <span>🖱️ Scroll: Zoom</span>
        </div>
      </div>
    </div>
  )
}

export default Viewport3D
