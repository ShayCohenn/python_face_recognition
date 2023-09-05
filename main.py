import os
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput
from face_rec import recognize_face_register, recognize_face_for_login

kivy.require('1.11.1')

# Main application class for login and registration.
class LoginRegisterApp(App):

    # Build the application UI.
    def build(self):
        # Create a ScreenManager
        screen_manager = ScreenManager()

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

        # Create the login screen
        login_screen = Screen(name='login_screen')
        login_layout = BoxLayout(orientation='vertical', spacing=10, padding=50)

        login_label = Label(text="Login Page")
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_release=self.goto_main_menu)

        login_button = Button(text="Login with Face Recognition", size_hint=(None, None), size=(200, 50))
        login_button.bind(on_release=self.start_camera_and_recognize)

        result_label = Label(text="")  # Label to display recognition result
        login_layout.add_widget(login_label)
        login_layout.add_widget(back_button)
        login_layout.add_widget(login_button)
        login_layout.add_widget(result_label)

        login_screen.add_widget(login_layout)

        # Create the register screen
        register_screen = Screen(name='register_screen')
        register_layout = BoxLayout(orientation='vertical', spacing=10, padding=50)

        register_label = Label(text="Register Page")

        name_input = TextInput(hint_text="Enter your name")

        save_button = Button(text="Save Images", size_hint=(None, None), size=(200, 50))
        save_button.bind(on_release=lambda instance: self.save_images(name_input.text))

        start_camera_button = Button(text="Start Camera", size_hint=(None, None), size=(200, 50))
        start_camera_button.bind(on_release=self.start_camera_register)

        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_release=self.goto_main_menu)

        register_layout.add_widget(register_label)
        register_layout.add_widget(name_input)
        register_layout.add_widget(save_button)
        register_layout.add_widget(start_camera_button)
        register_layout.add_widget(back_button)

        register_screen.add_widget(register_layout)

        # Add screens to the ScreenManager
        screen_manager.add_widget(main_menu)
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(register_screen)

        self.result_label = result_label

        return screen_manager
    
    # Start the camera and perform face recognition.
    def start_camera_and_recognize(self, _):
        recognized_result = recognize_face_for_login()
        self.show_recognized_result(recognized_result)

    # Display the recognized result.
    def show_recognized_result(self, result):
        message = f"Hello {result}"
        self.result_label.text = message

    # Navigate to the login screen.
    def goto_login_screen(self, _):
        self.root.current = 'login_screen'

    # Navigate to the register screen.
    def goto_register_screen(self, _):
        self.root.current = 'register_screen'

    # Navigate to the main menu screen.
    def goto_main_menu(self, _):
        self.root.current = 'main_menu'

    # Save detected face images to the specified directory.
    def save_images(self, name):
        image_dir = os.path.join("faces", f"{name}_images")
        os.makedirs(image_dir, exist_ok=True)

        for filename in os.listdir():
            if filename.startswith("face_") and filename.endswith(".png"):
                destination_file = os.path.join(image_dir, filename)
                if os.path.exists(destination_file):
                    base, ext = os.path.splitext(destination_file)
                    i = 1
                    while os.path.exists(destination_file):
                        destination_file = f"{base}_{i}{ext}"
                        i += 1
                os.rename(filename, destination_file)
    
    # Start the camera for registration.
    def start_camera_register(self, _):
        recognize_face_register(self)

if __name__ == '__main__':
    LoginRegisterApp().run()