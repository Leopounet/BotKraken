import os
import sys
import subprocess

from Structures.KrakenAPI import KrakenAPI
from Structures.AssetHandler import AssetHandler
from Structures.PlayerHandler import PlayerHandler

###############################################################################
############################## VARIABLES ######################################
###############################################################################

# login infos
command_file = "../commands.cmd"

###############################################################################
############################## CLASSES ########################################
###############################################################################

###############################################################################
############################## FUNCTIONS ######################################
###############################################################################


def kill():
    exit(0)

def restart(main_file):
    with open(command_file, "w") as file:
        file.write("")
    os.execv(main_file, sys.argv)

def clear():
    subprocess.call(['sh', './clear.sh'])

def reload_player():
    pass

def execute_command(main_file : str, kapi : KrakenAPI, ah : AssetHandler, ph : PlayerHandler) -> None:
    with open(command_file, "r") as file:
        for line in file:

            if line.startswith("KILL"):
                kill()

            if line.startswith("RESTART"):
                restart(main_file)

            if line.startswith("CLEAR"):
                clear()

            if line.startswith("RELOAD"):
                reload_player()

    with open(command_file, "w") as file:
        file.write("")

###############################################################################
############################## MAIN ###########################################
###############################################################################
