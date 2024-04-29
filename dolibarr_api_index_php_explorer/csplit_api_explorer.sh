#!/bin/bash

INPUT=$1

LIMIT=$( grep -c "^    [a-z]" ${INPUT} )
ADJUST=$(( ${LIMIT} - 1 ))

csplit ${INPUT} "/^    [a-z]/" "{${ADJUST}}"
cexit=$?

if [[ 0 -eq ${cexit} ]]; then
    for XXFILE in $( ls xx* ); do
        HEADLINE=$( head -1 ${XXFILE} | sed -e "s/^ *//" | tr " " "_" )
        mv -i ${XXFILE} "${HEADLINE}"
    done
fi