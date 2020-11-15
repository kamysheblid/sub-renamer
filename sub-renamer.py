#!/usr/bin/env python3
import os, argparse, logging, pathlib
from Levenshtein import distance
from episode.episode import Episode

# Get command line arguments and give help
parser = argparse.ArgumentParser(description=f'This program will automatically rename subtitles to match video filenames so your mediaplayer automatically finds them. If you do not give it a directory with -d then it looks in the current directory. Does not change filenames by default until you enable --force option')

parser.add_argument('-d','--directory',help='Directory to edit filenames.',default=os.getcwd())
parser.add_argument('-V','--video',help='Give video extension to only find videos with this exact extension.',default=['avi','mp4','mpeg','mkv'])
parser.add_argument('-S','--sub',help='Give subs extension to only rename subs with this exact extension.',default=['srt','ass','ssa','vtt'])
parser.add_argument('-f','--force',action='store_true',help='Carry out renaming files.',default=False)
parser.add_argument('-v','--verbose',action='store_true',default=False,help='Verbose: print more info.')
parser.add_argument('-vv','--debug',action='store_true',default=False,help='More Verbose: print debug info.')
parser.add_argument('-q','--quiet',action='store_true',default=False,help='Be less verbose, i.e. hide filename changes.')

args = parser.parse_args()

SUB_EXTS = args.sub
VID_EXTS = args.video

if args.verbose:
    logging.basicConfig(level=logging.INFO)
elif args.quiet:
    logging.basicConfig(level=logging.ERROR)
elif args.debug:
    logging.basicConfig(level=logging.DEBUG)

if args.force:
    print('Program will change names of all matching subtitles found.')
else:
    print('Program will not change any subtitle names. To change names, call with -f option')

def is_sub(filename):
    logging.debug(f'Searching {filename} for {SUB_EXTS} suffix')
    return any([True for ext in SUB_EXTS if filename.endswith('.'+ext)])

def is_video(filename):
    logging.debug(f'Searching {filename} for {VID_EXTS} suffix')
    return any([True for ext in VID_EXTS if filename.endswith('.'+ext)])

try:
    logging.debug(f'Attempting to Change directory to {args.directory}')
    os.chdir(args.directory)
except FileNotFoundError:
    logging.error(f'No such directory: {args.directory}')
    exit(1)

subtitles = sorted([pathlib.Path(filename) for filename in os.listdir() if is_sub(filename)])
videos = sorted([Episode(filename) for filename in os.listdir() if is_video(filename)], key=lambda ep: ep.file.name)

logging.debug(f'Subtitles found: {[sub.name for sub in subtitles]}')
logging.debug(f'Videos found: {[video.filename for video in videos]}')

for video in videos:
    logging.debug(f'Searching for {video.filename}')
    sub_matches = [(distance(video.filename,sub.name),sub) for sub in subtitles if video.episode in sub.name]
    logging.info(f'Found matches: {sub_matches}')
    if sub_matches:
        sub_match = sorted(sub_matches, key=lambda x: x[0] if x else None)[0][1]
        new_subtitle_filename = video.file.with_suffix(sub_match.suffix)
        print(f'Changing \"{sub_match}\" -> \"{new_subtitle_filename}\"')
        if args.force:
            sub_match.rename(new_subtitle_filename)
    else:
        logging.error(f'S{video.season}E{video.episode} not found for {video.filename}')
