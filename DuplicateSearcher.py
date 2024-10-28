import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os

from collections import defaultdict
from PIL import Image, ImageTk
import hashlib
import subprocess
import send2trash
import pygame


FONT_SIZE_1 = 12
FONT_SIZE_2 = 12

win = tk.Tk()
win.title("DEL Duplicate Searcher")
win.iconbitmap("images/icon.ico")

SCREEN_WIDTH = win.winfo_screenwidth()
SCREEN_HEIGHT = win.winfo_screenheight()

icon_paths = [
    "icon_open_in_player.jpg",
    "icon_open_in_explorer.jpg",
    "icon_delete.png"
]

button_paths = [
    "select_folder.jpg",
    "select_folder_red.jpg",
    "music.jpg",
    "music_red.jpg",
    "video.jpg",
    "video_red.jpg",
    "photos.jpg",
    "photos_red.jpg",
    "log.jpg",
    "log_red.jpg",
    "search.jpg",
    "search_red.jpg"
]

sounds = [
    "sounds\\sound1.mp3",
    "sounds\\sound2.mp3"
]

images = []
button_images = []

for img in icon_paths:
    img_temp = Image.open("images\\" + str(img)).resize((25, 25))
    images.append(ImageTk.PhotoImage(img_temp))

for img in button_paths:
    img_temp = Image.open("images\\" + str(img))
    button_images.append(ImageTk.PhotoImage(img_temp))

back_img = Image.open("images\\icon_background.jpg").resize((SCREEN_WIDTH, 261))
back_img = ImageTk.PhotoImage(back_img)

left_img = Image.open("images\\side.jpg")
left_img = ImageTk.PhotoImage(left_img)



def bytes_to_megabytes(size_in_bytes):
    return size_in_bytes / (1024 * 1024)

def start_file(path):
    try:
        os.startfile(path)
    except FileNotFoundError:
        messagebox.showerror("Ошибка", "Файл не найден")
    except Exception as e:
        messagebox.showerror("Ошибка", "Произошла ошибка при возпроизведении файла: ", e)

def open_in_explorer(path):
    subprocess.Popen(f'explorer /select,"{path}"')

def play_sound(sound_file):
    pygame.init()
    try:
        pygame.mixer.music.load(sound_file)
        pygame.mixer.music.play()
    except pygame.error as e:
        print("Ошибка воспроизведения звука:", e)


def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        buffer = file.read(4096)
        while len(buffer) > 0:
            hasher.update(buffer)
            buffer = file.read(4096)
    return hasher.hexdigest()

def find_duplicate_files_v3(ext_to_search):
    clear_content()

    duplicates = defaultdict(list)
    FOLDER_PATH = str(path_to_analyze.get("1.0", tk.END)).strip()

    for root, dirs, files in os.walk(FOLDER_PATH):
        for file in files:
            if file.endswith(ext_to_search):
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)
                duplicates[file_hash].append(file_path)

    duplicate_groups = {hash: files for hash, files in duplicates.items() if len(files) > 1}

    if not duplicate_groups:
        tk.Label(
            content_delete_frame, 
            text="Дубликатов не найдено", 
            font="Arial 12 bold", 
            fg="green"
        ).grid(column=0, row=0)
        return

    fill_with_duplicates(duplicate_groups.values())


# widgets order
PLAY_COLUMN = 0
IN_EXPLORER_COLUMN = 1
DELETE_COLUMN = 2
MB_LABEL_COLUMN = 3
PATH_COLUMN = 4

padxy = 2.5

def fill_row_with_files(file, row):
    file_size = os.path.getsize(file)
    file = os.path.normpath(file)

    tk.Button(
        content_delete_frame,
        image=images[0],
        borderwidth=0,
        command=lambda path=file: start_file(path)
    ).grid(column=PLAY_COLUMN, row=row, sticky="E", padx=padxy, pady=padxy)

    tk.Button(
        content_delete_frame,
        image=images[1],
        borderwidth=0,
        command=lambda path=file: open_in_explorer(path)
    ).grid(column=IN_EXPLORER_COLUMN, row=row, sticky="E", padx=padxy, pady=padxy)

    tk.Button(
        content_delete_frame,
        image=images[2],
        borderwidth=0,
        command=lambda path=file: remove_duplicate_totrash(path)
    ).grid(column=DELETE_COLUMN, row=row, sticky="E", padx=padxy, pady=padxy)

    tk.Label(
        content_delete_frame,
        text=f"{round(bytes_to_megabytes(file_size), 2)}MB",
        font=f"Arial {FONT_SIZE_2}"
    ).grid(column=MB_LABEL_COLUMN, row=row, sticky="E")

    tk.Label(
        content_delete_frame, text=file, font=f"Arial {FONT_SIZE_1}"
    ).grid(column=PATH_COLUMN, row=row, sticky="W")


def fill_with_duplicates(duplicate_groups):
    row = 0
    i = 0

    size_of_duplicates = 0
    count_of_found_duplicates = 0
    for files in duplicate_groups:
        group_size = 0

        group_size_label = tk.Label(
            content_delete_frame,
            font="Arial 12 italic"
        )
        group_size_label.grid(column=0, row=row, columnspan=5)

        row += 1

        for file in files:
            file_size = os.path.getsize(file)
            group_size += file_size
            count_of_found_duplicates += 1

            fill_row_with_files(file, row)

            row += 1
            i += 1

        group_size_label["text"] = \
        f'Размер группы файлов:{ round(bytes_to_megabytes(group_size), 2)}MB \
Кол-во файлов в группе: {len(files)}'

        count_of_found_duplicates -= 1

        group_size -= file_size
        size_of_duplicates += group_size

    count_of_files["text"] = f"{count_of_found_duplicates} шт"
    size_of_files["text"] = f"{ round(bytes_to_megabytes(size_of_duplicates), 2)}Mb"


def remove_duplicate_totrash(path):
    try:
        send2trash.send2trash(path)
        messagebox.showinfo("Успех", "Файл успешно перемещен в корзину.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при перемещении файла в корзину: \n{str(e)}")

    for widget in content_delete_frame.winfo_children():
        if widget["text"] == path:
            for inner_widget in content_delete_frame.winfo_children():
                if inner_widget.grid_info()["row"] == widget.grid_info()["row"]:
                    inner_widget["foreground"] = "red"
                    if inner_widget.grid_info()["column"] == DELETE_COLUMN:
                        inner_widget.config(state="disabled")

                    if inner_widget.grid_info()["column"] == IN_EXPLORER_COLUMN:
                        inner_widget.config(state="disabled")


def find_log_files():
    clear_content()

    FOLDER_PATH = str(path_to_analyze.get("1.0", tk.END)).strip()

    file_paths = []
    file_sizes = []
    total_size = 0
    total_count = 0

    for root, dirs, files in os.walk(FOLDER_PATH):
        for file in files:
            if file.endswith(".log"):
                file_path = os.path.normpath(os.path.join(root, file))
                file_size = os.path.getsize(file_path)

                file_sizes.append(file_size)
                file_paths.append(file_path)
                total_size += file_size
                total_count += 1

    tk.Button(
        content_delete_frame, 
        text="Удалить log-файлы", 
        command=lambda file_paths=file_paths: delete_log_files(file_paths)
    ).grid(column=0, row=0, columnspan=4, sticky=tk.W)

    row = 1
    for file in file_paths:
        fill_row_with_files(file, row)
        row += 1

    count_of_files["text"] = f"{total_count} log-файлов"
    size_of_files["text"] = f"{ round(bytes_to_megabytes(total_size), 2)}Mb"


def delete_log_files(file_paths):

    def delete():

        info_box.insert("1.0", "Начало чистки log-файлов\n")
        for file in file_paths:
            file = os.path.normpath(file)
            try:
                send2trash.send2trash(file)
                info_box.insert(tk.END, f"Файл {str(file)}\n успешно перемещен в корзину.\n")
            except Exception as e:
                info_box.insert(tk.END, f"Ошибка при перемещении файла в корзину: \n{str(e)}\n")

        info_box.tag_configure("red", foreground="red")
        info_box.insert(tk.END, "\nCompleted, Можно закрыть это окно.", "red")

    PERMISSION = messagebox.askokcancel("Внимание!", 
"log-файлы - файлы которые используют программы для отладки в случае ошибки. \
Удаляйте их только если знаете что делаете.\nВсе файлы будут перемещены в корзину.\n\n\
Продолжить?")

    if not bool(PERMISSION):
        return

    log_info_window = tk.Tk()
    log_info_window.title("Удаление log-файлов")
    log_info_window.resizable = False

    tk.Button(log_info_window, text="Удалить", command=delete).pack(padx=10, pady=10)
    info_box = tk.Text(log_info_window, width=100, height=30)
    info_box.pack(padx=10, pady=10)

    log_info_window.mainloop()


def find_out_type_of_file():
    # ext = str(selected_type_label["text"]).strip()
    ext = str(extension_to_analyze.get())
    if str(ext).strip() == ".log":
        find_log_files()
    else:
        find_duplicate_files_v3(ext)

def ask_folder_path():
    FOLDER_PATH = filedialog.askdirectory(title="Выберите папку для поиска дубликатов")
    path_to_analyze.delete("1.0", tk.END)
    path_to_analyze.insert("1.0", os.path.normpath(FOLDER_PATH))

def clear_content():
    for widget in content_delete_frame.winfo_children():
        widget.destroy()


# Frames
top_frame = tk.Frame(win)
top_frame.grid(column=0, row=0, columnspan=2, sticky=tk.NSEW)

manage_frame = tk.Frame(win)
manage_frame.grid(column=0, row=1, sticky=tk.NSEW)

left_image_label = tk.Label(manage_frame, image=left_img)
left_image_label.grid(column=0, row=0)

manage_delete_frame = tk.Frame(win)
manage_delete_frame.grid(column=1, row=1, sticky=tk.NSEW)

# Frame 1 top_frame

top_image_label_1 = tk.Label(top_frame, image=back_img)
top_image_label_1.grid(column=0, row=0, columnspan=3)

size_frame = tk.Frame(top_frame)
size_frame.place(x=1400, y=60)

count_of_files = tk.Label(top_frame, text="0 шт", font="Arial 26 bold", bg="red", fg="white")
count_of_files.place(x=1300, y=60)

size_of_files = tk.Label(top_frame, text="0.0Mb", font="Arial 26 bold", bg="red", fg="white")
size_of_files.place(x=1300, y=120)

version_label = tk.Label(
    top_frame, 
    borderwidth=0, 
    text="3.1", 
    font="Impact 20", 
    fg="white", bg="dark red"
)
version_label.place(x=1840, y=20)


# Frame 2 manage_frame

path_to_analyze = tk.Text(
    manage_frame, 
    bg="lightgray",
    fg="black", 
    width=38, height=4,
    font="Arial 14",
    borderwidth=1
)
path_to_analyze.place(x=58, y=10)

selected_type_frame = tk.Frame(manage_frame, background="lightgrey")

tk.Label(
    selected_type_frame, 
    text="Выбранная категория: ", 
    font="Arial 12 bold", 
    bg="lightgray", fg="red"
).grid(column=0, row=0)


extension_to_analyze = ttk.Combobox(selected_type_frame, width=34)
extension_to_analyze['values'] = ("Категория не выбрана",)
extension_to_analyze.current(0)
extension_to_analyze.grid(column=1, row=0)

selected_type_frame.place(x=60, y=100)


def on_enter(event, btn, x):
    btn.config(image=button_images[x+1])
    play_sound(sounds[0])

def on_leave(event, btn, x):
    btn.config(image=button_images[x])

def on_button_press(event, btn, x):
    btn.config(image=button_images[x+1])
    play_sound(sounds[1])

def on_button_release(event, btn, x):
    btn.config(image=button_images[x+1])

def change_selected_type(exts):
    extension_to_analyze["values"] = exts
    extension_to_analyze.current(0)



photo_ext = (".jpg", ".jpeg", ".png", ".gif", ".ico", ".bmp", ".webp", ".tiff")
music_ext = (".mp3", ".wav", ".flac")
video_ext = (".mp4", ".avi", ".mow", ".mts", ".m2ts")

exts = ["", music_ext, video_ext, photo_ext, ".log", ""]

positionsY = [170, 230, 290, 350, 410, 470]
btns = []

photo_i = 0
i = 0
for ext in exts:
    btn = tk.Button(
        manage_frame, 
        image=button_images[photo_i], 
        borderwidth=5,
        relief=tk.GROOVE,
        command=lambda ext=ext: change_selected_type(ext)
    )

    if i == 0:
        btn.config(command=ask_folder_path)

    if i == 5:
        btn.config(command=find_out_type_of_file)


    btn.bind("<Enter>", lambda event, btn=btn, x=photo_i: on_enter(event, btn, x))
    btn.bind("<Leave>", lambda event, btn=btn, x=photo_i: on_leave(event, btn, x))

    btn.bind("<ButtonPress-1>", lambda event, btn=btn, x=photo_i: on_button_press(event, btn, x))
    btn.bind("<ButtonRelease-1>", lambda event, btn=btn, x=photo_i: on_button_release(event, btn, x))

    btn.place(x=50, y=positionsY[i])

    btns.append(btn)

    photo_i += 2
    i += 1


mng_delete_help = tk.Frame(manage_frame)
mng_delete_help.place(x=260, y=630)

def path_update(action):
    global FONT_SIZE_1
    if action == "+":
        FONT_SIZE_1 += 1
        font_size_path_label["text"] = FONT_SIZE_1

    elif action == "-":
        FONT_SIZE_1 -= 1
        font_size_path_label["text"] = FONT_SIZE_1

    for widget in content_delete_frame.winfo_children():
        if widget.grid_info()["column"] == PATH_COLUMN:
            widget["font"] = f"Arial {FONT_SIZE_1}"

def font_size_update(action):
    global FONT_SIZE_2
    if action == "+":
        FONT_SIZE_2 += 1
        font_size_size_label["text"] = FONT_SIZE_2

    elif action == "-":
        FONT_SIZE_2 -= 1
        font_size_size_label["text"] = FONT_SIZE_2

    for widget in content_delete_frame.winfo_children():
        if (widget.grid_info()["column"] == MB_LABEL_COLUMN):
            widget["font"] = f"Arial {FONT_SIZE_2}"

c_font = "Arial 10 bold"
c_relief = tk.GROOVE
c_bw = 2
padxy = 1

tk.Button(
    mng_delete_help,
    text="\\/",
    fg="white", bg="dark red",
    activebackground="red",
    activeforeground="white",
    command=lambda: path_update("-"),
    font=c_font,
    relief=c_relief,
    borderwidth=c_bw
).grid(column=0, row=0, padx=padxy, pady=padxy)

tk.Button(
    mng_delete_help,
    text="/\\",
    fg="white", bg="dark red",
    activebackground="red",
    activeforeground="white",
    command=lambda: path_update("+"),
    font=c_font,
    relief=c_relief,
    borderwidth=c_bw
).grid(column=1, row=0, padx=padxy, pady=padxy)

font_size_path_label = tk.Label(mng_delete_help, text=FONT_SIZE_1, font=f"Arial 10 bold")
font_size_path_label.grid(column=2, row=0)

tk.Button(
    mng_delete_help,
    text="\\/",
    fg="white", bg="dark red",
    activebackground="red",
    activeforeground="white",
    command=lambda: font_size_update("-"),
    font=c_font,
    relief=c_relief,
    borderwidth=c_bw
).grid(column=0, row=1, padx=padxy, pady=padxy)

tk.Button(
    mng_delete_help,
    text="/\\",
    fg="white", bg="dark red",
    activebackground="red",
    activeforeground="white",
    command=lambda: font_size_update("+"),
    font=c_font,
    relief=c_relief,
    borderwidth=c_bw
).grid(column=1, row=1, padx=padxy, pady=padxy)

font_size_size_label = tk.Label(mng_delete_help, text=FONT_SIZE_2, font=f"Arial 10 bold")
font_size_size_label.grid(column=2, row=1)

# Frame 3 manage_delete_frame

def on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

scrollbar_vertical = tk.Scrollbar(manage_delete_frame, orient=tk.VERTICAL)
scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar_horizontal = tk.Scrollbar(manage_delete_frame, orient=tk.HORIZONTAL)
scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

canvas = tk.Canvas(manage_delete_frame,
    width=SCREEN_WIDTH-600, 
    height=SCREEN_HEIGHT-500, 
    yscrollcommand=scrollbar_vertical.set, 
    xscrollcommand=scrollbar_horizontal.set
)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_vertical.config(command=canvas.yview)
scrollbar_horizontal.config(command=canvas.xview)

content_delete_frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=content_delete_frame, anchor=tk.NW)

content_delete_frame.bind("<Configure>", 
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
content_delete_frame.bind("<MouseWheel>", on_mousewheel)



win.mainloop()