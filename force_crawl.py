import argparse

import marks

parser = argparse.ArgumentParser(description='Force a crawl of a player.')
parser.add_argument('nick', type=str, help='Name (lower-case) of the player to force crawl.')
args = parser.parse_args()

marks.reset( args.nick.lower() )
