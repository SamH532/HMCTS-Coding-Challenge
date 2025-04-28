#!/bin/bash

createdb -h localhost -p 5432 -U postgres taskdb
psql -h localhost -p 5432 -U postgres taskdb -c 'CREATE TABLE tasktable (taskid int unique, tasktitle varchar(127), taskdescription varchar(255), taskstatus varchar(15), taskdeadline(15))'
