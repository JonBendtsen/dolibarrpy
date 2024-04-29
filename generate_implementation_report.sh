#!/bin/bash

INPUT=$1


IFS="
"

echo -e "#COUNT\tENDPOINT" > "implementation_status.csv"
for ENDPOINT in $( grep -ir " /" "${INPUT}" | grep -E "delete|get|patch|post|put" | cut -d":" -f2 | sed -e "s/^ *//" ); do
    FOUND=$( grep -c -e "@endpoint '${ENDPOINT}'$" dolibarrpy/Dolibarrpy.py )
    echo -e "${FOUND}\t${ENDPOINT}" >> "implementation_status.csv"
done
