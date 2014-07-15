"""Example with Simple Graben model: rejection sampling according to geological evolutionary rules"""

import xml.etree.ElementTree as ET

import os, sys
import pickle
sys.path.append(os.path.realpath("../../geomuce"))
sys.path.append(os.path.realpath("../../geomodeller/pygeomod"))
sys.path.append(os.path.realpath(".."))

import geomuce_core as GC
import geobayes_core as GBC
import geomodeller_xml_obj as GO
# from pygeomod import *
from geomuce_test_obs_ID import draw_model
from geomuce_copy_files_export_model import copy_files_export_model

""" Settings """
modeldir = "/home/flo/git/geobayes/models/Simple_Graben_3"
modelfile = "Simple_Graben_3.xml"
workdir = "/home/flo/10_Geomodels/04_geobayes/simple_graben_4"

# set number of required successful simulations
n = 1000
n = 1
# set number of max n (to avoid infinite loop)
n_max = 50000000

""" Set grid dimensions for export """
nx = 100
ny = 2
nz = 100


""" Define action """
get_model_info = True
perform_sampling = True
export = True
debug = False # print debug runtime information


""" Define rules: identifier of rule will be matched to observation id's! """
rules = {'sedi2_left_1' : {'obs_id': 'sedi2_left', 'action' : 'less than', 'value' : -300},
         'sedi2_right_1' : {'obs_id': 'sedi2_right', 'action' : 'less than', 'value' : -300},
         'basement_centre_max' : {'obs_id': 'basement_centre', 'action' : 'more than', 'value' : -950},
         #'sedi2_left_lt_sedi2_right' : {'obs_id' : 'sedi2_left', 'action' : 'less than', 'other variable' : 'sedi2_right'},
         'sedi1_left_lt_sedi2_left' : {'obs_id' : 'sedi1_left', 'action' : 'less than', 'other variable' : 'sedi2_left'},
         'sedi1_centre_lt_sedi2_centre' : {'obs_id' : 'sedi1_centre', 'action' : 'less than', 'other variable' : 'sedi2_centre'},
         'sedi1_right_lt_sedi2_right' : {'obs_id' : 'sedi1_right', 'action' : 'less than', 'other variable' : 'sedi2_right'},
         'basement_left_lt_sedi1_left' : {'obs_id' : 'basement_left', 'action' : 'less than', 'other variable' : 'sedi1_left'},
         'basement_centre_lt_sedi1_centre' : {'obs_id' : 'basement_centre', 'action' : 'less than', 'other variable' : 'sedi1_centre'},
         'basement_right_lt_sedi1_right' : {'obs_id' : 'basement_right', 'action' : 'less than', 'other variable' : 'sedi1_right'},
         # 'min_diff_sedi1_left_sedi1_centre' : {'obs_id' : 'sedi1_left', 'action' : 'min diff', 'other variable' : 'sedi1_centre', 'value' : 50},
         'max_diff_sedi1_left_sedi1_right' : {'obs_id' : 'sedi1_left', 'action' : 'max diff', 'other variable' : 'sedi1_right', 'value' : 100},
         'sedi1_centre_lt_sedi1_left' : {'obs_id' : 'sedi1_centre', 'action' : 'less than', 'other variable' : 'sedi1_left'}, 
         'min_diff_sedi1_right_sedi2_right' : {'obs_id' : 'sedi2_right', 'action' : 'min diff', 'other variable' : 'sedi1_right', 'value' : 100},
         'max_diff_sedi1_centre_sedi2_centre' : {'obs_id' : 'sedi1_centre', 'action' : 'max diff', 'other variable' : 'sedi2_centre', 'value' : 300},
         'min_diff_sedi2_right_basement_right' : {'obs_id' : 'sedi1_right', 'action' : 'min diff', 'other variable' : 'basement_right', 'value' : 100},
         'min_diff_sedi1_centre_sedi2_centre' : {'obs_id' : 'sedi2_centre', 'action' : 'min diff', 'other variable' : 'sedi1_centre', 'value' : 100},
         'min_diff_sedi2_centre_basement_centre' : {'obs_id' : 'sedi1_centre', 'action' : 'min diff', 'other variable' : 'basement_centre', 'value' : 100},
         'min_diff_sedi1_left_sedi2_left' : {'obs_id' : 'sedi2_left', 'action' : 'min diff', 'other variable' : 'sedi1_left', 'value' : 100},
         'min_diff_sedi2_left_basement_left' : {'obs_id' : 'sedi1_left', 'action' : 'min diff', 'other variable' : 'basement_left', 'value' : 100},
#         'thickness_sedi1_left_lt_thickness_sedi_centre' : {'vertical distance' : ['sedi2_left', 'sedi1_left'],
#                                                            'action' : 'less than',
#                                                            'other vertical distance' : ['sedi2_centre', 'sedi1_centre']},
         'thickness_sedi1_left_lt_thickness_sedi_centre' : {'min vertical distance' : ['sedi2_left', 'sedi1_left'],
                                                            'action' : 'less than',
                                                            'diff value' : 50,
                                                            'other vertical distance' : ['sedi2_centre', 'sedi1_centre']},
         'fault_left_top' : {'obs_id' : 'fault_left_top', 'action' : 'more than', 'value' : 150, 'directon' : 'x'},
         'fault_left_base' : {'obs_id' : 'fault_left_base', 'action' : 'less than', 'value' : 450, 'directon' : 'x'},
         'fault_left_top_lt_fault_left_base' : {'obs_id' : 'fault_left_top', 'action' : 'less than', 'other variable' : 'fault_left_base', 'direction' : 'x'},
         'fault_right_top' : {'obs_id' : 'fault_right_top', 'action' : 'less than', 'value' : 850, 'directon' : 'x'},
         'fault_right_base' : {'obs_id' : 'fault_right_base', 'action' : 'more than', 'value' : 550, 'directon' : 'x'},
         'fault_right_base_lt_fault_right_top' : {'obs_id' : 'fault_right_base', 'action' : 'less than', 'other variable' : 'fault_right_top', 'direction' : 'x'},
         'diff_fault_left' : {'obs_id' : 'fault_left_top', 'action' : 'min diff', 'other variable' : 'fault_left_base', 'value' : 50, 'direction' : 'x'},
         'diff_fault_right' : {'obs_id' : 'fault_right_top', 'action' : 'min diff', 'other variable' : 'fault_right_base', 'value' : 50, 'direction' : 'x'}
         }

rules = {}

# assign normal pdfs with 50 m standard deviation to all obs ids as prior
# prior_pdfs = {'all' : {'dist' : 'normal', 'stdev' : 50}}
# prior_pdfs = {'default' : {'dist' : 'normal', 'stdev' : 150}, # default direction is vertical ('y')!
#               'fault_left_top' : {'dist' : 'normal', 'stdev' : 200, 'direction' : 'x'},
#               'fault_left_base' : {'dist' : 'normal', 'stdev' : 200, 'direction' : 'x'},
#               'fault_right_top' : {'dist' : 'normal', 'stdev' : 200, 'direction' : 'x'},
#               'fault_right_base' : {'dist' : 'normal', 'stdev' : 200, 'direction' : 'x'},
#                'sedi2_centre' : {'dist' : 'normal', 'stdev' : 200},
#                'basement_centre' : {'dist' : 'normal', 'stdev' : 400}}
#               #'basement_centre' : {'dist' : 'normal', 'relative' : 0.1}}

prior_pdfs = {'default' : {'dist' : 'normal', 'stdev' : 75}, # default direction is vertical ('y')!
              'fault_left_top' : {'dist' : 'normal', 'stdev' : 100, 'direction' : 'x'},
              'fault_left_base' : {'dist' : 'normal', 'stdev' : 100, 'direction' : 'x'},
              'fault_right_top' : {'dist' : 'normal', 'stdev' : 100, 'direction' : 'x'},
              'fault_right_base' : {'dist' : 'normal', 'stdev' : 100, 'direction' : 'x'},
               'sedi2_centre' : {'dist' : 'normal', 'stdev' : 100},
               'basement_centre' : {'dist' : 'normal', 'stdev' : 200}}
              #'basement_centre' : {'dist' : 'normal', 'relative' : 0.1}}


successful = 0
rejected = 0
not_passed_rule = ""

if get_model_info:
    """Get some information about the model: defined formation points, foliations, etc."""
    G1 = GO.GeomodellerClass()
    G1.load_geomodeller_file(os.path.join(modeldir, modelfile))
    G1.create_sections_dict()
    
    print G1.section_dict.keys()
    
    for sec in G1.section_dict.keys():
        print "\n\n"
        print 80*"*"
        print "\tSection name : %s" % sec
        print 80*"*"
        print "\n"
        print 80*"-"
        print "Points in section %s: " % sec
        print 80*"-"
        forms = G1.get_formation_point_data(G1.section_dict[sec])
        if forms == None:
            print "\t\t\tNo Formation Points in this section"
        else:
            for form in forms:
                
                data = form.find("{"+G1.xmlns+"}Data")
                print "\nObsID = %s" % form.get("ObservationID")
                print "\tFormation name\t= %s" % data.get("Name")                    
                element_point = form.find("{"+G1.gml+"}LineString")
                element_coords = element_point.find("{"+G1.gml+"}coordinates")
                tmp = element_coords.text.split(" ")
                for tmp1 in tmp:
                    if tmp1 == '': continue
                    tmp_cds = tmp1.split(",")
                    print("\tX = %.1f, Y = %.1f" % (float(tmp_cds[0]), float(tmp_cds[1])))
                    

                fol = form.find("{"+G1.xmlns+"}FoliationObservation")
                if fol is not None:
                    print("\tFoliation defined: azimuth = %.1f, dip = %.1f" % (float(fol.get("Azimuth")), float(fol.get("Dip"))))
                    # get position of foliation (yet another point)
                    pt = fol.find("{"+G1.gml+"}Point")
                    c = pt.find("{"+G1.gml+"}coordinates")
                    cds = c.text.split(",")
                    print("\t\tX = %.1f, Y = %.1f" % (float(cds[0]), float(cds[1])))
                    
        print "\n"
        print 80*"-"
        print "Foliations in section %s:" % sec
        print 80*"-"
        foliations = G1.get_foliations(G1.section_dict[sec])
        if foliations == None:
            print "\t\t\tNo foliations in this section"
        else:
            for fol1 in foliations:
                print "\nObsID = %s" % fol1.get("ObservationID")
                data = fol1.find("{"+G1.xmlns+"}Data")
                fol = fol1.find("{"+G1.xmlns+"}FoliationObservation")
                print "\tFormation name\t= %s" % data.get("Name")                    
                print("\tAzimuth = %.1f, dip = %.1f" % (float(fol.get("Azimuth")), float(fol.get("Dip"))))
                pt = fol.find("{"+G1.gml+"}Point")
                c = pt.find("{"+G1.gml+"}coordinates")
                cds = c.text.split(",")
                print("\tX = %.1f, Y = %.1f" % (float(cds[0]), float(cds[1])))
                
    print("\n" + 80 * "+" + "\n")

    # get model range
    (rx, ry, rz) = G1.get_model_range()
    print("Model range: x = %.1f, y = %.1f, z = %.1f\n" %  (rx, ry, rz))
    print("Cell size: dx = %.1f, dy = %.1f, dz = %.1f\n" % (rx/float(nx), ry/float(ny), rz/float(nz)))
    print("Required n-cells for dx = dy = 2000, dz = 200:\n")
    print("nx = %d, ny = %d, nz = %d\n" % (int(rx/2000), int(ry/2000), int(rz/200)))




if perform_sampling:
    U_obj = GBC.BayesUncertaintyClass(modeldir, modelfile)
    U_obj.set_workdir(workdir)
    U_obj.info()
    U_obj.initialize()
    U_obj.set_parameters() # stupid name, adjust when it makes sense! figure out how to add to inherited functions!!
    print U_obj.params
    tree_copy = ET.ElementTree(U_obj.rootelement)
    copy_file_name = U_obj.resultsdir +  "/%s_original.xml" % (U_obj.xml_file_name[0:-4]) 
    tree_copy.write(copy_file_name)
    # testing procedure:
#    U_obj.read_random_statefile("random_statefile")
#    U_obj.set_random_state()

    # normal procedure:    
    U_obj.initialize_random_state()
    U_obj.create_random_statefile()

    # create simulation runs
    U_obj.logfile.write("Number of simulation runs: %d\n" %n)
    U_obj.logfile.write("Start uncertainty runs\n")
    U_obj.logfile.write(2 * (80 * "*" + "\n"))
    
    # original procedure: change all foliations in surface topography
    
    print("\n\n")

    # store information about passed and not passed iterations
    passed_infos = []
    
    for i in range(n_max):
        
        sys.stdout.write("\r\t\trun %6d of %d - successful: %4d of %d, rejected: %6d" %(i, n_max, successful, n, rejected))
        sys.stdout.flush()
        # print("\rrun %6d of %d - successful: %4d of %d, rejected: %6d" %(i, n_max, successful, n, rejected))
        # U_obj.reload_geomodeller_file()
        # U_obj = UncertaintyClass(workdir,geomodeller_file)
        U2 = GBC.BayesUncertaintyClass(modeldir, modelfile)
        U_obj.logfile.write("Uncertainty Run %d\n" % i)
        U_obj.logfile.write(80 * "*" + "\n")
        U2.add_to_project_name("Model %02d" % i)       
#        U2.change_foliations_in_section(U_obj,
#                                        "SurfaceTopography", 
##                                        formation="Formation1", 
#                                        independent=True,
#                                        gauss_sigma = 5,
#                                        dip = True)
#        U2.change_foliations_in_section(U_obj,
#                                        "SurfaceTopography", 
##                                        formation="Formation1", 
#                                        independent=True,
#                                        gauss_sigma = 5,
#                                        azimuth = True)
#        U2.change_formation_points_in_section(U_obj,
#                                              "Section1",
#                                              gauss_sigma = 50.0,
#                                              gauss_mu = 0.0,
#                                              independent = True)
        
        passed_info = U2.change_formation_according_to_rules(U_obj, rules,
                                                              prior_pdfs = prior_pdfs,
                                                              debug = debug)
        
        passed_infos.append(passed_info)

        if not passed_info['passed']:
            if debug:
                print("\n\n\n\tIteration did not pass rule %s! Reject!!\n\n\n" % passed_info['rule'])
            # add to list of non-passed rules
            not_passed_rule += "%s\n" % passed_info['rule']
            rejected += 1
            continue
        
        successful += 1
        
        # Write out to file
        tree_new = ET.ElementTree(U2.rootelement)
        new_file_name = U_obj.resultsdir +  "/%s_%02d.xml" % (U_obj.xml_file_name[0:-4],i)        
        tree_new.write(new_file_name)
        U_obj.logfile.write("wrote resulting model to new file %s\n" % new_file_name)
        U_obj.logfile.write(80 * "*" + "\n")
        
        if successful == n: break
        
        if n == (n_max-1): print("\n\n\tMax number of iterations reached!!!\n\n\n")

    # Finalise logfile, save random state and create plot
    U_obj.logfile.write("\n" + 80 * "*" + "\n")
    U_obj.logfile.write("End of Uncertainty Simulation Runs\n")
    U_obj.logfile.write("\n" + 80 * "*" + "\n")
#    print U_obj.used_random_numbers
#    U_obj.random_numbers_to_logfile()
#    U_obj.logfile.write("\n")
#    U_obj.create_randomfile()
#    U_obj.create_random_number_hist(all=True)



if export:
    copy_files_export_model(modeldir, U_obj.resultsdir, nx, ny, nz, parallel = True, n_procs = 1)
    
if perform_sampling:
    
    print("\n\n\n")

    params_file = open(os.path.join(U_obj.resultsdir,"params.pkl"), "w")
    pickle.dump(U_obj.params, params_file)
    params_file.close()

    not_passed_rules_file = open(os.path.join(U_obj.resultsdir,"not_passed_rules.txt"), "w")
    not_passed_rules_file.write(not_passed_rule)
    not_passed_rules_file.close()

    passed_info_file = open(os.path.join(U_obj.resultsdir,"passed_info.pkl"), "w")
    pickle.dump(passed_infos, passed_info_file)
    passed_info_file.close()

    # save rules and prior pdf for later analysis
    prior_pdfs_file = open(os.path.join(U_obj.resultsdir,"prior_pdfs.pkl"), "w")
    pickle.dump(prior_pdfs, prior_pdfs_file)
    prior_pdfs_file.close()
    rules_file = open(os.path.join(U_obj.resultsdir,"rules.pkl"), "w")
    pickle.dump(rules, rules_file)
    rules_file.close()

print("Rejected iterations: %d" % rejected)
