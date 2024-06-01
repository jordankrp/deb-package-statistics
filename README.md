# deb-package-statistics
A python command line tool that outputs the statistics of the most frequent packages in a Debian contents index.

# Environment and Python package installation
Run `conda env create` to create your virtual environment with conda.
Activate the environment with `conda activate deb-package-stats` and then `pip install -r requirements.txt` to install all required packages.

# Run the script
You can change the file permissions of the script to make it a Python executable: `chmod +x package_statistics.py`.
Run the script by providing an architecture as an argument, e.g. `./package_statistics.py arm64`.