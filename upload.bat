python.exe setup.py bdist_wheel
python.exe -m twine upload dist/*
rd /s /q build
rd /s /q dist
rd /s /q PicImageSearch.egg-info
