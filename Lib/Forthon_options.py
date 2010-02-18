"""Define Forthon options"""

import sys
import os.path
import optparse

usage = "Forthon [options] pkgname [extra Fortran or C files to be compiled or objects to link]"
description = """
pkgname is the name of the package.
A complete package will have at least two files, the interface description
file and the fortran file. The default name for the interface file is
pkgname.v. Note that the first line of the interface file must be the package
name. The default name for the fortran file is pkgname.F

Extra files can for fortran or C files that are to be compiled and included
in the package.
"""

parser = optparse.OptionParser(usage=usage,description=description)

parser.add_option('--builddir',
                  help='Location where the temporary compilation files (such as object files) should be placed. This defaults to build/temp-osname.')
parser.add_option('--build-temp',default='',
                  help='Location where the *pymodule.o files should be placed. This is relative to the builddir. This defaults to the builddir.')
parser.add_option('--cargs',
                  help='Additional options for the C compiler. These are passed through distutils, which does the compilation of C code. If there are any spaces in options, it must be surrounded in double quotes.')
parser.add_option('--compile_first',default='',metavar="FILE",
                  help='The specified file is compiled first. Normally the file that is compiled first is the fortran file generated by Forthon, which would normally contain all of the modules. But if the modules are in a different file, for example, then that file would need to be compiled first and should be specified here.')
parser.add_option('-g','--debug',action='store_true',default=False,
                  help='Turns off optimization for fortran compiler.')
parser.add_option('-D','--defines',action='append',default=[],
                  help='Defines a macro which will be inserted into the makefile. This is required in some cases where a third party library must be specified. This can be specified multiple times.')
parser.add_option('-d','--dependencies',action='append',default=[],
                  help='Specifies that a package that the package being built depends upon. This option can be specified multiple times.')
parser.add_option('--f90',action='store_true',default=True,
                  help='Writes wrapper code using f90, which means that python accessible variables are defined in f90 modules. This is the default.')
parser.add_option('--f77',action='store_false',default=True,dest='f90',
                  help='Writes wrapper code using f77, which means that python accessible variables are defined in common blocks. This is obsolete and is not supported.')
parser.add_option('--fargs',action='append',dest='fargslist',default=[],
                  metavar="FARGS",
                  help='Additional options for the fortran compiler. For example to turn on profiling. If there are any spaces in options, it must be surrounded in double quotes.')
parser.add_option('-F','--fcomp',
                  help='Fortran compiler. Will automatically be determined if not supplied. It can be one of the following, depending on the machine: intel8, intel, pg, absort, nag, xlf, mpxlf, xlf_r, g95, gfortran.')
parser.add_option('--fcompexec',
                  help='The executable name of the fortran compiler, if it is different and the compiler name. The -F (--fcomp) option must also be specified.')
parser.add_option('--fixed_suffix',default='F',
                  help='Suffix to use for fortran files in fixed format. Defaults to F')
parser.add_option('-f','--fortranfile',
                  help='Specifiy full name of main fortran file. It defaults to pkgname.F.')
parser.add_option('--fopt',
                  help='Optimization option for the fortran compiler. This will replace the default optimization options. If there are any spaces in options, it must be surrounded in double quotes.')
parser.add_option('--free_suffix',default='F90',
                  help='Suffix to use for fortran files in free format. Defaults to F90')
parser.add_option('--implicitnone',action='store_true',default=True,
                  dest='implicitnone')
parser.add_option('--noimplicitnone',action='store_false',default=True,
                  dest='implicitnone',
                  help='Specifies whether implicitnone is enforced. The default is --implicitnone.')
parser.add_option('-I','--includedirs',action='append',default=[],
                  help='Additional include paths')
parser.add_option('-a','--initialgallot',action='store_true',default=False)
parser.add_option('--noinitialgallot',action='store_false',default=False,
                  help='Specifies whether all groups will be allocated when package is imported into python. The default is --noinitialgallot.')
parser.add_option('-i','--interfacefile',
                  help='Specify full name of interface file. It defaults to pkgname.v.')
parser.add_option('-L','--libdirs',action='append',default=[],
                  help='Additional library paths')
parser.add_option('-l','--libs',action='append',default=[],
                  help="Additional libraries that are needed. Note that the prefix 'lib' and any suffixes should not be included.")
parser.add_option('-t','--machine',default=sys.platform,
                  help='Machine type. Will automatically be determined if not supplied. Can be one of linux2, aix4, aix5, darwin, win32.')
parser.add_option('--macros',action='append',dest='othermacros',default=[],
                  metavar="MACROS",
                  help='Other interface files whose macros are needed')
parser.add_option('--realsize',choices=['4','8'],default='8',
                  metavar='[4,8]',
                  help='The size of reals to use for variables that are declared to of type real in the variable description file. It defaults to 8.')
parser.add_option('--static',action='store_true',default=False,
                  help='Build the static version of the code by default, rather than the dynamically linker version. Not yet supported.')
parser.add_option('--timeroutines',action='store_true',default=False)
parser.add_option('--notimeroutines',action='store_false',default=False,
                  help='Specifies if timers are added for each python callable fortran routine. The default is --notimeroutines.')
parser.add_option('--writemodules',action='store_true',default=True,
                  dest='writemodules')
parser.add_option('--nowritemodules',action='store_false',default=True,
                  dest='writemodules',
                  help="Don't write out the module definitions. Useful if the modules have been written already. Note that if variables of derived type are used, the original code will need to be modified. See example2. Also note that if this option is used, no checks are made to ensure the consistency between the interface file description and the actual module.")
parser.add_option('--underscoring',action='store_true',default=True)
parser.add_option('--nounderscoring',action='store_false',default=True,
                  dest='underscoring',
                  help='Specifies whether to use any underscores when doing fortran name mangling. For most systems, the default is --underscoring.')
parser.add_option('--2underscores',action='store_true',default=False,
                  dest='twounderscores')
parser.add_option('--no2underscores',action='store_false',default=False,
                  dest='twounderscores',
                  help='Specifies whether or not to use second underscores when doing fortran name mangling.')
parser.add_option('--with-numpy',action='store_true',default=True,
                  help='This is now the default. Numeric is no longer supported.')

# --- Print help and then exit if no arguments are given
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

class InputError(Exception):
    pass

# --- Only process the true argument list when this is called from Forthon.
# --- Otherwise ignore the arguments. This is needed since for example this
# --- module may be imported by the compilers module which is used by some
# --- program other than Forthon.
if os.path.basename(sys.argv[0]) == 'Forthon' or sys.argv[0] == '-c':
    (options, args) = parser.parse_args()
else:
    (options, args) = parser.parse_args(args=[])

