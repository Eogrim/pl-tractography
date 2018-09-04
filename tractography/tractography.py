#                                                            _
# tractography ds app
#
# (c) 2016 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import os
import subprocess

# import the Chris app superclass
from chrisapp.base import ChrisApp


class Tractography(ChrisApp):
    """
    An app to ....
    """
    AUTHORS         = 'FNNDSC (dev@babyMRI.org)'
    SELFPATH        = os.path.dirname(os.path.abspath(__file__))
    SELFEXEC        = os.path.basename(__file__)
    EXECSHELL       = 'python3'
    TITLE           = 'tracto'
    CATEGORY        = ''
    TYPE            = 'ds'
    DESCRIPTION     = 'An app to ...'
    DOCUMENTATION   = 'http://wiki'
    VERSION         = '0.1'
    ICON            = '' # url of an icon image
    LICENSE         = 'Opensource (MIT)'
    MAX_NUMBER_OF_WORKERS = 1  # Override with integer value
    MIN_NUMBER_OF_WORKERS = 1  # Override with integer value
    MAX_CPU_LIMIT         = '' # Override with millicore value as string, e.g. '2000m'
    MIN_CPU_LIMIT         = '' # Override with millicore value as string, e.g. '2000m'
    MAX_MEMORY_LIMIT      = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_MEMORY_LIMIT      = '' # Override with string, e.g. '1Gi', '2000Mi'
    MIN_GPU_LIMIT         = 0  # Override with the minimum number of GPUs, as an integer, for your plugin
    MAX_GPU_LIMIT         = 0  # Override with the maximum number of GPUs, as an integer, for your plugin

    # Fill out this with key-value output descriptive info (such as an output file path
    # relative to the output dir) that you want to save to the output meta file when
    # called with the --saveoutputmeta flag
    OUTPUT_META_DICT = {}
 
    def define_parameters(self):
        """
        Define the CLI arguments accepted by this plugin app.
        """

        self.add_argument("-v",
                            help        = "Verbosity level. A value of '10' is a good choice here.",
                            dest        = 'verbosity',
                            type        = str,
                            optional    = True,
                            default     = '1')
        self.add_argument("-D", 
                            help        = "The directory to be scanned for specific diffusion sequences. This script will automatically target specific data within this directory and start a processing pipeline.",
                            dest        = 'dicomInputDir',
                            type        = str,
                            optional    = False,
                            default     = '')
        self.add_argument("-U",
                            help        = "If specified, do NOT use 'diff_unpack' to convert from original DICOM data to nifti format. By default, the script will attempt to create a final trackvis trk file using the same components as the front end diffusion toolkit. In some cases better dcm to nifti conversion is possible using 'mri_convert' (for Siemens) or 'dcm2nii'(for GE). To use these alternatives, specifiy a '-U'",
                            dest        = 'unpack',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-b",
                            help        = "The b field value, passed through to 'dcm2trk'.",
                            dest        = 'bFieldVal',
                            type        = str,
                            optional    = True,
                            default     = '$Gi_bValue')
        self.add_argument("-d",
                            help        = "If specified, override the automatic sequence detection and run the pipeline seeded on the series containinig <dicomSeriesFile>. This filename is relative to the <dicomInputDir>.",
                            dest        = 'dicomSeriesFile',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-B",
                            help        = "This option should only be used with care and overrides the internal detection of the number of b0 volumes, forcing this to be <b0vols>.",
                            dest        = 'b0vols',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-A",
                            help        = "Specifies the reconstruction algorithm and model to use. The default algorithm is 'fact', and the default model is DTI. @see [-I] argument",
                            dest        = 'reconAlg',
                            type        = str,
                            optional    = True,
                            default     = 'fact')
        self.add_argument("-I",
                            help        = "Specifies the reconstruction algorithm and model to use. The default algorithm is 'fact', and the default model is DTI. @see [-A] argument",
                            dest        = 'imageModel',
                            type        = str,
                            optional    = True,
                            default     = 'DTI')
        self.add_argument("--m1",
                            help        = "Selects which volume to use as a mask image 1 or 2.  Acceptable values are 'dwi', 'fa', and 'adc'.  If specified, the lower threshold for the mask is given by the '-mN-lower-threshold' option.  @see [--m2] argument",
                            dest        = 'maskImage1',
                            type        = str,
                            optional    = True,
                            default     = 'dwi')
        self.add_argument("--m2",
                            help        = "Selects which volume to use as a mask image 1 or 2.  Acceptable values are 'dwi', 'fa', and 'adc'.  If specified, the lower threshold for the mask is given by the '-mN-lower-threshold' option.  @see [--m1] argument",
                            dest        = 'maskImage2',
                            type        = str,
                            optional    = True,
                            default     = 'none')
        self.add_argument("--m1-lower-threshold",
                            help        = "Use the <lth> as a lower cutoff threshold on mask image 1 or 2. To use the entire volume, use '0.0'. The mask image that is used depends on what is specified for the '-mN' option. This option only has an effect if the mask is not 'dwi'. @see [--m2-lower-threshold] argument",
                            dest        = 'lthm1',
                            type        = str,
                            optional    = True,
                            default     = '0.0')
        self.add_argument("--m2-lower-threshold",
                            help        = "Use the <lth> as a lower cutoff threshold on mask image 1 or 2. To use the entire volume, use '0.0'. The mask image that is used depends on what is specified for the '-mN' option. This option only has an effect if the mask is not 'dwi'. @see [--m1-lower-threshold] argument",
                            dest        = 'lthm2',
                            type        = str,
                            optional    = True,
                            default     = '0.0')
        self.add_argument("--m1-upper-threshold",
                            help        = " Use the <uth> as an upper cutoff threshold on the mask image 1 or 2. To use the entire volume, use '1.0'.  The mask image that is used depends on what is specified for the '-mN' option. This option only has an effect if the mask is not 'dwi'. @see [--m2-upper-threshold] argument",
                            dest        = 'uthm1',
                            type        = str,
                            optional    = True,
                            default     = '1.0')
        self.add_argument("--m2-upper-threshold",
                            help        = " Use the <uth> as an upper cutoff threshold on the mask image 1 or 2. To use the entire volume, use '1.0'.  The mask image that is used depends on what is specified for the '-mN' option. This option only has an effect if the mask is not 'dwi'. @see [--m1-upper-threshold] argument",
                            dest        = 'uthm1',
                            type        = str,
                            optional    = True,
                            default     = '1.0')
        self.add_argument("--angle-threshold",
                            help        = "Use the <angle> as the threshold angle for tracking.",
                            dest        = 'angle',
                            type        = str,
                            optional    = True,
                            default     = '$G_ANGLETHRESHOLD')
        self.add_argument("-g",
                            help        = "By default, 'tract_meta.bash' will attempt to determine the correct gradient file for the tract reconstruction step. Occassionally, this determination might fail; by using the -g flag, a <gradientTableFile> can be explicitly sent to the reconstruction process. Currently, for Siemens data, 'tract_meta.bash' can by default gradient tables of minimum 13 directions. Smaller directions will necessitate supplying a <gradientTableFile>.",
                            dest        = 'gradientTableFile',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-G",
                            help        = "GE sequences require some additional tweaking with their gradient gradient tables. By default, the pipeline will perform an inline fixing of parsed gradient tables, which typically entails toggling the sign on the Z direction, and in some cases swapping X and Y columns. To TURN OFF this default, specify this flag. Has no effect on Siemens sequences.",
                            dest        = 'G',
                            type        = str,
                            optional    = True,
                            default     = '$Gb_GEGradientInlineFix')
        self.add_argument("-L",
                            help        = "The directory to contain output log files from each stage of the pipeline, as well containing any expert option files. This will default to the <dicomInputDir>/log if not explicitly specified. In this case, once the pipeline has completed, this log directory will be copied to the output directory.",
                            dest        = 'logDir',
                            type        = str,
                            optional    = True,
                            default     = '<dicomInputDir>/log') #!!!!!!!!!!!!!!!!!!!!!!
        self.add_argument("-O",
                            help        = "Directory to contain pipeline output. Usually this is self-determined from the logs of stage 1. However, specifying it here forces an override. Note that this directory will be used as the root for the outputs of each underlying stage.",
                            dest        = 'outputDir',
                            type        = str,
                            optional    = True,
                            default     = '')    #!!!!!!!!!!!!!!!!!!!!!!
        self.add_argument("-o",
                            help        = "Several different datasets can map to the same MRID. By specifying an optional output <suffix>, a user can differentiate between different processing runs on the same core MRID. For example '-o _noECC' would append the text '_noECC' to each file created in the processing stream.",
                            dest        = 'osuffix',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-R",
                            help        = "Appends <DIRsuffix> to the postproc/<MRID> as well as <logDir>. Since multiple studies on the same patient can in principle have the same MRID, interference can result in some of the log files and source data. By adding this <DIRsuffix>, different analyses on the same MRID can be cleanly separated.",
                            dest        = 'DIRsuffix',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-S",
                            help        = " By default, this scripe will scan for any sequences in the <dicomInputDir> that match any of the sequences in the series list. This series list is an internal default, but can be overriden with this flag. In the case of the tractography stream, the first substring match in the <dicomSeriesList> found in the <dicomInputDir> is collected.",
                            dest        = 'dicomSeriesList',
                            type        = str,
                            optional    = True,
                            default     = '$G_DICOMSERIESLIST')
        self.add_argument("-t",
                            help        = "The stages to process. See STAGES section for more detail.",
                            dest        = 'stages',
                            type        = str,
                            optional    = True,
                            default     = '$G_STAGES')
        self.add_argument("-f",
                            help        = "If true, force re-running a stage that has already been processed.",
                            dest        = 'force',
                            type        = str,
                            optional    = True,
                            default     = '$Gb_forceStage')
        self.add_argument("-k",
                            help        = "If true, skip eddy current correction when creating the track volume.",
                            dest        = 'kill',
                            type        = str,
                            optional    = True,
                            default     = '$Gb_skipEddyCurrentCorrection')
        self.add_argument("-E",
                            help        = "Use expert options. This script pipeline relies upon a number of underlying processes. Each of these processes accepts its own set of control options. Many of these options are not exposed by 'tract_meta.bash', but can be specified by passing this -E flag. Currently, 'dcm2trk.bash', 'tract_slice.bash', 'dicom_dirSend.bash', and dicom_seriesCollect.bash understand the -E flag. To pass expert options, create (in the <logDir>) a text file of the form <processName>.opt that contains additional options for <processName>. If found, the contents are read and also passed to the <processName> as 'fs_meta.bash' executes it. For example, to specify a different dicom sequence to process, create a 'dicom_seriesCollect.bash.opt' file containing:        -S \"3D SPGR AX-30 DEGREE\"         Indicating that the collection stage should find and copy all data pertaining to the given sequence.",
                            dest        = 'expert',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-c",
                            help        = "The '-c' indicates that the actual recon should be run on a compute cluster, with scheduling files stored in <clusterDir>. The cluster file is 'schedule.log', formatted in the standard stage-stamp manner. This schedule.log file is polled by a 'filewatch' process running on seychelles, and parsed by 'pbsubdiff.sh'. @see [-C] argument",
                            dest        = 'cluster',
                            type        = str,#!!!!!!!!
                            optional    = True,
                            default     = '$Gb_runCluster')
        self.add_argument("-C",
                            help        = "The '-c' indicates that the actual recon should be run on a compute cluster, with scheduling files stored in <clusterDir>. The cluster file is 'schedule.log', formatted in the standard stage-stamp manner. This schedule.log file is polled by a 'filewatch' process running on seychelles, and parsed by 'pbsubdiff.sh'. @see [-c] argument",
                            dest        = 'clusterDir',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-X",
                            help        = "Specifying any of the above multiplies the corresponding column in the gradient file with -1. @see [-Y][-Z] argument",
                            dest        = 'columnX',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-Y",
                            help        = "Specifying any of the above multiplies the corresponding column in the gradient file with -1. @see [-X][-Z] argument",
                            dest        = 'columnY',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-Z",
                            help        = "Specifying any of the above multiplies the corresponding column in the gradient file with -1. @see [-X][-Y] argument",
                            dest        = 'columnZ',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("-m", "-M",
                            help        = "Email the output of each sub-stage to <mailReportsTo>. Useful if running on a cluster and no output monitoring easily available. Use the small '-m' to only email the output from stdout logs; use capital '-M' to email stdout, stderr, and log file.",
                            dest        = 'mailReportsTo',
                            type        = str,
                            optional    = False, #!!!!!!!!
                            default     = '')
        self.add_argument("-n",
                            help        = "If specified, this option specified the name of the user that submitted the job to the cluster.  This name is added to the schedule.log file output for the cluster.  If not specified, it will be left blank",
                            dest        = 'clusterUserName',
                            type        = str,
                            optional    = True,
                            default     = '')
        self.add_argument("--migrate-analysis",
                            help        = "This option allows the specification of an alternative directory to <outputDir> where the processing occurs.  Basically what will happen is the input scans are copied to <migrateDir>, processing is done, and the files are then moved over back to the <outDir> when finished.  The purpose of this is to allow for use of cluster storage for doing processing automatically.",
                            dest        = 'migrateDir',
                            type        = str,
                            optional    = True,
                            default     = '')








    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        
        print(options)
        print("-m "+options.mailReportsTo)
        subprocess.Popen(["/bin/bash", "test.sh", "-p",\
        	"-v "+options.verbosity, \
        	"-D "+options.dicomInputDir, \
        	"-U "+options.unpack, \
        	"-b "+options.bFieldVal, \
        	"-d "+options.dicomSeriesFile, \
        	"-B "+options.b0vols, \
        	"-A "+options.reconAlg, \
        	"-I "+options.imageModel, \
        	"--m1 "+options.maskImage1, \
        	"--m2 "+options.maskImage2, \
        	"--m1-lower-threshold "+options.lthm1, \
        	"--m2-lower-threshold "+options.lthm2, \
        	"--m1-upper-threshold "+options.uthm1, \
        	"--m2-upper-threshold "+options.uthm1, \
        	"--angle-threshold "+options.angle, \
        	"-g "+options.gradientTableFile, \
        	"-G "+options.G, \
        	"-L "+options.logDir, \
        	"-O "+options.outputDir, \
        	"-o "+options.osuffix, \
        	"-R "+options.DIRsuffix, \
        	"-S "+options.dicomSeriesList, \
        	"-t "+options.stages, \
        	"-f "+options.force, \
        	"-k "+options.kill, \
        	"-E "+options.expert, \
        	"-c "+options.cluster, \
        	"-C "+options.clusterDir, \
        	"-X "+options.columnX, \
        	"-Y "+options.columnY, \
        	"-Z "+options.columnZ, \
        	"-m "+options.mailReportsTo, \
        	"-n "+options.clusterUserName, \
        	"--migrate-analysis "+options.migrateDir, \
        	"/home/christophe/Documents/cookiecutter/pl-tractography/tractography"])

        #subprocess.Popen(["/bin/bash", "tract_meta.bash", "-p","-G", "./scripts"])



# ENTRYPOINT
if __name__ == "__main__":
    app = Tractography()
    app.launch()
