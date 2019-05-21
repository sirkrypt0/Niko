import sys
import win32com.client 

shell = win32com.client.Dispatch("WScript.Shell")
shortcut = shell.CreateShortCut("c:\\test.lnk")
shortcut.Targetpath = "c:\\ftemp"
shortcut.save()
