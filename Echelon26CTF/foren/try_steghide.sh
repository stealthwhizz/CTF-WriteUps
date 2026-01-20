#!/bin/bash
for pass in "SNIT_CF" "Mentor" "Vallabhbhai" "National" "Institute" "Technology" "Classified" "APPROVED" "aad7bae0" ""; do
    echo "Trying: '$pass'"
    steghide extract -sf Mentor_Chellenge_fixed.jpg -p "$pass" -f 2>&1 | grep -E "(wrote|could not)" | head -1
done
