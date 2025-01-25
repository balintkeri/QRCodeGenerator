
from qrcode import make as createQRCode
import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame, self).__init__(parent, title=title, size=(500, 500))
        
        self.panel          = wx.Panel(self)
        self.input          = wx.TextCtrl(self.panel, style = wx.TE_PROCESS_ENTER, value = "Your URL",)
        self.input.Bind(wx.EVT_TEXT_ENTER , self.on_generate)
        self.image_display  = wx.StaticBitmap(self.panel)
        self.generate_btn   =wx. Button(self.panel, label="Generate")
        self.generate_btn.Bind(wx.EVT_BUTTON, self.on_generate)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.input, 0, wx.ALL|wx.EXPAND, 15)
        self.main_sizer.Add(self.generate_btn, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.CENTER, 15)
        self.main_sizer.Add(self.image_display, 1, wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, 15)

        self.panel.SetSizer(self.main_sizer)

        self.Centre()
        self.Show()

    def loadImg(self, path):
        img = wx.Image(path, wx.BITMAP_TYPE_ANY)
            
        max_width = self.image_display.GetSize().x
        if max_width <= 0:
            max_width = 500 
        w = img.GetWidth()
        h = img.GetHeight()
        if w > max_width:
            h = h * max_width // w
            w = max_width
            img = img.Scale(w, h, wx.IMAGE_QUALITY_HIGH)

        self.image_display.SetBitmap(wx.Bitmap(img))
        self.panel.Layout()
        
    
    def on_generate(self, event):
        selected_text = self.input.GetValue()
        if len(selected_text) > 0:
            img = createQRCode(selected_text)
            with wx.FileDialog(self, "Save XYZ file", wildcard="PNG image (*.png)|*.png", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
                if fileDialog.ShowModal() == wx.ID_CANCEL:
                    return
                pathname = fileDialog.GetPath()
                try:
                    img.save(pathname)
                    self.loadImg(pathname)

                    wx.MessageBox(f"The QR code of \"{selected_text}\" saved to {pathname}", "Info", wx.OK | wx.ICON_INFORMATION)
                except IOError:
                    wx.MessageBox(f"Error during saving", "Error", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(f"Empthy input", "Error", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App()
    MyFrame(None, "QR Code Generator")
    app.MainLoop()
