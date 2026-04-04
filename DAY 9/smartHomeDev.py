#12. Smart Home Devices (Multiple Inheritance)
#A smart home device may have both WiFi connectivity and Voice control features.
#Create classes WiFiDevice and VoiceAssistant, and a class SmartSpeaker that
#inherits from both using multiple inheritance.
class WifiDevices():
    def connectivity(self):
        print("Device is Connected to wifi")
class VoiceAssistance():
    def voice_control(self):
        print("Now,You can access any device through voice control")
class Smart_speaker(WifiDevices,VoiceAssistance):
    def feature(self):
        print("Cool !!\n Features Working")    


s=Smart_speaker()
s.connectivity()
s.voice_control()
s.feature()