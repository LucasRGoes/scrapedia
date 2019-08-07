"""Scrapedia's source of exception classes.

Classes: ScrapediaError, ScrapediaFetchError, ScrapediaParseError,
ScrapediaTransformError, ScrapediaNotFoundError
"""

class ScrapediaError(Exception):
	"""Generic error to be implemented by further classes in order to uncouple
	Scrapedia's exceptions from others.
	"""
	pass


class ScrapediaFetchError(ScrapediaError):
	"""To be raised whenever an error concerning HTTP requests of Futpédia's
	webpages occurs.
	"""
	pass


class ScrapediaParseError(ScrapediaError):
	"""To be raised whenever an error related to parsing occurs like missing
	expected content from a fetched page.
	"""
	pass


class ScrapediaTransformError(ScrapediaError):
	"""To be raised whenever an error related to the transformation of parsed content occurs.
	"""
	pass


class ScrapediaNotFoundError(ScrapediaError):
	"""To be raised whenever there is an error where a chosen team, game or championship data is not found on the requested or cached data."""
	pass


class ScrapediaSearchError(ScrapediaError):
	"""To be raised whenever a search stage fails."""
	pass
