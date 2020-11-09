git-sindria:
	python3 -m compileall -f git-sindria.py
	#python3 -m compileall -f -d bin -b git-sindria.py

clean:
	rm -rf __pycache__
	#rm git-sindria.pyc