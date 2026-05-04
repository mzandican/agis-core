import numpy as np
from typing import Dict, List, Tuple

class StateEncoder:
    """Converts raw data streams into statistical state vectors"""
    
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.buffer = []
    
    def add_observation(self, value: float, timestamp: float):
        """Add new data point to buffer"""
        self.buffer.append({
            'timestamp': timestamp,
            'value': value
        })
        # Keep only last N observations
        if len(self.buffer) > self.window_size:
            self.buffer.pop(0)
    
    def encode(self) -> Dict:
        """Transform buffer into state vector"""
        if len(self.buffer) < 3:
            return {
                'mean': 0.0,
                'variance': 0.0,
                'std_dev': 0.0,
                'entropy': 0.0,
                'trend': 0.0,
                'confidence': 0.0
            }
        
        values = np.array([x['value'] for x in self.buffer])
        
        # Basic statistics
        mean = np.mean(values)
        variance = np.var(values)
        std_dev = np.std(values)
        
        # Simple entropy estimate (using variance as proxy)
        entropy = 0.5 * np.log(2 * np.pi * np.e * variance) if variance > 0 else 0.0
        
        # Trend detection (linear regression slope)
        if len(values) > 1:
            x = np.arange(len(values))
            trend = np.polyfit(x, values, 1)[0]
        else:
            trend = 0.0
        
        # Confidence based on sample size
        confidence = min(len(self.buffer) / self.window_size, 1.0)
        
        return {
            'mean': float(mean),
            'variance': float(variance),
            'std_dev': float(std_dev),
            'entropy': float(entropy),
            'trend': float(trend),
            'confidence': float(confidence),
            'sample_size': len(self.buffer)
        }
    
    def reset(self):
        """Clear the buffer"""
        self.buffer = []
