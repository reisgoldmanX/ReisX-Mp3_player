from pypresence import Presence
from tkinter import *
import tkinter.ttk as ttk
from pygame import mixer
from mutagen.mp3 import MP3
from random import choice
import time
import os
from requests import get


root = Tk()
root.title("ReisX: Mp3 player")
root.geometry("560x430")
root.iconbitmap("images/Theicon.ico")
root.resizable(False, False)
mixer.init()

music_dir = os.getcwd() + "\Music\\"
client_id = "838036099221684234"
RPC = Presence(client_id)
state = "Dev: reisgoldmanX"
details = "Just started"
is_working = None


def updateDiscord(durum, detaylar):
    global is_working
    big_image = f"m--zikbot"
    big_text = f"ReisX: Mp3 Player"
    small_image = f"info"
    small_text = f"Dev: reisgoldmanX#3697"

    state_dc = f"{durum}"
    details_dc = f"{detaylar}"
    buttons = [{"label": "Download", "url": "https://bitmedidaha.com"}]

    try:
        RPC.update(large_image=big_image, large_text=big_text, small_image=small_image, small_text=small_text, state=state_dc, details=details_dc, buttons=buttons)
        is_working = True
    except:
        is_working = False

    if is_working is True:
        dc_label.config(image=discord_green)

    elif is_working is False:
        dc_label.config(image=discord_red)


def discord_activity_loop():
    time.sleep(1 / 10)
    try:
        updateDiscord(durum=state, detaylar=details)
    except:
        pass


def connect():
    connection = None
    try:
        r = get("https://google.com")
        r.raise_for_status()
        connection = True
    except:
        connection = False

    if connection is True:
        try:
            RPC.connect()
        except Exception as e:
            pass
            print(e)
    elif connection is False:
        pass


def play_time():
    if stopped:
        return

    current_time = mixer.music.get_pos() / 1000

    song = song_box.get(ACTIVE)
    song = f'{music_dir + song}.mp3'
    song_mut = MP3(song)

    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    current_time += 1
    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'Time Elapsed: {converted_song_length}  of  {converted_song_length}  ')
        next_song()
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))

    else:

        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'{song_box.size()} songs/ Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

        global state, details
        state = f'{converted_current_time}  of  {converted_song_length}'

        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    status_bar.after(1000, play_time)


def add_songs():
    delete_all_songs()
    songs = os.listdir(music_dir)

    counter = 0
    for song in songs:
        song = song.replace(f"{music_dir}", "")
        song = song.replace(".mp3", "")

        if str(song_box.get(first=counter)) == song:
            counter += 1
            pass
        else:
            song_box.insert(END, song)


def add_mixed_songs():
    delete_all_songs()
    songs = os.listdir(music_dir)

    song_list = []
    for song in songs:
        song = song.replace(f"{music_dir}", "")
        song = song.replace(".mp3", "")
        song_list.append(song)

    for i in range(0, len(song_list)):
        random = choice(song_list)
        song_list.remove(random)
        song_box.insert(END, random)

    
def play():

    global stopped
    stopped = False

    song = song_box.get(ACTIVE)

    global state, details
    details = f"{song}"
    song = f'{music_dir + song}.mp3'
    mixer.music.load(song)
    mixer.music.play(loops=0)

    play_time()


global stopped
stopped = False


def stop():

    status_bar.config(text='')
    my_slider.config(value=0)

    mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    status_bar.config(text='')
    global stopped
    stopped = True


def next_song():
    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)

    global state, details
    details = f"{song}"

    song = f'{music_dir + song}.mp3'

    mixer.music.load(song)
    mixer.music.play(loops=0)

    song_box.selection_clear(0, END)

    song_box.activate(next_one)

    song_box.selection_set(next_one, last=None)


def previous_song():

    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = song_box.curselection()

    next_one = next_one[0] - 1

    song = song_box.get(next_one)

    global state, details
    details = f"{song}"
    song = f'{music_dir + song}.mp3'

    mixer.music.load(song)
    mixer.music.play(loops=0)

    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last=None)


def delete_song():
    stop()

    song_box.delete(ANCHOR)

    mixer.music.stop()


def delete_all_songs():
    stop()
    song_box.delete(0, END)
    mixer.music.stop()


global paused
paused = False


def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True


def slide(x):
    song = song_box.get(ACTIVE)
    song = f'{music_dir + song}.mp3'

    mixer.music.load(song)
    mixer.music.play(loops=0, start=int(my_slider.get()))


def volume(x):
    mixer.music.set_volume(volume_slider.get())

    current_volume = mixer.music.get_volume()
    current_volume = current_volume * 100

    vol.set(str(current_volume))
    vol_label.pack()


master_frame = Frame(root)
master_frame.pack(pady=20)

song_box = Listbox(master_frame, bg="black", fg="green", width=60, selectbackground="green", selectforeground="black")
song_box.grid(row=0, column=0)


back_btn_img = PhotoImage(file='images/back50.png')
forward_btn_img = PhotoImage(file='images/forward50.png')
play_btn_img = PhotoImage(file='images/play50.png')
pause_btn_img = PhotoImage(file='images/pause50.png')
stop_btn_img = PhotoImage(file='images/stop50.png')

discord_red = PhotoImage(file="images/discord_red_in.png")
discord_green = PhotoImage(file="images/discord_green_in.png")

dc_label = Label(image=discord_red)
dc_label.pack(side=TOP, anchor=NW)


controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)


volume_frame = LabelFrame(master_frame, text="Volume")
volume_frame.grid(row=0, column=1, padx=30)


back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)

back_button.grid(row=0, column=0, padx=10)
forward_button.grid(row=0, column=1, padx=10)
play_button.grid(row=0, column=2, padx=10)
pause_button.grid(row=0, column=3, padx=10)
stop_button.grid(row=0, column=4, padx=10)


my_menu = Menu(root)
root.config(menu=my_menu)

add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Playlist settings", menu=add_song_menu)
add_song_menu.add_command(label="Refresh the playlist", command=add_songs)
add_song_menu.add_command(label="Mix the playlist", command=add_mixed_songs)

remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)


status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)


volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=7)

vol = StringVar()
vol.set("")
vol_label = Label(volume_frame, textvariable=vol, bg="white", fg="black")


root.bind("<Alt_R><slash>", lambda event: pause(paused))
root.bind("<Alt_R><*>", lambda event: stop())
root.bind("<Alt_R><minus>", lambda event: previous_song())
root.bind("<Alt_R><+>", lambda event: next_song())

if __name__ == '__main__':
    connect()
    add_songs()

    while 1:
        discord_activity_loop()
        try:
            root.update()
        except:
            mixer.music.stop()
            mixer.quit()
            try:
                RPC.close()
            except:
                pass
            break





