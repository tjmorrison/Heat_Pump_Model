'''
R744 Refigeration calculations
written by Travis Morrison \\
Email: tjmorrison635@gmail.com \\
In collaboration with RyanL Lewis

-----------------------------------------------------------------------------------------------------------------------
Goal: Understand the feasibility of using R744 in a heat pump to effectively heat and cool a home with an existing hot
 water system. To perform these calculations we will assume the following:

        This needs refinement
    *   That the heating/cooling system is a large reservoir with home heat exchanger between the heat pump and the resivor.
    *
    *   For heating we will need to heat the water to 54.4 $^{\circ}$C (130 $^{\circ}$F), for the extreme cold case,
        say -12.2 $^{\circ}$C (10 $^{\circ}$F)
    *   For cooling we will need to cool the water to  7.2 $^{\circ}$C (45 $^{\circ}$F) for the extreme hot case,
        say 35 $^{\circ}$C (95 $^{\circ}$F)
    *   The physical effect of the tubing used to carry
        the refrigerant around the enclosure is ignored.
    *   For now we only will exam a single stage system
'''
#======================================================================================================================
import CoolProp.CoolProp as CP
import CoolProp.Plots as CPP
#======================================================================================================================
Refrigerant = 'R744' # Set the refrigerant
pressure_at_critical_point = CP.PropsSI(Refrigerant, 'pcrit') # Get the critical point pressure

# We'll want to test the feasibility in both cooling and heating
# doesnt work yet...
Heat_pump_direction = 'cooling'
if Heat_pump_direction == 'cooling':
    cool_coeff = 1
else:
    cool_coeff = -1
# ============================================= STATE 1 ================================================================
# Initial state, say vapor at 10 deg C
P1 = 3.75e6 # [Pa], note this is about 3x 1 atm
T1 = 10     # [Deg C]
H1 = CP.PropsSI('H', 'T', T1 + 273.15, 'P', P1 , Refrigerant) # remember that enthalpy is the internal energy per unit
                                                              # plus the product of the temperature*volume
print("The enthalpy at state 1 is: ", H1, "J/kg")
print("The phase at state 1 is: ", CP.PhaseSI('T', T1 + 273.15, 'P', P1, Refrigerant)) # state needs to be gas
# =========================================== STATE 1 to 2 =============================================================
# State 2 takes our initial ref and compresses it
Compressor_power = 50 # J/s/kKg or W/Kg ~ just taken from sample P-H diagram for now
Compressor_eff_power = 0.78*Compressor_power # Assumes %78 efficiency after mechanical and hydraulic losses
Work_in = Compressor_eff_power # Here we assume an adiabatic process so no heat loss from the compressor
H2 = H1 + Work_in
P2 = 10e6 # Pa from P-H diagram
T2 = CP.PropsSI('T', 'H', H2, 'P', P2, Refrigerant)
print("The enthalpy at state 2 is: ", H2, "J/kg")
print("The temperature at state 2 is: ", T2, "J/kg")
print("The phase at state 2 is: ", CP.PhaseSI('T', T2, 'P', P2, Refrigerant)) # here super crit means >Pcrit and >Tcrit
# ========================================== STATE 2 to 3 ==============================================================
# Calculate the effective heat transfer at the condenser
H3 = 325000 # J/Kg
Q_2_3 = -(H3-H2) # since there is no work on the gas, just change of state
P3 = P2 # Since this process is isobaric
T3 = CP.PropsSI('T', 'H', H3, 'P', P3, Refrigerant)
print("The heat removed from the system from the condenser:", Q_2_3,"J/kg")
print("The temperature at state 3 is: ", T3, "K")
print("The phase at state 3 is: ", CP.PhaseSI('T', T3, 'P', P3, Refrigerant)) # here supercrit means >Pcrit and >Tcrit

# Another way to wonder about this is from estimating the heat transfer from,
# Note: That if T3 doesnt equal T3_V2, the cycle will not work
Conds_Heat_trans_coeff = 300 # [W/m^2K] For high pressure
# https://www.engineersedge.com/thermodynamics/overall_heat_transfer-table.htm
T_outside = 54.4 + 273.15 # deg K extreme heat case for outside
Q_2_3_V2 = Conds_Heat_trans_coeff*(T2-T_outside) # W/m^2 Heat expelled from condenser
H3_V2 = H2-Q_2_3_V2
T3_V2 = CP.PropsSI('T', 'H', H3_V2, 'P', P3, Refrigerant)
print("The effective temperature at the condenser is: ", T3_V2, "deg C")
print("The final enthalpy state is: ", H3_V2, "deg C")
print("The phase at state 3 is: ", CP.PhaseSI('T', T3_V2, 'P', P3, Refrigerant)) # here super crit means >Pcrit and > Tcrit
# ========================================== STATE 3 to 4 ==============================================================
# Here we are going to go through the expansion valve, but note that the R744 cycle doesn't use an expansion value- see
# textbook
