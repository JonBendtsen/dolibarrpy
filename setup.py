from setuptools import setup
import os

setup(
    name='dolibarrpy',
    packages=['dolibarrpy'],
    version="0.8.9",
    license='MIT',
    description='Python wrapper for Dolibarr API',
    long_description='This project is a python wrapper for the API for Dolibarr ERP & CRM found at dolibarr.org. It is not yet complete, but most major GET endpoints has been implemented. In the beginning I will mostly focus on implementing the API endpoints that I use.',
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
