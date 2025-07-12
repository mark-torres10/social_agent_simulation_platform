import React from 'react'
import styles from './page.module.css'

export default function Home() {
  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>Agent Simulation Platform</h1>
        <p className={styles.description}>
          A research and experimentation tool for simulating social media agents and their interactions
        </p>
        
        <div className={styles.features}>
          <div className={styles.feature}>
            <h3>Configurable Agent-Based Simulation</h3>
            <p>Specify the number of agents and simulation rounds, with support for custom personas and traits.</p>
          </div>
          
          <div className={styles.feature}>
            <h3>Interactive UI</h3>
            <p>Configure simulation parameters, initialize simulations, and view results in real-time.</p>
          </div>
          
          <div className={styles.feature}>
            <h3>Backend Simulation Engine</h3>
            <p>Manages agent initialization, feed generation, sessions, and memory management.</p>
          </div>
          
          <div className={styles.feature}>
            <h3>Results Visualization</h3>
            <p>View simulation results per day and per agent, including profiles, feeds, thoughts, and actions.</p>
          </div>
        </div>
        
        <div className={styles.actions}>
          <button className={styles.primaryButton}>
            Start Simulation
          </button>
          <button className={styles.secondaryButton}>
            View Documentation
          </button>
        </div>
      </div>
    </main>
  )
}