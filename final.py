from test import test
import face_recognition
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import os
import subprocess
import datetime


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")

        self.cap = cv2.VideoCapture(0)
        self.url = "v3.mp4"
        self.cap.open(self.url)

        self.most_recent_capture_pil = None
        self.most_recent_capture_arr = None

        self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'register new user', 'gray',
                                                                    self.register_new_user, fg='black')
        self.register_new_user_button_main_window.place(x=750, y=400)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()

        if ret:
            self.most_recent_capture_arr = frame
            img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
            self.most_recent_capture_pil = Image.fromarray(img_)
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)

            self._label.imgtk = imgtk
            self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):

        label = test(
            image = self.most_recent_capture_arr ,
            model_dir = r"C:\Users\admin\Desktop\FaceApp\FaceAntiSpoofing\resources\anti_spoof_models",
            device_id = 0
        )
        if label == 1 : 

            unknown_img_path = './.tmp.jpg'

            cv2.imwrite(unknown_img_path , self.most_recent_capture_arr)

            output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path], stderr=subprocess.STDOUT))
            
            name = output.split(',')[1][:-5]
            print(name) # prints 'unknown_person' or 'no_persons_found' or the name of the person

            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box("Error", "Unknown user. Please register first.")
            else:
                util.msg_box("Successfully login", 'Welcome, {}.'.format(name))
                with open(self.log_path , 'a') as f : 
                    f.write('{} , {}\n'.format(name, datetime.datetime.now()))
                    f.close()

            os.remove(unknown_img_path)
        else : 
            util.msg_box("Fake Face Detected", "Fake face detected. Please try again.")

    def logout(self):
        # Display logout message
        util.msg_box("Logout", "You have been logged out successfully.")

        self.main_window.destroy()


        

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window, "Enter Username:")
        self.text_label_register_new_user.place(x=750, y=70)

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, "Accept", 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, "Try Again", 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label_register_new_user = util.get_img_label(self.register_new_user_window)
        self.capture_label_register_new_user.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label_register_new_user)
       

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        if self.most_recent_capture_pil:
            imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
            label.imgtk = imgtk
            label.configure(image=imgtk)

            self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    
    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c").strip()

        if name:
            if self.register_new_user_capture is not None:
                filename = '{}.jpg'.format(name)
                filepath = os.path.join(self.db_dir, filename)
                cv2.imwrite(filepath, self.register_new_user_capture)
                print(f"Image saved as: {filepath}")
            else:
                print("Error: No image captured.")
        else:
            print("Error: Please enter a username.")

        util.msg_box("Success", "User registered successfully.")

        self.register_new_user_window.destroy()


if __name__ == "__main__":
    app = App()
    app.start()