from setuptools import setup
import os

setup(
    name='dolibarrpy',
    packages=['dolibarrpy'],
    version="0.3.0",
    license='MIT',
    description='Python wrapper for Dolibarr API',
    long_description='Python wrapper for Dolibarr',
    long_description_content_type='text/markdown',
    author='Jon Bendtsen',
    author_email='jon.bendtsen.github@jonb.dk',
    url='https://github.com/JonBendtsen/dolibarrpy.git',
    keywords=['Dolibarr', 'python'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.9',
    ],
)
