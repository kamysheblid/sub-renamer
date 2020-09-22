#!/usr/bin/env python3
import os, re, argparse
from pathlib import PurePath

SUB_EXTS = '(srt|ass|ssa|vtt)'
VID_EXTS = '(avi|mp4|mpeg|mkv)'

# Get command line arguments and give help
parser = argparse.ArgumentParser(description='This program will automatically rename subtitles to match video filenames so your mediaplayer automatically finds them. If you do not give it a directory with -d then it looks in the current directory. The program looks for the video extensions {0}, and the subtitle extensions {1} if it is not told to be more specific with -V and -S options.'.format(VID_EXTS,SUB_EXTS))

parser.add_argument('--directory','-d',help='Directory to edit filenames.')
parser.add_argument('--video','-V',help='Give video extension to only find videos with this exact extension.')
parser.add_argument('--sub','-S',help='Give subs extension to only rename subs with this exact extension.')
parser.add_argument('--trial','-n',action='store_true',help='No action: print names of files to be renamed, but do not rename.')
parser.add_argument('--verbose','-v',action='store_true',help='Verbose: print names of files that are successfully change.')

args = parser.parse_args()

# If a directory was given, then change to it
if args.directory:
    os.chdir(args.directory)
directory_contents = os.listdir()

# Find all the video files in the directory
video_files = []
for f in directory_contents:
    srch = re.match(r'.*\.' + args.video if args.video else r'.*\.'+VID_EXTS,f)
    if srch: video_files.append(srch.group(0))

# regex to find subtitle episodes
# The 2nd group is the season, and 4th group is the episode
r0 = re.compile(r'.*(S|Season|season|s)([0-9]{2}).*(E|Episode|episode|e)([0-9]{2}).*\.' + (args.sub if args.sub else SUB_EXTS))

for f in sorted(os.listdir()):
    # Find an episode subtitle
    episode = r0.search(f)

    if episode:
        # Find the videos that share same episode and season number
        video_file = [video_file for video_file in video_files if episode.group(4) in video_file if episode.group(2)]

        # Rename them and tell user, but check if final_extension is given and rename using that, else rename it to extension of file
        if len(video_file) == 1:
            new_subname = re.sub(r'\.[a-z0-9]+',PurePath(f).suffix,video_file[0])
            if args.verbose or args.trial:
                print('{0} -> {1}'.format(f,new_subname))
            if not args.trial:
                os.rename(f,new_subname)
        elif len(video_file) > 1:
            print('ERROR: I found too many matching video files:')
            [print(vid) for vid in video_file]
            exit(1)
