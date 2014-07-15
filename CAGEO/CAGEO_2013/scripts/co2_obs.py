"""create a plot for the mass and mass changes in several units"""
# from matplotlib import use
# use("Agg")

import sys
from matplotlib import rc
rc('font',**{'family':'sans-serif',
#             'sans-serif':['Computer Modern Sans serif'],
             'size'   : 10})
import matplotlib.pyplot as plt
import matplotlib 
# matplotlib.rcParams.update({'font.size': 12})
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, MaxNLocator
import numpy 

if len(sys.argv) > 1:
    lines = open(sys.argv[1],"r").readlines()[1:]
else:
    lines = open("CO2_itough_inv.col","r").readlines()[1:]
lines[0] = lines[0].rstrip()

# phases = ('gas', 'liquid')

phase = 'liquid'

read_col_data = True # read data from .col file
plot_observations = True
plot_all_in_one = True
plot_obs_ids = True # plot obs ids in plot when value > threshold
threshold = 0.02
plot_total_masses = False

show_labels = True # show labels in obs plot

m_size = 0 # marker-size
lw = 1 # linewidth

if read_col_data:    

# for phase in phases:
    if phase == 'gas':
        plot1 = '  SIM    0-e8g    '
        plot2 = '  SIM    0-j8g    '
        plot3 = '  SIM    0-o8g    '
        plot4 = '  SIM    0-t8g    '
        plot5 = '  SIM    0-y8g    '
        plot6 = '  SIM    0-ac8g   '
        plot7 = '  SIM    0-ah8g   '
        plot8 = '  SIM    0-am8g   '
        
    elif phase == 'liquid':
        plot1 = '  SIM    0-e8l    '
        plot2 = '  SIM    0-j8l    '
        plot3 = '  SIM    0-o8l    '
        plot4 = '  SIM    0-t8l    '
        plot5 = '  SIM    0-y8l    '
        plot6 = '  SIM    0-ac8l   '
        plot7 = '  SIM    0-ah8l   '
        plot8 = '  SIM    0-am8l   '
        
    plots = [plot1, plot2, plot3, plot4, plot5, plot6, plot7, plot8]
    
    
    # this seems to be the setting in iTOUGH2:
    col_width = 18
    
    # determine number of entries:
    cols = len(lines[0])/col_width
    
    # create dictionary for output:
    col_data = {}
    
    total = numpy.zeros((len(lines)-1,))
    
    # now read data in cols:
    for i in range(cols+1):
        start = col_width * i
        end = col_width * (i+1)
        col_name = lines[0][start:end]
        col_d = []
        for line in lines[1:]:
            col_d.append(float(line[start:end]))
        print("%s max: %e min: %e diff = %e" % (col_name, max(col_d), min(col_d), max(col_d)-min(col_d)))
        col_data[col_name] = numpy.array(col_d)
        if "0-t" in col_name:
            total += numpy.array(col_d)
    
    print numpy.shape(col_data['         [a]      '])
    print numpy.shape(total)
    total = total - total[0]
    
    for name in col_data.keys():
        print("'"+name+"'")
    
    #
    #
    #    Plot all lines
    #
    #

    print col_data.keys()
    
    
if plot_observations:
    
    plt.subplots_adjust(hspace = 2.5)
    fig = plt.figure(figsize=(9,12))
    ax1= fig.add_subplot(811)
    ax2= fig.add_subplot(812)
    ax3= fig.add_subplot(813)
    ax4= fig.add_subplot(814)
    ax5= fig.add_subplot(815)
    ax6= fig.add_subplot(816)
    ax7= fig.add_subplot(817)
    ax8= fig.add_subplot(818)
    
    # ax1.plot(col_data['         [a]      '],col_data['  SIM    0-tFault '],"go-")
    # ax2.plot(col_data['         [a]      '],col_data['  SIM    0-tRres  '],"go-")
    ax1.plot(col_data['         [a]      '],col_data[plot1],"go-",markersize=3)
    ax1.text(0.15, 0.7, 'O1',
             transform = ax1.transAxes,
            color='green', fontsize=12)
    ax2.plot(col_data['         [a]      '],col_data[plot2],"ro-",markersize=3)
    ax2.text(0.15, 0.7, 'O2',
             transform = ax2.transAxes,
            color='red', fontsize=12)
    ax3.plot(col_data['         [a]      '],col_data[plot3],"bo-",markersize=3)
    ax3.text(0.15, 0.7, 'O3',
             transform = ax3.transAxes,
            color='blue', fontsize=12)
    ax4.plot(col_data['         [a]      '],col_data[plot4],"o-",color="sienna",markersize=3)
    ax4.text(0.15, 0.7, 'O4',
             transform = ax4.transAxes,
            color='sienna', fontsize=12)
    ax5.plot(col_data['         [a]      '],col_data[plot5],"ko-",markersize=3)
    ax5.text(0.15, 0.7, 'O5',
             transform = ax5.transAxes,
            color='black', fontsize=12)
    ax6.plot(col_data['         [a]      '],col_data[plot6],"ko-",markersize=3)
    ax6.text(0.15, 0.7, 'O6',
             transform = ax6.transAxes,
            color='black', fontsize=12)
    ax7.plot(col_data['         [a]      '],col_data[plot7],"ko-",markersize=3)
    ax7.text(0.15, 0.7, 'O7',
             transform = ax7.transAxes,
            color='black', fontsize=12)
    ax8.plot(col_data['         [a]      '],col_data[plot8],"ko-",markersize=3)
    ax8.text(0.15, 0.7, 'O8',
             transform = ax8.transAxes,
            color='black', fontsize=12)
    
    # create plot with total:
    # ax3.plot(col_data['         [a]      '],total,"ko-")
    
    # ax1.set_title("CO$_2$ in Reservoir")
    ax1.set_ylabel("CO$_2$ %s phase" % phase)
    ax1.yaxis.set_major_locator( MaxNLocator(4) )
    ax2.set_ylabel("CO$_2$ %s phase" % phase)
    ax2.yaxis.set_major_locator( MaxNLocator(4) )
    ax3.set_ylabel("CO$_2$ %s phase" % phase)
    ax3.yaxis.set_major_locator( MaxNLocator(4) )
    ax4.set_ylabel("CO$_2$ %s phase" % phase)
    ax4.yaxis.set_major_locator( MaxNLocator(4) )
    ax5.set_ylabel("CO$_2$ %s phase" % phase)
    ax5.yaxis.set_major_locator( MaxNLocator(4) )
    ax6.set_ylabel("CO$_2$ %s phase" % phase)
    ax6.yaxis.set_major_locator( MaxNLocator(4) )
    ax7.set_ylabel("CO$_2$ %s phase" % phase)
    ax7.yaxis.set_major_locator( MaxNLocator(4) )
    ax8.set_ylabel("CO$_2$ %s phase" % phase)
    ax8.yaxis.set_major_locator( MaxNLocator(4) )
    
    
    
    
    # ax2 = fig.add_subplot(212)
    # ax2.plot(time,co2_res,"ro-")
    # ax2.set_title("CO2 mass in reservoir")
    # ax2.set_ylabel("CO2 mass")
    # ax1.set_xlabel("Time [years]")
    ax8.set_xlabel("Time [years]")
    
    plt.tight_layout()
    
    plt.savefig("observation_wells_%s.png" % phase, bbox_inches='tight')
    plt.savefig("observation_wells_%s.eps" % phase, bbox_inches='tight')
    
    # Now: scale all to same maximum value for comparison
    limits = (0,0.07)
    ax1.set_ylim(limits)
    ax2.set_ylim(limits)
    ax3.set_ylim(limits)
    ax4.set_ylim(limits)
    ax5.set_ylim(limits)
    ax6.set_ylim(limits)
    ax7.set_ylim(limits)
    ax8.set_ylim(limits)
    
    
    plt.savefig("observation_wells_scaled_%s.png" % phase, bbox_inches='tight')
    plt.savefig("observation_wells_scaled_%s.eps" % phase, bbox_inches='tight')
    
colours = ['black', 'yellowgreen', 'red', 'blue', 'sienna', 'green', 'orangered', 'navy']
if plot_all_in_one:
    # fig = plt.figure(figsize=(4,2))
    fig = plt.figure(figsize=(8,4))
    ax1 = fig.add_subplot(111)
    
    
    ax1.plot(col_data['         [a]      '],col_data[plot1],"o-",color=colours[0],markersize=m_size, linewidth=lw)
    ax1.plot(col_data['         [a]      '],col_data[plot2],"o-",color=colours[1],markersize=m_size, linewidth=lw)
    ax1.plot(col_data['         [a]      '],col_data[plot3],"o-",color=colours[2],markersize=m_size, linewidth=lw)
    ax1.plot(col_data['         [a]      '],col_data[plot4],"o-",color=colours[3],markersize=m_size, linewidth=lw)
    ax1.plot(col_data['         [a]      '],col_data[plot5],"o-",color=colours[4],markersize=m_size, linewidth=lw)
    ax1.plot(col_data['         [a]      '],col_data[plot6],"o-",color=colours[5],markersize=m_size, linewidth=lw)
    ax1.plot(col_data['         [a]      '],col_data[plot7],"o-",color=colours[6],markersize=m_size, linewidth=lw)
    ax1.plot(col_data['         [a]      '],col_data[plot8],"o-",color=colours[7],markersize=m_size, linewidth=lw)
    
    
    print("Check if column values are over threshold")
    for i,key in enumerate(plots):
        if max(col_data[key]) > threshold:
            id = list(col_data[key] > threshold).index(True)
            print max(col_data[key]) 

            ax1.text(col_data['         [a]      '][id], col_data[key][id], 'O%d' % (i+1),
                     bbox={'facecolor' : 'white', 'pad' : 7},
                    color=colours[i], fontsize=12)
    
    ax1.set_xlabel("Time [years]") 
    ax1.set_ylabel("CO$_2$ fraction %s phase" % phase)
    ax1.yaxis.set_major_locator( MaxNLocator(5) )
#    ax1.text(0.15, 0.7, 'O1',
#             transform = ax1.transAxes,
#            color='green', fontsize=12)
#    ax1.text(0.15, 0.7, 'O2',
#             transform = ax1.transAxes,
#            color='red', fontsize=12)
#    ax1.text(0.15, 0.7, 'O3',
#             transform = ax1.transAxes,
#            color='blue', fontsize=12)
#    ax1.text(0.15, 0.7, 'O4',
#             transform = ax1.transAxes,
#            color='sienna', fontsize=12)
#    ax1.text(0.15, 0.7, 'O5',
#             transform = ax1.transAxes,
#            color='black', fontsize=12)
#    ax1.text(0.15, 0.7, 'O6',
#             transform = ax1.transAxes,
#            color='black', fontsize=12)
#    ax1.text(0.15, 0.7, 'O7',
#             transform = ax1.transAxes,
#            color='black', fontsize=12)
#    ax1.text(0.15, 0.7, 'O8',
#             transform = ax1.transAxes,
#            color='black', fontsize=12)

    ax1.set_ylim((-0.005,0.07))

    plt.savefig("observation_wells_all_in_one_%s.png" % phase, bbox_inches = 'tight')
    plt.savefig("observation_wells_all_in_one_%s.eps" % phase, bbox_inches = 'tight')



if plot_total_masses:
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rel_atmos = col_data['  SIM    0-tATMOS '] / col_data['  SIM    0-TotalC']
    rel_fault = col_data['  SIM    0-tFault '] / col_data['  SIM    0-TotalC']
    rel_waste = col_data['  SIM    0-tWaste '] / col_data['  SIM    0-TotalC']
    rel_cover = col_data['  SIM    0-tCover '] / col_data['  SIM    0-TotalC']
    rel_reser = col_data['  SIM    0-tRes   '] / col_data['  SIM    0-TotalC']
    rel_capro = col_data['  SIM    0-tCap   '] / col_data['  SIM    0-TotalC']
    ax.plot(col_data['         [a]      '],rel_reser)
    ax.plot(col_data['         [a]      '],rel_reser + rel_fault)
    ax.plot(col_data['         [a]      '],rel_reser + rel_fault + rel_cover)
    ax.plot(col_data['         [a]      '],rel_reser + rel_fault + rel_cover + rel_atmos)
    ax.plot(col_data['         [a]      '],rel_reser + rel_fault + rel_cover + rel_atmos + rel_capro + rel_waste)

    plt.savefig('relative_total_masses.eps')



