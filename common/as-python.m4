dnl as-python.m4 0.1.1
dnl autostars m4 macro for python checks

dnl From Andrew Dalke
dnl Updated by James Henstridge
dnl Updated by Andy Wingo to loop through possible pythons
dnl Updated by Thomas Vander Stichele to check for presence of packages/modules

dnl $Id: as-python.m4,v 1.3 2006/02/28 16:49:31 thomasvs Exp $

# AS_PATH_PYTHON([MINIMUM-VERSION])

# Adds support for distributing Python modules and packages.  To
# install modules, copy them to $(pythondir), using the python_PYTHON
# automake variable.  To install a package with the same name as the
# automake package, install to $(pkgpythondir), or use the
# pkgpython_PYTHON automake variable.

# The variables $(pyexecdir) and $(pkgpyexecdir) are provided as
# locations to install python extension modules (shared libraries).
# Another macro is required to find the appropriate flags to compile
# extension modules.

# If your package is configured with a different prefix to python,
# users will have to add the install directory to the PYTHONPATH
# environment variable, or create a .pth file (see the python
# documentation for details).

# If the MINIMUM-VERSION argument is passed, AS_PATH_PYTHON will
# cause an error if the version of python installed on the system
# doesn't meet the requirement.  MINIMUM-VERSION should consist of
# numbers and dots only.

# Updated to loop over all possible python binaries by Andy Wingo
# <wingo@pobox.com>

AC_DEFUN([AS_PATH_PYTHON],
 [
  dnl Find a version of Python.  Only checks for python 2.2 or newer.

  dnl should we do the version check?
  ifelse([$1],[],
         [AC_PATH_PROG(PYTHON, python python2.7 python2.6 python2.5 python2.4 python2.3 python2.2)],
         [
     AC_MSG_NOTICE(Looking for Python version >= $1)
    changequote(<<, >>)dnl
    prog="
import sys
minver = tuple(map(int,'$1'.split('.'))) + ('final', 0)
pyver = sys.version_info
if pyver >= minver:
	sys.exit(0)
else:
	sys.exit(1)"
    changequote([, ])dnl

    python_good=false
    for python_candidate in python python2.7 python2.6 python2.5 python2.4 python2.3 python2.2; do
      unset PYTHON
      AC_PATH_PROG(PYTHON, $python_candidate) 1> /dev/null 2> /dev/null

      if test "x$PYTHON" = "x"; then continue; fi

      if $PYTHON -c "$prog" 1>&AC_FD_CC 2>&AC_FD_CC; then
        AC_MSG_CHECKING(["$PYTHON":])
	AC_MSG_RESULT([okay])
        python_good=true
        break;
      else
        dnl clear the cache val
        unset ac_cv_path_PYTHON
      fi
    done
  ])

  if test "$python_good" != "true"; then
    AC_MSG_ERROR([No suitable version of python found])
  fi

  AC_MSG_CHECKING([local Python configuration])

  dnl Need to change quote character because of [:2]
  AC_SUBST(PYTHON_VERSION)
  changequote(<<, >>)dnl
  PYTHON_VERSION=`$PYTHON -c "import sys; print '.'.join(map(str,sys.version_info[:2]))"`
  changequote([, ])dnl


  dnl Use the values of $prefix and $exec_prefix for the corresponding
  dnl values of PYTHON_PREFIX and PYTHON_EXEC_PREFIX.  These are made
  dnl distinct variables so they can be overridden if need be.  However,
  dnl general consensus is that you shouldn't need this ability.

  AC_SUBST(PYTHON_PREFIX)
  PYTHON_PREFIX='${prefix}'

  AC_SUBST(PYTHON_EXEC_PREFIX)
  PYTHON_EXEC_PREFIX='${exec_prefix}'

  dnl At times (like when building shared libraries) you may want
  dnl to know which OS platform Python thinks this is.

  AC_SUBST(PYTHON_PLATFORM)
  PYTHON_PLATFORM=`$PYTHON -c "import sys; print sys.platform"`


  dnl Set up 4 directories:

  dnl pythondir -- where to install python scripts.  This is the
  dnl   site-packages directory, not the python standard library
  dnl   directory like in previous automake betas.  This behaviour
  dnl   is more consistent with lispdir.m4 for example.
  dnl
  dnl Also, if the package prefix isn't the same as python's prefix,
  dnl then the old $(pythondir) was pretty useless.

  AC_SUBST(pythondir)
  pythondir=$PYTHON_PREFIX"/lib/python"$PYTHON_VERSION/site-packages

  dnl pkgpythondir -- $PACKAGE directory under pythondir.  Was
  dnl   PYTHON_SITE_PACKAGE in previous betas, but this naming is
  dnl   more consistent with the rest of automake.
  dnl   Maybe this should be put in python.am?

  AC_SUBST(pkgpythondir)
  pkgpythondir=\${pythondir}/$PACKAGE

  dnl pyexecdir -- directory for installing python extension modules
  dnl   (shared libraries)  Was PYTHON_SITE_EXEC in previous betas.

  AC_SUBST(pyexecdir)
  pyexecdir=$PYTHON_EXEC_PREFIX"/lib/python"$PYTHON_VERSION/site-packages

  dnl pkgpyexecdir -- $(pyexecdir)/$(PACKAGE)
  dnl   Maybe this should be put in python.am?

  AC_SUBST(pkgpyexecdir)
  pkgpyexecdir=\${pyexecdir}/$PACKAGE

  AC_MSG_RESULT([looks good])
])

dnl AS_PYTHON_IMPORT(PACKAGE/MODULE, [ACTION-IF-FOUND, [ACTION-IF-NOT-FOUND, [PREAMBLE, [POSTAMBLE]]]])
dnl Try to import the given PACKAGE/MODULE

AC_DEFUN([AS_PYTHON_IMPORT],
[
  dnl Check if we can import a given module.
  dnl Requires AS_PATH_PYTHON to be called before.
  dnl PREAMBLE and POSTAMBLE, if given, is code executed right before and after
  dnl the import; stdout is rerouted to config.log, and stderr to the console.

  AC_MSG_CHECKING([for python module $1])

  changequote(<<, >>)dnl
  prog="
import sys

try:
    $4
    import $1
    $5
    sys.exit(0)
except ImportError, e:
    raise SystemExit(*e.args)
except SystemExit, e:
    if not e.args or (e.args[0] != 0 and not isinstance(e.args[0], str)):
        raise SystemExit('Unknown error')
    raise
except Exception, e:
    print '  Error while trying to import $1:'
    print '    %r: %s' % (e, e)
    sys.exit(1)"
  changequote([, ])dnl

if $PYTHON -c "$prog" 1>&AS_MESSAGE_LOG_FD 2>&AS_MESSAGE_FD
then
    AC_MSG_RESULT(found)
    ifelse([$2], , :, [$2])
else
    dnl python has already printed a message on the message fd
    ifelse([$3], , :, [$3])
fi
])

dnl a macro to check for ability to create python extensions
dnl  AM_CHECK_PYTHON_HEADERS([ACTION-IF-POSSIBLE], [ACTION-IF-NOT-POSSIBLE])
dnl function also defines PYTHON_INCLUDES
AC_DEFUN([AM_CHECK_PYTHON_HEADERS],
 [
  AC_REQUIRE([AM_PATH_PYTHON])
  AC_MSG_CHECKING(for headers required to compile python extensions)

  dnl deduce PYTHON_INCLUDES
  py_prefix=`$PYTHON -c "import sys; print sys.prefix"`
  py_exec_prefix=`$PYTHON -c "import sys; print sys.exec_prefix"`
  PYTHON_INCLUDES="-I${py_prefix}/include/python${PYTHON_VERSION}"

  if test "$py_prefix" != "$py_exec_prefix"; then
    PYTHON_INCLUDES="$PYTHON_INCLUDES -I${py_exec_prefix}/include/python${PYTHON_VERSION}"
  fi
  AC_SUBST(PYTHON_INCLUDES)

  dnl check if the headers exist:
  save_CPPFLAGS="$CPPFLAGS"
  CPPFLAGS="$CPPFLAGS $PYTHON_INCLUDES"
AC_TRY_CPP([#include <Python.h>],dnl
[AC_MSG_RESULT(found)
$1],dnl
[AC_MSG_RESULT(not found)
$2])
CPPFLAGS="$save_CPPFLAGS"
])
