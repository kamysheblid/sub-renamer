#!/usr/bin/env python3
import os, argparse
from episode import Episode

SUB_EXTS = ['srt','ass','ssa','vtt']
VID_EXTS = ['avi','mp4','mpeg','mkv']

# Get command line arguments and give help
parser = argparse.ArgumentParser(description='This program will automatically rename subtitles to match video filenames so your mediaplayer automatically finds them. If you do not give it a directory with -d then it looks in the current directory. The program looks for the video extensions {0}, and the subtitle extensions {1} if it is not told to be more specific with -V and -S options.'.format(VID_EXTS,SUB_EXTS))

parser.add_argument('--directory','-d',help='Directory to edit filenames.',default=os.getcwd())
parser.add_argument('--video','-V',help='Give video extension to only find videos with this exact extension.',default=VID_EXTS)
parser.add_argument('--sub','-S',help='Give subs extension to only rename subs with this exact extension.',default=SUB_EXTS)
parser.add_argument('--trial','-n',action='store_true',help='No action: print names of files to be renamed, but do not rename.',default=False)
parser.add_argument('--verbose','-v',action='store_true',help='Verbose: print names of files that are not changed and their season and episode numbers.')
parser.add_argument('--quiet','-q',action='store_true',help='Be less verbose, i.e. hide filename changes.')

args = parser.parse_args()

# Print a newline to make it easier to read
print()

SUB_EXTS = args.sub
VID_EXTS = args.video

try:
    os.chdir(args.directory)
except FileNotFoundError:
    print('No such directory:',args.directory)
    exit(1)

# Separate the subs and vids, put them in
# separate dicts so they can be searched
subtitles = dict()
videos = dict()
for f in os.listdir():
    ep = Episode(f)
    # If it cannot parse, then just move on
    if not ep.episode:
        continue
    if ep.suffix:
        if ep.suffix in SUB_EXTS:
            subtitles.update({(ep.season,ep.episode):ep})
        elif ep.suffix in VID_EXTS:
            videos.update({(ep.season,ep.episode):ep})

# Combine the matching subs and vids
for elt in sorted(subtitles):
    if elt in videos.keys():
        subtitle = subtitles[elt]
        video = videos[elt]

        new_sub_filename = subtitle.subtitle_rename(video)

        if not args.quiet:
            print('{0} -> {1}'.format(subtitle.filename,new_sub_filename))
        if not args.trial:
            os.rename(subtitle.filename,new_sub_filename)

    elif args.verbose:
        print('Video for S{0}E{1} not found'.format(elt[0],elt[1]))
