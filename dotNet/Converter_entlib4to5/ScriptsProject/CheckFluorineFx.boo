namespace ScriptsProject

import System
import System.IO


def  CheckFluorineReferences(path):
	dirs = Directory.GetDirectories(path)
	files = Directory.GetFiles(path, "*.dll.refresh")
	for file in files:
		NormalizeReference(file)
	
	for dir in dirs:
		CheckFluorineReferences(dir)


private def NormalizeReference(path as string):
	doc = System.IO.File.OpenText(path)
	
	#\Program Files\FluorineFx\Bin\net\3.5\FluorineFx.dll
	#C:\Program Files\FluorineFx\Bin\net\3.5\FluorineFx.dll 
	convertDic = {
		"FluorineFx.dll":"""C:\Program Files\FluorineFx\Bin\net\3.5\FluorineFx.dll""",
		"FluorineFx.ServiceBrowser.dll":"""C:\Program Files\FluorineFx\Bin\net\3.5\FluorineFx.ServiceBrowser.dll""",
		"ICSharpCode.SharpZipLib.dll":"""C:\Program Files\FluorineFx\Bin\net\3.5\ICSharpCode.SharpZipLib.dll""",
		"log4net.dll":"""C:\Program Files\FluorineFx\Bin\net\3.5\log4net.dll""",
		"MySql.Data.dll":"""C:\Program Files\FluorineFx\Bin\net\3.5\MySql.Data.dll"""
		}
	