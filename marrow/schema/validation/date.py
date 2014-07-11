# encoding: utf-8

from datetime import datetime, date, time, timedelta

from .base import Instance, Range


class Date(Instance, Range):
	instance = (datetime, date)


class Time(Instance, Range):
	instance = (datetime, time)


class DateTime(Instance, Range):
	instance = (datetime, )


class Delta(Instance, Range):
	instance = (timedelta, )
