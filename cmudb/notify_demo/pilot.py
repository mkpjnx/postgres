#!/usr/bin/python3
import psycopg
import sys

if len(sys.argv) != 4:
    print(sys.argv)
    print("Usage: pilot.py cmd_type cmd_arg target")
    exit(0)

cmd_type = sys.argv[1]
cmd_arg = sys.argv[2]
target = int(sys.argv[3])

# Connect to an existing database
with psycopg.connect("dbname=notify_demo user=postgres") as conn:
    # Open a cursor to perform database operations
    with conn.cursor() as cur:
        # Query the database and obtain data as Python objects.
        cur.execute(
            "INSERT INTO commands (type, args, target) "
            "VALUES ('%s','%s',%s);" % (cmd_type, cmd_arg, target))
