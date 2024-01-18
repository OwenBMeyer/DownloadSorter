import customtkinter
from tkinter import filedialog
import os
import shutil

class FTypeCheckboxFrame(customtkinter.CTkFrame):
    def __init__(self, master, values):
        super().__init__(master)
        self.values = values
        self.checkboxes = []

        self.title = customtkinter.CTkLabel(self, text="Select File Types", fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")

        for i, value in enumerate(self.values):
            checkbox = customtkinter.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        selectedTypes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                print("    Selected Checkbox: ", checkbox.cget("text"))
                selectedTypes.append(checkbox.cget("text"))
        print("Selected filetypes: ", selectedTypes)
        return selectedTypes
    
class PathSelectFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.origin = ""
        self.destination = ""
        
        self.title = customtkinter.CTkLabel(self, text="Select Path", fg_color="transparent", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=(10,0), sticky="w")
        self.oPathButton = customtkinter.CTkButton(self, text="Origin Folder", command=self.originFolderSelect)
        self.oPathButton.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.originText = customtkinter.CTkTextbox(self, height=50, fg_color="gray70", corner_radius=6)
        self.originText.grid(row=2, column=0, padx=10, pady=(0,10), sticky="w")
        self.originText.insert("0.0", "No origin selected.")
        self.originText.configure(state="disabled")

        self.dPathButton = customtkinter.CTkButton(self, text="Destination Folder", command=self.destinationFolderSelect)
        self.dPathButton.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.destinationText = customtkinter.CTkTextbox(self, height=50, fg_color="gray70", corner_radius=6)
        self.destinationText.grid(row=4, column=0, padx=10, pady=(0,10), sticky="w")
        self.destinationText.insert("0.0", "No destination selected.")
        self.destinationText.configure(state="disabled")
        #self.destinationText = customtkinter.CTkLabel(self, text=self.destination, fg_color="gray30", corner_radius=6)
        #self.destinationText.grid(row=4, column=0, padx=10, pady=(10,0), sticky="w")
    
    def originFolderSelect(self):
        self.origin = filedialog.askdirectory()
        self.originText.configure(state="normal")
        self.originText.delete("0.0", "end")
        self.originText.insert("0.0", self.origin)
        self.originText.configure(state="disabled")
        print(self.origin)

    def destinationFolderSelect(self):
        self.destination = filedialog.askdirectory()
        self.destinationText.configure(state="normal")
        self.destinationText.delete("0.0", "end")
        self.destinationText.insert("0.0", self.destination)
        self.destinationText.configure(state="disabled")
        print(self.destination)

    def getOrigin(self):
        return self.origin
    
    def getDestination(self):
        return self.destination

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("File Organizer")
        self.geometry("500x350")
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.resizable(0,0)

        self.originPath = ""
        self.destinationPath = ""
        self.fileTypes = [".png", ".jpg", ".jpeg", ".mov", ".mp4", ".pdf"]

        self.pathFrame = PathSelectFrame(self)
        self.pathFrame.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nsew")

        self.checkbox_frame = FTypeCheckboxFrame(self, self.fileTypes)
        self.checkbox_frame.grid(row=0, column=1, padx=(0, 10), pady=(10,0), sticky="nsew")

        self.runButton = customtkinter.CTkButton(self, text="Run Program", command=self.run)
        self.runButton.grid(row=4, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def run(self):
        selectedFiles = self.checkbox_frame.get()
        for fileType in selectedFiles:
            self.move(self.pathFrame.getOrigin(), self.pathFrame.getDestination(), fileType)

    def move(self, originPath, desinationPath, fileType):
        if originPath == "" or desinationPath == "":
            pass
        else:
            for file in os.listdir(originPath):
                if file.endswith(fileType):
                    shutil.move(os.path.join(originPath, file), desinationPath)

    
if __name__ == "__main__":
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("dark-blue")

    app = App()
    app.mainloop()