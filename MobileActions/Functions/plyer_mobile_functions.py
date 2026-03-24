from plyer import email, call, sms
from kivy.properties import NumericProperty, ObjectProperty


# =======================================EMAIL===========================================
send_email_schema = {
        "function": {
            "name": "send_email",
            "description": "Sends an email.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "to": {"type": "STRING", "description": "The recipient email address."},
                    "subject": {"type": "STRING", "description": "The email subject."},
                    "body": {"type": "STRING", "description": "The email body."},
                    "create_chooser": {"type": "BOOLEAN", "description": "Whether to display a program chooser to handle the message."}
                },
                "required": ["to", "subject"],
            },
        }
    }
def send_email(to: str, subject:str, body: str = "", create_chooser: bool = True):
    """Sends an email.
    Parameters:
        to: The recipient email address (e.g. 'abc@gmail.com').
        subject: The email subject/title/.
        body: The email body.
        create_chooser: Whether to display a program chooser to handle the message.

    """
    try:
        email.send(recipient= to,
                   subject= subject,
                   text=body,
                   create_chooser= create_chooser)
    except Exception as e:
        raise Exception(f"Error in sending Email to {to}, with subject of {subject}: {e}")

    return {"response": f"Sent the email to {to} with subject of {subject} and body of {body[0:10]} ...!"}
# ==================================================================================
# =======================================CALL===========================================
phone_call_schema = {
        "function": {
            "name": "phone_call",
            "description": "Make a call with number or open phone dial.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "number": {"type": "STRING", "description": "The number to which we want to call."},
                    "dial_call": {"type": "BOOLEAN", "description": "True if you want to dial call via phone, and False if you want to call the number directly."}
                },
                "required": ["number", "dial_call"],
            },
        }
    }

def phone_call(number:str = "", dial_call: bool = False):
    """Make a call with number or open phone dial.
    Parameters:
        number: The number to which we want to call.
        dial_call: True if you want to dial call via phone, and False if you want to call the number directly.

    """
    try:
        if(dial_call):
            call.dialcall()
        else:
            call.makecall(tel=number)
    except Exception as e:
        raise Exception(f"Error in calling to {number} or dialling: {e}")

    return {"response": f"Call made to the number {number} or opened dialling, successfully!"}

# ==================================================================================
# =======================================SMS===========================================
phone_sms_schema = {
        "function": {
            "name": "phone_sms",
            "description": "Send a sms message.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "sms_recipient": {"type": "STRING", "description": "The recipient number."},
                    "sms_message": {"type": "STRING", "description": "The message body."}
                },
                "required": ["sms_recipient"],
            },
        }
    }

def phone_sms(sms_recipient:str = "", sms_message:str = ""):
    """Send a sms message.
    Parameters:
        sms_recipient: The recipient number.
        sms_message: The message body.

    """
    try:
        sms.send(recipient= sms_recipient, message= sms_message)
    except Exception as e:
        raise Exception(f"Error in sending sms message to {sms_recipient}: {e}")

    return {"response": f"SMS message sent to {sms_recipient}, successfully!"}

# ==================================================================================
# =======================================LIGHT===========================================
LIGHT = ObjectProperty()
ILLUMINATION = NumericProperty()
def get_illumination(illumination, light):
    ILLUMINATION = light.illumination or illumination

turnOn_light_schema = {
        "function": {
            "name": "turnOn_light",
            "description": "Turn on the light.",
            "parameters": {
                "type": "OBJECT",
                "properties": {},
                "required": [],
            },
        }
    }

def turnOn_light():
    """
    Turn on the light.
    """
    try:
        from plyer import light
        from kivy.clock import Clock
        light.enable()
        Clock.schedule_interval(get_illumination(ILLUMINATION, light), 1 / 20.)
    except Exception as e:
        raise Exception(f"Error in turning the light on: {e}")

    return {"response": f"Light's turned on successfully!"}


turnOff_light_schema = {
        "function": {
            "name": "turnOff_light",
            "description": "Turn off the light.",
            "parameters": {
                "type": "OBJECT",
                "properties": {},
                "required": [],
            },
        }
    }


def turnOff_light():
    """
    Turn off the light.
    """
    try:
        from plyer import light
        from kivy.clock import Clock
        light.disable()
        Clock.unschedule(get_illumination(ILLUMINATION, light))
    except Exception as e:
        raise Exception(f"Error in turning the light off: {e}")

    
    return {"response": f"Light's turned off successfully!"}

# ==================================================================================
# =======================================screenshot===========================================

take_screenshot_schema = {
    "function": {
        "name": "take_screenshot",
        "description": "To capture a digital image of what is currently visible on the monitor.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    }
}

def take_screenshot():
    """
    To capture a digital image of what is currently visible on the monitor.
    """
    try:
        from plyer import screenshot
        screenshot.capture()
    except Exception as e:
        raise Exception(f"Error in taking the screenshot: {e}")

    return {"response": f"taken a screenshot successfully!"}


# ==================================================================================
# =======================================battery===========================================
battery_status_schema = {
    "function": {
        "name": "battery_status",
        "description": "Provides information about the battery of your device.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    }
}

def battery_status():
    """
    Provides information about the battery of your device.
    """
    try:
        from plyer import battery

    except Exception as e:
        raise Exception(f"Error in finding the battery info: {e}")

    return {"response": f"Battery status in percentage: {battery.status['percentage']}. Whether the battery is charging: {battery.status['isCharging']}!"}

# ==================================================================================
# =======================================bluetooth===========================================
bluetooth_status_schema = {
    "function": {
        "name": "bluetooth_status",
        "description": "To get the bluetooth status info.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    }
}

def bluetooth_status():
    """
    To get the bluetooth status info. It is not yet extended to allow bluetooth connections.
    """
    try:
        from plyer import bluetooth
        return {"response": f"Bluetooth info: {bluetooth.info}."}
    except Exception as e:
        raise Exception(f"Error in finding the Bluetooth info: {e}")


# ==================================================================================
# =======================================Brightness===========================================
BRIGHTNESS = NumericProperty()

get_current_brightness_schema = {
    "function": {
        "name": "get_current_brightness",
        "description": "To get the current level of brightness.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    }
}

def get_current_brightness():
    """
        To get the current level of brightness.
    """
    try:
        from plyer import brightness
        BRIGHTNESS = brightness.current_level()
        return {"response": f"current level of brightness is: {BRIGHTNESS}."}
    except Exception as e:
        raise Exception(f"Error in finding the current level of brightness: {e}")


increase_brightness_schema = {
    "function": {
        "name": "increase_brightness",
        "description": "To level up the current brightness.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    }
}
def increase_brightness():
    """
        To level up the current brightness.
    """
    try:
        from plyer import brightness
        min_ = 0
        max_ = 100
        increase_jump = 10
        prev_level = brightness.current_level()
        level = prev_level + increase_jump
        BRIGHTNESS =  level if level <= max_ else max_
        brightness.set_level(BRIGHTNESS)

        return {"response": f"brightness has set to: {BRIGHTNESS} from the previous level of {prev_level}."}
    except Exception as e:
        raise Exception(f"Error in increasing the level of brightness: {e}")




decrease_brightness_schema = {
    "function": {
        "name": "decrease_brightness",
        "description": "To level down the current brightness.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    }
}
def decrease_brightness():
    """
        To level down the current brightness.
    """
    try:
        from plyer import brightness
        min_ = 0
        max_ = 100
        decrease_jump = 10
        prev_level = brightness.current_level()
        level = prev_level - decrease_jump
        BRIGHTNESS = level if level >= min_ else min_
        brightness.set_level(BRIGHTNESS)

        return {"response": f"brightness has set to: {BRIGHTNESS} from the previous level of {prev_level}."}
    except Exception as e:
        raise Exception(f"Error in decreasing the level of brightness: {e}")





set_brightness_schema = {
    "function": {
        "name": "set_brightness",
        "description": "To set a specific level to the current brightness.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "level": {"type": "STRING", "description": "The brightness level in the range of 0 to 100."},
            },
            "required": ["level"],
        },
    }
}
def set_brightness(level):
    """
        To set a specific level to the current brightness.
    """
    try:
        from plyer import brightness
        min_ = 0
        max_ = 100
        level = int(level)
        prev_level = brightness.current_level()

        level = level if level >= min_ else min_
        level = level if level <= max_ else max_

        BRIGHTNESS = level
        brightness.set_level(BRIGHTNESS)

        return {"response": f"brightness has set to: {BRIGHTNESS} from the previous level of {prev_level}."}
    except Exception as e:
        raise Exception(f"Error in setting the level of brightness: {e}")



# ==================================================================================
# =======================================Camera===========================================
from os import getcwd
from os.path import exists

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from plyer import camera

class MsgPopup(Popup):
    def __init__(self, msg):
        super().__init__()
        self.ids.message_label.text = msg


class CameraDemo(FloatLayout):
    def __init__(self):
        super().__init__()
        self.cwd = getcwd() + "/"
        self.ids.path_label.text = self.cwd

    def do_capture(self):
        self.filepath = self.cwd + self.ids.filename_text.text

        if exists(self.filepath):
            popup = MsgPopup("Picture with this name already exists!")
            popup.open()
            return False

        try:
            camera.take_picture(filename=self.filepath,
                                on_complete=self.camera_callback)
        except NotImplementedError:
            popup = MsgPopup(
                "This feature has not yet been implemented for this platform.")
            popup.open()

    def camera_callback(self, filepath):
        if exists(filepath):
            popup = MsgPopup("Picture saved!")
            popup.open()
        else:
            popup = MsgPopup("Could not save your picture!")
            popup.open()


take_picture_schema = {
    "function": {
        "name": "take_picture",
        "description": "To take a picture using camera.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    }
}

def take_picture():
    """
    To take a picture using camera.
    """
    cam = CameraDemo()
    try:
        cam.do_capture()
        return {"response": f"Picture took. You can find it in {cam.filepath}."}

    except Exception as e:
        raise Exception(f"Error in setting the level of brightness: {e}")

# ==================================================================================
# =======================================humidity===========================================
# 
# get_humidity_schema = {
#     "function": {
#         "name": "get_humidity",
#         "description": "To get the current humidity using the humidity sensor.",
#         "parameters": {
#             "type": "OBJECT",
#             "properties": {},
#             "required": [],
#         },
#     }
# }
# 
# def get_humidity():
#     """
#         To get the current humidity using the humidity sensor.
#     """
#     try:
#         from plyer import brightness
#         BRIGHTNESS = brightness.current_level()
#         return {"response": f"current level of brightness is: {BRIGHTNESS}."}
#     except Exception as e:
#         raise Exception(f"Error in finding the current level of brightness: {e}")

# ==================================================================================
# =======================================application===========================================
# Only works on Android
from jnius import autoclass, cast
from kivy.utils import platform

class access_applications:
    _instance = None

    def __init__(self):
        # Get Android context and package manager
        self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
        self.activity = self.PythonActivity.mActivity
        self.PackageManager = autoclass('android.content.pm.PackageManager')

    def __new__(cls, *args, **kwargs):
        if(cls._instance is None):
            cls._instance = super().__new__(cls)
        
        return cls._instance
            

            
    # def list(self):
    #
    #     pm = self.activity.getPackageManager()
    #
    #     # Get all installed apps
    #     installed_apps = pm.getInstalledApplications(self.PackageManager.GET_META_DATA)

    def get_android_apps(self):
        if platform != 'android': return []

        PackageManager = autoclass('android.content.pm.PackageManager')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')

        context = PythonActivity.mActivity.getApplicationContext()
        package_manager = context.getPackageManager()

        # Get all installed apps
        installed_apps = package_manager.getInstalledApplications(PackageManager.GET_META_DATA)

        app_list = []
        for app in installed_apps.toArray():
            app_name = app.loadLabel(package_manager).toString()
            package_name = app.packageName
            app_list.append((app_name, package_name))

        return app_list

    def open_app(self, package_name):
        if platform != 'android': return
        context = self.PythonActivity.mActivity.getApplicationContext()
        package_manager = context.getPackageManager()

        intent = package_manager.getLaunchIntentForPackage(package_name)
        if intent:
            context.startActivity(intent)




list_application_schema = {
    "function": {
        "name": "list_application",
        "description": "To list the applications installed on this android platform.",
        "parameters": {
            "type": "OBJECT",
            "properties": {},
            "required": [],
        },
    }
}

def list_application():
    """
    To list the applications installed on this android platform.
    """
    ap = access_applications()

    try:
        app_list = ap.get_android_apps()
        return {"response": f"All application list is: {app_list}."}

    except Exception as e:
        raise Exception(f"Error in listing the application: {e}")



open_application_schema = {
    "function": {
        "name": "open_application",
        "description": "To list the applications installed on this android platform.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "application_name": {"type": "STRING", "description": "Name of the application to be opened."}
            },
            "required": ["application_name"],
        },
    }
}

def open_application(application_name):
    """
    To list the applications installed on this android platform.
    """
    ap = access_applications()

    try:
        ap.open_app(application_name)
        return {"response": f"Application {application_name} opened."}

    except Exception as e:
        raise Exception(f"Error in opening the application {application_name}: {e}")




tools = [list_application_schema,
         open_application_schema,
         set_brightness_schema,
         decrease_brightness_schema,
         increase_brightness_schema,
         get_current_brightness_schema,
         send_email_schema,
         battery_status_schema,
         bluetooth_status_schema,
         phone_call_schema,
         phone_sms_schema,
         take_picture_schema,
         take_screenshot_schema,
         turnOff_light_schema,
         turnOn_light_schema,
         ]

print(tools)
# [{"role": "developer",
#   "content": "Current date and time given in YYYY-MM-DDTHH:MM:SS format: 2025-04-02T08:13:21\nDay of week is Wednesday\nYou are a model that can do function calling with the following functions\n"},
#  {"role": "user",
#   "content": "Please send an email to jessica.moraes@examplecorp.com with the subject \"Lunch tomorrow?\" and the message body \"Are you free to grab a bite at the new caf\u00e9 near the office around 1 PM?\"."},
#  {"role": "assistant", "tool_calls": [{"function": {"name": "send_email", "arguments": {
#      "body": "Are you free to grab a bite at the new caf\u00e9 near the office around 1 PM?",
#      "to": "jessica.moraes@examplecorp.com", "subject": "Lunch tomorrow?"}}}]}
#  ]




#
#