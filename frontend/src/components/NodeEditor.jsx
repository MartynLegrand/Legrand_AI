import React, { useState } from 'react'
import './NodeEditor.css'

const PRIMITIVES = [
  { id: 'cube', name: 'Cube', icon: '⬜' },
  { id: 'sphere', name: 'Sphere', icon: '🔵' },
  { id: 'cylinder', name: 'Cylinder', icon: '🛢️' },
  { id: 'cone', name: 'Cone', icon: '🔺' },
  { id: 'torus', name: 'Torus', icon: '🍩' },
  { id: 'plane', name: 'Plane', icon: '▭' },
]

const MODIFIERS = [
  { id: 'subdivision', name: 'Subdivision', icon: '🔲' },
  { id: 'bevel', name: 'Bevel', icon: '⬡' },
  { id: 'array', name: 'Array', icon: '📊' },
]

function NodeEditor({ onCreatePrimitive, onApplyModifier, sceneData }) {
  const [selectedTab, setSelectedTab] = useState('primitives')
  const [selectedObject, setSelectedObject] = useState(null)
  const [modifierParams, setModifierParams] = useState({})

  const handlePrimitiveClick = (primitiveId) => {
    onCreatePrimitive(primitiveId)
  }

  const handleModifierClick = (modifierId) => {
    if (!selectedObject) {
      alert('Please select an object first')
      return
    }
    onApplyModifier(selectedObject, modifierId, modifierParams)
  }

  return (
    <div className="node-editor panel">
      <div className="node-editor-header">
        <h2>🎨 Node Editor</h2>
        <p className="subtitle">Create and modify 3D objects</p>
      </div>

      <div className="tabs">
        <button 
          className={`tab ${selectedTab === 'primitives' ? 'tab-active' : ''}`}
          onClick={() => setSelectedTab('primitives')}
        >
          Primitives
        </button>
        <button 
          className={`tab ${selectedTab === 'modifiers' ? 'tab-active' : ''}`}
          onClick={() => setSelectedTab('modifiers')}
        >
          Modifiers
        </button>
      </div>

      <div className="tab-content">
        {selectedTab === 'primitives' && (
          <div className="primitives-grid">
            {PRIMITIVES.map((primitive) => (
              <button
                key={primitive.id}
                className="node-button"
                onClick={() => handlePrimitiveClick(primitive.id)}
                title={`Create ${primitive.name}`}
              >
                <span className="node-icon">{primitive.icon}</span>
                <span className="node-name">{primitive.name}</span>
              </button>
            ))}
          </div>
        )}

        {selectedTab === 'modifiers' && (
          <div className="modifiers-section">
            <div className="object-selector">
              <label>Select Object:</label>
              <select 
                value={selectedObject || ''}
                onChange={(e) => setSelectedObject(e.target.value)}
                className="input"
              >
                <option value="">-- Select Object --</option>
                {sceneData.objects?.map((obj) => (
                  <option key={obj.name} value={obj.name}>
                    {obj.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="modifiers-grid">
              {MODIFIERS.map((modifier) => (
                <button
                  key={modifier.id}
                  className="node-button"
                  onClick={() => handleModifierClick(modifier.id)}
                  disabled={!selectedObject}
                  title={`Apply ${modifier.name}`}
                >
                  <span className="node-icon">{modifier.icon}</span>
                  <span className="node-name">{modifier.name}</span>
                </button>
              ))}
            </div>

            {selectedObject && (
              <div className="modifier-params">
                <h3>Parameters</h3>
                <div className="param-group">
                  <label>Levels (Subdivision):</label>
                  <input 
                    type="number" 
                    className="input"
                    defaultValue={2}
                    onChange={(e) => setModifierParams({ ...modifierParams, levels: parseInt(e.target.value) })}
                  />
                </div>
                <div className="param-group">
                  <label>Width (Bevel):</label>
                  <input 
                    type="number" 
                    className="input"
                    step="0.1"
                    defaultValue={0.1}
                    onChange={(e) => setModifierParams({ ...modifierParams, width: parseFloat(e.target.value) })}
                  />
                </div>
                <div className="param-group">
                  <label>Count (Array):</label>
                  <input 
                    type="number" 
                    className="input"
                    defaultValue={3}
                    onChange={(e) => setModifierParams({ ...modifierParams, count: parseInt(e.target.value) })}
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <div className="scene-objects">
        <h3>Scene Objects ({sceneData.object_count || 0})</h3>
        <div className="objects-list">
          {sceneData.objects?.map((obj) => (
            <div key={obj.name} className="object-item">
              <span className="object-type">{obj.type}</span>
              <span className="object-name">{obj.name}</span>
            </div>
          ))}
          {(!sceneData.objects || sceneData.objects.length === 0) && (
            <p className="empty-state">No objects in scene</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default NodeEditor
