#BUILD reads

### Notes for running on c9.io
-starting and signing into postgres db (build_reads)
    $ sudo sudo -u postgres psql build_reads

-starting server (points to http://build-reads-go-bears.c9users.io:8080/ in browser)
    $ python server.py

-running SqlAlchemy access to postgres db
    $ python model.py

-alternatively you can run model.py in python's interactive mode to add records to db
    $ python -i model.py

