# About
Pre-assignment for Reaktor's software developer, 2020. Hosted version of this program is available [here](https://mahmudul-dpkg.herokuapp.com/)

The goal of this assignment is to parse the contents of /var/lib/dpkg/status file and display them in the file via an HTML interface. The program output should contain the following information of each packages:

- Name
- Description
- Package dependencies
- Reverse depeneencies

# Requirements
In order to run this program, it requires python installed on your computer
- python 3

# Run
https://github.com/mhjony/dpkg-status.git <br />
cd dpkg-status <br />
python3 analyse.py > index.html <br />
open index.html
