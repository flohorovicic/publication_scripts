"""Python script to generate TOUGH2 MESH from Geomodel

Automatic version, adapted from iPython notebook "Geomodel to iTOUGH inv" """


# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>

# <markdowncell>

# Generate script to automate Geomodel to TOUGH2 processing for inclusion in iTOUGH2 inversion routines

# <codecell>

import os, sys
import subprocess
# Add Python project folders to Pythonpath - not required if installed into the system Pythonpath!
# GeoPyTOUGH module
import geopytough
# Module for manipulation of the GeoModeller model
import geomodelller_xml_obj as GO
# from geomuce_copy_files_export_model import copy_files_export_model
# PyTOUGH modules
import t2data as t2d
import mulgrids as mul
import t2listing as t2l

# NOTE: the import of matplotlib is different to the iPython notebook version, used to save model view to file
from matplotlib import use
use("Agg")
import matplotlib.pyplot as plt


# <markdowncell>

# Input block for adjustment of geomodel - Adapt this with Pest commands

# <codecell>

fault_top = 300
fault_bottom = 300
cap_top = 100
reservoir_top = 100
reservoir_left = -50
reservoir_right = -50

# <markdowncell>

# Some more settings

# <codecell>

os.chdir(r'/home/flo/04_iTOUGH2/CO2_paper/geomodel_to_itough2_inv')
geomodel_dir = r'/home/flo/04_iTOUGH2/CO2_paper/ori_geomodel/CO2_3D_model_5'
geomodeller_xml_file = 'CO2_3D_model_5.xml'
G1 = GO.GeomodellerClass()
G1.load_geomodeller_file(os.path.join(geomodel_dir, geomodeller_xml_file))
G1.write_xml('ori.xml')

# <markdowncell>

# Model settings

# <codecell>

# The parameters_example.csv file contains rock properties and formation names
csv_file_name= 'parameters_example.csv'
(nx, ny, nz) = (80, 1, 50)

# <markdowncell>

# Change geological model with Python scripts

# <markdowncell>

# Get Sections in model and extract points from sections

# <codecell>

sect = G1.get_sections()
points = G1.get_formation_point_data(sect[0])

# <markdowncell>

# All points that are assoicated with the fault contain "fault" in their ObservationID (in Geomodeller). We now locate all those points and shift them by a specified x-value

# <codecell>

for point in points:
    name = point.find("{"+G1.xmlns+"}Data").get("Name")
    obs_id = point.attrib['ObservationID']
    if ("fault" in obs_id) and ("top" in obs_id):
        G1.change_formation_point_pos(point, add_x_coord = fault_top)
        print "Adjust fault top with " + obs_id
    if ("fault" in obs_id) and ("bottom" in obs_id):
        G1.change_formation_point_pos(point, add_x_coord = fault_bottom)
        print "Adjust fault bottom with " +obs_id
    if obs_id == 'cap':
        G1.change_formation_point_pos(point, add_x_coord = cap_top)
        print "Adjust top of cap rock with " + obs_id
    if obs_id == 'res_right':
        G1.change_formation_point_pos(point, add_x_coord = reservoir_right)
        print "Adjust right side of reservori anticline with " + obs_id
    if obs_id == 'res_top':
        G1.change_formation_point_pos(point, add_x_coord = reservoir_top)
        print "Adjust top of reservoir anticline with " + obs_id
    if obs_id == 'res_left':
        G1.change_formation_point_pos(point, add_x_coord = reservoir_left)
        print "Adjust left side of reservoir anticline with " +obs_id

        

# <markdowncell>

# Now save the Geomodel xml file and copy it together with all relevant Geomodeller files into a new project directory

# <codecell>

G1.write_xml('updated.xml')

# <codecell>

# os.chdir(r'/home/flo/04_iTOUGH2/CO2_paper/geomodel_to_itough2_inv')
# print os.getcwd()
geopytough.copy_files_export_model(geomodel_dir, 'updated.xml', os.getcwd(), nx, ny, nz)

# <markdowncell>

# Now create a new TOUGH2 input file based on the changed geological model

# <codecell>

# os.chdir(r'/home/flo/04_iTOUGH2/CO2_paper/geomodel_to_itough2_inv/tmp')
dat = geopytough.GeoT2Data('CO2_template.dat')
dat.load_geomodel(os.path.join(".",geomodeller_xml_file))
dat.create_regular_mesh_from_geomodel(nx, ny, nz, keep_rocktypes = True, save_mesh = True, convention = 0)
dat.update_properties_from_csv_list(csv_file_name)
dat.update_model_from_exported_grid(grid_file = "exported_grid_updated.txt")
# dat.set_atmosphere_block_name("ATMOS")
injection_block = dat.geo.block_name_containing_point((3000,2500,-1000))
gener = dat.generatorlist[0]
gener.block = injection_block
dat.write('tmp2.dat')
dat.write('tmp.dat', meshfilename = "MESH")
geo = geopytough.GeoMulgrid("mesh.geo")
dat2 = t2d.t2data("tmp2.dat")
geo.slice_plot('x', rocktypes = dat2.grid, aspect = 'equal', 
                cbar_orientation = 'horizontal', 
                plt = plt,
                show = False,
                rocknames = ['Reservoir', 'Cap', 'Fault', 'Border', 'Cover'],
                plot_limits = ((0,5000),(-2000,0)),
                linewidth = 0.1,
                colourmap = 'summer')

plt.savefig("model_rock_types.png", bbox_inches='tight')
plt.savefig("model_rock_types.eps", bbox_inches='tight')

plt.close()


# <markdowncell>

# Run the simulation and, after finished, visualise results with next command

# <codecell>

# lst = t2l.t2listing("CO2_template.out")
# lst.last()
# print lst.time / 3.1536E7
# geo.slice_plot('x', variable = lst.element['XCO2aq'], aspect = 'equal', 
#                cbar_orientation = 'horizontal', 
#                plot_limits = ((0,5000),(-2000,0)),
#                linewidth = 0.1,
#                colourmap = 'gray_r')

# <codecell>


