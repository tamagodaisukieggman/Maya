from __future__ import division, print_function, absolute_import

from . import app

def show_chr_checker(*arg):
    app.show_checker_gui("chr")

def show_prp_checker(*arg):
    app.show_checker_gui("prp")

def show_enm_checker(*arg):
    app.show_checker_gui("enm")

def show_wep_checker(*arg):
    app.show_checker_gui("wep")