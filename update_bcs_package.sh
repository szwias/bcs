#!/bin/bash
backup
cd /home/szymon/Desktop/bcs/ || exit
cp bcs/baza/baza_*.sql bcs_package/src/bcs_dump.sql
sed -i 's/\bpostgres\b/projectuser/g' bcs_package/src/bcs_dump.sql
echo "✅ Package updated"
