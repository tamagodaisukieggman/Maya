set maya_script=%userprofile%\Documents\maya\scripts\FILENAME

if exist %maya_script:FILENAME=vaccine.py% (
del %maya_script:FILENAME=userSetup.py%
del %maya_script:FILENAME=vaccine.py%
del %maya_script:FILENAME=vaccine.pyc%
)