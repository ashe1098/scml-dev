# required for typing
from abc import abstractmethod
from typing import Union, Iterable, List, Optional
import numpy as np

# my need
from scml.scml2020.components.trading import *
from scml.scml2020 import *
from negmas import *
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
import seaborn as sns

class MyTradePredictor(TradePredictionStrategy):  
#     # 継承して利用する際は最初の引数にしないと反映されない(MRO的に)
#     #PredictionBasedTradingStrategyとReactiveAgentでしか使われてない
#     """
#     TradePredictionStrategy
#     *FixedTradePredictionStrategy
#     """
#     # PredictionBasedTradingStrategyで使う．expectedからneededを決める．
#     def trade_prediction_init(self):
#         self.expected_outputs = self.awi.n_lines * np.ones(self.awi.n_steps, dtype=int)
#         self.expected_inputs = self.awi.n_lines * np.ones(self.awi.n_steps, dtype=int)

    def trade_prediction_init(self):
        inp = self.awi.my_input_product

        def adjust(x, demand):
            """Adjust the predicted demand/supply filling it with a default value or repeating as needed"""
            if x is None:
                x = max(1, self.awi.n_lines // 4)  # 元は // 2
            elif isinstance(x, Iterable):
                return np.array(x)
            predicted = int(x) * np.ones(self.awi.n_steps, dtype=int)
            if demand:
                predicted[: inp + 1] = 0
            else:
                predicted[inp - self.awi.n_processes :] = 0
            return predicted

        # adjust predicted demand and supply
        self.expected_outputs = adjust(self.expected_outputs, True)
        self.expected_inputs = adjust(self.expected_inputs, False)


    def trade_prediction_step(self):
        pass

    @property
    def internal_state(self):
        state = super().internal_state
        state.update(
            {
                "expected_inputs": self.expected_inputs,
                "expected_outputs": self.expected_outputs,
                "input_cost": self.input_cost,
                "output_price": self.output_price,
            }
        )
        return state

    def on_contracts_finalized(
        self,
        signed: List[Contract],
        cancelled: List[Contract],
        rejectors: List[List[str]],
    ) -> None:
        super().on_contracts_finalized(signed, cancelled, rejectors)
        if not self._add_trade:
            return
        for contract in signed:
            t, q = contract.agreement["time"], contract.agreement["quantity"]
            if contract.annotation["seller"] == self.id:
                self.expected_outputs[t] += q
            else:
                self.expected_inputs[t] += q


class MyERPredictor(ExecutionRatePredictionStrategy):  
    # 継承して利用する際は最初の引数にしないと反映されない(MRO的に)
    # PredictionBasedTradingStrategyとStepNegotiationManagerでしか使われてない
    """
    ExecutionRatePredictionStrategy
    FixedERPStrategy
    *MeanERPStrategy
    """
    def __init__(self, *args, execution_fraction=0.5, **kwargs):
        super().__init__(*args, **kwargs)
        self._execution_fraction = execution_fraction
        self._total_quantity = None

    def predict_quantity(self, contract: Contract):
        return contract.agreement["quantity"] * self._execution_fraction

    def init(self):
        super().init()
        self._total_quantity = max(1, self.awi.n_steps * self.awi.n_lines // 10)

    @property
    def internal_state(self):
        state = super().internal_state
        state.update({"execution_fraction": self._execution_fraction})
        return state

    def on_contract_executed(self, contract: Contract) -> None:
        super().on_contract_executed(contract)
        old_total = self._total_quantity
        q = contract.agreement["quantity"]
        self._total_quantity += q
        self._execution_fraction = (
            self._execution_fraction * old_total + q
        ) / self._total_quantity

    def on_contract_breached(
        self, contract: Contract, breaches: List[Breach], resolution: Optional[Contract]
    ) -> None:
        super().on_contract_breached(contract, breaches, resolution)
        old_total = self._total_quantity
        q = int(contract.agreement["quantity"] * (1.0 - max(b.level for b in breaches)))
        self._total_quantity += contract.agreement["quantity"]
        self._execution_fraction = (
            self._execution_fraction * old_total + q
        ) / self._total_quantity
