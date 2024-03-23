# Import necessary modules
import os
import pygame
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.lang import Builder
from kivy.clock import Clock

# Load the KV language string
kv_string = """
<RootLayout>:
    orientation: 'vertical'
    SelectedFileLabel:
        id: selected_file_label
    FileChooserListView:
        id: file_chooser
        on_selection: root.on_file_selected()
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(40)
        spacing: dp(10)
        Button:
            text: 'Play'
            on_release: root.play_music()
        Button:
            text: 'Pause'
            on_release: root.pause_music()
        Button:
            text: 'Stop'
            on_release: root.stop_music()
    Slider:
        id: volume_slider
        min: 0
        max: 100
        value: 70
        on_value_pos: root.set_volume(self.value)
    Label:
        id: playback_time_label
        text: 'Playback Time: 00:00'
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(40)
        padding: dp(10)
        Label:
            id: duration_label
            text: 'Duration: --:--'
        Slider:
            id: seek_slider
            min: 0
            max: 100
            value: 0
            on_touch_up: root.seek_music(self.value)
"""

# Define the root layout class
class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__(**kwargs)
        self.selected_file = None
        self.playback_clock_event = None

    def play_music(self):
        if self.selected_file:
            pygame.mixer.music.load(self.selected_file)
            pygame.mixer.music.play()
            self.start_playback_clock()
            self.ids.seek_slider.max = pygame.mixer.Sound(self.selected_file).get_length()

    def pause_music(self):
        pygame.mixer.music.pause()

    def stop_music(self):
        pygame.mixer.music.stop()
        self.stop_playback_clock()
        self.ids.seek_slider.value = 0

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume / 100)

    def on_file_selected(self):
        # Update the selected file label
        self.selected_file = self.ids.file_chooser.selection[0] if self.ids.file_chooser.selection else None
        self.ids.selected_file_label.text = self.selected_file if self.selected_file else "No file selected"

        # Update the duration label
        if self.selected_file:
            audio = pygame.mixer.Sound(self.selected_file)
            duration_minutes = int(audio.get_length() // 60)
            duration_seconds = int(audio.get_length() % 60)
            self.ids.duration_label.text = f'Duration: {duration_minutes:02d}:{duration_seconds:02d}'
        else:
            self.ids.duration_label.text = 'Duration: --:--'

    def update_playback_time(self, dt):
        if pygame.mixer.music.get_busy():
            playback_time = pygame.mixer.music.get_pos() / 1000
            minutes = int(playback_time // 60)
            seconds = int(playback_time % 60)
            self.ids.playback_time_label.text = f'Playback Time: {minutes:02d}:{seconds:02d}'
            self.ids.seek_slider.value = playback_time
        else:
            self.stop_playback_clock()

    def start_playback_clock(self):
        self.playback_clock_event = Clock.schedule_interval(self.update_playback_time, 1)

    def stop_playback_clock(self):
        if self.playback_clock_event:
            self.playback_clock_event.cancel()
            self.playback_clock_event = None

    def seek_music(self, value):
        pygame.mixer.music.set_pos(value)

# Define the label class for displaying the selected file
class SelectedFileLabel(Label):
    pass

# Define the main application class
class MelodyApp(App):
    def build(self):
        # Initialize Pygame mixer
        pygame.mixer.init()

        # Load the KV language string
        Builder.load_string(kv_string)
        return RootLayout()

# Run the application
if __name__ == '__main__':
    MelodyApp().run()
