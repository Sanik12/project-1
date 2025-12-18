
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.list import OneLineAvatarIconListItem, IconLeftWidget
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.scrollview import MDScrollView
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock

from kivy.utils import platform

import random
import string

# --- Android phone size simulation (desktop only) ---
Window.size = (360, 640)
Window.resizable = False

KV = """
MDScreen:
    md_bg_color: 0.95, 0.96, 0.97, 1

    MDBottomNavigation:
        panel_color: 1, 1, 1, 1

        # ===== HOME TAB =====
        MDBottomNavigationItem:
            name: "accounts"
            text: "Accounts"
            icon: "key"

            MDBoxLayout:
                orientation: "vertical"
                padding: "12dp"
                spacing: "16dp"

                MDBoxLayout:
                    orientation: "vertical"
                    adaptive_height: True
                    padding: "16dp"
                    spacing: "12dp"

                    canvas.before:
                        Color:
                            rgba: 1, 1, 1, 1
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [16]

                    MDBoxLayout:
                        size_hint_y: None
                        height: "48dp"
                        spacing: "8dp"

                        MDIcon:
                            icon: "magnify"
                            theme_text_color: "Primary"
                            size_hint: None, None
                            size: "64dp", "64dp"
                            pos_hint: {"center_y": 0.5}

                        MDTextField:
                            id: search_input
                            hint_text: "Search accounts..."
                            radius: [24, 24, 24, 24]
                            mode: "round"
                            size_hint_x: 1
                            height: "48dp"
                            pos_hint: {"center_y": 0.5}
                            on_text: app.filter_accounts(self.text)

                       

                    MDBoxLayout:
                        adaptive_height: True
                        
                        spacing: "8dp"

                        MDRaisedButton:
                            text: "A-Z"
                            pos_hint: {"center_y": 0.53}
                            on_release: app.sort_accounts("az")
                        MDRaisedButton:
                            text: "Z-A"
                            pos_hint: {"center_y": 0.53}
                            on_release: app.sort_accounts("za")
                        MDRaisedButton:
                            text: "Newest"
                            pos_hint: {"center_y": 0.53}
                            on_release: app.sort_accounts("newest")
                        MDRaisedButton:
                            text: "Oldest"
                            pos_hint: {"center_y": 0.53}
                            on_release: app.sort_accounts("oldest")

                OneLineAvatarIconListItem:
                    text: "Add password"
                    on_release: app.open_add_password_dialog()
                    IconLeftWidget:
                        icon: "plus-circle-outline"

                MDSeparator:
                    color: 0.88, 0.88, 0.88, 1

                ScrollView:
                    MDList:
                        id: password_list
                        padding: 0, 0, 0, "80dp"

        # ===== PASSWORD GENERATOR TAB =====
        MDBottomNavigationItem:
            name: "password_gen"
            text: "Password Gen"
            icon: "shield-key-outline"

            ScrollView:
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "20dp"
                    size_hint_y: None
                    height: self.minimum_height

                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "20dp"
                        spacing: "20dp"
                        size_hint_y: None
                        height: self.minimum_height

                        canvas.before:
                            Color:
                                rgba: 1, 1, 1, 1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [16]

                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: "12dp"
                            size_hint_y: None
                            height: "60dp"

                            MDIcon:
                                icon: "key-variant"
                                theme_text_color: "Primary"
                                font_size: "48sp"
                                size_hint_x: None
                                width: "60dp"

                            MDLabel:
                                text: "Generate a strong password"
                                halign: "left"
                                valign: "middle"
                                theme_text_color: "Primary"

                        MDTextField:
                            id: length_input
                            hint_text: "Enter password length (e.g., 12)"
                            mode: "rectangle"
                            input_filter: "int"
                            max_text_length: 3
                            size_hint_y: None
                            height: "48dp"

                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: "10dp"
                            size_hint_y: None
                            height: "48dp"
                            MDLabel:
                                text: "Include Uppercase?"
                                valign: "middle"
                            MDSwitch:                             
                                id: uppercase_switch
                                active: True

                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: "10dp"
                            size_hint_y: None
                            height: "48dp"
                            MDLabel:
                                text: "Include Special Characters?"
                                valign: "middle"
                            MDSwitch:
                                id: special_switch
                                active: True

                        MDRaisedButton:
                            text: "Generate Password"
                            pos_hint: {"center_x": 0.5}
                            on_release: app.generate_password()

                        MDTextField:
                            id: password_output
                            hint_text: "Generated Password"
                            readonly: True
                            mode: "rectangle"
                            size_hint_y: None
                            height: "48dp"

        # ===== SETTINGS TAB =====
        MDBottomNavigationItem:
            name: "settings"
            text: "Settings"
            icon: "cog"

            ScrollView:
                MDBoxLayout:
                    orientation: "vertical"
                    padding: "16dp"
                    spacing: "16dp"
                    size_hint_y: None
                    height: self.minimum_height

                    
                    # SECURITY
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "36dp"
                        spacing: "12dp"
                        size_hint_y: None
                        height: self.minimum_height
                        canvas.before:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [16]

                        MDLabel:
                            text: "Security"
                            font_style: "H6"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: "10dp"
                            size_hint_y: None
                            height: "48dp"
                            MDLabel:
                                text: "Require Master Password"
                                valign: "middle"
                            MDSwitch:
                                id: master_password
                                pos_hint: {"center_y": 0.34}
                                on_active: app.on_master_password_toggle(self.active)

                    # APP PASSWORD
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "36dp"
                        spacing: "12dp"
                        size_hint_y: None
                        height: self.minimum_height
                        canvas.before:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [16]

                        MDLabel:
                            text: "Password"
                            font_style: "H6"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDBoxLayout:
                            orientation: "horizontal"
                            spacing: "10dp"
                            size_hint_y: None
                            height: "48dp"
                            MDLabel:
                                text: "Set Master Password"
                                valign: "middle"
                            MDRaisedButton:
                                text: "SET"
                                pos_hint: {"center_y": 0.53}
                                on_release: app.on_set_master_password()                            


                    # APP INFO
                    MDBoxLayout:
                        orientation: "vertical"
                        padding: "36dp"
                        spacing: "22dp"
                        size_hint_y: None
                        height: self.minimum_height
                        canvas.before:
                            Color:
                                rgba: 1,1,1,1
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [16]

                        MDLabel:
                            text: "App Info"
                            font_style: "H6"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Version: 1.0.0"
                        MDLabel:
                            text: "Developer: Jason Duodoo"
"""

# --- Add Password Dialog Content ---


class AddPasswordContent(MDScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = "250dp"  # Fixed height to avoid KivyMD dialog calculation issues

        layout = MDBoxLayout(
            orientation="vertical",
            spacing="12dp",
            padding="12dp",
            size_hint_y=None
        )
        layout.bind(minimum_height=layout.setter("height"))

        self.site_input = MDTextField(
            hint_text="Website / App",
            mode="rectangle",
            size_hint_y=None,
            height="48dp"
        )
        layout.add_widget(self.site_input)

        self.user_input = MDTextField(
            hint_text="Username / Email",
            mode="rectangle",
            size_hint_y=None,
            height="48dp"
        )
        layout.add_widget(self.user_input)

        self.pass_input = MDTextField(
            hint_text="Password",
            mode="rectangle",
            size_hint_y=None,
            height="48dp"
        )
        layout.add_widget(self.pass_input)

        self.add_widget(layout)

# --- Main App ---


class PasswordManagerApp(MDApp):
    def build(self):
        self.store = JsonStore("passwords.json")
        self.locked = False
        self.root_switch_sync = self.store.exists("security")

        if self.store.exists("security"):
            self.locked = True

        # Stores accounts as {site_name: (username, password)}
        self.accounts = {}

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "DeepPurple"

        screen = Builder.load_string(KV)
        screen.ids.master_password.active = self.store.exists("security")

        self.dialog = None
        self.add_dialog = None

        self.locked = self.store.exists("security")
        if self.locked:
            Clock.schedule_once(lambda dt: self.ask_master_password(), 0.5)
        return screen

    def ask_master_password(self):
        self.unlock_input = MDTextField(
            hint_text="Enter Master Password",
            password=True,
            mode="rectangle"
        )

        self.unlock_dialog = MDDialog(
            title="Unlock App",
            type="custom",
            content_cls=self.unlock_input,
            auto_dismiss=False,
            buttons=[

                MDRaisedButton(
                    text="  UNLOCK ",
                    on_release=lambda x: self.verify_master_password(),
                    pos_hint={"center_y": 0.5},

                ),
                MDRaisedButton(
                    text=" USE PHONE PASSWORD  ",
                    on_release=lambda x: self.unlock_with_phone(),
                    pos_hint={"center_y": 0.5},
                )
            ],

        )

        self.unlock_dialog.open()

    def unlock_with_phone(self):
        if platform != "android":
            self.show_warning(
                "Phone unlock is only available on mobile devices.")
            return

    def on_master_password_toggle(self, active):
        if not active:
            confirm = MDDialog(
                title="Disable Master Password?",
                text="This will permanently delete your master password.",
                auto_dismiss=False,
                buttons=[
                    MDRaisedButton(
                        text="CANCEL",
                        on_release=lambda x: (
                            setattr(self.root.ids.master_password,
                                    "active", True),
                            confirm.dismiss()
                        )
                    ),
                    MDRaisedButton(
                        text="DELETE",
                        on_release=lambda x: (
                            self.store.delete("security") if self.store.exists(
                                "security") else None,
                            setattr(self, "locked", False),
                            confirm.dismiss(),
                            self.show_warning(
                                "Master password has been deleted.")
                        )
                    ),
                ],
            )
            confirm.open()
        else:
            self.open_set_password_dialog()

    def verify_master_password(self):
        entered = self.unlock_input.text.strip()
        stored = self.store.get("security")["master_password"]

        if entered == stored:
            self.locked = False
            self.unlock_dialog.dismiss()
            self.unlock_input.text = ""
        else:
            self.show_warning("Incorrect master password.")

    def toggle_theme(self, active):
        self.theme_cls.theme_style = "Dark" if active else "Light"

    def generate_password(self):
        length_input = self.root.ids.length_input.text
        include_upper = self.root.ids.uppercase_switch.active
        include_special = self.root.ids.special_switch.active

        try:
            length = int(length_input)
            if length <= 0:
                raise ValueError
        except:
            self.root.ids.password_output.text = "Enter valid length!"
            return

        if length < 8:
            self.show_warning(
                "Password is short! Consider using 8+ characters."
            )

        charset = string.ascii_lowercase + string.digits
        if include_upper:
            charset += string.ascii_uppercase
        if include_special:
            charset += string.punctuation

        password = "".join(random.choice(charset) for _ in range(length))
        self.root.ids.password_output.text = password

    def on_set_master_password(self):
        if self.root.ids.master_password.active:
            self.open_set_password_dialog()
        else:
            self.show_warning(
                "Enable 'Require Master Password' to set it first.")

    def view_account_details(self, account):
        detail_dialog = MDDialog(
            title=f"Account: {account['username']}",
            text=f"Website/App: {account['site']}\nPassword: {account['password']}",
            size_hint=(0.8, None),
            height="220dp",
            buttons=[
                MDRaisedButton(
                    text="DELETE",
                    md_bg_color=(1, 0.3, 0.3, 1),
                    on_release=lambda x: self.delete_account(
                        account, detail_dialog)
                ),
                MDRaisedButton(
                    text="CLOSE",
                    on_release=lambda x: detail_dialog.dismiss()
                ),
            ]
        )
        detail_dialog.open()

    def delete_account(self, account, dialog):
        site = account["site"]

        # Remove from stored accounts
        if site in self.accounts:
            self.accounts[site] = [
                acc for acc in self.accounts[site] if acc != account
            ]

            # Remove site key if empty
            if not self.accounts[site]:
                del self.accounts[site]

        # Refresh the visible list
        self.refresh_account_list()

        dialog.dismiss()

    def refresh_account_list(self):
        password_list = self.root.ids.password_list
        password_list.clear_widgets()

        for site_accounts in self.accounts.values():
            for account in site_accounts:
                item = OneLineAvatarIconListItem(
                    text=account["username"],
                    on_release=lambda x, a=account: self.view_account_details(
                        a)
                )
                item.add_widget(IconLeftWidget(icon="account-circle"))
                password_list.add_widget(item)

    def save_master_password(self):
        password = self.master_pass_input.text.strip()
        if not password:
            self.show_warning("Password cannot be empty.")
            return

        # Store the master password in memory (you can later use it for authentication)
        self.store.put("security", master_password=password)

        # Clear the input field
        self.master_pass_input.text = ""

        # Close the dialog
        self.master_pass_dialog.dismiss()

        # Inform user
        self.show_warning("Master password set successfully!")

        def on_set_master_password(self):
            if self.root.ids.master_password.active:
                self.open_set_password_dialog()
            else:
                self.show_warning(
                    "Enable 'Require Master Password' to set it first.")

    def open_set_password_dialog(self):

        # Only create the dialog once
        if not hasattr(self, "master_pass_dialog"):
            self.master_pass_input = MDTextField(
                hint_text="Enter Master Password",
                password=True,
                mode="rectangle"
            )

            self.master_pass_dialog = MDDialog(
                title="Enter New Master Password",
                type="custom",
                content_cls=self.master_pass_input,
                buttons=[
                    MDRaisedButton(
                        text="CANCEL",
                        on_release=lambda x: self.master_pass_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="SAVE",

                        on_release=lambda x: self.save_master_password()

                    ),
                ],
            )

        self.master_pass_dialog.open()

    def sort_accounts(self, mode):
        password_list = self.root.ids.password_list
        password_list.clear_widgets()

        all_accounts = []
        for site_accounts in self.accounts.values():
            all_accounts.extend(site_accounts)

        if mode == "az":
            all_accounts.sort(key=lambda x: x["username"].lower())
        elif mode == "za":
            all_accounts.sort(
                key=lambda x: x["username"].lower(), reverse=True)
        elif mode == "newest":
            all_accounts.sort(key=lambda x: x["created"], reverse=True)

        for account in all_accounts:
            item = OneLineAvatarIconListItem(
                text=account["username"],
                on_release=lambda x, a=account: self.view_account_details(a)
            )
            item.add_widget(IconLeftWidget(icon="account-circle"))
            password_list.add_widget(item)

    def show_warning(self, message):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Warning",
                text=message,
                size_hint=(0.8, None),
                height="180dp"
            )
        else:
            self.dialog.text = message
        self.dialog.open()

    def filter_accounts(self, query):
        query = query.strip().lower()
        password_list = self.root.ids.password_list
        password_list.clear_widgets()  # clear the current list

        for site_accounts in self.accounts.values():
            for account in site_accounts:
                if query in account['username'].lower():  # search by username/email
                    item = OneLineAvatarIconListItem(
                        text=account['username'],
                        on_release=lambda x, a=account: self.view_account_details(
                            a)
                    )
                    item.add_widget(IconLeftWidget(icon="account-circle"))
                    password_list.add_widget(item)

    def open_add_password_dialog(self):
        if not self.add_dialog:
            self.add_dialog = MDDialog(
                title="Add Password",
                type="custom",
                content_cls=AddPasswordContent(),
                buttons=[
                    MDRaisedButton(
                        text="CANCEL",
                        on_release=lambda x: self.add_dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="SAVE",
                        on_release=lambda x: self.save_password()
                    ),
                ],
            )
        self.add_dialog.open()

    def save_password(self):
        content = self.add_dialog.content_cls

        site = content.site_input.text.strip()
        username = content.user_input.text.strip()
        password = content.pass_input.text.strip()

        if not site or not username or not password:
            self.show_warning("All fields are required.")
            return

        # Create account dict
        account = {
            "site": site,
            "username": username,
            "password": password,
            # simple timestamp substitute
            "created": len(self.accounts) + random.random()
        }

        # Store account
        if site not in self.accounts:
            self.accounts[site] = []
        self.accounts[site].append(account)

        # Add username/email as the main list item
        item = OneLineAvatarIconListItem(
            text=username,  # main list shows username/email
            on_release=lambda x, a=account: self.view_account_details(a)
        )
        item.add_widget(IconLeftWidget(icon="account-circle"))
        self.root.ids.password_list.add_widget(item)

        # Clear inputs
        content.site_input.text = ""
        content.user_input.text = ""
        content.pass_input.text = ""

        self.add_dialog.dismiss()


if __name__ == "__main__":
    PasswordManagerApp().run()
