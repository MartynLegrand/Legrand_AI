import React from 'react'
import './Header.css'

function Header({ wsConnected, onClearScene }) {
  return (
    <header className="header">
      <div className="header-left">
        <h1 className="logo">⚡ Legrand 3D</h1>
        <span className="version">v1.0.0 MVP</span>
      </div>
      <div className="header-center">
        <span className="status">
          <span className={`status-indicator ${wsConnected ? 'status-connected' : 'status-disconnected'}`}></span>
          {wsConnected ? 'Connected' : 'Disconnected'}
        </span>
      </div>
      <div className="header-right">
        <button className="btn btn-secondary" onClick={onClearScene}>
          🗑️ Clear Scene
        </button>
      </div>
    </header>
  )
}

export default Header
