namespace FindXsltError

partial class MainForm(System.Windows.Forms.Form):
	private components as System.ComponentModel.IContainer = null
	
	protected override def Dispose(disposing as bool) as void:
		if disposing:
			if components is not null:
				components.Dispose()
		super(disposing)
	
	// This method is required for Windows Forms designer support.
	// Do not change the method contents inside the source code editor. The Forms designer might
	// not be able to load this method if it was changed manually.
	private def InitializeComponent():
		self.panel1 = System.Windows.Forms.Panel()
		self.pathTextBox = System.Windows.Forms.TextBox()
		self.checkXsltButton = System.Windows.Forms.Button()
		self.displayLogRichTextBox = System.Windows.Forms.RichTextBox()
		self.folderBrowserDialog = System.Windows.Forms.FolderBrowserDialog()
		self.panel1.SuspendLayout()
		self.SuspendLayout()
		# 
		# panel1
		# 
		self.panel1.Controls.Add(self.pathTextBox)
		self.panel1.Controls.Add(self.checkXsltButton)
		self.panel1.Dock = System.Windows.Forms.DockStyle.Top
		self.panel1.Location = System.Drawing.Point(0, 0)
		self.panel1.Name = "panel1"
		self.panel1.Size = System.Drawing.Size(457, 61)
		self.panel1.TabIndex = 3
		# 
		# pathTextBox
		# 
		self.pathTextBox.Dock = System.Windows.Forms.DockStyle.Top
		self.pathTextBox.Location = System.Drawing.Point(0, 0)
		self.pathTextBox.Name = "pathTextBox"
		self.pathTextBox.Size = System.Drawing.Size(457, 20)
		self.pathTextBox.TabIndex = 3
		# 
		# checkXsltButton
		# 
		self.checkXsltButton.Location = System.Drawing.Point(3, 26)
		self.checkXsltButton.Name = "checkXsltButton"
		self.checkXsltButton.Size = System.Drawing.Size(95, 23)
		self.checkXsltButton.TabIndex = 2
		self.checkXsltButton.Text = "Check xslt"
		self.checkXsltButton.UseVisualStyleBackColor = true
		self.checkXsltButton.Click += self.CheckXsltButtonClick as System.EventHandler
		# 
		# displayLogRichTextBox
		# 
		self.displayLogRichTextBox.Dock = System.Windows.Forms.DockStyle.Bottom
		self.displayLogRichTextBox.Location = System.Drawing.Point(0, 67)
		self.displayLogRichTextBox.Name = "displayLogRichTextBox"
		self.displayLogRichTextBox.Size = System.Drawing.Size(457, 272)
		self.displayLogRichTextBox.TabIndex = 2
		self.displayLogRichTextBox.Text = ""
		# 
		# MainForm
		# 
		self.AutoScaleDimensions = System.Drawing.SizeF(6, 13)
		self.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		self.ClientSize = System.Drawing.Size(457, 339)
		self.Controls.Add(self.panel1)
		self.Controls.Add(self.displayLogRichTextBox)
		self.Name = "MainForm"
		self.Text = "MainForm"
		self.panel1.ResumeLayout(false)
		self.panel1.PerformLayout()
		self.ResumeLayout(false)
	private pathTextBox as System.Windows.Forms.TextBox
	private folderBrowserDialog as System.Windows.Forms.FolderBrowserDialog
	private displayLogRichTextBox as System.Windows.Forms.RichTextBox
	private checkXsltButton as System.Windows.Forms.Button
	private panel1 as System.Windows.Forms.Panel

