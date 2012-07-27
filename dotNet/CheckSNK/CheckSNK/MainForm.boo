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

	
	private def  NavigateDirectoryLookProjects(path, rootpath):
		dirs = Directory.GetDirectories(path)
		files = Directory.GetFiles(path, "*.csproj")
		for file in files:
			CheckProjectFile(file, rootpath)
			
		for dir in dirs:
			NavigateDirectoryLookProjects(dir, rootpath)

	
	private def CheckProjectFile(filepath as string, rootpath as string):
		skname = "rts.snk"
		pname = Path.GetFileName(filepath)
		self.displayLogRichTextBox.Text += "Project file: " + pname +"\n"
		doc = XDocument.Load(filepath)
		ns = XNamespace.Get("http://schemas.microsoft.com/developer/msbuild/2003")
		#<PropertyGroup>
		#    <AssemblyOriginatorKeyFile>rts.snk</AssemblyOriginatorKeyFile>
		#</PropertyGroup>
		changes = 0
		relative = filepath.Replace(pname, "").TrimEnd(Path.DirectorySeparatorChar)
		relative = MakeRelativePath(relative, rootpath)
		relative = relative.Replace(Path.GetFileName(rootpath), skname)
		assemblynode = doc.Descendants(ns + "AssemblyOriginatorKeyFile").FirstOrDefault()
		#we only modify the ones that already have a strong key
		if assemblynode == null:
			return
		if assemblynode.Value != relative:
			assemblynode.SetValue(relative)
			changes += 1
			self.displayLogRichTextBox.Text += "U " + pname + ": AssemblyOriginatorKeyFile to "+ skname +"\n"
		#check if a keyfile already exist
		#<None Include="rts.snk" />
		keyfilenode = doc.Descendants(ns + "None").Where({
				ig as XElement | ig.Attribute("Include") != null and
				ig.Attribute("Include").Value.Contains(skname)
				}).FirstOrDefault()
		if keyfilenode == null:
			# <ItemGroup>
			#   <None Include="..\rts.snk">
			#     <Link>rts.snk</Link>
			#   </None>
			#</ItemGroup>
			keyfilenode = XElement(ns + "ItemGroup",
					XElement(ns + "None", XAttribute("Include", relative),
						XElement(ns + "Link", skname)))
			lastItemGroup = doc.Descendants(ns + "ItemGroup").LastOrDefault()
			lastItemGroup.AddBeforeSelf(keyfilenode)
			changes += 1
			self.displayLogRichTextBox.Text += "U " + pname + ": Add Link to "+ relative +"\n"
		elif keyfilenode != null and keyfilenode.Attribute("Include").Value != relative:
			keyfilenode.SetAttributeValue("Include", relative)
			changes += 1
			if keyfilenode.HasElements:
				keyfilenode.Element(ns+"Link").SetValue(skname)
			else:
				keyfilenode.Add(XElement(ns+"Link", skname))
		#for propertyGroup in doc.Descendants(ns + "PropertyGroup"):
		#	for node in propertyGroup.Elements(ns + "AssemblyOriginatorKeyFile").ToList():
		#		if node.Value.Contains(skname):
		#			self.displayLogRichTextBox.Text += "U " + node.Value + " to "+ relative +"\n"
		#			node.SetValue(relative)
		#			changes += 1
		self.displayLogRichTextBox.Text += "Changes:" + changes +"\n"
		if changes > 0:
			doc.Save(filepath)
	
	private def ProjectsButtonClick(sender as object, e as System.EventArgs):
		rootPath = self.pathTextBox.Text
		NavigateDirectoryLookProjects(rootPath, rootPath)


	/// <summary>
    /// Creates a relative path from one file or folder to another.
    /// </summary>
    /// <param name="fromPath">Contains the directory that defines the start of the relative path.</param>
    /// <param name="toPath">Contains the path that defines the endpoint of the relative path.</param>
    /// <param name="dontEscape">Boolean indicating whether to add uri safe escapes to the relative path</param>
    /// <returns>The relative path from the start directory to the end path.</returns>
	private def MakeRelativePath(frompath as string, topath as string):
		fromUri = Uri(frompath)
		touri = Uri(topath)
		relativeuri = fromUri.MakeRelativeUri(touri)
		relativepath = Uri.UnescapeDataString(relativeuri.ToString())
		return relativepath.Replace(char('/'), Path.DirectorySeparatorChar)



[STAThread]
public def Main(argv as (string)) as void:
	Application.EnableVisualStyles()
	Application.SetCompatibleTextRenderingDefault(false)
	Application.Run(MainForm())

