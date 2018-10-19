from cv2 import namedWindow
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from focusWidgets import FocusWithColor
from functools import partial
from kivy.utils import get_color_from_hex

'''
Pop up button, any key press will dismiss the popup.
'''



#bind keyboard to button/widget
class PopUpButton(Button):
    popup = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(PopUpButton, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if (self.popup is not None):
            self.popup.dismiss()
        return True

class Authentication:
    def __init__(self, dbHelper):
        self.m_dbHelper = dbHelper

    '''
    Login functionality
    check if user and corresponding password match from data base.
    '''

    def login(self, nameWidget, passwordWidget, calleeWidget):
        retVal = False
        result = self.m_dbHelper.findDeviceUser(nameWidget.text, passwordWidget.text)
        if (result.count() <= 0):
            text = "Either User Name or Password Is Incorrect."
            print(text)
            self.createPopUp(text, calleeWidget)
        elif (result.count() == 1):
            retVal = True
            nameWidget.text = ""
            passwordWidget.text = ""

        if (retVal == True):
            self.m_dbHelper.setCurrentDeviceUser(result[0])

        return retVal

    # creates and opens pop up
    def createPopUp(self, text, calleeWidget):
        box = BoxLayout(orientation='vertical')
        lab = Label(text=text)
        button = PopUpButton(text="OK")
        box.add_widget(lab)
        box.add_widget(button)
        popup = Popup(title='Info',
                      content=box,
                      size_hint=(0.6, 0.2))
        button.focus = True
        calleeWidget.focus = False
        button.bind(on_press=popup.dismiss)
        button.popup = popup
        popup.open()

    def isUserAdmin(self):
        currUser = self.m_dbHelper.getCurrentDeviceUser()
        if (currUser["role"] == "admin"):
            return True
        else:
            return False

    def signUp(self, nameWidget, passwordWidget, confirmPasswordWidget, roleWidget, calleeWidget):
        retVal = False
        if (self.basicNotEmptyChecks(nameWidget.text, passwordWidget.text, confirmPasswordWidget.text, calleeWidget)):
            # check if password and confirm password match
            if (passwordWidget.text != confirmPasswordWidget.text):
                text = "passwords dont match"
                print(text)
                self.createPopUp(text, calleeWidget)

            else:
                # check if name is not admin
                if (nameWidget.text.lower() == "admin"):
                    text = "cannot use that user name, enter another."
                    print(text)
                    self.createPopUp(text, calleeWidget)

                else:
                    # check if user with same password and name exists in db
                    if (self.m_dbHelper.findDeviceUser(nameWidget.text, passwordWidget.text).count() <= 0):
                        entry = {
                            "name": nameWidget.text,
                            "password": passwordWidget.text,
                            "role": roleWidget.text
                        }
                        if (self.m_dbHelper.insertDeviceUserInDb(entry)):
                            retVal = True
                            text = "Account created Successfully"
                            print(text)
                            self.createPopUp(text,calleeWidget)
                            self.clearAddUserData(nameWidget, passwordWidget, confirmPasswordWidget, roleWidget)

                    else:
                        text = "enter different user name and password"
                        print(text)
                        self.createPopUp(text, calleeWidget)

        return retVal

    #checks if all fields are filled.
    def basicNotEmptyChecks(self, name, password, confirmPassword, calleeWidget):
        text = ""
        retVal = True
        if (len(name) <= 0):
            text = text + "name is empty,"
            retVal = False
        if (len(password) <= 0):
            text = text + "password is empty,"
            retVal = False
        if (len(confirmPassword) <= 0):
            text = text + "confirm password is empty,"
            retVal = False

        if (retVal == False):
            print(text)
            self.createPopUp(text, calleeWidget)
        return retVal


    def logOut(self):
        entry = {
            "name": "",
            "password":"",
            "role": "local"
        }
        self.m_dbHelper.setCurrentDeviceUser(entry)
        return True

    def clearAddUserData(self, nameWidget, passwordWidget, confirmPasswordWidget, roleWidget):
        nameWidget.text = ""
        passwordWidget.text = ""
        confirmPasswordWidget.text = ""
        roleWidget.text = ""
        return True
