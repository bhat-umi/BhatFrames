# BhatFrames

For Running the server

```
 uvicorn app.main:app --reload

```

**Droping Database** 

```
\c postgres

```

**Terminate Connections** :

```
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'bhatframe_db'
AND pid <> pg_backend_pid();

```

**Drop the Database** :

```
DROP DATABASE bhatframe_db;

```
