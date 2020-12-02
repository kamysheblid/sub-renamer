#!/usr/bin/env python3
import os, argparse, logging, pathlib
from Levenshtein import distance
from episode.episode import Episode
#from gooey import Gooey

class Namespace:
    def __init__(self):
        return

ns = Namespace()

logging.basicConfig(level=logging.ERROR)
args = 0

def get_args():
    # Get command line arguments and give help
    parser = argparse.ArgumentParser(description=f'This program will automatically rename subtitles to match video filenames so your mediaplayer automatically finds them. If you do not give it a directory with -d then it looks in the current directory. Does not change filenames by default until you enable --force option')

    parser.add_argument('-d','--directory',help='Directory to edit filenames.',default=os.getcwd())
    parser.add_argument('-V','--video',help='Give video extension to only find videos with this exact extension.',default=['avi','mp4','mpeg','mkv'])
    parser.add_argument('-S','--sub',help='Give subs extension to only rename subs with this exact extension.',default=['srt','ass','ssa','vtt'])
    parser.add_argument('-f','--force',action='store_true',help='Carry out renaming files.',default=False)
    parser.add_argument('-v','--verbose',action='store_true',default=False,help='Verbose: print more info.')
    parser.add_argument('-vv','--debug',action='store_true',default=False,help='More Verbose: print debug info.')
    parser.add_argument('-q','--quiet',action='store_true',default=False,help='Be less verbose, i.e. hide filename changes.')

    global args
    args = parser.parse_args()

    ns.SUB_EXTS = args.sub
    ns.VID_EXTS = args.video

    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG)

    if args.force:
        print('Program will change names of all matching subtitles found.')
    else:
        print('Program will not change any subtitle names. To change names, call with -f option')


    try:
        logging.debug(f'Attempting to Change directory to {args.directory}')
        os.chdir(args.directory)
    except FileNotFoundError:
        logging.error(f'No such directory: {args.directory}')
        exit(1)

    return args


def is_sub(filename):
    logging.debug(f'Searching {filename} for {ns.SUB_EXTS} suffix')
    return any([True for ext in ns.SUB_EXTS if filename.endswith('.'+ext)])

def is_video(filename):
    logging.debug(f'Searching {filename} for {ns.VID_EXTS} suffix')
    return any([True for ext in ns.VID_EXTS if filename.endswith('.'+ext)])

def match_subs():
    subtitles = sorted([Episode(filename) for filename in os.listdir() if is_sub(filename)])
    videos = sorted([Episode(filename) for filename in os.listdir() if is_video(filename)])

    logging.debug(f'Subtitles found: {[sub.filename for sub in subtitles]}')
    logging.debug(f'Videos found: {[video.filename for video in videos]}')

    matched = []

    for video in videos:
        logging.debug(f'Searching for matching subtitle for video file {video.filename}')

        #try to fit the subtitles into the Episode class as well, if it fails use alternative method below
        try:
            logging.debug(f'Searching for subtitles using Episode class')
            sub_matches = list(filter(lambda sub: sub.episode == video.episode and sub.season == video.season, subtitles))
            if len(sub_matches) == 1:
                matched.append((video,sub_matches[0]))
        except:
            logging.debug(f'Search failed \nUsing alternative method')
            sub_matches = [(distance(video.filename,sub.filename),sub) for sub in subtitles if video.episode in sub.filename]
            logging.info(f'Found matches: {sub_matches}')
            if sub_matches:
                sub_match = sorted(sub_matches)[0]
                matched.append((video,sub_match))
            else:
                logging.error(f'S{video.season}E{video.episode} not found for {video.filename}')

    return matched

def rename_files(matches_list):
    for video,sub_match in matches_list:
        new_subtitle_filename = video.file.with_suffix(sub_match.file.suffix)
        print(f'Changing \"{sub_match}\" -> \"{new_subtitle_filename}\"')
        if args.force:
            sub_match.file.rename(new_subtitle_filename)
    return

if __name__ == '__main__':
    get_args()
    matches = match_subs()
    print(len(matches))
    rename_files(matches)
