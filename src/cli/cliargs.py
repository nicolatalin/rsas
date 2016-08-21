from src.gui.gui import GUI
from src.cli.cli import CLI
from src.lib.const import CONST
import argparse


class CliArgs:

    def __init__(self):
        parser = argparse.ArgumentParser(prog=CONST.PROG_SHORTNAME, description=CONST.PROG_SHORTDESC)
        parser.add_argument('-c', '--console', action='store_true', help='command line mode: start interactive console')
        parser.add_argument('-e', '--execute', choices=sorted(CLI.CMDs().keys()), help='command line mode: command to execute')
        self.args = parser.parse_args()

    def start(self):
        if self.args.console:
            CLI.console()
        elif self.args.execute:
            CLI.do(self.args.execute)
        else:
            GUI.start()
