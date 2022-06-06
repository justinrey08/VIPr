import tkinter as Tk
import tkinter.messagebox
import customtkinter
from tkinter import *

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


def u_name():
    root_tk1 = customtkinter.CTk()  # create CTk window like you do with the Tk window
    root_tk1.title('Hello, ' + intro.userinput.get())
    root_tk1.geometry("400x240")
    root_tk1.iconbitmap('@/home/justinrey/Capstone/econ.xbm')

def intro():
    root_tk = customtkinter.CTk()  # create CTk window like you do with the Tk window
    root_tk.title("Visual Presenter by JusHuNashSons")
    root_tk.geometry("400x240")
    root_tk.iconbitmap('@/home/justinrey/Capstone/econ.xbm')
    # Use CTkEntry instead of tkinter Entry
    userinput = customtkinter.CTkEntry(master=root_tk,
                                            width=120,
                                            placeholder_text=" Enter your Name")
    userinput.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
    # Use CTkButton instead of tkinter Button
    button = customtkinter.CTkButton(master=root_tk, text="Begin Visualizing", command=u_name)
    button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    root_tk.mainloop()

intro()

class App(customtkinter.CTk):

    WIDTH = 800
    HEIGHT = 500

    def __init__(self):
        super().__init__()

        self.title("Visual Presenter by JusHuNashSon")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        self.iconbitmap('@/home/justinrey/Capstone/econ.xbm')

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)


        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_info.grid(row=0, column=0, columnspan=2, rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="This is the base GUI,\n" +
                                                        "for our Visual Presenter,\n" +
                                                        "to be embedded by a ML model, \n" +
                                                        "and a web scraper",
                                                   text_font=("Montserrat Black", 10),
                                                   height=200,
                                                   fg_color=("white", "gray38"),  # <- custom tuple-color
                                                   justify=tkinter.LEFT)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        # ============ frame_right ============

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Enter your text to be visualized")
        self.entry.grid(row=7, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Enter text",
                                                command=self.tag_scrape_images)
        self.button_5.grid(row=7, column=2, columnspan=2, pady=20, padx=20, sticky="we")
        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_right,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_1.grid(row=8, column=0, pady=20, padx=20, sticky="w")
        # set default values
        self.switch_1.select()



    def tag_scrape_images(self):

        def extract_features(sentence, index):
            import re
            return {
                'word': sentence[index],
                'is_first': index == 0,
                'is_last': index == len(sentence) - 1,
                'is_capitalized': sentence[index][0].upper() == sentence[index][0],
                'is_all_caps': sentence[index].upper() == sentence[index],
                'is_all_lower': sentence[index].lower() == sentence[index],
                'is_alphanumeric': int(bool((re.match('^(?=.*[0-9]$)(?=.*[a-zA-Z])', sentence[index])))),
                'prefix-1': sentence[index][0],
                'prefix-2': sentence[index][:2],
                'prefix-3': sentence[index][:3],
                'prefix-3': sentence[index][:4],
                'suffix-1': sentence[index][-1],
                'suffix-2': sentence[index][-2:],
                'suffix-3': sentence[index][-3:],
                'suffix-3': sentence[index][-4:],
                'prev_word': '' if index == 0 else sentence[index - 1],
                'next_word': '' if index < len(sentence) else sentence[index + 1],
                'has_hyphen': '-' in sentence[index],
                'is_numeric': sentence[index].isdigit(),
                'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
            }

        from urllib.request import urlopen
        from urllib.request import urlretrieve
        import bs4 as bs
        import os
        import pickle

        text = self.entry.get()
        features = [extract_features(text.split(), idx) for idx in range(len(text.split()))]
        pickled_model = pickle.load(open('penn_treebank_crf_postagger.sav', 'rb'))
        predictions_test = pickled_model.predict_single(features)
        pairs_test = [(text.split()[idx], predictions_test[idx]) for idx in range(len(text.split()))]
        print(pairs_test)

        # In[2]:

        searchString = pairs_test
        folderName = '_'.join(searchString.split(" "))
        currPath = os.path.dirname(os.path.realpath(__file__))
        reqPath = os.path.join(currPath, folderName)
        if os.path.isdir(reqPath) == False:
            os.mkdir(folderName)

        # In[5]:

        searchQuery = '+'.join(searchString.split(" "))
        myLink = "https://imgur.com/search/score?q=" + searchQuery

        # In[6]:

        source = urlopen(myLink, timeout=10).read()
        soup = bs.BeautifulSoup(source, "html.parser")

        # In[7]:

        def alterSrc(s):
            l = len(s)
            for i in range(0, l):
                if s[i] == 'b' and s[i + 1] == '.':
                    return s[0:i] + s[i + 1:]

        # In[8]:

        atags = soup.findAll("a", {"class": "image-list-link"})
        imgtags = [a.find("img") for a in atags]
        srcs = ["https:" + alterSrc(img['src']) for img in imgtags]

        # In[9]:

        print("Downloading...")
        for l in srcs:
            filename = os.path.join(reqPath, os.path.basename(l))
            urlretrieve(l, filename)
        print("Successful!")

        # In[ ]:

    def change_mode(self):
        if self.switch_1.get()==1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.start()
