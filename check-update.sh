#!/bin/sh
curl -s "https://pari.math.u-bordeaux.fr/download.html" |grep "revision" |sed -e 's,.*">,,;s,<.*,,;'

