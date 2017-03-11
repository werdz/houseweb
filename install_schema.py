import houseweb.db
import argparse

drop_schema_sql = """
DROP TABLE data;
DROP TABLE data_source;
"""

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
	is_target boolean not null,
	value int not null
);

CREATE TABLE users (
	user_id bigserial primary key,
	username varchar(100) not null,
	password_hash varchar(500) not null,
	enabled boolean not null
);
"""

def exec_sql(sql):
	conn = houseweb.db.get_connection()
	cur = conn.cursor()
	cur.execute(create_schema_sql)
	conn.commit()
	cur.close()
	conn.close()

def create_db():
	exec_sql(create_schema_sql)

def drop_db():
	exec_sql(drop_schema_sql)

def main():
	parser = argparse.ArgumentParser(description='Install the database schema')
	parser.add_argument('command', help="Command to run (create, drop)",metavar='CMD')
	args = parser.parse_args()

	if args.command == "create":
		create_db()
	elif args.command == "drop":
		drop_db()


if __name__ == '__main__':
	main()