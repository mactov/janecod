#!python3
import argparse
from InteractiveShell import InteractiveShell

parser = argparse.ArgumentParser(description='Code Generator Interactive Shell')
parser.add_argument('--silent', default=False, help="Turns Jane's messages off",
                    action='store_true')
args = parser.parse_args()
jane = InteractiveShell(args.silent, 'text')
jane.start_interact()


