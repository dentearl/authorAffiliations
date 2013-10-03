SHELL:=/bin/bash -e
export SHELLOPTS=pipefail

.PHONY= all demo clean

all: bin/author_affiliations

bin/author_affiliations: src/author_affiliations.py
	mkdir -p $(dir $@)
	cp $< $@.tmp
	chmod 755 $@.tmp
	mv $@.tmp $@

demo: pasteIntoPaper.txt

pasteIntoPaper.txt: bin/author_affiliations example/affiliations.txt
	$^ > $@.tmp
	mv $@.tmp $@

clean:
	rm -rf  bin/ pasteIntoPaper.txt
