from setuptools import setup
import os

setup(
    name='dolibarr',
    packages=['dolibarr'],
    version="0.1.20",
    license='MIT',
    description='Python wrapper for Dolibarr API',
    long_description='Python wrapper for Dolibarr',
    long_description_content_type='text/markdown',
    author='Mark Meadows',
    author_email='mark@mvmdata.com',
    url='https://gitlab.com/mvmdata/dolibarr',
    # download_url = 'https://gitlab.com/mvmdata/dolibarr/archive/v_01.tar.gz',
    keywords=['Dolibarr', 'python'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
