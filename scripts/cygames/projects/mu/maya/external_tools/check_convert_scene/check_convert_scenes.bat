@echo off


set MAYAPY="C:\Program Files\Autodesk\Maya2018\bin\mayapy.exe"
set SCRIPT="Z:\mtk\tools\maya\external_tools\check_convert_scene\check_convert_scenes.py"

echo ==== check convert scenes ====

%MAYAPY% %SCRIPT%


pause