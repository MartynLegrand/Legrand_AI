import React, { useState, useEffect } from 'react'
import NodeEditor from './components/NodeEditor'
import Viewport3D from './components/Viewport3D'
import Properties from './components/Properties'
import Header from './components/Header'
import './App.css'
import axios from 'axios'

function App() {
  const [selectedObject, setSelectedObject] = useState(null)
  const [sceneData, setSceneData] = useState({ objects: [] })
  const [previewUrl, setPreviewUrl] = useState(null)
  const [wsConnected, setWsConnected] = useState(false)

  // WebSocket connection
  useEffect(() => {
    const connectWebSocket = () => {
      const ws = new WebSocket('ws://localhost:8000/ws')

      ws.onopen = () => {
        console.log('✅ WebSocket connected')
        setWsConnected(true)
      }

      ws.onmessage = (event) => {
        const message = JSON.parse(event.data)
        console.log('📨 WebSocket message:', message)

        if (message.type === 'connected') {
          setSceneData(message.data)
        } else if (message.type === 'primitive_created' || 
                   message.type === 'modifier_applied' ||
                   message.type === 'transform_updated') {
          // Reload scene data
          fetchSceneData()
          if (message.data.export) {
            setPreviewUrl(message.data.export.url + '?t=' + Date.now())
          }
        } else if (message.type === 'scene_cleared') {
          setSceneData({ objects: [] })
          setSelectedObject(null)
          setPreviewUrl(null)
        }
      }

      ws.onerror = (error) => {
        console.error('❌ WebSocket error:', error)
        setWsConnected(false)
      }

      ws.onclose = () => {
        console.log('🔌 WebSocket disconnected')
        setWsConnected(false)
        // Attempt to reconnect after 3 seconds
        setTimeout(connectWebSocket, 3000)
      }

      return ws
    }

    const ws = connectWebSocket()

    return () => {
      if (ws) ws.close()
    }
  }, [])

  const fetchSceneData = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/scene')
      if (response.data.status === 'success') {
        setSceneData(response.data)
      }
    } catch (error) {
      console.error('Error fetching scene data:', error)
    }
  }

  const handleCreatePrimitive = async (type) => {
    try {
      const response = await axios.post('http://localhost:8000/api/primitive', {
        type: type,
        name: `${type}_${Date.now()}`,
        location: [0, 0, 0],
        scale: [1, 1, 1]
      })

      if (response.data.status === 'success') {
        console.log('✅ Primitive created:', response.data)
      }
    } catch (error) {
      console.error('Error creating primitive:', error)
    }
  }

  const handleApplyModifier = async (objectName, modifierType, params) => {
    try {
      const response = await axios.post('http://localhost:8000/api/modifier', {
        object_name: objectName,
        modifier_type: modifierType,
        params: params
      })

      if (response.data.status === 'success') {
        console.log('✅ Modifier applied:', response.data)
      }
    } catch (error) {
      console.error('Error applying modifier:', error)
    }
  }

  const handleUpdateTransform = async (objectName, transform) => {
    try {
      const response = await axios.post('http://localhost:8000/api/transform', {
        object_name: objectName,
        ...transform
      })

      if (response.data.status === 'success') {
        console.log('✅ Transform updated:', response.data)
      }
    } catch (error) {
      console.error('Error updating transform:', error)
    }
  }

  const handleClearScene = async () => {
    try {
      await axios.post('http://localhost:8000/api/scene/clear')
    } catch (error) {
      console.error('Error clearing scene:', error)
    }
  }

  return (
    <div className="app">
      <Header 
        wsConnected={wsConnected} 
        onClearScene={handleClearScene}
      />
      <div className="main-content">
        <NodeEditor 
          onCreatePrimitive={handleCreatePrimitive}
          onApplyModifier={handleApplyModifier}
          sceneData={sceneData}
        />
        <Viewport3D 
          previewUrl={previewUrl}
          onSelectObject={setSelectedObject}
        />
        <Properties 
          selectedObject={selectedObject}
          onUpdateTransform={handleUpdateTransform}
        />
      </div>
    </div>
  )
}

export default App
