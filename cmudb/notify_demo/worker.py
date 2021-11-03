from os import times
import psycopg
from psycopg.rows import dict_row
import select, sys

target = sys.argv[1]


def get_command(cmd_id):
    global curs
    curs.execute("SELECT * FROM commands WHERE id = %s;"%(cmd_id))
    rows = curs.fetchall()
    return rows

def run_command(cmd):
    global curs
    output = cmd['args']
    status = ''
    if cmd['type'] == 'cmd_run':
        status = 'success'
    else:
        status = 'aborted'
    curs.execute(
            "INSERT INTO results (cmd_id, status, output) "
            "VALUES (%s,'%s','%s');" % (cmd['id'], status, output))

# Connect to an existing database
conn = psycopg.connect("dbname=notify_demo user=postgres", autocommit=True)
curs = conn.cursor(row_factory=dict_row)
curs.execute("LISTEN cmd_update;")

print("Waiting for notifications on channel 'cmd_update'")
notifs = conn.notifies()

#TODO: We should bootstrap to catch any commands we missed?

while True:
    to_execute = []
    for notify in notifs:
        cmd_target, cmd_id = notify.payload.split(',')
        print("Got NOTIFY:", notify.pid, notify.channel, notify.payload)
        
        # Filter out commands that are not meant for us
        if(cmd_target != target):
            print("Skipping...")
            continue

        to_execute += get_command(cmd_id)
        break
    for cmd in to_execute:
        print("Executing command ", cmd)
        run_command(cmd)
