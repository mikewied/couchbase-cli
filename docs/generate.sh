#!/bin/bash
for filename in couchbase-cli*; do
        echo $filename
		#ext="${filename##*.}"
		name="${filename%.*}"
		#echo $name
		#echo $ext
		asciidoc -o ../man/${name}.html $filename
		#xmlto man ../man/${name}.xml -o ../man
		#rm ../man/${name}.xml
done

#asciidoc -b docbook -d manpage -f asciidoc.conf couchbase-cli-cluster-edit.txt
#xmlto man couchbase-cli-cluster-edit.xml
#rm couchbase-cli-cluster-edit.xml
