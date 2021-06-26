# %%
# -*- coding: utf-8 -*-
from tespy.networks import Network
from tespy.components import (
    Sink, Source, Splitter, Compressor, Condenser, Pump, HeatExchangerSimple,
    Valve, Drum, HeatExchanger, CycleCloser
)
from tespy.connections import Connection, Ref
from tespy.tools.characteristics import CharLine
from tespy.tools.characteristics import load_default_char as ldc
from tespy.tools import document_model

import numpy as np
import pandas as pd

# %% network

#set the fluid network and units
nw = Network(
    fluids=['water', 'NH3', 'air'], T_unit='C', p_unit='bar', h_unit='kJ / kg',
    m_unit='kg / s'
)
# %% components

# First argument of the component class is the label (name)

# sources & sinks
cc = CycleCloser('coolant cycle closer') 
cc_cons = CycleCloser('consumer cycle closer')
amb = Source('ambient air')
amb_out1 = Sink('sink ambient 1')
amb_out2 = Sink('sink ambient 2')

# ambient air system
sp = Splitter('splitter')
fan = Compressor('fan')

# consumer system

cd = Condenser('condenser')
dhp = Pump('district heating pump')
cons = HeatExchangerSimple('consumer')

# evaporator system

ves = Valve('valve')
dr = Drum('drum')
ev = HeatExchanger('evaporator')
su = HeatExchanger('superheater')
erp = Pump('evaporator reciculation pump')

# compressor-system

cp1 = Compressor('compressor 1')
cp2 = Compressor('compressor 2')
ic = HeatExchanger('intercooler')
# %%