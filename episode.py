import re, pathlib

# regex to find season and episode info on files
re_season = re.compile(r'([Ss][easonEASON]*)[ .-]*([0-9]{2})')
re_episode = re.compile(r'([Ee][pisodeEPISODE]*)[ .-]*([0-9]{2})')

class Episode:
    '''This class stores information about an episode.
Just feed it a filename, and it will use module re (regexp) to find out what season and episode the file is. 
'''
    def __init__(self,filename):
        self.filename = filename
        self.season = self.get_season()
        self.episode = self.get_episode()
        self.suffix = self.get_suffix()
        return

    def __str__(self):
        return 'S{0}E{1} : {2}'.format(self.season,self.episode,self.filename)

    def get_season(self):
        season = re_season.search(self.filename)
        if not season: return
        return season.group(2) if season.re.groups == 2 else None

    def get_episode(self):
        episode = re_episode.search(self.filename)
        if not episode: return
        return episode.group(2) if episode.re.groups == 2 else None

    def get_suffix(self):
        return pathlib.PosixPath(self.filename).suffix.strip('.')

    def subtitle_rename(self,video):
        return re.sub(video.suffix,self.suffix,video.filename)
