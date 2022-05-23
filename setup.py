import cx_Freeze

executables = [cx_Freeze.Executable('dino.py')]

cx_Freeze.setup(
	name = "Dino Game",
	options = {
		'build_exe':{'packages':['pygame'], 
					 'include_files':['img', 'sounds']}
	},
	executables = executables
)