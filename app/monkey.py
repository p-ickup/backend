"""Ensure gevent monkey patching happens before any other imports"""
from gevent import monkey
monkey.patch_all()