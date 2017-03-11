import houseweb.db
import logging
import os
import time
import datetime
import logging

from evohomeclient2 import EvohomeClient

_REPEAT_INTERVAL = 60 * 15

def get_time_since_update(cur):
    sql = "SELECT MAX(date_added) FROM data"
    cur.execute(sql)
    dt = cur.fetchone()[0]

    if dt is None:
        return _REPEAT_INTERVAL

    delta = datetime.datetime.now() - dt
    return delta.seconds

def update_evohome(cur):
    client = EvohomeClient(os.environ['EVOHOME_USER'], os.environ['EVOHOME_PASSWORD'])
    actual_sql = "INSERT INTO data (data_source_id, date_added, field, is_target, value) VALUES (1, current_timestamp, %s, false, %s)"
    target_sql = "INSERT INTO data (data_source_id, date_added, field, is_target, value) VALUES (1, current_timestamp, %s, true, %s)"

    for device in client.temperatures():
        if device['thermostat'] == 'DOMESTIC_HOT_WATER':
            cur.execute(actual_sql, ("Hot Water", "%d" % (device['temp'] * 100)))

        if device['thermostat'] == 'EMEA_ZONE':
            cur.execute(actual_sql, (device['name'], "%d" % (device['temp'] * 100)))
            cur.execute(target_sql, (device['name'], "%d" % (device['setpoint'] * 100)))

def main():
    logging.basicConfig()
    logger = logging.getLogger('updater')

    conn = houseweb.db.get_connection()
    cur = conn.cursor()

    sleep_time = _REPEAT_INTERVAL - get_time_since_update(cur)
    if sleep_time > 0:
        logger.info('Pre-start sleep for %d seconds',sleep_time)
        time.sleep(sleep_time)
    
    while True:
        logger.info('Updating EvoHome data')
        update_evohome(cur)

        conn.commit()

        logger.info('Sleeping for %d', _REPEAT_INTERVAL)
        time.sleep(_REPEAT_INTERVAL)


    cur.close()
    conn.close()

if __name__ == '__main__':
    main()
