# Contain custom execption

class StorageDataCorruptedError(Exception):
	"""Raised when json file is corrupted"""
	pass