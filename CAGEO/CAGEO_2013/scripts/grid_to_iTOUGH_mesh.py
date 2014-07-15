"""Export the mesh for the CO2 iTOUGH example, also includes some postprocessing"""

import numpy
import os
import subprocess
import time
# from processing import Process
import pickle

from geopytough import *
import t2listing


if __name__ == '__main__':
    
    # delete MESH file if it existed
    
    geomodel_dir = os.getcwd()
    ori_dir = geomodel_dir
    #geomodeller_xml_file = 'geomodel.xml'
    geomodeller_xml_file = 'CO2_3D_model_2.xml'
    os.chdir(ori_dir)
    template_model = 'template.dat'
    # template_model = 'test.dat'
    new_tough_file = 'MESH'
    new_grid_file = 'MESH_grid.dat'
    csv_file_name= 'parameters_example.csv'
    output_lst_file = 'CO2_fwd.out'
    # directory to save rocklists for later visualisation and analysis:
    rocklist_dir = os.path.join(geomodel_dir,"postprocessing")
    # post_proc_steps = (9,19,29) # steps for postprocessing saves
    post_proc_steps = "all"
    co2_thresholds = [0.01,0.02,0.03,0.04,0.05] # threshold for mass fraction of CO2

    
    """ cells """
    # low res
    (nx, ny, nz) = (50, 1, 40)
    # med res
    # (nx, ny, nz) = (100, 1, 50)
    # high res
    # (nx, ny, nz) = (100, 1, 80)
    # very high res (simulation approx. 8 hours per run!
    # (nx, ny, nz) = (200, 1, 80)

    print "\n\n\t\tSubprocess call: recompute model\n\n\n"
    print("Directory: " + geomodel_dir)
    print("Geomodeller file: " + geomodeller_xml_file)
    
    while True:
        proc = subprocess.Popen(['export_model',path.join(geomodel_dir,geomodeller_xml_file),str(nx),str(ny),str(nz)])
        for i in range(10):
            time.sleep(5)
            if proc.poll() == 0: 
                print("Process finished successfully")
                break
        if proc.poll() == None:
            proc.kill()
            print("\n\n\tProcess killed, restart!\n\n")
            continue
        elif proc.poll() == 0:
            print("Process finished successfully")
            break
        print("\n\n\tProcess not finished correctly!\n\n\n")
        break
    # print subprocess.call(['export_model',path.join(geomodel_dir,geomodeller_xml_file),str(nx),str(ny),str(nz)])

    """Prepare Tough2 data file"""
    dat = GeoT2Data(template_model)

    dat.title = 'iGeoPyTough2 - CO2 leackage study'
    dat.load_geomodel(os.path.join(geomodel_dir,geomodeller_xml_file))

    # store rocktype list for later use
    import copy
    rtypes = copy.deepcopy(dat.grid.rocktype)

    print "Create regular mesh"
    dat.create_regular_mesh_from_geomodel(nx, ny, nz)
    
    #
    # NOTE: this step is only required to create the TOUGH formtion names!
    #
    # print "Update rock properties"
    dat.update_properties_from_csv_list(os.path.join(ori_dir,csv_file_name))

        
    print "Create rocklist directory"
    try:
        os.makedirs("postprocessing")
    except OSError:
        print("Directory rocklists already exists")
        
        
    # determine rocklist name for subsequent numbering
    for n in range(1000):
        if ("rocklist_%03d.txt" % n) in os.listdir(rocklist_dir):
            continue
        else:
            # also determine rocklist of last time step for postprocessing:
            rocklist_name_last = "rocklist_%03d.txt" % (n-1)
            rocklist_name = "rocklist_%03d.txt" % n
            break
    
    print "Map lithologies from exported grid file"
    dat.update_model_from_exported_grid(save_grid = True, 
                                        save_rocktypes = True,
                                        rock_filename = os.path.join(rocklist_dir,rocklist_name))

    print "Set atmosphere block name"
    dat.set_atmosphere_block_name('ATMOS')

    # print "Adjust existing rocktypes"
    # print rtypes
    # for rt in dat.grid.rocktypelist:
    #     if rtypes.has_key(rt.name):
    #         print "Pre-existing rocktype, adjust"
    #         dat.grid.rocktype[rt.name] = rtypes[rt.name]
    #         print rtypes[rt.name].relative_permeability
    #         print dat.grid.rocktype[rt.name].relative_permeability

    # dat.grid.get_rocktype_indices()
    # dat.grid.get_rocktype_frequencies()
    # dat.grid.clean_rocktypes()

    print "write to file"
    dat.write("new.dat", meshfilename = "MESH") # , iTOUGH2=True)
    dat.geo.write(new_grid_file)


    #
    # P O S T  P R O C E S S I N G
    # 
    print("\n"+80*"*"+"\n")
    print("\n\tP O S T   P R O C E S S I N G\n\n")
    print("\n"+80*"*"+"\n")

    # store all results in dictionary and pickle
    results = {}    

    # first: check if output file in directory; if not, then first run, skip post processing
    if "rocklist_001.txt" in os.listdir(rocklist_dir):
        # open rocklist from last timestep
        filename = os.path.join(rocklist_dir,rocklist_name_last)
        r = numpy.ravel(numpy.loadtxt(filename,dtype="int"))
        # rtypes = numpy.unique(r)
        lst = t2listing.t2listing("CO2_fwd.out")

        #
        # determine block volume for calculation of total mass
        #
        # NOTE: one volume for all!
  
        vol = dat.geo.block_volume(dat.geo.layerlist[10],dat.geo.columnlist[10])
        results['block_volume'] = vol
        # save porosities
        por = [dat.grid.rocktypelist[id].porosity for id in r]
        results['porosity'] = por
        results['rocktype_indices'] = r 
        r_name = numpy.array([dat.grid.rocktypelist[r1].name for r1 in r])
        results['rocktype_names'] = r_name

        #
        # save results at pre-defined steps for co2 in entire model
        #
        print("Save XCO2aq for defined time steps\n")
        results['XCO2aq'] = {}
        results['DL'] = {}
        if post_proc_steps == "all":
            post_proc_steps = range(len(lst.steps))
        for i,step in enumerate(lst.steps):
            print("---> Step %d" % step)
            try:
            	lst.set_step(step)
            except IndexError:
                print("\n\tNo data for step %d!!\n\n" % step)
                continue
            co2 = lst.element['XCO2aq']
            dl = lst.element['DL']
            results['XCO2aq'][i] = copy.deepcopy(co2)
            results['DL'][i] = copy.deepcopy(dl)
        #
        # save total mass of CO2 in each rock compartment
        #
        print("Save sum of XCO2aq for all rock types\n")
        results['co2_thres_sums'] = {}
        results['time'] = []

        for co2_threshold in co2_thresholds:
            results['co2_thres_sums'][co2_threshold] = {}
            for rt in dat.grid.rocktypelist:
                results['co2_thres_sums'][co2_threshold][rt.name] = []
        for step in lst.steps:
            try:
            	lst.set_step(step)
            except IndexError:
                print("\n\tNo data for step %d!!\n\n" % step)
                continue
            print("--> Sums time step %d" % step) 
            co2 = lst.element['XCO2aq']
            density = lst.element['DL']
            for co2_threshold in co2_thresholds:
                for rt in dat.grid.rocktypelist:
                    # total_sum = sum(co2[r==rt] * density[r==rt] * vol)
                    n_blocks = sum(co2[r_name==rt.name] > co2_threshold)
                    fraq_blocks = n_blocks / float(sum(r_name==rt.name))
                    results['co2_thres_sums'][co2_threshold][rt.name].append(fraq_blocks)

            # save time of timestep
            results['time'].append(lst.time)
        # pickle object to file
        for n in range(1000):
            if ("results_%03d.pkl" % n) in os.listdir(rocklist_dir):
                continue
            else:
                results_name = "results_%03d.pkl" % n
                break
        print("Pickle results to file %s\n" % results_name)
        f = open(os.path.join(rocklist_dir,results_name),'w')
        pickle.dump(results,f)
                 
        









