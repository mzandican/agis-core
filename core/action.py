from typing import Dict, Optional
from .geometry import GeometryEngine
from .drift import DriftDetector

class ActionEngine:
    """Converts geometric state into actionable decisions"""
    
    def __init__(self):
        self.action_history = []
    
    def decide(self, 
               geometry: Dict, 
               drift_score: float,
               state: Dict) -> Dict:
        """
        Main decision logic
        Returns recommended action based on geometric intelligence
        """
        
        action = {
            'recommendation': 'hold',
            'confidence': 0.0,
            'reasoning': '',
            'risk_level': 'medium',
            'timestamp': None
        }
        
        # Extract key metrics
        curvature = geometry.get('curvature', 0.0)
        gradient = geometry.get('gradient_flow', 0.0)
        instability = len(geometry.get('instability_zones', []))
        
        # Decision tree based on geometric signals
        
        # HIGH DRIFT → Stabilize/Reduce Risk
        if drift_score > 0.7:
            action['recommendation'] = 'stabilize'
            action['risk_level'] = 'high'
            action['confidence'] = 1.0 - drift_score
            action['reasoning'] = f'High drift detected ({drift_score:.2f}). Reduce exposure.'
            
        # HIGH CURVATURE + INSTABILITY → Caution
        elif curvature > 0.5 and instability > 2:
            action['recommendation'] = 'caution'
            action['risk_level'] = 'medium-high'
            action['confidence'] = 0.6
            action['reasoning'] = f'High curvature ({curvature:.2f}) with {instability} instability zones.'
            
        # LOW DRIFT + POSITIVE GRADIENT → Explore
        elif drift_score < 0.3 and gradient > 0:
            action['recommendation'] = 'explore'
            action['risk_level'] = 'low'
            action['confidence'] = 0.75
            action['reasoning'] = f'Stable environment with positive trend. Increase exploration.'
            
        # FLAT GEOMETRY → Maintain
        elif curvature < 0.2 and abs(gradient) < 0.1:
            action['recommendation'] = 'hold'
            action['risk_level'] = 'low'
            action['confidence'] = 0.8
            action['reasoning'] = 'Stable flat geometry. Maintain current position.'
            
        # NEGATIVE GRADIENT → Contract
        elif gradient < -0.3:
            action['recommendation'] = 'contract'
            action['risk_level'] = 'medium'
            action['confidence'] = 0.65
            action['reasoning'] = f'Negative gradient flow ({gradient:.2f}). Reduce positions.'
            
        # Default
        else:
            action['recommendation'] = 'monitor'
            action['risk_level'] = 'medium'
            action['confidence'] = 0.5
            action['reasoning'] = 'Mixed signals. Continue monitoring.'
        
        # Add metadata
        action['metrics'] = {
            'drift_score': drift_score,
            'curvature': curvature,
            'gradient': gradient,
            'instability_count': instability,
            'state_confidence': state.get('confidence', 0.0)
        }
        
        self.action_history.append(action)
        
        return action
    
    def get_action_history(self) -> list:
        """Return last 10 actions"""
        return self.action_history[-10:]
