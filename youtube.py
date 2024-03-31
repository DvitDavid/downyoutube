import flet 
import os
import subprocess
import time

from flet import AlertDialog, Container, ElevatedButton, Page, ProgressBar, Row, Text, TextField
from pytube import YouTube




def main(page:Page):
    page.title = "Descarregar de Youtube"
    page.window_width=730
    page.window_height=260
    page.splash = ProgressBar(visible=False)
    lbl_titol = Text("Descarregar video o audio de Youtube", size=30)
    txt_url = TextField(label='URL', autofocus=True)
    bt_enviar_video = ElevatedButton("Descarregar Video")
    bt_enviar_audio = ElevatedButton("Descarregar Audio")
    dlg_missatge = AlertDialog(title=Text("Descàrrega exitosa."),  on_dismiss=lambda _: print("test"))
    
         

    def bt_click(event):
        carpeta_actual = os.getcwd()
        yt = YouTube(txt_url.value)
        page.splash = ProgressBar(visible=True)
        video = yt.streams.get_highest_resolution()
        page.update()
        video.download(output_path = carpeta_actual)
        time.sleep(0.5)
        page.dialog = dlg_missatge
        dlg_missatge.content=Text(f"{carpeta_actual}")
        dlg_missatge.open = True
        page.splash = ProgressBar(visible=False)
        page.update()
    
    def bt_click_audio(event):
        
        carpeta_actual = os.getcwd()
        yt = YouTube(txt_url.value)
        page.splash = ProgressBar(visible=True)
        audio= yt.streams.filter(only_audio=True, subtype='webm', abr='160kbps').first()

        final_audio = audio.download(output_path = carpeta_actual)
        page.update()
        
        base, ext = os.path.splitext(final_audio) 
        nou_audio = base + '.mp3'
        os.rename(final_audio, nou_audio)
        time.sleep(0.5)      
        
        page.dialog = dlg_missatge
        dlg_missatge.content=Text(f"{carpeta_actual}")
        dlg_missatge.open = True
        page.splash = ProgressBar(visible=False)        
        page.update()   

    
    bt_enviar_video.on_click = bt_click
    bt_enviar_audio.on_click = bt_click_audio
    

    page.add(
        lbl_titol,
        txt_url,
        Row(controls=[bt_enviar_video, bt_enviar_audio]),        
    )

if __name__ == "__main__":
    # flet.app(target=main, view=flet.WEB_BROWSER, port=5500)
    flet.app(target=main)