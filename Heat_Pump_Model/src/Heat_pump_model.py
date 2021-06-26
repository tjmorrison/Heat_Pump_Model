from tespy.networks import Network

nw = Network(fluids=['water', 'NH3'],
             T_unit='C', p_unit='bar', h_unit='kJ / kg', m_unit='kg / s')

from tespy.components import (
    Source, Sink, CycleCloser, Valve, Drum, Pump, Compressor,
    Condenser, HeatExchangerSimple, HeatExchanger)

# sources & sinks

c_in = Source('coolant in')
cons_closer = CycleCloser('consumer cycle closer')

va = Sink('valve')

# consumer system

cd = Condenser('condenser')
rp = Pump('recirculation pump')
cons = HeatExchangerSimple('consumer')

from tespy.connections import Connection, Ref

# consumer system

c_in_cd = Connection(c_in, 'out1', cd, 'in1')

close_rp = Connection(cons_closer, 'out1', rp, 'in1')
rp_cd = Connection(rp, 'out1', cd, 'in2')
cd_cons = Connection(cd, 'out2', cons, 'in1')
cons_close = Connection(cons, 'out1', cons_closer, 'in1')

nw.add_conns(c_in_cd, close_rp, rp_cd, cd_cons, cons_close)

# connection condenser - evaporator system

cd_va = Connection(cd, 'out1', va, 'in1')

nw.add_conns(cd_va)

cd.set_attr(pr1=1, pr2=0.99, ttd_u=5, design=['pr2', 'ttd_u'],
            offdesign=['zeta2', 'kA_char'])
rp.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])
cons.set_attr(pr=0.99, design=['pr'], offdesign=['zeta'])

c_in_cd.set_attr(T=170, fluid={'water': 0, 'NH3': 1})
close_rp.set_attr(T=60, p=10, fluid={'water': 1, 'NH3': 0})
cd_cons.set_attr(T=90)

# %% key parameter

cons.set_attr(Q=-230e3)


nw.solve('design')
nw.print_results()
nw.save('condenser')

cons.set_attr(Q=-200e3)

nw.solve('offdesign', design_path='condenser')
nw.print_results()

# sources & sinks

amb_in = Source('source ambient')
amb_out = Sink('sink ambient')

cp1 = Sink('compressor 1')

# evaporator system

va = Valve('valve')
dr = Drum('drum')
ev = HeatExchanger('evaporator')
su = HeatExchanger('superheater')
pu = Pump('pump evaporator')

# evaporator system

va_dr = Connection(va, 'out1', dr, 'in1')
dr_pu = Connection(dr, 'out1', pu, 'in1')
pu_ev = Connection(pu, 'out1', ev, 'in2')
ev_dr = Connection(ev, 'out2', dr, 'in2')
dr_su = Connection(dr, 'out2', su, 'in2')

nw.add_conns(va_dr, dr_pu, pu_ev, ev_dr, dr_su)

amb_in_su = Connection(amb_in, 'out1', su, 'in1')
su_ev = Connection(su, 'out1', ev, 'in1')
ev_amb_out = Connection(ev, 'out1', amb_out, 'in1')

nw.add_conns(amb_in_su, su_ev, ev_amb_out)

# connection evaporator system - compressor system

su_cp1 = Connection(su, 'out2', cp1, 'in1')

nw.add_conns(su_cp1)

from tespy.tools.characteristics import CharLine
from tespy.tools.characteristics import load_default_char as ldc
# evaporator system

kA_char1 = ldc('heat exchanger', 'kA_char1', 'DEFAULT', CharLine)
kA_char2 = ldc('heat exchanger', 'kA_char2', 'EVAPORATING FLUID', CharLine)

ev.set_attr(pr1=0.99, pr2=0.99, ttd_l=5,
            kA_char1=kA_char1, kA_char2=kA_char2,
            design=['pr1', 'ttd_l'], offdesign=['zeta1', 'kA_char'])
su.set_attr(pr1=0.99, pr2=0.99, ttd_u=2, design=['pr1', 'pr2', 'ttd_u'],
            offdesign=['zeta1', 'zeta2', 'kA_char'])
pu.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])

# evaporator system cold side

pu_ev.set_attr(m=Ref(va_dr, 0.75, 0))
su_cp1.set_attr(state='g')

# evaporator system hot side

amb_in_su.set_attr(T=12, p=1, fluid={'water': 1, 'NH3': 0})
ev_amb_out.set_attr(T=9)

# sources & sinks

ic_in = Source('source intercool')
ic_out = Sink('sink intercool')

cool_closer = CycleCloser('coolant cycle closer')

# compressor-system

cp1 = Compressor('compressor 1')
cp2 = Compressor('compressor 2')
he = HeatExchanger('intercooler')

c_in_cd = Connection(c_in, 'out1', cd, 'in1')

c_in_cd = Connection(cool_closer, 'out1', cd, 'in1')
# compressor-system

cp1_he = Connection(cp1, 'out1', he, 'in1')
he_cp2 = Connection(he, 'out1', cp2, 'in1')
cp2_close = Connection(cp2, 'out1', cool_closer, 'in1')

ic_in_he = Connection(ic_in, 'out1', he, 'in2')
he_ic_out = Connection(he, 'out2', ic_out, 'in1')

nw.add_conns(cp1_he, he_cp2, ic_in_he, he_ic_out, cp2_close)

cp1.set_attr(eta_s=0.8, design=['eta_s'], offdesign=['eta_s_char'])
cp2.set_attr(eta_s=0.8, pr=5, design=['eta_s'], offdesign=['eta_s_char'])
he.set_attr(pr1=0.99, pr2=0.98, design=['pr1', 'pr2'],
            offdesign=['zeta1', 'zeta2', 'kA_char'])

            # condenser system

c_in_cd.set_attr(fluid={'water': 0, 'NH3': 1})

# compressor-system

he_cp2.set_attr(T=40, p0=10)
ic_in_he.set_attr(p=5, T=20, fluid={'water': 1, 'NH3': 0})
he_ic_out.set_attr(T=30, design=['T'])

nw.solve('design', init_path='condenser')
