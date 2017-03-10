import houseweb.db
import argparse

create_schema_sql = """
CREATE TABLE data_source (
	data_source_id bigserial primary key,
	data_source_name varchar(20) not null
);

INSERT INTO data_source (data_source_name) VALUES ('Evohome'), ('Efergy');

CREATE TABLE data (
	data_id bigserial primary key,
	data_source_id bigint references data_source (data_source_id),
	date_added timestamp not null,
	field varchar(100) not null, 
	value int not null
);

CREATE TABLE users (
	user_id bigserial primary key,
	username varchar(100) not null,
	password_hash varchar(500) not null,
	enabled boolean not null
);
"""

def create_db():
	conn = houseweb.db.get_connection()
	cur = conn.cursor()
	cur.execute(create_schema_sql)
	conn.commit()
	cur.close()
	conn.close()

def main():
	parser = argparse.ArgumentParser(description='Install the database schema')
	parser.add_argument('command', help="Command to run (create)",metavar='CMD')
	args = parser.parse_args()

	if args.command == "create":
		create_db()

if __name__ == '__main__':
	main()