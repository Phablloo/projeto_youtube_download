from tkinter import *
from pytube import YouTube
from tkinter import filedialog
from pytube.exceptions import RegexMatchError

janela = Tk()
janela.title('Ptube')

def download(link_, audio_only=False, resolution=None, file_format=None):
    if link_:
        try:
            folder = filedialog.askdirectory()
            yt = YouTube(link_)
            if audio_only:
                if resolution:
                    stream = yt.streams.filter(only_audio=True, abr=resolution).first()
                else:
                    stream = yt.streams.filter(only_audio=True).first()
                if file_format:
                    file_extension = file_format.lower()
                    stream.download(folder, filename=f"{yt.title}.{file_extension}")
                else:
                    stream.download(folder)
            else:
                if resolution:
                    stream = yt.streams.filter(res=resolution).first()
                else:
                    stream = yt.streams.get_highest_resolution()
                if file_format:
                    file_extension = file_format.lower()
                    stream.download(folder, filename=f"{yt.title}.{file_extension}")
                else:
                    stream.download(folder)
            show_message()
        except RegexMatchError:
            show_error_message()
    else:
        show_error_message()

def show_message():
    janela_msg = Toplevel()
    janela_msg.title('Aviso')
    janela_msg.geometry('300x200')

    Label(janela_msg, text='Download concluído', font='arial 12 bold', pady=30).pack()

    Button(janela_msg, text='OK', command=janela_msg.destroy).pack()

def show_error_message():
    janela_msg = Toplevel()
    janela_msg.title('Aviso')
    janela_msg.geometry('300x200')

    Label(janela_msg, text='Insira um link válido', font='arial 12 bold', pady=30).pack()

    Button(janela_msg, text='OK', command=janela_msg.destroy).pack()

def show_quality_options(audio_only=False):
    options = []
    if audio_only:
        streams = YouTube(link.get()).streams.filter(only_audio=True)
        for stream in streams:
            if stream.abr not in options:
                options.append(stream.abr)
    else:
        streams = YouTube(link.get()).streams.filter(progressive=True)
        for stream in streams:
            if stream.resolution not in options:
                options.append(stream.resolution)
    if not options:
        show_error_message()
    else:
        janela_quality = Toplevel()
        janela_quality.title('Qualidade')
        janela_quality.geometry('300x200')

        Label(janela_quality, text='Escolha a qualidade:', font='arial 12 bold', pady=30).pack()

        for option in options:
            Button(janela_quality, text=option, command=lambda x=option: show_format_options(audio_only=audio_only, resolution=x)).pack()

def show_format_options(audio_only=False, resolution=None):
    options = ['MP3', 'WAV']
    janela_format = Toplevel()
    janela_format.title('Formato')
    janela_format.geometry('300x200')

    Label(janela_format, text='Escolha o formato:', font='arial 12 bold', pady=30).pack()

    for option in options:
        Button(janela_format, text=option, command=lambda x=option: download(link.get(), audio_only=audio_only, resolution=resolution, file_format=x)).pack()

quadro = Frame(janela)
quadro.pack()

Label(quadro, text='Link:', font='arial 12 bold').pack(side='left')
link = Entry(quadro, font='arial 20', width=50)
link.pack(side='left')

Button(quadro, bg='green', text='Vídeo', bd=1, fg='white', width=4, height=2,
       command=lambda: show_quality_options()).pack(side='left')

Button(quadro, bg='green', text='Áudio', bd=1, fg='white', width=4, height=2,
       command=lambda: show_quality_options(audio_only=True)).pack(side='left')

janela.mainloop()