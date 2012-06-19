namespace FindXsltError

import System
import System.Collections
import System.Drawing
import System.Windows.Forms
import System.Xml.Linq
import System.Linq.Enumerable
import System.Collections.Generic
import System.IO

partial class MainForm:
	
	private defaultColor = Color.Black
	
	public def constructor():
		// The InitializeComponent() call is required for Windows Forms designer support.
		InitializeComponent()
		self.defaultColor = self.displayLogRichTextBox.SelectionColor

	
	private def CheckXsltButtonClick(sender as object, e as System.EventArgs):
		errors = 0
		if not string.IsNullOrEmpty(self.pathTextBox.Text) and Directory.Exists(self.pathTextBox.Text):
			NavigateDirectoryCheck(self.pathTextBox.Text, errors)
		elif self.folderBrowserDialog.ShowDialog() == DialogResult.OK:
			NavigateDirectoryCheck(self.folderBrowserDialog.SelectedPath, errors)
		LogErrorUI(string.Format("Problems found:{0}\r\n", errors));
				
		
	private def LogInfoUI(msg as string):
		self.displayLogRichTextBox.SelectionColor = self.defaultColor
		self.displayLogRichTextBox.SelectedText = msg
	
	private def LogErrorUI(msg as string):
		self.displayLogRichTextBox.SelectionColor = Color.Red
		self.displayLogRichTextBox.SelectedText = msg
		
	private def  NavigateDirectoryCheck(path as string, ref errors as int):
		try:
			dirs = Directory.GetDirectories(path)
			files = Directory.GetFiles(path, "*.xslt")
		except:
			LogErrorUI(string.Format("ERROR dir1:{0}", path))
			return
			
		for file in files:
			try:
				CheckConfigs(file, errors)
			except ex as Exception:
				LogErrorUI(string.Format("ERROR file:{0}", file))
		for dir in dirs:
			if not Directory.Exists(dir):
				continue
			NavigateDirectoryCheck(dir, errors)

	
	private def CheckConfigs(path as string, ref errors as int):
		LogInfoUI("xslt file " + path +"\n")
		try:
			doc = XDocument.Load(path)
		except:
			LogErrorUI(string.Format("ERROR open file:{0}", path))
			return
		
		nodes = [node for node as XElement in doc.Descendants() if node.HasAttributes]
		for node as XElement in nodes:
			for attr as XAttribute in node.Attributes():
				if attr.Value == "editor" and node.Name.LocalName == "div":
					errors += 1
					#if the div(editor) is found it is not in a CDATA 
					#that is a potential problem variety
					msg = string.Format("Found {0} at path:{1}\r\n",  attr.Value, path)
					LogErrorUI(msg)
		

[STAThread]
public def Main(argv as (string)) as void:
	Application.EnableVisualStyles()
	Application.SetCompatibleTextRenderingDefault(false)
	Application.Run(MainForm())

