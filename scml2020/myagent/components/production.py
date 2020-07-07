# required for typing
import numpy as np
from negmas import Contract
from typing import List, Dict, Tuple

from scml.scml2020.common import NO_COMMAND

# my need
from scml.scml2020.components.production import *
from scml.scml2020 import *
from negmas import *
import matplotlib.pyplot as plt
from pprint import pprint
import pandas as pd
import seaborn as sns

class MyProductor(ProductionStrategy):  
    """
    ProductionStrategy
    *SupplyDrivenProductionStrategy  # 買う契約を締結したら，買ったもの全てを作る
    DemandDrivenProductionStrategy  # 売る契約を締結したら，それまでに作る
    TradeDrivenProductionStrategy  # 買う契約と売る契約それぞれに対して，生産ラインを確保しているが，そんなことする必要ある？
    """
    def step(self):
        super().step()
        commands = NO_COMMAND * np.ones(self.awi.n_lines, dtype=int)
        inputs = min(self.awi.state.inventory[self.awi.my_input_product], len(commands))
        commands[:inputs] = self.awi.my_input_product
        commands[inputs:] = NO_COMMAND
        self.awi.set_commands(commands)


    def on_contracts_finalized(
        self: "SCML2020Agent",
        signed: List[Contract],
        cancelled: List[Contract],
        rejectors: List[List[str]],
    ) -> None:
        super().on_contracts_finalized(signed, cancelled, rejectors)
        latest = self.awi.n_steps - 2  # 最悪どこまで遅い生産を許容するか
        earliest_production = self.awi.current_step
        for contract in signed:
            is_seller = contract.annotation["seller"] == self.id
            if is_seller:
                continue
            step = contract.agreement["time"]
            # find the earliest time I can do anything about this contract
            if step > latest + 1 or step < earliest_production:
                continue
            # if I am a buyer, I will schedule production
            input_product = contract.annotation["product"]
            steps, _ = self.awi.schedule_production(
                process=input_product,
                repeats=contract.agreement["quantity"],
                step=(step, latest),
                line=-1,
                method="earliest",
                partial_ok=True,
            )
            self.schedule_range[contract.id] = (
                min(steps) if len(steps) > 0 else -1,
                max(steps) if len(steps) > 0 else -1,
                is_seller,
            )
