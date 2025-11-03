"""
Module pour les simulations de scénarios marketing
"""

import pandas as pd

class ScenarioSimulator:
    def __init__(self):
        self.scenarios = []
    
    def simulate_roi_scenario(self, base_revenue: float, base_cost: float, 
                            revenue_change: float, cost_change: float) -> dict:
        """
        Simule l'impact des changements de revenu et coût sur le ROI
        """
        new_revenue = base_revenue * (1 + revenue_change / 100)
        new_cost = base_cost * (1 + cost_change / 100)
        
        # Calcul ROI original
        original_roi = ((base_revenue - base_cost) / base_cost) * 100
        new_roi = ((new_revenue - new_cost) / new_cost) * 100
        roi_change = new_roi - original_roi
        
        scenario = {
            'scenario_type': 'roi_sensitivity',
            'original_roi': round(original_roi, 2),
            'new_roi': round(new_roi, 2),
            'roi_change': round(roi_change, 2),
            'original_revenue': base_revenue,
            'new_revenue': new_revenue,
            'original_cost': base_cost,
            'new_cost': new_cost,
            'revenue_change_pct': revenue_change,
            'cost_change_pct': cost_change
        }
        
        self.scenarios.append(scenario)
        return scenario