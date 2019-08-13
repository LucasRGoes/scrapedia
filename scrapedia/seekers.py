"""The seekers module holds all classes and functions related to searching specific excerpts of text on a web page's HTML file.

ABCs: Seeker

Classes: ChampionshipSeeker, GameSeeker, SeasonSeeker, TeamSeeker
"""

import abc

from bs4 import BeautifulSoup

from .errors import ScrapediaSearchError


class Seeker(abc.ABC):
	"""An abstract base class for other seeker classes to implement.

	Methods: search
	"""
	@abc.abstractmethod
	def search(self, content: bytes):
		"""Searches web page's content for excerpts that hold data of interest.

		Parameters
		----------
		content: bytes -- the raw HTML text to be searched

		Returns -- the raw data that holds the information to be extracted
		"""
		pass


class ChampionshipSeeker(Seeker):
	"""A seeker class specialized in finding data concerning championships.

	Extends: Seeker

	Methods: search
	"""
	def __init__(self):
		"""ChampionshipSeeker's constructor."""
		pass

	def search(self, content: bytes) -> str:
		"""Search web page's content for raw data concerning championships.

		Parameters @Seeker
		Returns @Seeker
		"""
		soup = BeautifulSoup(content, 'html.parser')
		raw_data = soup.find(name='script', attrs={'type': 'text/javascript',
												   'language': 'javascript',
												   'charset': 'utf-8'})
		if raw_data is None:
			raise ScrapediaSearchError('The expected championships raw data'
									   ' could not be found.')

		stt = raw_data.string.find('[{')
		end = raw_data.string.find('}]') + 2
		return raw_data.string[stt:end]


class GameSeeker(Seeker):
	"""A seeker class specialized in finding data concerning a season's games.

	Extends: Seeker

	Methods: search
	"""
	def __init__(self):
		"""GameSeeker's constructor."""
		pass

	def search(self, content: bytes) -> str:
		"""Search web page's content for raw data concerning a season's games.

		Parameters @Seeker
		Returns @Seeker
		"""
		soup = BeautifulSoup(content, 'html.parser')

		# Searches for HTML with tables
		raw_games = soup.find_all(name='li', class_='lista-classificacao-jogo')

		if raw_games is None:
			raise ScrapediaParseError('The expected season\'s games raw data'
									  ' could not be found.')

		print(raw_games)

		return raw_games


class SeasonSeeker(Seeker):
	"""A seeker class specialized in finding data concerning a championship's
	seasons.

	Extends: Seeker

	Methods: search
	"""
	def __init__(self):
		"""SeasonSeeker's constructor."""
		pass

	def search(self, content: bytes) -> str:
		"""Search web page's content for raw data concerning a championship's
		seasons.

		Parameters @Seeker
		Returns @Seeker
		"""
		soup = BeautifulSoup(content, 'html.parser')
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
	"""A seeker class specialized in finding data concerning teams.

	Extends: Seeker

	Methods: search
	"""
	def __init__(self):
		"""TeamSeeker's constructor."""
		pass

	def search(self, content: bytes) -> list:
		"""Search web page's content for raw data concerning teams.

		Parameters @Seeker
		Returns @Seeker
		"""
		soup = BeautifulSoup(content, 'html.parser')
		raw_data = soup.find_all(name='li',
								 attrs={'itemprop': 'itemListElement'})

		if not len(raw_data) > 0:
			raise ScrapediaSearchError('The expected teams raw data could not'
									   ' be found.')

		return raw_data
