#!/usr/bin/env python3
import os, argparse, logging, pathlib, importlib.util
from episode.episode import Episode
from pprint import pformat

class Namespace:
    def __init__(self):
        return

ns = Namespace()


def get_args():
    # Get command line arguments and give help
    parser = argparse.ArgumentParser(description=f'This program will automatically rename subtitles to match video filenames so your mediaplayer automatically finds them. If you do not give it a directory with -d then it looks in the current directory. Does not change filenames by default until you enable --force option')

    parser.add_argument('-d','--directory',action='append',help='Directory to edit filenames.',default=os.getcwd())
    parser.add_argument('-V','--video',action='store',help='Give video extension to only find videos with this exact extension.',default=['avi','mp4','mpeg','mkv'],nargs='+')
    parser.add_argument('-S','--sub',help='Give subs extension to only rename subs with this exact extension.',default=['srt','ass','ssa','vtt'],nargs='+')
    parser.add_argument('-f','--force',action='store_true',help='Carry out renaming files.',default=False)
    parser.add_argument('-t','--test',action='store_true',help='Do not rename any files, just show what would happen.',default=False)
    parser.add_argument('-v','--verbose',action='store_true',default=False,help='Verbose: print more info.')
    parser.add_argument('-vv','--debug',action='store_true',default=False,help='More Verbose: print debug info.')
    parser.add_argument('-q','--quiet',action='store_true',default=False,help='Be less verbose, i.e. hide filename changes.')

    ns.args = parser.parse_args()

    # If user adds own extensions, I have to make sure it is a list so I can find the suffixes in the Episode class
    ns.SUB_EXTS = ns.args.sub if isinstance(ns.args.sub,list) else sorted([ns.args.sub], lambda x: len(x))
    ns.VID_EXTS = ns.args.video if isinstance(ns.args.video,list) else sorted([ns.args.video], lambda x: len(x))

    if ns.args.verbose:
        logging.basicConfig(level=logging.INFO)
        logging.info('Set logging to INFO level')
    elif ns.args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('Set logging to INFO level')
    else:
        logging.basicConfig(level=logging.ERROR)


    if ns.args.force:
        print('WARNING: Program will change names of all matching subtitles found.')
    else:
        print('\nNOTE: Program will not change any subtitle names. To change names, call with -f option\n')

    try:
        logging.debug(f'Attempting to Change directory to {ns.args.directory}')
        os.chdir(ns.args.directory)
    except FileNotFoundError:
        logging.error(f'No such directory: {ns.args.directory}')
        exit(1)

    return ns.args

def is_sub(filename):
    logging.debug(f'Searching {filename} for {ns.SUB_EXTS} suffix')
    for ext in ns.SUB_EXTS:
        logging.debug(f'Checking extension: {ext}')
        if filename.endswith('.'+ext):
            return True
    # return any([True for ext in ns.SUB_EXTS if filename.endswith('.'+ext)])

def is_video(filename):
    logging.debug(f'Searching {filename} for {ns.VID_EXTS} suffix')
    for ext in ns.VID_EXTS:
        logging.debug(f'Checking {filename} for extension: {ext}')
        if filename.endswith('.'+ext):
            return True


    logging.debug(f'Searching {filename} for {ns.VID_EXTS} suffix')
    return any([True for ext in ns.VID_EXTS if filename.endswith('.'+ext)])

def match_subs():
    filelist = os.listdir()
    logging.debug(f'File: {filelist}')
    subtitles = sorted([Episode(filename,ns.SUB_EXTS) for filename in filelist if is_sub(filename)])
    videos = sorted([Episode(filename,ns.VID_EXTS) for filename in filelist if is_video(filename)])

    logging.info(f'\nSubtitles found: {[sub.filename for sub in subtitles]}\n')
    logging.info(f'\nVideos found: {[video.filename for video in videos]}\n')

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
            logging.debug(f'Search failed. Using alternative method')
            if not importlib.util.find_spec('Levenshtein'):
                logging.error('I couldnt find the Levenshtein module, so I cant use the alternative method.\nTo get the module do `pip3 install python-Levenshtein`')
            continue
            from Levenshtein import distance

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
        are_you_sure = False
        new_subtitle_filename = sub_match.new_filename(video)

        if not ns.args.force and not ns.args.test:
            check = input(f'Renaming \"{sub_match.filename}\" -> \"{new_subtitle_filename}\" Are you sure you want to continue [y/!/n/N]: ')
            if check == '!':
                ns.args.force = True
            elif check == 'N':
                ns.args.test = True
            elif check.lower() == 'y':
                are_you_sure = True
            else:
                are_you_sure = False

        if ns.args.force or are_you_sure and not ns.args.test:
            print(f'Renamed \"{sub_match.filename}\" -> \"{new_subtitle_filename}\"') if ns.args.force else None
            sub_match.file.rename(new_subtitle_filename)
    return

if __name__ == '__main__':
    get_args()
    logging.info('Starting match_subs')
    matches = match_subs()
    logging.info(f'Matches:\n{pformat(matches)}\n')
    rename_files(matches)
