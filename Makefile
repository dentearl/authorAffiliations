SHELL:=/bin/bash -e
export SHELLOPTS=pipefail

.PHONY= all demo clean

all: bin/authorAffiliations.py

bin/authorAffiliations.py: src/authorAffiliations.py
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

demo: pasteIntoPaper.txt

pasteIntoPaper.txt: bin/authorAffiliations.py example/affiliations.txt
	$^ > $@.tmp
	mv $@.tmp $@

clean:
	rm -rf  bin/ pasteIntoPaper.txt
