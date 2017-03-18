#! /usr/bin/env python
import os
from distutils.core import setup
from distutils.extension import Extension
from subprocess import Popen, PIPE, CalledProcessError


try:
    from Cython.Distutils import build_ext
except ImportError:
    raise SystemExit("Requires Cython (http://cython.org/)")

try:
    ode_cflags = Popen(
        ["pkg-config", "--cflags", "ode"],
        stdout=PIPE).stdout.read().decode('ascii').split()
    ode_libs = Popen(
        ["pkg-config", "--libs", "ode"],
        stdout=PIPE).stdout.read().decode('ascii').split()
except (OSError, CalledProcessError):
    # raise SystemExit("Failed to find ODE with 'pkg-config'. Please make sure "
    #                  "that it is installed and available on your system path.")
    print("Failed to find ODE with 'pkg-config'. Please make sure "
          "that it is installed and available on your system path.")

extra_link_args = None
logpath = os.path.join(os.path.pardir, os.path.pardir, 'build', 'vs2010', 'obj',
                       'Release', 'ode.tlog', 'link.command.1.tlog')
try:
    with open(logpath) as f:
        extra_link_args = f.read()
except IOError as err:
    print('''couldn't open compile log file "%s"''' % logpath)
    print("""
             **********
    ******************************
    ********** REASON ************
    ******************************
             **********
%s
""" % err)

ode_ext = Extension("ode", ["ode.pyx"],
                    include_dirs="..\..\include",
                    extra_compile_args=r"""/I..\..\include /D NDEBUG /D dNODEBUG /D dIDEDOUBLE /D CCD_IDEDOUBLE /D WIN32""")
                    # extra_compile_args=r"""/I..\..\INCLUDE /I..\..\ODE\SRC /I..\..\ODE\SRC\JOINTS /I..\..\OPCODE /I..\..\GIMPACT\INCLUDE /I..\..\LIBCCD\SRC /I..\..\OU\INCLUDE /nologo /W3 /WX- /O2 /Oy /GL /D _MT /D NDEBUG /D dNODEBUG /D dIDEDOUBLE /D CCD_IDEDOUBLE /D WIN32 /D _CRT_SECURE_NO_DEPRECATE /D _USE_MATH_DEFINES /D _OU_NAMESPACE=odeou /D ODE_DLL /D _DLL /D _WINDLL /D _MBCS /GF /Gm- /EHsc /MD /GS /Gy /fp:precise /Zc:wchar_t /Zc:forScope /Zc:inline /Fo"OBJ\RELEASEDOUBLEDLL\\" /Fd"OBJ\RELEASEDOUBLEDLL\VC140.PDB" /Gd /TP""",
                    # extra_link_args=extra_link_args)


if __name__ == "__main__":
    setup(
        name="Open Dynamics Engine",
        version="0.12",
        author="Gideon Klompje",
#        author_email="",
#        maintainer="",
#        maintainer_email="",
        url="http://www.ode.org",
        description="Bindings for the Open Dynamics Engine",
        long_description=(
            "A free, industrial quality library for simulating articulated "
            "rigid body dynamics - for example ground vehicles, legged "
            "creatures, and moving objects in VR environments. It's fast, "
            "flexible & robust. Built-in collision detection."),
#        download_url="https://opende.svn.sourceforge.net/svnroot/opende",
#        classifiers=[],
#        platforms=[],
        license="BSD License, GNU Lesser General Public License (LGPL)",
        cmdclass={"build_ext": build_ext},
        ext_modules=[ode_ext]
    )
