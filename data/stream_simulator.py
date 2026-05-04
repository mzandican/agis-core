import numpy as np
import time
from typing import Dict

class StreamSimulator:
    """Generates realistic data streams with various patterns"""
    
    def __init__(self, pattern: str = 'random_walk'):
        self.pattern = pattern
        self.current_value = 100.0
        self.t = 0
        
    def generate(self) -> Dict:
        """Generate next data point"""
        self.t += 1
        
        if self.pattern == 'random_walk':
            change = np.random.normal(0, 1)
            self.current_value += change
            
        elif self.pattern == 'mean_reverting':
            mean = 100.0
            speed = 0.1
            change = speed * (mean - self.current_value) + np.random.normal(0, 0.5)
            self.current_value += change
            
        elif self.pattern == 'trending':
            trend = 0.05
            change = trend + np.random.normal(0, 0.3)
            self.current_value += change
            
        elif self.pattern == 'volatile':
            volatility = np.abs(np.random.normal(2, 1))
            change = np.random.normal(0, volatility)
            self.current_value += change
            
        elif self.pattern == 'regime_shift':
            # Simulate sudden regime changes
            if np.random.random() < 0.02:  # 2% chance of regime shift
                self.current_value *= np.random.choice([0.9, 1.1])
            change = np.random.normal(0, 1)
            self.current_value += change
        
        else:  # default
            change = np.random.normal(0, 1)
            self.current_value += change
        
        return {
            'timestamp': time.time(),
            'value': float(self.current_value),
            'change': float(change),
            'pattern': self.pattern
        }
    
    def generate_batch(self, n: int = 100) -> list:
        """Generate batch of data points"""
        return [self.generate() for _ in range(n)]
    
    def reset(self, initial_value: float = 100.0):
        """Reset simulator"""
        self.current_value = initial_value
        self.t = 0
