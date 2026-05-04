import numpy as np
from typing import Dict, List

class GeometryEngine:
    """Approximates geometric structure from statistical states"""
    
    def __init__(self):
        self.state_history = []
        self.max_history = 50
    
    def add_state(self, state: Dict):
        """Add encoded state to history"""
        self.state_history.append(state)
        if len(self.state_history) > self.max_history:
            self.state_history.pop(0)
    
    def compute_curvature(self) -> float:
        """
        Estimate curvature from variance changes
        High curvature = rapid change in uncertainty
        """
        if len(self.state_history) < 5:
            return 0.0
        
        variances = [s['variance'] for s in self.state_history]
        
        # Second derivative (acceleration of variance)
        first_diff = np.diff(variances)
        if len(first_diff) < 2:
            return 0.0
        
        curvature = np.std(first_diff)
        return float(curvature)
    
    def compute_gradient_flow(self) -> float:
        """
        Direction and magnitude of uncertainty change
        """
        if len(self.state_history) < 3:
            return 0.0
        
        variances = [s['variance'] for s in self.state_history]
        
        # Linear trend
        x = np.arange(len(variances))
        slope = np.polyfit(x, variances, 1)[0]
        
        return float(slope)
    
    def detect_instability_zones(self, threshold: float = 0.5) -> List[int]:
        """
        Identify regions of high geometric instability
        Returns indices of unstable states
        """
        if len(self.state_history) < 5:
            return []
        
        variances = [s['variance'] for s in self.state_history]
        rolling_std = []
        
        for i in range(4, len(variances)):
            window = variances[i-4:i+1]
            rolling_std.append(np.std(window))
        
        # Find spikes
        threshold_val = np.mean(rolling_std) + threshold * np.std(rolling_std)
        unstable_indices = [i for i, val in enumerate(rolling_std) if val > threshold_val]
        
        return unstable_indices
    
    def get_geometry_summary(self) -> Dict:
        """Complete geometric description"""
        return {
            'curvature': self.compute_curvature(),
            'gradient_flow': self.compute_gradient_flow(),
            'instability_zones': self.detect_instability_zones(),
            'state_count': len(self.state_history),
            'avg_variance': np.mean([s['variance'] for s in self.state_history]) if self.state_history else 0.0
      }
