from __future__ import division, print_function, absolute_import

from . import app

def show_chr_checker(*arg):
    app.show_checker_gui("chr")

def show_prp_checker(*arg):
    app.show_checker_gui("prp")