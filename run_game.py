#!/usr/bin/python

"""
run_game.py: Used to run game
- basically just appends the source directory to the path and imports/runs main
"""

import sys, os

mainpath = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.append(mainpath)
sys.path.append(os.path.join(mainpath,'src'))

import main

main.main(mainpath)
