'''
R744 Refrigeration calculations
written by Travis Morrison \\
Email: tjmorrison635@gmail.com \\
In collaboration with Ryan H. Lewis me@ryanlewis.net

-----------------------------------------------------------------------------------------------------------------------
Goal: Understand the feasibility of using R744 in a heat pump to effectively heat and cool a home with an existing hot
 water system. To perform these calculations we will assume the following:

    *   That the heating/cooling system is a large reservoir with home heat exchanger between the heat pump and the reservoir.
        #TODO: Can you please comment here what are the stages as it related to the physical setup?
    *   For heating we will need to heat the water to 82 $^{\circ}$C (180 $^{\circ}$F), for the extreme cold case,
        say -12.2 $^{\circ}$C (10 $^{\circ}$F)
    *   For cooling we will need to cool the water to  5 $^{\circ}$C (45 $^{\circ}$F) for the extreme hot case,
        say 43 $^{\circ}$C (110 $^{\circ}$F)
    *   The physical effect of the tubing used to carry
        the refrigerant around the enclosure is ignored.
    *   For now we only will exam a single stage system
'''
#======================================================================================================================
import CoolProp.CoolProp as CP

import CoolProp.Plots as CPP
#======================================================================================================================

Refrigerant1= 'R410A' 
Refrigerant2= 'R744'
#TODO: Add more constants here from the hardcoded constants below..

pressure_at_critical_point = CP.PropsSI(Refrigerant2,'pcrit') #Get the critical point presure

#Apply this flag to switch our calculation from heating to cooling--doesnt work yet...
cool_coeff = {'cooling': 1, 'heating': -1}

# Useful Functions
def c2K(Temp):
    #Function to convert celsius to Kelvin
    TempK = Temp + 273.15
    return TempK
def K2c(Temp):
    #Function to convert celsius to Kelvin
    Tempc = Temp - 273.15
    return Tempc
def c2F(Temp):
    #Function to convert celsius to Fahrenheit
    TempF = (Temp*(9/5)) + 32
    return TempF
def K2F(Temp):
    #Function to convert Kelvin to Fahrenheit
    TempF = ((Temp-273.15)*(9/5)) + 32
    return TempF

# Stage modeling for R744 ~likely will be our second stage
#============================================= STATE 1 =================================================================
# Initial state, say vapor  at 3.75e6 Pa. This assuption comes from the P-H diagram for R744
H1 = 450e3 # [J/kg]  remember that enthalpy is the internal energy per unit plus  the product of the temperature*volume
P1 = 3.75e6 # [Pa] 
T1 = CP.PropsSI('T','H',H1,'P',P1, Refrigerant2) # Find the Temperature at Stage 1
print("The temperature at state 1 is: ", K2c(T1), " Deg C, or ",  K2F(T1), " Deg F")
print("The state at state 1 is: ", CP.PhaseSI('T',T1,'P',P1,Refrigerant2)) # it should be a gas

#=========================================== STATE 1 to 2 =================================================================
#State 2 takes our initial ref and compresses it
Compressor_power = 50 # J/s/kKg or W/Kg ~ just taken from sample P-H diagram for now
Compressor_eff_power = 0.78*Compressor_power # Assume %78 efficiency after mechanical and hydraulic losses ~seems common across applications
Work_in = Compressor_eff_power # Here we assume an adiabatic process so no heat loss from the compressor- Will need to account for in the future
H2 = H1 + Work_in # Since our process is adabatic the change in ethalpy is just the intial enthalpy plus the work from the compressor
P2 = 10e6 #[Pa] This will depend on our compressor, but a first guess
T2 = CP.PropsSI('T','H',H2,'P',P2,Refrigerant2) 
print("The enthalpy at state 2 is: ", H2, "J/kg")
print("The temperature at state 2 is: ", T2, "J/kg")
print("The phase at state 2 is: ", CP.PhaseSI('T',T2,'P',P2,Refrigerant2)) #here super crit means >Pcrit and >Tcrit
#========================================== STATE 2 to 3 ===============================================================
#Calculate the effective heat transfer at the condenser
H3 = 325000 #J/Kg
Q_2_3 = -(H3-H2) #since there is no work on the gas, just change of state
P3 = P2 # Since this process is isobaric
T3 = CP.PropsSI('T','H',H3,'P',P3,Refrigerant2) #TODO: Shouldn't this be Refrigerant1?
print("The heat removed from the system from the condenser:", Q_2_3,"J/kg")
print("The temperature at state 3 is: ", T3, "K")
print("The phase at state 3 is: ", CP.PhaseSI('T',T3,'P',P3,Refrigerant2)) #here super crit means >Pcrit and >Tcrit

# Another way to wonder about this is from estimating the heat transfer from
Conds_Heat_trans_coeff = 300 #[W/m^2K] For high pressure  https://www.engineersedge.com/thermodynamics/overall_heat_transfer-table.htm
# Where do these constants come from?
T_outside = 30 +273.15#54.4 +273.15 # deg K extreme heat case for outside
Q_2_3_V2 = Conds_Heat_trans_coeff*(T2-T_outside) #W/m^2 Heat expelled from condenser
H3_V2 = H2-Q_2_3_V2
T3_V2 = CP.PropsSI('T','H',H3_V2,'P',P3,Refrigerant2)
print("The effective temperature at the condenser is: ", T3_V2, "deg C")
print("The final enthalpy state is: ", H3_V2, "deg C")
print("The phase at state 3 is: ", CP.PhaseSI('T',T3_V2,'P',P3,Refrigerant2)) #here super crit means >Pcrit and >Tcrit
#========================================== STATE 3 to 4 ===============================================================