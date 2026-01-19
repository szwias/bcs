#!/bin/bash
backup
cd /home/szymon/Desktop/bcs/ || exit
cp bcs/baza/baza_*.sql bcs_dump.sql
echo "✅ Current database dump copied"
sed -i 's/\bpostgres\b/projectuser/g' bcs_dump.sql
echo "✅ Changed dump's user to 'projectuser'"
cp bcs_dump.sql bcs_package/src/bcs_dump.sql
echo "✅ Database copied to 'bcs_package'"
