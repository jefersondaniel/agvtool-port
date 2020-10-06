from setuptools import setup
import agvtool_port

long_description = open('README.rst', 'r').read()

setup(
    name='agvtool_port',
    version=agvtool_port.__version__,
    packages=['agvtool_port'],
    setup_requires=['wheel'],
    install_requires=['pbxproj==2.11.0'],
    entry_points={
        "console_scripts": [
            "agvtool = agvtool_port.__main__:__main__"
        ],
    },
    description="agvtool port for python",
    long_description=long_description,
    url='https://github.com/jefersondaniel/agvtool-port',
    author='Jeferson Daniel',
    author_email='jeferson.daniel412@gmail.com',
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
