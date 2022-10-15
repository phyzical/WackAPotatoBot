install:
	brew install zlib
	export LDFLAGS="-L/usr/local/opt/zlib/lib"
	export CPPFLAGS="-I/usr/local/opt/zlib/include"
	export PKG_CONFIG_PATH="/usr/local/opt/zlib/lib/pkgconfig"
	python3 -m pip install -U pip
	python3 -m pip install -r requirements.txt
run:
	python3  main.py
update-requirements:
	pip freeze > requirements.txt