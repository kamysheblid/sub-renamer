import re, pathlib, logging

# regex to find season and episode info on files
re_season = re.compile(r'([Ss](eason|EASON|eries|ERIES)*)[ \.-]*([0-9]{1,2})')
re_episode = re.compile(r'([Ee](pisode|pISODE)*)[ .-]*([0-9]{1,2})')

class Episode:
    '''This class stores information about an episode.
Just feed it a filename, and it will use module re (regexp) to find out what season and episode the file is. 
'''
    def __init__(self,filename,suffix=None):
        self.file = pathlib.PosixPath(filename)
        self.filename = self.file.name
        self.season = self.get_season()
        self.episode = self.get_episode()
        self.suffix = self.get_suffix(suffix)
        return
    def __str__(self):
        return 'S{0}E{1} : {2}'.format(self.season,self.episode,self.filename)
    def __repr__(self):
        return self.__str__()
    def __gt__(self, ep):
        return self.filename > ep.filename
    def get_season(self):
        season_search = re_season.search(self.filename)
        logging.debug(f'Result for season search: {season_search}')
        if not season_search: return None
        season = season_search.groups()[-1]
        logging.debug(f'Season result: {season}')
        return int(season)
    def get_episode(self):
        episode_search = re_episode.search(self.filename)
        logging.debug(f'Result for episode search: {episode_search}')
        if not episode_search: return None
        episode = episode_search.groups()[-1]
        logging.debug(f'Episode result: {episode}')
        return int(episode)
    def get_suffix(self,possible_suffixes):
        for suf in possible_suffixes:
            if suf in self.filename:
                return suf
    def new_filename(self, video):
        if video.suffix and self.suffix:
            logging.debug('sjia')
            new_filename = video.filename.replace(video.suffix,self.suffix)
            return new_filename
        else:
            logging.error(f'{self} and {video} failed rename function')
        return None
