from datetime import datetime, date, time, timedelta

from . import Instance, Range


class Date(Instance, Range):
	"""Ensure the given object can qualify as a date instance within a given range.
	
	That is, one of datetime or date from the datetime module.
	"""
	
	instance = (datetime, date)


class Time(Instance, Range):
	"""Ensure the given object can qualify as a time instance within a given range.
	
	That is, one of datetime or time from the datetime module.
	"""
	instance = (datetime, time)


class DateTime(Instance, Range):
	"""Ensure the given instance is a datetime object within a given range."""
	instance = (datetime, )


class Delta(Instance, Range):
	"""Ensure the given instance is a timedelta object within a given range."""
	instance = (timedelta, )
