#!/usr/bin/env python
import os
from datetime import date

from carputils import settings
from carputils import tools
from carputils import mesh

EXAMPLE_DIR = os.path.dirname(__file__)



# define parameters exposed to the user on the commandline
def parser():
    parser = tools.standard_parser()
    parser.add_argument('--tend',
                        type=float, default=20.,
                        help='Duration of simulation (ms). Run for longer to also see repolarization.')
    return parser

def jobID(args):
    """
    Generate name of top level output directory.
    """
    today = date.today()
    return '{}_simple_{}_{}_np{}'.format(today.isoformat(), args.tend,
                                         args.flv, args.np)

@tools.carpexample(parser, jobID)
def run(args, job):
    # Path to your mesh file
    meshname = "/home/diya/Documents/openCARP/external/experiments/tutorials/02_EP_tissue/00_simple/atrial"
    

    # Load the mesh
    #geom = mesh.load(meshname)

    # Get basic command line, including solver options from external .par file
    cmd = tools.carp_cmd(tools.simfile_path(os.path.join(EXAMPLE_DIR, 'simple.par')))
    
    # Attach electrophysiology physics (monodomain) to mesh region with tag 1
    cmd += tools.gen_physics_opts(IntraTags=[1])

    cmd += ['-simID',    job.ID,
            '-meshname', meshname,
            '-tend',     args.tend]

    # Set monodomain conductivities
    cmd += ['-num_gregions',         1,
            '-gregion[0].name',     "myocardium",
            '-gregion[0].num_IDs',  1,
            '-gregion[0].ID',       "1",
            '-gregion[0].g_el',     0.625,
            '-gregion[0].g_et',     0.236,
            '-gregion[0].g_en',     0.236,
            '-gregion[0].g_il',     0.174,
            '-gregion[0].g_it',     0.019,
            '-gregion[0].g_in',     0.019,
            '-gregion[0].g_mult',   0.5]

    # Define the ionic model to use
    cmd += ['num_imp_regions',      1,
            'imp_region[0].im',     'Courtemanche',
            'imp_region[0].num_IDs',1,
            'imp_region[0].ID[0]',  1]

    # Define the geometry of the stimulus directly in the command line
    # Replace with your specific stimulus location and parameters
    cmd += ['-stimulus', 'x', '0', '100', '0', '1']

    if args.visualize:
        cmd += ['-gridout_i', 3]    # output both surface & volumetric mesh for visualization

    # Run simulation
    job.carp(cmd)

    # Do visualization
    if args.visualize and not settings.platform.BATCH:
        geom = os.path.join(job.ID, os.path.basename(meshname)+'_i')
        data = os.path.join(job.ID, 'vm.igb.gz')
        view = tools.simfile_path(os.path.join(EXAMPLE_DIR, 'simple.mshz'))
        job.meshalyzer(geom, data, view)

if __name__ == '__main__':
    run()
'''
def parser():
    parser = tools.standard_parser()
    group = parser.add_argument_group('experiment specific options')
    group.add_argument('--duration',
                       type=float,
                       default=20.,
                       help='Duration of simulation in [ms] (default: 20.)')
    group.add_argument('--S1-strength',
                       type=float,
                       default=20.,
                       help='Stimulus strength in [uA/cm^2] (default: 20.)')
    group.add_argument('--S1-dur',
                       type=float,
                       default=2.,
                       help='Stimulus duration in [ms] (default: 2.)')
    return parser

def jobID(args):
    today = date.today()
    return '{}_basic_{}'.format(today.isoformat(), args.duration)

@tools.carpexample(parser, jobID)
def run(args, job):
    # Path to your mesh file
    meshname = "/home/diya/Documents/openCARP/external/experiments/tutorials/02_EP_tissue/00_simple/atrial"

    # Stimulus parameters
    stim = ['-num_stim', 1,
            '-stimulus[0].name', 'S1',
            '-stimulus[0].stimtype', 0,
            '-stimulus[0].strength', args.S1_strength,
            '-stimulus[0].duration', args.S1_dur]

    # Additional electrode parameters (if needed, you might want to clarify or remove redundancy)
    electrode = ['-num_stim', 1,
                 '-stimulus[0].name', 'S1',
                 '-stimulus[0].stimtype', 0,
                 '-stimulus[0].strength', args.S1_strength,
                 '-stimulus[0].duration', args.S1_dur]

    # Get basic command line, including solver options
    cmd = tools.carp_cmd(os.path.join(EXAMPLE_DIR, 'basic.par'))

    # Add command line options for the simulation
    cmd += ['-simID', job.ID,
            '-meshname', meshname,
            '-dt', 25,
            '-tend', args.duration]
    cmd += stim + electrode

    # Include visualization options if requested
    if args.visualize:
        cmd += ['-gridout_i', 3]
        cmd += ['-gridout_e', 3]
        cmd += ['-spacedt', 0.1]

    # Run the simulation
    job.carp(cmd)

    # Visualization
    if args.visualize and not settings.platform.BATCH:
        # Prepare file paths
        geom = os.path.join(job.ID, os.path.basename(meshname) + '_i')
        data = os.path.join(job.ID, 'vm.igb.gz')
        view = os.path.join(EXAMPLE_DIR, 'view_vm.mshz')

        # GUI option for visualization
        if args.webGUI:
            data2 = os.path.join(job.ID, 'vm.igb')
            folderNameExp = f'/experiments/01_basic_usage_{job.ID}'
            os.mkdir(folderNameExp)
            cmdMesh = f'meshtool collect -imsh={geom} -omsh={folderNameExp}/{job.ID} -nod={data2} -ifmt=carp_txt -ofmt=ens_bin'
            outMesh = os.system(cmdMesh)
            if outMesh == 0:
                print('Meshtool - conversion successful')
            else:
                print('Meshtool - conversion failed')
        else:
            job.meshalyzer(geom, data, view)

if __name__ == '__main__':
    run()
   '''
