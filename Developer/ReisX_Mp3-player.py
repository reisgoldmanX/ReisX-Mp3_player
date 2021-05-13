from tkinter import *
import tkinter.ttk as ttk
from pygame import mixer
from mutagen.mp3 import MP3
from random import choice
from keyboard import is_pressed
from pypresence import Presence
from time import time, strftime, gmtime
from os import getcwd, listdir


root = Tk()
root.title("ReisX: Mp3 player")
root.geometry("560x430")
root.iconbitmap("images/Theicon.ico")
root.resizable(False, False)
mixer.init()

music_dir = getcwd() + "\Music\\"
client_id = "838036099221684234"
RPC = Presence(client_id)
state = "Dev: reisgoldmanX"
details = "Listening..."
current_song = ""

connection = None
running = True
now_stamp = int(time())


def updateDiscord(durum, detaylar):
    big_image = f"m--zikbot"
    big_text = f"ReisX: Mp3 Player"
    small_image = f"info"
    small_text = f"Dev: reisgoldmanX#3697"

    state_dc = f"{durum}"
    details_dc = f"{detaylar}"
    buttons = [{"label": "Github", "url": "https://github.com/reisgoldmanX/ReisX-Mp3_player"}]
    start_time = now_stamp

    try:
        RPC.update(large_image=big_image, large_text=big_text, small_image=small_image, small_text=small_text, state=state_dc, details=details_dc, start=start_time, buttons=buttons)
    except:
        return


def connectDiscord():
    global connection
    try:
        RPC.connect()
        connection = True
    except:
        connection = False
        pass


def hotkeys():
    if is_pressed("left shift + z") is True:
        volume_slider.set(volume_slider.get() + 0.0002)

    elif is_pressed("left shift + x") is True:
        volume_slider.set(volume_slider.get() - 0.0002)
    else:
        pass


def play_time():
    global song_length
    if stopped:
        return

    current_time = mixer.music.get_pos() / 1000

    song = song_box.get(ACTIVE)
    song = f'{music_dir + song}.mp3'
    song_mut = MP3(song)

    song_length = song_mut.info.length
    converted_song_length = strftime('%M:%S', gmtime(song_length))

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
        converted_current_time = strftime('%M:%S', gmtime(int(my_slider.get())))
        status_bar.config(text=f'{current_song} |  {song_box.size()} / {int(song_box.index(str(ACTIVE))) + 1}  | Time Elapsed: {converted_current_time}  of  {converted_song_length}  ')

        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    status_bar.after(1000, play_time)


def add_songs():
    delete_all_songs()
    for song in get_music():
        song = song.replace(f"{music_dir}", "")
        song = song.replace(".mp3", "")
        song_box.insert(END, song)


def add_mixed_songs():
    delete_all_songs()
    for i in range(0, len(get_music())):
        random = choice(get_music())
        get_music().remove(random)
        song_box.insert(END, random.replace(".mp3", ""))


def get_music():
    songs = listdir(music_dir)
    for song in songs:
        edited_song = song.replace(".mp3", "")
        if edited_song in song_box.get(first=0, last=END):
            songs.remove(song)
    return songs


def play():
    global stopped, paused, current_song
    stopped = False
    if paused is True:
        pause(paused)
        mixer.music.unload()
        status_bar.config(text='')
        my_slider.config(value=0)

    song = song_box.get(ACTIVE)
    current_song = song
    updateDiscord(song, details)

    song = f'{music_dir + song}.mp3'

    mixer.music.load(song)
    mixer.music.play(loops=0)

    play_time()


stopped = False


def stop():
    status_bar.config(text='Stopped')
    my_slider.config(value=0)

    mixer.music.stop()
    song_box.selection_clear(ACTIVE)

    status_bar.config(text='')
    global stopped
    stopped = True


def next_song():
    global paused, current_song
    paused = False

    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)

    current_song = song
    updateDiscord(song, details)

    song = f'{music_dir + song}.mp3'

    mixer.music.load(song)
    mixer.music.play(loops=0)

    song_box.selection_clear(0, END)

    song_box.activate(next_one)

    song_box.selection_set(next_one, last=None)


def previous_song():
    global paused, current_song
    paused = False

    status_bar.config(text='')
    my_slider.config(value=0)

    next_one = song_box.curselection()

    next_one = next_one[0] - 1

    song = song_box.get(next_one)
    current_song = song
    updateDiscord(song, details)

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


paused = False


def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        mixer.music.unpause()
        paused = False
        updateDiscord(current_song, details)
    else:
        mixer.music.pause()
        paused = True
        updateDiscord(current_song, "Paused.")


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

playlist_settings_menu = Menu(my_menu)
my_menu.add_cascade(label="Playlist settings", menu=playlist_settings_menu)
playlist_settings_menu.add_command(label="Refresh the playlist", command=add_songs)
playlist_settings_menu.add_command(label="Mix the playlist", command=add_mixed_songs)
playlist_settings_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
playlist_settings_menu.add_command(label="Delete Playlist", command=delete_all_songs)


status_bar = Label(root, text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)


my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=2, column=0, pady=10)


volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=101)
volume_slider.pack(pady=7)

vol = StringVar()
vol.set("")
vol_label = Label(volume_frame, textvariable=vol, bg="white", fg="black")


def on_start():
    connectDiscord()
    add_songs()


def on_close():
    global running
    root.iconify()
    root.destroy()
    running = False


if __name__ == '__main__':
    on_start()
    root.protocol("WM_DELETE_WINDOW", on_close)

    while running:
        hotkeys()
        root.update()
        if not running:
            break
