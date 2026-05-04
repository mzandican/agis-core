import numpy as np
from typing import Dict, List
from scipy import stats

class DriftDetector:
    """Detects distribution shifts and model breakdown"""
    
    def __init__(self, window_size: int = 30, threshold: float = 0.05):
        self.window_size = window_size
        self.threshold = threshold
        self.reference_window = []
        self.current_window = []
    
    def add_observation(self, value: float):
        """Add new observation"""
        self.current_window.append(value)
        
        # Maintain window sizes
        if len(self.current_window) > self.window_size:
            self.current_window.pop(0)
        
        # Update reference (older data)
        if len(self.current_window) >= self.window_size // 2:
            if len(self.reference_window) < self.window_size:
                self.reference_window.append(value)
                if len(self.reference_window) > self.window_size:
                    self.reference_window.pop(0)
    
    def compute_kl_divergence(self) -> float:
        """
        Approximate KL divergence between reference and current
        """
        if len(self.reference_window) < 10 or len(self.current_window) < 10:
            return 0.0
        
        # Simple histogram-based KL divergence
        ref_hist, bins = np.histogram(self.reference_window, bins=10, density=True)
        curr_hist, _ = np.histogram(self.current_window, bins=bins, density=True)
        
        # Add small epsilon to avoid log(0)
        epsilon = 1e-10
        ref_hist = ref_hist + epsilon
        curr_hist = curr_hist + epsilon
        
        # Normalize
        ref_hist = ref_hist / np.sum(ref_hist)
        curr_hist = curr_hist / np.sum(curr_hist)
        
        # KL divergence
        kl_div = np.sum(curr_hist * np.log(curr_hist / ref_hist))
        
        return float(max(0, kl_div))  # KL should be non-negative
    
    def compute_drift_score(self) -> float:
        """
        Overall drift score (0.0 to 1.0)
        """
        if len(self.current_window) < 10:
            return 0.0
        
        # Method 1: Statistical test (Kolmogorov-Smirnov)
        if len(self.reference_window) >= 10:
            ks_stat, p_value = stats.ks_2test(
                self.reference_window,
                self.current_window
            )
            drift_ks = 1.0 - p_value
        else:
            drift_ks = 0.0
        
        # Method 2: Mean shift
        if len(self.reference_window) >= 10:
            ref_mean = np.mean(self.reference_window)
            curr_mean = np.mean(self.current_window)
            ref_std = np.std(self.reference_window)
            
            if ref_std > 0:
                mean_shift = abs(curr_mean - ref_mean) / ref_std
                drift_mean = min(mean_shift / 3.0, 1.0)  # Normalize
            else:
                drift_mean = 0.0
        else:
            drift_mean = 0.0
        
        # Combine methods
        drift_score = 0.5 * drift_ks + 0.5 * drift_mean
        
        return float(min(max(drift_score, 0.0), 1.0))
    
    def is_drifting(self) -> bool:
        """Check if drift exceeds threshold"""
        return self.compute_drift_score() > self.threshold
    
    def reset_reference(self):
        """Reset reference window to current"""
        self.reference_window = self.current_window.copy()
        self.current_window = []
