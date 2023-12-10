You can use importer-html.py and importer-log.py to import text log from SIM_Forwarder old version to database version.

How to use:
	You should first edit your target phone number in phonenum.txt
	The target database is ../mydatabase.db, you may need to copy exmaple.db to mydatabase.db
Then, Run:
	python importer-html.py floder-path-of-html
	python importer-log.py floder-path-of-log
Finally:
	in db_commands.txt, some sql commands are provided to optimize the database.