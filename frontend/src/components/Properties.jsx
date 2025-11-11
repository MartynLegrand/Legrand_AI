import React, { useState, useEffect } from 'react'
import './Properties.css'

function Properties({ selectedObject, onUpdateTransform }) {
  const [transform, setTransform] = useState({
    location: [0, 0, 0],
    rotation: [0, 0, 0],
    scale: [1, 1, 1]
  })

  useEffect(() => {
    if (selectedObject) {
      setTransform({
        location: selectedObject.location || [0, 0, 0],
        rotation: selectedObject.rotation || [0, 0, 0],
        scale: selectedObject.scale || [1, 1, 1]
      })
    }
  }, [selectedObject])

  const handleTransformChange = (type, axis, value) => {
    const newTransform = { ...transform }
    const axisIndex = ['x', 'y', 'z'].indexOf(axis)
    newTransform[type][axisIndex] = parseFloat(value)
    setTransform(newTransform)
  }

  const handleApplyTransform = () => {
    if (!selectedObject) return
    onUpdateTransform(selectedObject.name, transform)
  }

  return (
    <div className="properties panel">
      <div className="properties-header">
        <h2>⚙️ Properties</h2>
      </div>

      <div className="properties-content">
        {selectedObject ? (
          <>
            <div className="property-section">
              <h3>Object Info</h3>
              <div className="property-item">
                <label>Name:</label>
                <span className="property-value">{selectedObject.name}</span>
              </div>
              <div className="property-item">
                <label>Type:</label>
                <span className="property-value">{selectedObject.type}</span>
              </div>
            </div>

            <div className="property-section">
              <h3>Transform</h3>
              
              <div className="transform-group">
                <label className="transform-label">Location</label>
                <div className="transform-inputs">
                  <div className="input-group">
                    <span className="axis-label">X</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.location[0]}
                      onChange={(e) => handleTransformChange('location', 'x', e.target.value)}
                    />
                  </div>
                  <div className="input-group">
                    <span className="axis-label">Y</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.location[1]}
                      onChange={(e) => handleTransformChange('location', 'y', e.target.value)}
                    />
                  </div>
                  <div className="input-group">
                    <span className="axis-label">Z</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.location[2]}
                      onChange={(e) => handleTransformChange('location', 'z', e.target.value)}
                    />
                  </div>
                </div>
              </div>

              <div className="transform-group">
                <label className="transform-label">Rotation</label>
                <div className="transform-inputs">
                  <div className="input-group">
                    <span className="axis-label">X</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.rotation[0]}
                      onChange={(e) => handleTransformChange('rotation', 'x', e.target.value)}
                    />
                  </div>
                  <div className="input-group">
                    <span className="axis-label">Y</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.rotation[1]}
                      onChange={(e) => handleTransformChange('rotation', 'y', e.target.value)}
                    />
                  </div>
                  <div className="input-group">
                    <span className="axis-label">Z</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.rotation[2]}
                      onChange={(e) => handleTransformChange('rotation', 'z', e.target.value)}
                    />
                  </div>
                </div>
              </div>

              <div className="transform-group">
                <label className="transform-label">Scale</label>
                <div className="transform-inputs">
                  <div className="input-group">
                    <span className="axis-label">X</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.scale[0]}
                      onChange={(e) => handleTransformChange('scale', 'x', e.target.value)}
                    />
                  </div>
                  <div className="input-group">
                    <span className="axis-label">Y</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.scale[1]}
                      onChange={(e) => handleTransformChange('scale', 'y', e.target.value)}
                    />
                  </div>
                  <div className="input-group">
                    <span className="axis-label">Z</span>
                    <input
                      type="number"
                      step="0.1"
                      className="input"
                      value={transform.scale[2]}
                      onChange={(e) => handleTransformChange('scale', 'z', e.target.value)}
                    />
                  </div>
                </div>
              </div>

              <button 
                className="btn btn-primary apply-button"
                onClick={handleApplyTransform}
              >
                Apply Transform
              </button>
            </div>
          </>
        ) : (
          <div className="empty-properties">
            <span className="empty-icon">📝</span>
            <p>Select an object to view properties</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Properties
