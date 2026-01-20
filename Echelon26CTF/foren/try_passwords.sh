#!/bin/bash
for pass in "svnit" "SVNIT" "yashmakwana" "Yashmakwana" "YASHMAKWANA" "mentor" "vallabhbhai"; do
    echo "Trying password: '$pass'"
    steghide extract -sf Mentor_Chellenge_fixed.jpg -p "$pass" -f 2>&1 | grep -E "(wrote|could not)" | head -1
done
