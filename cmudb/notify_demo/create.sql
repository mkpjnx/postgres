DROP TABLE results;
DROP TABLE commands;
DROP TYPE cmd_type;
DROP TYPE cmd_status;
-- Command schema
CREATE type cmd_type AS ENUM ('cmd_run', 'cmd_abort');
CREATE TABLE IF NOT EXISTS commands (
  id serial PRIMARY KEY,
  cdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  type cmd_type,
  args TEXT,
  target integer
);

-- Result Schema
CREATE type cmd_status AS ENUM ('running', 'success', 'aborted');
CREATE TABLE results (
  id serial PRIMARY KEY,
  cmd_id int REFERENCES commands(id),
  cdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status cmd_status,
  output TEXT
);

-- Function to be called by trigger, sends (target,cmd_id) to 'cmd_update'
CREATE OR REPLACE FUNCTION notify_command_updates() RETURNS TRIGGER AS 
$$
BEGIN
  PERFORM pg_notify('cmd_update',
    CAST(NEW.target AS TEXT)||','||CAST(NEW.id AS TEXT));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Register Trigger
CREATE TRIGGER cmd_notify
AFTER INSERT ON commands FOR EACH ROW
EXECUTE PROCEDURE notify_command_updates();
