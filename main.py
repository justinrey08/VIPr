import tkinter as Tk
import tkinter.messagebox
import customtkinter
import requests
import shutil
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.request import Request
import bs4 as bs
import os
import pickle
import re
from tkinter import *

# Modes: "System" (standard), "Dark", "Light"
customtkinter.set_appearance_mode("System")
# Themes: "blue" (standard), "green", "dark-blue"
customtkinter.set_default_color_theme("dark-blue")
exclude = list(["VBP", "IN", "DT", "CC", "PRP$", "MD", "PRP"])
# Get relative path to the current file


def relative_path(file_name):
    return os.path.join(os.getcwd(), file_name)


def get_soup(url, header):
    return bs.BeautifulSoup(urlopen(Request(url, headers=header)), 'html.parser')

def alterSrc(s):
            l = len(s)
            for i in range(0, l):
                if s[i] == 'b' and s[i + 1] == '.':
                    return s[0:i] + s[i + 1:]

class App(customtkinter.CTk):
    WIDTH = 800
    HEIGHT = 500

    def __init__(self):
        super().__init__()
        self.userName = "VIPr"
        self.intro()
        self.iconbitmap(f"@{relative_path('econ.xbm')}")
        self.title("Visual Presenter by: JusHunNashSon")

    def main_window(self):
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        print()
        # call .on_closing() when app gets closed
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.iconbitmap(f"@{relative_path('econ.xbm')}")

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
        self.frame_info.grid(row=0, column=0, columnspan=2,
                             rowspan=4, pady=20, padx=20, sticky="nsew")

        # ============ frame_info ============

        # configure grid layout (1x1)
        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text=f"Hello, {self.userName}! You are currently using a\n" +
                                                        "prototype of VIPr, a visual presenter which utilizes\n" +
                                                        "Machine Learning and Web Scraping to automate gathering\n" +
                                                        "images for your visual presentation, developed by JusHunNashSon.\n" +
                                                        "Feel free to enter any textual data you wish to visualize.",
                                                   text_font=(
                                                       "Montserrat Black", 10),
                                                   height=200,
                                                   # <- custom tuple-color
                                                   fg_color=(
                                                       "white", "gray38"),
                                                   justify=tkinter.CENTER)
        self.label_info_1.grid(column=0, row=0, sticky="nwe", padx=15, pady=15)

        # ============ frame_right ============

        self.entry = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            placeholder_text="Enter your text to be visualized")
        self.entry.grid(row=7, column=0, columnspan=2,
                        pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Enter text",
                                                command=self.tag_scrape_images)
        self.button_5.grid(row=7, column=2, columnspan=2,
                           pady=20, padx=20, sticky="we")
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

        text = self.entry.get()
        features = [extract_features(text.split(), idx)
                    for idx in range(len(text.split()))]
        pickled_model = pickle.load(
            open('penn_treebank_crf_postagger.sav', 'rb'))
        predictions_test = pickled_model.predict_single(features)
        pairs_test = [(text.split()[idx], predictions_test[idx])
                      for idx in range(len(text.split()))]
        # Get the tags
        tags = [pair[1] for pair in pairs_test if pair != "JJ"]
        # Get the words
        words = [pair[0] for pair in pairs_test if pair != "JJ"]
        # Zip the words and tags
        zipped = zip(words, tags)
        # Create a dictionary
        d = dict(zipped)
        # Create a list of tuples
        l = list(d.items())
        # Unzip the list
        words, tags = zip(*l)

        pairs = list()
        for i in range(len(l)):
            if(l[i][1] not in exclude):
                # remove non alphanumeric characters
                l[i] = (re.sub('[^A-Za-z0-9]+', '', l[i][0]), l[i][1])
                pairs.append(l[i][0])

        print(pairs)

        # In[2]:

        # Create a folder to store the images and create a file to store the tags
        if not os.path.exists(f"{self.userName}_images"):
            os.makedirs(f"{self.userName}_images")
        with open(f"{self.userName}_tags.txt", "w") as f:
            for pair in pairs:
                f.write(f"{pair}\n")

        # In[5]:
        # Search for images using https://imgur.com/search/score?q
        images = []
        for i in range(len(pairs)):
            query = pairs[i]
            url = "https://imgur.com/search/score?q=" + query
            source = urlopen(url, timeout=10).read()
            soup = bs.BeautifulSoup(source, "html.parser")
            atags = soup.findAll("a", {"class": "image-list-link"})
            imgtags = [a.find("img") for a in atags]
            images.append(f"https:{imgtags[0]['src']}")
        
        print(images)

    # In[6]:
        # Download the images
        for i in range(len(images)):
            # get the image name
            image_name = images[i].split("/")[-1]
            # get the image extension
            image_extension = image_name.split(".")[-1]
            # download the image
            urlretrieve(images[i], f"{self.userName}_images/{image_name}")

    def pass_value(self, userName):
        self.userName = userName
        self.main_window()

    def intro(self):
        self.geometry("400x240")
        # Use CTkEntry instead of tkinter Entry
        userinput = customtkinter.CTkEntry(
            width=120,
            placeholder_text="Enter your Name")
        userinput.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
        button = customtkinter.CTkButton(
            master=self, text="Begin Visualizing", command=lambda: self.pass_value(userinput.get()))
        button.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

    def change_mode(self):
        if self.switch_1.get() == 1:
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
