"""
 py2app/py2exe build script for MyApplication.

 Will automatically ensure that all build prerequisites are available
 via ez_setup

 Usage (Mac OS X):
     python setup.py py2app

 Usage (Windows):
     python setup.py py2exe
 """

import ez_setup
ez_setup.use_setuptools()

import sys
from setuptools import setup, find_packages
# from distutils.core import setup

OPTIONS = {
    'argv_emulation': False,
    'includes': [
        'create_dashboard',
        'database_manager',
        'parse_patient_files',
        'patients_schema'
        # 'sqlalchemy.dialects.sqlite'
    ]
    # 'iconfile': 'trayicon32.icns',
}

# common_options = dict(name = "WorksiteRX Dashboard Generator", version = "0.1", description = description, argv_emulation=True, includes = scripts, resources = files)

if sys.platform == 'darwin':
    extra_options = dict(
        setup_requires=['py2app'],
        options = { 'py2app': OPTIONS}
        # Cross-platform applications generally expect sys.argv to
        # be used for opening files.
        # options=dict(py2app=dict(argv_emulation=True, includes = scripts, resources = files)),
    )
elif sys.platform == 'win32':
    extra_options = dict(
        setup_requires=['py2exe'],
        options = { 'py2exe': OPTIONS }
    )
# else:
#     extra_options = dict(
#         # Normally unix-like platforms will use "setup.py install"
#         # and install the main script as such
#         scripts=[mainscript]
#     )

setup(
    name="WorksiteRX Dashboard Generator",
    version = "0.1",
    author = 'Alyssa Freeman',
    author_email = 'alyssafreeman@kensatek.com',
    description = "WorksiteRX Dashboard Generator creates an aggregate patient dashboard excel file from a set of patient excel files",
    # includes = scripts,
    app = ['dashboard.py'],
    # data_files = ["dashboard_template.xlsx", "incentive_template.xlsx", "patients_schema.sql"],
    packages = find_packages(),
    package_data = {
      'dashboard': ['data/*.sql', 'data/*.xlsx'],
    },
    # include_package_data = True,
    **extra_options
)