#!/bin/bash

src_db=$1
dst_db=$2
pgdump=`which pg_dump`
pgrestore=`which postgis_restore.pl`
psql=`which psql`
if [ $# -lt 2 -o $# -gt 2 ]; then
	echo -e "Create a database with owner\n";
	echo -e "username\$ psql \n"
	echo -e "PSQL console"
	echo -e "username# create database db_name owner owner_name; \n"
	echo "Usage: dbdump.sh src_db dst_db"
	exit 1;
fi

# dump the database
$pgdump -Fc $src_db > $src_db'.dump'
# restore the database to dst_db
 # -C -d $dst_db $src_db'.dump'
$pgrestore $src_db'.dump' | $psql $dst_db
# remove the original dump file
# rm -f $src_db'.dump'
exit 0;