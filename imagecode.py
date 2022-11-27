# -*- coding: utf-8 -*-
import os
import tkinter
from pathlib import Path
from tkinter import filedialog

import customtkinter
from pytoimage import PyImage  # class of create img

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# if not directory - create her
if not os.path.exists('img'):
    os.mkdir('img')


def pycode_to_img(file_path: str, start: int = 0, end: int = 0):
    try:
        # if not exist this file return false code
        if not Path(file_path).is_file():
            return '[-] Uu-ups... please check a file path!'

        code = PyImage(file_path, background=(255, 255, 255))  # created object 'PyImage' and set background
        palette = {
            'line': (255, 0, 255),
            'normal': (0, 0, 0),
        }  # select color of code

        code.set_color_palette(palette=palette)  # Set palette
        code.generate_image(start=start, end=end)  # Endpoint of generate
        img_name = file_path.split("/")[-1].replace('.py',
                                                    '.png')  # by default start name of img file (format - '.png')
        code.save_image(f'img/{img_name}')  # save file with name in 'img' directory

        return f"[+] Image 'img/{img_name}' success created"
    except Exception as _ex:
        return f'[-] Uu-ups... please check a file path!\n{_ex}'


class ImageCode(customtkinter.CTk):
    WIDTH = 920
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title(ImageCode.__name__)
        self.geometry(f"{ImageCode.WIDTH}x{ImageCode.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=6)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        self.frame_info = customtkinter.CTkFrame(master=self.frame_left)
        self.frame_info.grid(row=2, column=0, rowspan=1, pady=20, padx=20)

        self.frame_selected_path = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_selected_path.grid(row=1, column=0, rowspan=1, pady=20, padx=20)

        self.frame_res = customtkinter.CTkFrame(master=self.frame_right)
        self.frame_res.grid(row=8, column=0, rowspan=1, pady=20, padx=20)

        # ============ frame_left ============

        # configure grid layout (1x11)

        self.frame_left.grid_rowconfigure(0, minsize=10)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)  # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text=ImageCode.__name__,
                                              text_font=("Roboto Medium", -20))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        # ============ frame_info ============

        # configure grid layout (1x1)

        self.frame_info.rowconfigure(0, weight=1)
        self.frame_info.columnconfigure(0, weight=1)

        self.label_info = customtkinter.CTkLabel(master=self.frame_info,
                                                 text="ImageCode is an application,\n" +
                                                      "which creates an image,\n" +
                                                      "the code you wrote",
                                                 height=100,
                                                 corner_radius=6,  # <- custom corner radius
                                                 fg_color=("white", "gray38"),  # <- custom tuple-color
                                                 text_font=("Roboto Medium", 11),
                                                 justify=tkinter.LEFT)
        self.label_info.grid(column=0, row=0, padx=15, pady=15)

        self.label_mode = customtkinter.CTkLabel(master=self.frame_left, text="Appearance Mode:",
                                                 text_font=("Roboto Medium", 11))
        self.label_mode.grid(row=9, column=0, pady=0, padx=5, sticky="w")

        self.option_menu = customtkinter.CTkOptionMenu(master=self.frame_left,
                                                       values=["Light", "Dark", "System"],
                                                       text_font=("Roboto Medium", 11),
                                                       command=self.change_appearance_mode)
        self.option_menu.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)

        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=400)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # ============ frame_right ============

        self.select_path_button = customtkinter.CTkButton(master=self.frame_right,
                                                          text="Path",
                                                          text_font=("Roboto Medium", 11),
                                                          command=self.open_file_dialog)
        self.select_path_button.grid(row=0, column=0, pady=10, padx=10)

        self.selected_path = customtkinter.CTkLabel(master=self.frame_selected_path,
                                                    text="Path not selected",
                                                    text_color='green',
                                                    text_font=("Roboto Medium", 11))
        self.selected_path.grid(row=1, column=0)

        self.set_start_end = customtkinter.CTkSwitch(master=self.frame_right,
                                                     text="Set start and end",
                                                     text_font=("Roboto Medium", 11),
                                                     onvalue=True,
                                                     offvalue=False,
                                                     command=self.switch_entry)
        self.set_start_end.grid(row=0, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.start = customtkinter.CTkEntry(master=self.frame_right,
                                            placeholder_text='Start',
                                            placeholder_text_color='green',
                                            width=50,
                                            height=10)
        self.start.grid(row=1, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.end = customtkinter.CTkEntry(master=self.frame_right,
                                          placeholder_text="End",
                                          placeholder_text_color="green",
                                          width=50,
                                          height=10)
        self.end.grid(row=2, column=2, columnspan=1, pady=10, padx=20, sticky="we")

        self.select_path_button = customtkinter.CTkButton(master=self.frame_res,
                                                          text='Select path',
                                                          text_font=("Roboto Medium", 11),
                                                          fg_color=None,
                                                          hover=False,
                                                          command=lambda: os.system(r'explorer img'))
        self.select_path_button.grid(row=8, column=0, pady=10, padx=10)

        self.convert_button = customtkinter.CTkButton(master=self.frame_right,
                                                      text="Start convert",
                                                      text_font=("Roboto Medium", 11),
                                                      fg_color="green",
                                                      command=self.start_converter)
        self.convert_button.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values

        self.option_menu.set("System")
        self.start.configure(state=tkinter.DISABLED)
        self.end.configure(state=tkinter.DISABLED)

    def switch_entry(self):
        if not self.set_start_end.get():
            self.start.configure(state=tkinter.DISABLED)
            self.end.configure(state=tkinter.DISABLED)
        else:
            self.start.configure(state=tkinter.NORMAL)
            self.end.configure(state=tkinter.NORMAL)

    def open_file_dialog(self):
        path = filedialog.askopenfilename()
        self.selected_path.configure(text=path)

    def start_converter(self):
        start = self.start.get()
        end = self.end.get()
        res = pycode_to_img(self.selected_path.text, start=int(start) if start.isdigit() else 0,
                            end=int(end) if end.isdigit() else 0) if self.set_start_end.get() else pycode_to_img(
            self.selected_path.text
        )
        color = 'green' if res.startswith("[+]") else 'red'
        self.select_path_button.configure(text=res, text_color=color)

    @staticmethod
    def change_appearance_mode(new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def on_closing(self):
        self.destroy()


if __name__ == "__main__":
    app = ImageCode()
    app.mainloop()
