from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import time

from data.stream_simulator import StreamSimulator
from core.encoder import StateEncoder
from core.geometry import GeometryEngine
from core.drift import DriftDetector
from core.action import ActionEngine

app = FastAPI(
    title="AGIS Core",
    description="Adaptive Geometric Intelligence System",
    version="0.1.0"
)

simulator = StreamSimulator(pattern='random_walk')
encoder = StateEncoder(window_size=20)
geometry = GeometryEngine()
drift = DriftDetector(window_size=30)
action_engine = ActionEngine()

class DataPoint(BaseModel):
    value: float
    timestamp: Optional[float] = None

@app.get("/")
def root():
    return {
        "system": "AGIS Core",
        "status": "running",
        "version": "0.1.0"
    }

@app.post("/ingest")
def ingest_data( DataPoint):
    timestamp = data.timestamp or time.time()
    encoder.add_observation(data.value, timestamp)
    drift.add_observation(data.value)
    return {
        "status": "ingested",
        "value": data.value,
        "timestamp": timestamp
    }

@app.get("/state")
def get_state():
    state = encoder.encode()
    return state
@app.get("/geometry")
def get_geometry():
    current_state = encoder.encode()
    geometry.add_state(current_state)
    return geometry.get_geometry_summary()

@app.get("/drift")
def get_drift():
    return {
        "drift_score": drift.compute_drift_score(),
        "is_drifting": drift.is_drifting(),
        "kl_divergence": drift.compute_kl_divergence()
    }

@app.get("/action")
def get_action():
    current_state = encoder.encode()
    geometry.add_state(current_state)
    drift_score = drift.compute_drift_score()
    geom_summary = geometry.get_geometry_summary()
    recommendation = action_engine.decide(
        geometry=geom_summary,
        drift_score=drift_score,
        state=current_state
    )
    return recommendation

@app.get("/simulate/{n}")
def simulate_stream(n: int = 10):
    for _ in range(n):
        data = simulator.generate()
        encoder.add_observation(data['value'], data['timestamp'])
        drift.add_observation(data['value'])
    
    state = encoder.encode()
    geometry.add_state(state)
    geom_summary = geometry.get_geometry_summary()
    drift_score = drift.compute_drift_score()
    action = action_engine.decide(geom_summary, drift_score, state)
    
    return {
        "final_value": simulator.current_value,
        "state": state,
        "geometry": geom_summary,
        "drift": drift_score,
        "action": action
    }

@app.post("/reset")def reset_system():
    encoder.reset()
    simulator.reset()
    return {"status": "reset complete"}
