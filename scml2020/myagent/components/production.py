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

class MyProductor(SupplyDrivenProductionStrategy):  
    """
    ProductionStrategy
    SupplyDrivenProductionStrategy
    DemandDrivenProductionStrategy
    TradeDrivenProductionStrategy
    """
    pass