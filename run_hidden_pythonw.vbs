Set WshShell = CreateObject("WScript.Shell")

' Get the directory where this VBS file is located
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Path to your Python script
pythonScript = scriptDir & "\rpc.py"

' Run with pythonw.exe (Windows Python without console)
' 0 = hidden window, False = don't wait for completion
WshShell.Run "pythonw """ & pythonScript & """", 0, False
