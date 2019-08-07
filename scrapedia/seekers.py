"""Scrapedia's seekers are the pipeline's stage where the requested
information is analyzed and reduced so that only the interesting portions
remain and are returned.

ABCs: Seeker

Classes: ChampionshipSeeker, SeasonSeeker, TeamSeeker
"""

import abc

from bs4 import BeautifulSoup

from .errors import ScrapediaSearchError


class Seeker(abc.ABC):
	"""An abstract base class for other seeker classes to implement.

	Methods: search
	"""
	@abc.abstractmethod
	def search(self, txt: str) -> str:
		"""Search text for raw data.

		Parameters
		----------
		txt: str -- the text to be searched

		Returns
		-------
		raw_data: str -- the raw data of interest
		"""
		pass


class ChampionshipSeeker(Seeker):
	"""A seeker class specialized in finding data about championships.

	Extends: Seeker

	Methods: search
	"""
	def __init__(self):
		pass

	def search(self, txt: str) -> str:
		"""Search text for raw data concerning championships.

		Parameters @Seeker
		Returns @Seeker
		"""
		soup = BeautifulSoup(txt, 'html.parser')
		raw_data = soup.find(name='script', attrs={'type': 'text/javascript',
												   'language': 'javascript',
												   'charset': 'utf-8'})
		if raw_data is None:
			raise ScrapediaSearchError('The expected championships raw data'
									   ' could not be found.')

		stt = raw_data.string.find('[{')
		end = raw_data.string.find('}]') + 2
		return raw_data.string[stt:end]


class SeasonSeeker(Seeker):
	"""A seeker class specialized in finding data about a championship's
	seasons.

	Extends: Seeker

	Methods: search
	"""
	def __init__(self):
		pass

	def search(self, txt: str) -> str:
		"""Search text for raw data concerning a championship's seasons.

		Parameters @Seeker
		Returns @Seeker
		"""
		soup = BeautifulSoup(txt, 'html.parser')
		raw_data = soup.find(
			'script',
			string=lambda s: s is not None and s.find('static_host') != -1
		)

		if raw_data is None:
			raise ScrapediaSearchError('The expected championship\'s seasons'
									   ' raw data could not be found.')

		stt = raw_data.string.find('{"campeonato":')
		end = raw_data.string.find('}]};') + 3
		return raw_data.string[stt:end]


class TeamSeeker(Seeker):
	"""A seeker class specialized in finding data about teams.

	Extends: Seeker

	Methods: search
	"""
	def __init__(self):
		pass

	def search(self, txt: str) -> str:
		"""Search text for raw data concerning teams.

		Parameters @Seeker
		Returns @Seeker
		"""
		soup = BeautifulSoup(txt, 'html.parser')
		raw_data = soup.find_all(name='li',
								 attrs={'itemprop': 'itemListElement'})

		if not len(raw_data) > 0:
			raise ScrapediaSearchError('The expected teams raw data could not'
									   ' be found.')

		return raw_data
