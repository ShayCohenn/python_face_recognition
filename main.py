import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserListView
import cv2
import os

# Set the Kivy version
kivy.require('1.11.1')

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        self.capture = None

    def start_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.ids.image_preview.texture = None

    def stop_camera(self):
        if self.capture:
            self.capture.release()
            self.capture = None

    def capture_image(self):
        if self.capture:
            ret, frame = self.capture.read()
            if ret:
                cv2.imwrite('captured_image.jpg', frame)
                self.display_image('captured_image.jpg')
                self.stop_camera()

    def upload_image(self, selected_file):
        if selected_file:
            self.display_image(selected_file[0])

    def display_image(self, image_path):
        self.ids.image_preview.source = image_path

class LoginRegisterApp(App):
    def build(self):
        # Create a ScreenManager
        sm = ScreenManager()

        # Create the main menu screen
        main_menu = Screen(name='main_menu')
        main_menu_layout = BoxLayout(orientation='vertical', spacing=10, padding=50)
        
        register_button = Button(text="Register", size_hint=(None, None), size=(200, 50))
        register_button.bind(on_release=self.goto_register_screen)

        login_button = Button(text="Login", size_hint=(None, None), size=(200, 50))
        login_button.bind(on_release=self.goto_login_screen)

        main_menu_layout.add_widget(register_button)
        main_menu_layout.add_widget(login_button)

        main_menu.add_widget(main_menu_layout)

        # Create the register screen
        register_screen = RegisterScreen(name='register_screen')
        register_layout = BoxLayout(orientation='vertical', spacing=10, padding=50)

        register_label = Label(text="Register Page")

        start_camera_button = Button(text="Start Camera", size_hint=(None, None), size=(200, 50))
        start_camera_button.bind(on_release=register_screen.start_camera)

        stop_camera_button = Button(text="Stop Camera", size_hint=(None, None), size=(200, 50))
        stop_camera_button.bind(on_release=register_screen.stop_camera)

        capture_image_button = Button(text="Capture Image", size_hint=(None, None), size=(200, 50))
        capture_image_button.bind(on_release=register_screen.capture_image)

        image_preview = Image()

        # Create a FileChooserListView widget for image upload
        file_chooser = FileChooserListView()
        file_chooser.bind(on_submit=register_screen.upload_image)

        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_release=self.goto_main_menu)

        register_layout.add_widget(register_label)
        register_layout.add_widget(start_camera_button)
        register_layout.add_widget(stop_camera_button)
        register_layout.add_widget(capture_image_button)
        register_layout.add_widget(file_chooser)
        register_layout.add_widget(image_preview)
        register_layout.add_widget(back_button)

        register_screen.add_widget(register_layout)

        # Add screens to the ScreenManager
        sm.add_widget(main_menu)
        sm.add_widget(register_screen)

        return sm

    def goto_register_screen(self, instance):
        self.root.current = 'register_screen'

    def goto_login_screen(self, instance):
        self.root.current = 'login_screen'

    def goto_main_menu(self, instance):
        self.root.current = 'main_menu'

if __name__ == '__main__':
    LoginRegisterApp().run()
