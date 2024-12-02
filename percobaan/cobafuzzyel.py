import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pandas as pd
import matplotlib.pyplot as plt

class CryptocurrencyFuzzySelector:
    def __init__(self):
        # Input variables
        self.risk = ctrl.Antecedent(np.arange(0, 11, 1), 'risk')
        self.return_potential = ctrl.Antecedent(np.arange(0, 101, 1), 'return_potential')
        self.investment_period = ctrl.Antecedent(np.arange(0, 13, 1), 'investment_period')
        
        # Output variable
        self.investment_score = ctrl.Consequent(np.arange(0, 101, 1), 'investment_score')
        
        # Membership functions untuk risk
        self.risk['low'] = fuzz.trimf(self.risk.universe, [0, 0, 4])
        self.risk['medium'] = fuzz.trimf(self.risk.universe, [2, 5, 8])
        self.risk['high'] = fuzz.trimf(self.risk.universe, [6, 10, 10])
        
        # Membership functions untuk return potential
        self.return_potential['low'] = fuzz.trimf(self.return_potential.universe, [0, 0, 30])
        self.return_potential['medium'] = fuzz.trimf(self.return_potential.universe, [20, 50, 80])
        self.return_potential['high'] = fuzz.trimf(self.return_potential.universe, [70, 100, 100])
        
        # Membership functions untuk investment period
        self.investment_period['short'] = fuzz.trimf(self.investment_period.universe, [0, 0, 4])
        self.investment_period['medium'] = fuzz.trimf(self.investment_period.universe, [2, 6, 10])
        self.investment_period['long'] = fuzz.trimf(self.investment_period.universe, [8, 12, 12])
        
        # Membership functions untuk investment score
        self.investment_score['low'] = fuzz.trimf(self.investment_score.universe, [0, 0, 40])
        self.investment_score['medium'] = fuzz.trimf(self.investment_score.universe, [30, 50, 70])
        self.investment_score['high'] = fuzz.trimf(self.investment_score.universe, [60, 100, 100])
        
        # Aturan fuzzy
        rules = [
            ctrl.Rule(self.risk['low'] & self.return_potential['high'] & self.investment_period['short'], self.investment_score['high']),
            ctrl.Rule(self.risk['medium'] & self.return_potential['medium'] & self.investment_period['medium'], self.investment_score['medium']),
            ctrl.Rule(self.risk['high'] & self.return_potential['low'] & self.investment_period['long'], self.investment_score['low']),
            ctrl.Rule(self.risk['low'] & self.return_potential['low'] & self.investment_period['long'], self.investment_score['medium']),
            ctrl.Rule(self.risk['high'] & self.return_potential['high'] & self.investment_period['short'], self.investment_score['medium'])
        ]
        
        self.investment_system = ctrl.ControlSystem(rules)
        self.investment_simulator = ctrl.ControlSystemSimulation(self.investment_system)
    
    def evaluate_cryptocurrency(self, risk, return_potential, investment_period):
        self.investment_simulator.input['risk'] = risk
        self.investment_simulator.input['return_potential'] = return_potential
        self.investment_simulator.input['investment_period'] = investment_period
        
        self.investment_simulator.compute()
        return self.investment_simulator.output['investment_score']
    
    def visualize_membership_functions(self):
        fig, (ax0, ax1, ax2, ax3) = plt.subplots(nrows=4, figsize=(10, 15))
        
        self.risk.view(ax=ax0)
        ax0.set_title('Risk Membership Functions')
        
        self.return_potential.view(ax=ax1)
        ax1.set_title('Return Potential Membership Functions')
        
        self.investment_period.view(ax=ax2)
        ax2.set_title('Investment Period Membership Functions')
        
        self.investment_score.view(ax=ax3)
        ax3.set_title('Investment Score Membership Functions')
        
        plt.tight_layout()
        plt.show()
    
    def analyze_cryptocurrencies(self, cryptocurrencies):
        results = []
        for crypto in cryptocurrencies:
            score = self.evaluate_cryptocurrency(
                crypto['risk'], 
                crypto['return_potential'], 
                crypto['investment_period']
            )
            results.append({
                'name': crypto['name'],
                'investment_score': score
            })
        
        return sorted(results, key=lambda x: x['investment_score'], reverse=True)

# Contoh penggunaan
crypto_selector = CryptocurrencyFuzzySelector()

# Visualisasi fungsi keanggotaan
crypto_selector.visualize_membership_functions()

# Daftar cryptocurrency untuk dievaluasi
cryptocurrencies = [
    {'name': 'Bitcoin', 'risk': 7, 'return_potential': 65, 'investment_period': 6},
    {'name': 'Ethereum', 'risk': 6, 'return_potential': 55, 'investment_period': 5},
    {'name': 'Cardano', 'risk': 4, 'return_potential': 45, 'investment_period': 4},
    {'name': 'Solana', 'risk': 5, 'return_potential': 60, 'investment_period': 3},
    {'name': 'Polkadot', 'risk': 3, 'return_potential': 40, 'investment_period': 5}
]

# Analisis cryptocurrency
results = crypto_selector.analyze_cryptocurrencies(cryptocurrencies)
print("\nHasil Evaluasi Cryptocurrency:")
for result in results:
    print(f"{result['name']}: Skor Investasi = {result['investment_score']:.2f}")