from cx_Freeze import setup, Executable
base = None
#Remplacer "monprogramme.py" par le nom du script qui lance votre programme
executables = [Executable("Interface_global.py", base=base)]
#Renseignez ici la liste complète des packages utilisés par votre application
packages = ["idna","opcua","matplotlib","numpy","PIL",
            "tkinter","xlrd","xlsxwriter","xlwt","xlutils"
            "time","datetime","openpyxl","random","functools","simpy"]
options = {
    'build_exe': {    
        'packages':packages,
    },
}
#Adaptez les valeurs des variables "name", "version", "description" à votre programme.
setup(
    name = "Jumeau Numérique",
    options = options,
    version = "0.1",
    description = 'Voici le jumeau numérique',
    executables = executables
)
#python setup.py build