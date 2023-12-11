# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
import os
import sys
sys.path.append(os.path.dirname(__file__))
from . import command


if __name__ == "__main__":
    if 'EXPORT_FILES' in os.environ:
        exportfiles = os.environ['EXPORT_FILES'].replace(os.sep, '/').split(";")

        for i, exportfile in enumerate(exportfiles):
            if os.path.isfile(exportfile) or os.path.isdir(exportfile):
                continue
            else:
                print('!'*100)
                print(u"\nError : The path contains an invalid string.\n")
                print('!'*100)
                break

        else:
            print("File path check complete.")
            if 'EX_EXCLUDE' in os.environ:
                command.bat_export(exportfiles, True)
            else:
                command.bat_export(exportfiles)
    else:
        print('#'*100)
        print(u"\nHow to use : Drag and drop the file or folder you want to output.\n")
        print('#'*100)
