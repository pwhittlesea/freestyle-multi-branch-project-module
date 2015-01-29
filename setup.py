import os
from setuptools import setup,find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "freestyle-multi-branch-project-module",
    version = "0.0.1",
    author = "Phillip Whittlesea",
    author_email = "pw.github@thega.me.uk",
    description = ("Jenkins Multi Branch module for jenkins-job-builder"),
    license = "Apache 2.0",
    keywords = "jenkins, plugin",
    url = "https://github.com/pwhittlesea/freestyle-multi-branch-project-module.git",
    packages=find_packages(),    
    long_description=read('README'),
    install_requires=["jenkins-job-builder>=0.6.0"],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],
    entry_points={
        'jenkins_jobs.projects': [
            'multibranch=modules.project_multibranch:MultiBranch',
        ],
    }
)
