from pileup_ddd.dislocation import Dislocation, SlipPlanes
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import json
import sys

PARAM={
    # number of dislocations in the speciment
    'number of dislocation' : 8, 

    # factor of bulk modulus
    'G' : 8.48e10, 

    #scale of burgers vector
    'burgers vector' : 2.54e-10 ,

    # length of simulation specimen
    'length of specimen' : 78,

    # poissons ratio
    'poissons ratio' : 2.5e-1,

    # mobility factor
    'B' : 1e-4, 

    # time step
    'delta time step' :1e-15,

    #number of time step 
    'number of steps' : 250000, # n time step

    #external force
    'external force' : -1e08 # external force
}

def main():
    save_data = sys.argv[1]
    n = PARAM['number of dislocation']
    G0 = PARAM['G'] 
    b0 = PARAM['burgers vector'] 
    B0 = PARAM['B']
    tau_ext_0=PARAM['external force']
    nu = PARAM['poissons ratio']
    L = PARAM['length of specimen']
    dt = PARAM['delta time step']
    n_steps = PARAM['number of steps'] 

    G = 1.0
    b = 1 
    L = 78*b


    stress_0 = G/(2*np.pi*(1-nu))
    B = B0/G0 
    tau_ext = -tau_ext_0/G0 # external force    

    x_0, y_0 = 0, 0
    x_1, y_1 = L, 1
    slip_plane_length = x_1 - x_0
    slip_system = []
    n_slip_planes_slip_system = 1
    lattice_constant = abs(y_1-y_0)/n_slip_planes_slip_system
    n_dislocation_on_slip_system = [n]
    dislocations = []
    initial_pos = []

    for sp_i in range(n_slip_planes_slip_system): 
        delta_y = sp_i*lattice_constant
        sp = SlipPlanes(id=sp_i, x=x_0, y=y_0+delta_y, length=slip_plane_length, angle=0)
        for dis_i in range(n_dislocation_on_slip_system[sp_i]):
            b=1
            x_local = np.random.rand() * slip_plane_length
            dis = Dislocation(id=dis_i, x_loc=x_local,b=b, sp_id=sp_i, fx=0.0, f_ext=tau_ext)
            dislocations.append(dis)
            initial_pos.append((x_local, y_0+delta_y))
        slip_system.append(sp)

    for i in tqdm(range(n_steps)):
        #force zero
        for dis in dislocations:
            dis.fx = 0
    
        for i, dislocation in enumerate(dislocations):
            while i < len(dislocations)-1:
                dislocation.computeForce(
                    dislocations[i+1],
                    slip_system=slip_system, 
                    D=slip_plane_length,
                    stress_0=stress_0)
                i+=1
        
            dislocation.imgForcePileUp(slip_system=slip_system, stress_0=stress_0)

        # move dislocation 
        for dislocation in dislocations:
            dislocation.moveDislocation(D=slip_plane_length, B=B, dt=dt) 

    ## returning the data into 2D-DDD schema

    # # with open('/Users/ihsan/Documents/PhD_Work/2020/HMC/pilot_project/PILEUP-DDD/examples/schema/schema.json', 'r') as f: 
    #     data = json.load(f)
    
    system_description=dict.fromkeys([
        'Delta time step', 'Number of simulation step', 'Number of dislocation', 'Geometry', 
        'Material properties', 'Loading condition', 'Slip system', 'Dislocations'
    ])

    geometry = dict.fromkeys(['Point 1', 'Point 2'])
    geometry.update({'Point 1': (x_0, y_0), 'Point 2': (x_1, y_1)})


    mat_props= dict.fromkeys(['Mobility', 'Poissons ratio', 'Bulk modulus'])
    mat_props_mobility = {'unit': '', 'value': B0}
    mat_props_poiss_ratio = {'unit': '', 'value': nu}
    mat_props_bulk_mod = {'unit': 'Pascal', 'value':G0}

    mat_props.update({'Mobility':mat_props_mobility, 'Poissons ratio':mat_props_poiss_ratio, 'Bulk modulus':mat_props_bulk_mod})

    loading_condition = dict.fromkeys(['External force'])
    loading_condition_ext_force = {'unit': 'Newton', 'value': tau_ext_0}

    loading_condition.update({'External force': loading_condition_ext_force})

    slip_system_dict = dict.fromkeys(['Number of slip plane', 'Slip plane'])
    slip_plane_list = []

    for sp in slip_system: 
        slip_plane_dict = dict.fromkeys(['id', 'length', 'angle', 'r0'])
        slip_plane_dict.update({'id':sp.id, 'length':slip_plane_length, 'angle': sp.angle, 'r0':(sp.x, sp.y)})
        slip_plane_list.append(slip_plane_dict)
    slip_system_dict.update({'Number of slip plane': n_slip_planes_slip_system, 'Slip plane': slip_plane_list})

    dislocations_dict=dict.fromkeys(['dislocations'])
    
    dislocation_list= list()

    for dislocation in dislocations:
        dislocation_data_burgers_vector={'unit':'meter', 'value':b0}
        dislocation_data_force = {'unit':'Newton', 'value':dislocation.fx}

        dislocation_data = {'id' : dislocation.id, 
                            'Slip plane id': dislocation.sp_id, 
                            'Position' : (dislocation.x_loc, slip_system[dis.sp_id].y), 
                            'Burgers vector': dislocation_data_burgers_vector,
                            'Force': dislocation_data_force 
                            }
        dislocation_list.append(dislocation_data)
    
    system_description.update({'Delta time step': dt, 'Number of simulation step' : n_steps, 'Number of dislocation':n , 
    'Geometry':geometry, 
    'Material properties':mat_props, 
    'Loading condition':loading_condition, 
    'Slip system':slip_system_dict,
    'Dislocations':dislocation_list})

    with open(save_data, 'w') as f:
        json.dump(system_description, f, indent=4)


if __name__ == "__main__":
    main()