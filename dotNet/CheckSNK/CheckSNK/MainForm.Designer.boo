namespace Converter_entlib4to5

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
		self.projectsButton = System.Windows.Forms.Button()
		self.displayLogRichTextBox = System.Windows.Forms.RichTextBox()
		self.panel1.SuspendLayout()
		self.SuspendLayout()
		# 
		# panel1
		# 
		self.panel1.Controls.Add(self.pathTextBox)
		self.panel1.Controls.Add(self.projectsButton)
		self.panel1.Dock = System.Windows.Forms.DockStyle.Top
		self.panel1.Location = System.Drawing.Point(0, 0)
		self.panel1.Name = "panel1"
		self.panel1.Size = System.Drawing.Size(472, 54)
		self.panel1.TabIndex = 1
		# 
		# pathTextBox
		# 
		self.pathTextBox.Dock = System.Windows.Forms.DockStyle.Top
		self.pathTextBox.Location = System.Drawing.Point(0, 0)
		self.pathTextBox.Name = "pathTextBox"
		self.pathTextBox.Size = System.Drawing.Size(472, 20)
		self.pathTextBox.TabIndex = 4
		# 
		# projectsButton
		# 
		self.projectsButton.Location = System.Drawing.Point(3, 28)
		self.projectsButton.Name = "projectsButton"
		self.projectsButton.Size = System.Drawing.Size(98, 23)
		self.projectsButton.TabIndex = 0
		self.projectsButton.Text = "Convert Projects"
		self.projectsButton.UseVisualStyleBackColor = true
		self.projectsButton.Click += self.ProjectsButtonClick as System.EventHandler
		# 
		# displayLogRichTextBox
		# 
		self.displayLogRichTextBox.Anchor = cast(System.Windows.Forms.AnchorStyles,(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom) 
						| System.Windows.Forms.AnchorStyles.Left) 
						| System.Windows.Forms.AnchorStyles.Right))
		self.displayLogRichTextBox.Location = System.Drawing.Point(0, 60)
		self.displayLogRichTextBox.Name = "displayLogRichTextBox"
		self.displayLogRichTextBox.Size = System.Drawing.Size(472, 291)
		self.displayLogRichTextBox.TabIndex = 0
		self.displayLogRichTextBox.Text = ""
		# 
		# MainForm
		# 
		self.AutoScaleDimensions = System.Drawing.SizeF(6, 13)
		self.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font
		self.ClientSize = System.Drawing.Size(472, 350)
		self.Controls.Add(self.panel1)
		self.Controls.Add(self.displayLogRichTextBox)
		self.Name = "MainForm"
		self.Text = "MainForm"
		self.Load += self.MainFormLoad as System.EventHandler
		self.panel1.ResumeLayout(false)
		self.panel1.PerformLayout()
		self.ResumeLayout(false)
	private pathTextBox as System.Windows.Forms.TextBox
	private projectsButton as System.Windows.Forms.Button
	private displayLogRichTextBox as System.Windows.Forms.RichTextBox
	private panel1 as System.Windows.Forms.Panel
	
	

