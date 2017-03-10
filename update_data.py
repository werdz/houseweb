import houseweb.db
import logging
import os

from evohomeclient2 import EvohomeClient

def update_evohome(cur):
	client = EvohomeClient(os.environ['EVOHOME_USER'], os.environ['EVOHOME_PASSWORD'])
	sql = "INSERT INTO data (data_source_id, date_added, field, value) VALUES (1, current_timestamp, %s, %s)"

	for device in client.temperatures():
		if device['thermostat'] == 'DOMESTIC_HOT_WATER':
			cur.execute(sql, ("Actual Hot Water", "%d" % (device['temp'] * 100)))

		if device['thermostat'] == 'EMEA_ZONE':
			cur.execute(sql, ("Actual %s" % device['name'], "%d" % (device['temp'] * 100)))
			cur.execute(sql, ("Target %s" % device['name'], "%d" % (device['setpoint'] * 100)))

def main():
	conn = houseweb.db.get_connection()
	cur = conn.cursor()
	update_evohome(cur)
	conn.commit()
	cur.close()
	conn.close()

if __name__ == '__main__':
	main()
