# Copyright 2019 Segula Technologies - Agence Française pour la Biodiversité.
# Copyright 2020-2022 Segula Technologies - Office Français de la Biodiversité.
from setuptools import setup, find_packages

# read version
exec(open('okplm/_version.py').read())

# import long description data
with open('README.md', 'r') as f:
    long_description = f.read()

# configure setup
setup(
    name='okplm',
    version=__version__,
    packages=find_packages(),
    author=['Jordi Prats-Rodríguez', 'Pierre-Alain Danis'],
    author_email=['jprats@segula.es', 'pierre-alain.danis@biodiversite.fr'],
    description='Water temperature simulation with the OKP lake model',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.irstea.fr/alamode/okplm',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or ' +
        'later (GPLv3+)'],
    python_requires='>=3.5',
    install_requires=['numpy'],
    entry_points={
        'console_scripts': [
            'run_okp = okplm.okp_model:main']}
)
