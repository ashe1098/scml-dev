# required for typing
from typing import List, Optional, Dict, Any
import numpy as np
from negmas import (
    Issue, AgentMechanismInterface, Contract, Negotiator,
    MechanismState, Breach,
)

# my need
from scml.scml2020 import *
from negmas import *
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
import seaborn as sns

# class MyPredictor(MeanERPStrategy):  
#     # 継承して利用する際は最初の引数にしないと反映されない(MRO的に)
#     #PredictionBasedTradingStrategかReactiveAgentでしか使われてない
#     #かと思ったらStepNegotiationManagerでも継承されてる
#     """
#     TradePredictionStrategy
#     FixedTradePredictionStrategy
#     ExecutionRatePredictionStrategy
#     FixedERPStrategy
#     MeanERPStrategy
#     """
#     # PredictionBasedTradingStrategyで使う．expectedからneededを決める．
#     # (PredictionBasedTradingStrategyのsuper().init()で連鎖的に呼び出されてる
#     def trade_prediction_init(self):
#         self.expected_outputs = self.awi.n_lines * np.ones(self.awi.n_steps, dtype=int)
#         self.expected_inputs = self.awi.n_lines * np.ones(self.awi.n_steps, dtype=int)

class MyNegotiationManager(StepNegotiationManager):
    """
    NegotiationManager
    StepNegotiationManager
    IndependentNegotiationsManager
    MovingRangeNegotiationManager
    """
    def target_quantity(self, step: int, sell: bool) -> int:
        """A fixed target quantity of half my production capacity"""
        return self.awi.n_lines // 2

    def acceptable_unit_price(self, step: int, sell: bool) -> int:
        """The catalog price seems OK"""
        return self.awi.catalog_prices[self.awi.my_output_product] if sell else self.awi.catalog_prices[self.awi.my_input_product]

    def create_ufun(self, is_seller: bool, issues=None, outcomes=None):
        """A utility function that penalizes high cost and late delivery for buying and and awards them for selling"""
        if is_seller:
            return LinearUtilityFunction((0, 0.25, 1))
        return LinearUtilityFunction((0, -0.5, -0.8))
