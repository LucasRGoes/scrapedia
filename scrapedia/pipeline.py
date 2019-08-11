"""The pipeline module is the one responsible for doing the scraping. It is
composed of a producer, a series of stages and a consumer.

	For Scrapedia the producer takes the form of a requester, responsible for
fetching Futpédia's web pages and dispatching its contents to subsequent
stages.

	The first stage following the producer is the seeker, being specialized
for each web page. It searches for specific excerpts on the web pages'
contents to send to the next stage.

	The second stage is the parser, being specialized for each web page like
the seeker. It receives a string and parses it, sending only the data of
interest to the final stage of the pipeline.

	The consumer and final stage of the pipeline is the packer. The packer
receives the data of interest and uses it to build a suitable data schema for
the response.

Classes: Pipeline, PipelineFactory
"""

from enum import Enum

from . import requesters, seekers, parsers, packers


class Pipeline(object):
	"""The Pipeline class follows a Pipeline design pattern proposed by
	Lorenzo Bolla (https://lbolla.info/pipelines-in-python). It is composed of
	a producer, a series of stages and a consumer that are used together to
	scrap a web page.

	Methods: start

	Static Methods: create_producer, create_stage, create_consumer
	"""
	def __init__(self, *args):
		"""Pipeline's constructor. It iterates over the arguments to build the
		pipeline using the chosen functions.

		Parameters
		----------
		*args -- a list of functions used to build the pipeline
		"""
		if len(args) < 3:
			raise ValueError(
				'the minimum number of arguments to build a pipeline is 3')

		if not all(type(x).__name__ == 'function'
				   or type(x).__name__ == 'method' for x in args):
			raise ValueError('all arguments should be functions')

		self._args = args

		# This method can be used to create the pipeline too.
		self.__rewind_pipeline()

	def __rewind_pipeline(self):
		"""A private function that rewinds the pipeline by recreating the used
		generators allowing it to be used again.
		"""
		args = self._args

		consumer = Pipeline.create_consumer(args[-1])
		next(consumer)

		temp = consumer
		for func in reversed(args[1:-1]):
			stage = Pipeline.create_stage(func, temp)
			next(stage)
			temp = stage

		producer = Pipeline.create_producer(args[0], temp)
		next(producer)

		self._pipeline = producer

	def scrap(self, path: str):
		"""Starts the pipeline, executes each stage and returns the results of
		the scraping over the web page served by the chosen path.

		Returns -- the information of interest scraped from the web page
		"""
		try:
			self._pipeline.send(path)
		except StopIteration as res:
			self._pipeline.close()
			self.__rewind_pipeline()
			return res.value

	@staticmethod
	def create_producer(func, next_stage):
		"""Creates a producer, the first stage of a pipeline.
	
		Parameters
		----------
		func -- the function to be executed by the stage
		next_stage -- the stage to be called after the current one ends the
		execution of its function

		Returns -- result of the next stage
		"""
		tmp = (yield)
		try:
			next_stage.send(func(tmp))
		except StopIteration as res:
			next_stage.close()
			return res.value

	@staticmethod
	def create_stage(func, next_stage):
		"""Creates a middle stage of a pipeline.
	
		Parameters
		----------
		func -- the function to be executed by the stage
		next_stage -- the stage to be called after the current one ends the
		execution of its function

		Returns -- result of the next stage
		"""
		tmp = (yield)
		try:
			next_stage.send(func(tmp))
		except StopIteration as res:
			next_stage.close()
			return res.value

	@staticmethod
	def create_consumer(func):
		"""Creates a consumer, the final stage of a pipeline.
	
		Parameters
		----------
		func -- the function to be executed by the consumer

		Returns -- result of the function
		"""
		tmp = (yield)
		return func(tmp)


class DataStructure(Enum):
	DATA_FRAME = 1


class PipelineFactory(object):
	"""A factory to allow easier construction of pipelines.

	Methods: build_pipeline
	"""
	def __init__(self, structure: DataStructure=DataStructure.DATA_FRAME,
				 retry_limit: int=10, backoff_factor: int=1,
				 cache_maxsize: int=10, cache_ttl: int=300):
		"""PipelineFactory's constructor. These parameters are used on the
		construction of the pipelines.

		Parameters
		----------
		structure: DataStructure -- the data structure built at the end of the
		pipeline (default DataStructure.DATA_FRAME)
		retry_limit: int -- number of maximum retrying of requests on
		cases where the status code is in a given set (default 10)
		backoff_factor: int -- the number in seconds that serves as the wait
		time between failed requests, getting bigger on each failure
		(default 1)
		cache_maxsize: int -- maximum number of objects to be stored
		simultaneously on the internal cache (default 10)
		cache_ttl: int -- time to live in seconds for internal caching of
		data (default 300)
		"""
		self.structure = structure
		self.retry_limit = retry_limit
		self.backoff_factor = backoff_factor
		self.cache_maxsize = cache_maxsize
		self.cache_ttl = cache_ttl

	def build(self, target: str) -> Pipeline:
		"""Instantiates a Pipeline object for the chosen target that can be championships, seasons, teams and so forth.

		Returns: Pipeline -- the pipeline built using the components
		associated with the chosen target
		"""
		if target == 'championships':
			seeker = seekers.ChampionshipSeeker()
			parser = parsers.ChampionshipParser()
		elif target == 'seasons':
			seeker = seekers.SeasonSeeker()
			parser = parsers.SeasonParser()
		elif target == 'teams':
			seeker = seekers.TeamSeeker()
			parser = parsers.TeamParser()
		else:
			raise ValueError(
				'The target parameter should be one of championships, seasons'
				' or teams.'
			)

		requester = requesters.FutpediaRequester(
			retry_limit=self.retry_limit, backoff_factor=self.backoff_factor)

		packer = packers.DataFramePacker(
			cache_maxsize=self.cache_maxsize, cache_ttl=self.cache_ttl)

		return Pipeline(requester.fetch, seeker.search, parser.parse,
						packer.pack)
