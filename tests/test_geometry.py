import numpy as np
from core.encoder import StateEncoder
from core.geometry import GeometryEngine
from core.drift import DriftDetector

def test_encoder_basic():
    """Test state encoder with simple data"""
    encoder = StateEncoder(window_size=10)
    
    for i in range(15):
        encoder.add_observation(float(i), float(i))
    
    state = encoder.encode()
    
    assert state['sample_size'] == 10  # Window size
    assert state['mean'] > 0
    print("✓ Encoder test passed")

def test_geometry_curvature():
    """Test geometry engine curvature detection"""
    geometry = GeometryEngine()
    
    # Add states with increasing variance
    for i in range(10):
        state = {
            'variance': float(i * 2),
            'mean': 0.0
        }
        geometry.add_state(state)
    
    curvature = geometry.compute_curvature()
    assert curvature >= 0
    print("✓ Geometry curvature test passed")

def test_drift_detection():
    """Test drift detector"""
    drift = DriftDetector(window_size=20)
    
    # Add stable data
    for _ in range(20):
        drift.add_observation(np.random.normal(100, 5))
    
    # Add shifted data
    for _ in range(20):
        drift.add_observation(np.random.normal(150, 5))
    
    drift_score = drift.compute_drift_score()
    assert drift_score > 0.3  # Should detect shift
    print("✓ Drift detection test passed")

if __name__ == "__main__":
    test_encoder_basic()
    test_geometry_curvature()
    test_drift_detection()
    print("\n✅ All tests passed!")
