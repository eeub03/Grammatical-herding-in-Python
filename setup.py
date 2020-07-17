from setuptools import setup
setup(
    name = 'ghpy',
    version = '1.0.2',
    author = 'Joseph Michael Morgan',
    author_email = 'thejosephmor@gmail.com',

    packages = ['src.fitness',
                'src.grammars',
                'src.Herd',
                'src.mapping',
                'src.parameters',
                'src.PGEGrammar',
                'src.stats',
                'src.fitness.santa_fe'],
    package_data = {'fitness.santa_fe': ['trail/data.dat']},
    scripts = ['scripts\GHPY.py'],
    license = ["LICENSE.TXT"],
    description = ["Grammatical Herding in Python"],
    install_requires = ["numpy",
                        "pandas",
                        "mesa"]
)