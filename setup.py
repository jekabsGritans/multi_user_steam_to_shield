from subprocess import call
with open('requirements.txt','r') as f:
	mods = f.read().split('\n')
for mod in mods:
	call(f'pip install {mod}')