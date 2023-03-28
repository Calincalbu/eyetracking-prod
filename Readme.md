# Eyetracking master's project

In this project I use the eye-tracking data gathered from a Varjo VR-2 headset to analyse the cognitive load during a simulation. 


## Prerequisites
- Python 3.8.5+
- Dataset

## Installing
- Setup virtual environment in root folder ('Eyetracking')
`python -m venv .venv`
- Switch to venv
`source .venv/bin/activate`
- Install requirements
`pip install -r requirements.txt`
- Inject custom generator matrix from
 `generators/CALIN`
 to 
 `.venv/lib/python3.9/site-packages/Bio/Align/substitution_matrices/data/CALIN`

 ## Running
 - `python "Extracting data.py"`



## Other files in the root folder
| Name               | Description                                                               |
|--------------------|---------------------------------------------------------------------------|
| Data               | Has subjects eyetracking data in December 2021                            |
| Data2              | Has subjects eyetracking data in March 2022                               |
| generators         | Contains code for matrix generator and a matrix used in scanpath analysis |
| Extracting data.py | Main script                                                               |                                                           |
| functions.py       | Contains algorithms used by main script                                   |
| requirements.txt   | Contains python modules used in the project, usable with pip install -r   |
| Results.json       | IPA and scanpath analysis                                                 |
| Results2.json      | IPA and scanpath analysis                                                 |

