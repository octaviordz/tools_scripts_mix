namespace Converter_entlib4to5

import System
import System.Collections
import System.Drawing
import System.Windows.Forms
import System.Xml.Linq
import System.Linq.Enumerable
import System.Collections.Generic
import System.IO

partial class MainForm:
	public def constructor():
		// The InitializeComponent() call is required for Windows Forms designer support.
		InitializeComponent()
	
	private def MainFormLoad(sender as object, e as System.EventArgs):
		// TODO: Add constructor code after the InitializeComponent() call.
		pass

	
	private def  NavigateDirectoryLookProjects(path):
		dirs = Directory.GetDirectories(path)
		files = Directory.GetFiles(path, "*.csproj")
		for file in files:
			CheckProjectFile(file)
			
		for dir in dirs:
			NavigateDirectoryLookProjects(dir)

	
	private def CheckProjectFile(path as string):
		self.displayLogRichTextBox.Text += "Project file " + path +"\n"
		doc = XDocument.Load(path)
		ns = XNamespace.Get("http://schemas.microsoft.com/developer/msbuild/2003")		
//		navigator = doc.CreateNavigator()
//		navigator.MoveToFollowing(XPathNodeType.Element);
//		dic = navigator.GetNamespacesInScope(XmlNamespaceScope.All);
		entLib4 = ["Microsoft.Practices.EnterpriseLibrary.Common, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.EnterpriseLibrary.Logging, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL", 
			"Microsoft.Practices.EnterpriseLibrary.ExceptionHandling, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.EnterpriseLibrary.ExceptionHandling.Logging, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.Unity, Version=1.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			#"Microsoft.Practices.Unity.Interception.dll",
			"Microsoft.Practices.Unity.Configuration, Version=1.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			#"Microsoft.Practices.ServiceLocation.dll",
			"Microsoft.Practices.ObjectBuilder2, Version=2.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL"]
			
		entLib5 = ["Microsoft.Practices.EnterpriseLibrary.Common, Version=5.0.505.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.EnterpriseLibrary.Logging, Version=5.0.505.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL", 
			"Microsoft.Practices.EnterpriseLibrary.ExceptionHandling, Version=5.0.505.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.EnterpriseLibrary.ExceptionHandling.Logging, Version=5.0.505.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.Unity, Version=2.1.505.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			#"Microsoft.Practices.Unity.Interception.dll",
			"Microsoft.Practices.Unity.Configuration, Version=2.1.505.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			#"Microsoft.Practices.ServiceLocation.dll",
			""]
		
		changes = 0
		for itemGroup in doc.Descendants(ns + "ItemGroup"):
			for node in itemGroup.Elements(ns + "Reference").ToList():
					attr =node.Attribute("Include")
					if node.HasElements:
						target = node.Element(ns + "RequiredTargetFramework")
						if target is not null and (target.Value == "3.5" or target.Value == "3.0"):
							changes += 1
							target.Remove()
							self.displayLogRichTextBox.Text += "U " + path +" Remove RequiredTargetFramework for "+ attr.Value + "\n"
						else:
							msg = attr.Value + " ::"+ node.Value + "\n"
							self.displayLogRichTextBox.Text += "Warning " + path +" "+ msg
					elif attr.Value in entLib4:
						newvalue = entLib5[entLib4.IndexOf(attr.Value)]
						if newvalue == "":
							node.Remove()
						else:
							node.SetAttributeValue("Include", newvalue)
						changes += 1
						self.displayLogRichTextBox.Text += "U " + attr.Value + " to " +newvalue + "\n"
		if changes > 0:			
			doc.Save(path)
	
	private def ProjectsButtonClick(sender as object, e as System.EventArgs):
		#rootPath = """C:\Path\To\Project\"""
		rootPath = self.pathTextBox.Text
		NavigateDirectoryLookProjects(rootPath)
				
	private def ConfigsButtonClick(sender as object, e as System.EventArgs):
		#rootPath = """C:\Path\To\Project\"""
		rootPath = self.pathTextBox.Text
		NavigateDirectoryConfigs(rootPath)
		
	private def AssemblyInfoButtonClick(sender as object, e as System.EventArgs):
		#rootPath = """C:\Path\To\Project\"""
		rootPath = self.pathTextBox.Text
		NavigateDirectoryAssemblyInfo(rootPath)
		
	private def  NavigateDirectoryConfigs(path):
		dirs = Directory.GetDirectories(path)
		files = Directory.GetFiles(path, "*.config")
		for file in files:
			CheckConfigs(file)
			
		for dir in dirs:
			NavigateDirectoryConfigs(dir)

	
	private def CheckConfigs(path as string):
		self.displayLogRichTextBox.Text += "Config file " + path +"\n"
		doc = XDocument.Load(path)
		
		entLib4 = ["Microsoft.Practices.EnterpriseLibrary.Common, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.EnterpriseLibrary.Logging, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL", 
			"Microsoft.Practices.EnterpriseLibrary.ExceptionHandling, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.EnterpriseLibrary.ExceptionHandling.Logging, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.Unity, Version=1.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			#"Microsoft.Practices.Unity.Interception.dll",
			"Microsoft.Practices.Unity.Configuration, Version=1.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			#"Microsoft.Practices.ServiceLocation.dll",
			"Microsoft.Practices.ObjectBuilder2, Version=2.1.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35, processorArchitecture=MSIL",
			"Microsoft.Practices.EnterpriseLibrary.Data"]

		looked = [item.Split(char(','))[0] for item as string in entLib4]
		
		def IsLookedPart(str as string):
			for l in looked:
				if str.Contains(l):
					return true
			return false
		
		#, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35
		def TrimFromVersion(str as string):
			parts = str.Split(char(','))
			pk, cul, ver = parts[-1:], parts[-2:], parts[-3:]
			publicKey, culture, version = pk[0], cul[0], ver[0]
			hasPublicKey = publicKey.Trim().StartsWith("PublicKeyToken")
			hasCulture = culture.Trim().StartsWith("Culture")
			hasVersion = version.Trim().StartsWith("Version")
			sections = publicKey, culture, version
			sum = 0
			for section in sections:
				sum += section.Length
				
			if hasPublicKey and hasCulture and hasVersion:
				#count = sections.Sum({s as string | s.Length})
				count = sum
				length = str.Length - (count + 3)
				result = str[0: length]
				return result				
			return null
		
		changes = 0	
		nodes = [node for node as XElement in doc.Descendants() if node.HasAttributes]
		for node as XElement in nodes:
			for attr as XAttribute in node.Attributes():
				if IsLookedPart(attr.Value):
					newvalue = TrimFromVersion(attr.Value)
					if newvalue is not null:
						changes+=1
						attr.SetValue(newvalue)
						self.displayLogRichTextBox.Text += "Found " + attr.Value + " NV:"+ newvalue +"\n"
		if changes > 0:
			doc.Save(path)		
			
		
	private def  NavigateDirectoryAssemblyInfo(path):
		dirs = Directory.GetDirectories(path)
		files = Directory.GetFiles(path, "AssemblyInfo.cs")
		for file in files:
			CheckAssemblyInfo(file)
			
		for dir in dirs:
			NavigateDirectoryAssemblyInfo(dir)
	
	private def CheckAssemblyInfo(path as string):
		self.displayLogRichTextBox.Text += "Config file " + path +"\n"
		lines = System.IO.File.ReadAllLines(path)
		#[assembly: AssemblyVersion("1.0.0.0")]
		#[assembly: AssemblyFileVersion("1.0.0.0")]
		changes = 0
		for line in lines:		
			if line == '[assembly: AssemblyVersion("2.5.0.0")]':
				line = '[assembly: AssemblyVersion("2.5.1.0")]'
				changes += 1				
			elif line == '[assembly: AssemblyFileVersion("2.5.0.0")]':
				line = '[assembly: AssemblyFileVersion("2.5.1.0")]'
				changes += 1
				
		System.IO.File.WriteAllLines(path, lines)
		self.displayLogRichTextBox.Text += "Total changes " + changes +"\n"		
		
			

[STAThread]
public def Main(argv as (string)) as void:
	Application.EnableVisualStyles()
	Application.SetCompatibleTextRenderingDefault(false)
	Application.Run(MainForm())

