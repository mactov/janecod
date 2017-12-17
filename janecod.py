#!python3
import argparse
from CodeGenerator import CodeGenerator

parser = argparse.ArgumentParser(description='Code Generator Interactive Shell')
parser.add_argument('--silent', default=False, help="Turns Jane's messages off",
                    action='store_true')
args = parser.parse_args()
jane = CodeGenerator(args.silent)
jane.start()


