"""
Module pour la conversion entre différentes métriques marketing
"""

class MetricConverter:
    def __init__(self):
        self.conversion_history = []
    
    def cpc_to_cpm(self, cpc: float, ctr: float) -> dict:
        """
        Convertit CPC en CPM
        
        Args:
            cpc (float): Coût par clic
            ctr (float): Click-Through Rate (en pourcentage)
            
        Returns:
            dict: Résultats de conversion
        """
        try:
            # Conversion: CPM = CPC * CTR * 1000
            ctr_decimal = ctr / 100
            cpm = cpc * ctr_decimal * 1000
            
            result = {
                'cpc': cpc,
                'ctr': ctr,
                'cpm': round(cpm, 2),
                'conversion_type': 'cpc_to_cpm'
            }
            
            self.conversion_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f'Erreur de conversion: {str(e)}'}
    
    def cpm_to_cpc(self, cpm: float, ctr: float) -> dict:
        """
        Convertit CPM en CPC
        """
        try:
            ctr_decimal = ctr / 100
            cpc = cpm / (ctr_decimal * 1000)
            
            result = {
                'cpm': cpm,
                'ctr': ctr,
                'cpc': round(cpc, 2),
                'conversion_type': 'cpm_to_cpc'
            }
            
            self.conversion_history.append(result)
            return result
            
        except ZeroDivisionError:
            return {'error': 'CTR ne peut pas être zéro'}
        except Exception as e:
            return {'error': f'Erreur de conversion: {str(e)}'}
    
    def cpa_to_cpc(self, cpa: float, conversion_rate: float) -> dict:
        """
        Convertit CPA en CPC
        """
        try:
            conversion_rate_decimal = conversion_rate / 100
            cpc = cpa * conversion_rate_decimal
            
            result = {
                'cpa': cpa,
                'conversion_rate': conversion_rate,
                'cpc': round(cpc, 2),
                'conversion_type': 'cpa_to_cpc'
            }
            
            self.conversion_history.append(result)
            return result
            
        except Exception as e:
            return {'error': f'Erreur de conversion: {str(e)}'}