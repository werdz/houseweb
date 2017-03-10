import psycopg2
import os
import urllib.parse

urllib.parse.uses_netloc.append("postgres")

def get_connection():
	"""Return a connection to the application database.
	"""
	url = urllib.parse.urlparse(os.environ['DATABASE_URL'])

	if url.username is not None and url.password is not None and url.hostname is not None and url.port is not None:
		conn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname, port=url.port)
	else:
		conn = psycopg2.connect(database=url.path[1:])

	return conn
