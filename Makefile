git-sindria:
	python3 -m compileall -f git-sindria.py
	#python3 -m compileall -f -d bin -b git-sindria.py

install:
	mkdir -p /opt
	mkdir -p /opt/git-sindria
	cp __pycache__/*.pyc /opt/git-sindria/git-sindria.pyc
	chmod +x /opt/git-sindria/git-sindria.pyc
	cp git-sindria.sh /usr/local/bin/git-sindria
	chmod +x /usr/local/bin/git-sindria

clean:
	rm -rf /opt/git-sindria
	rm -f /usr/local/bin/git-sindria
	rm -rf __pycache__
	#rm git-sindria.pyc