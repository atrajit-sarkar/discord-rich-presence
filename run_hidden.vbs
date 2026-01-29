Set WshShell = CreateObject("WScript.Shell")

' Get the directory where this VBS file is located
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Path to your Python script
pythonScript = scriptDir & "\rpc.py"

' Run Python script hidden (0 = hidden window, False = don't wait for completion)
' This will use the default Python installation
WshShell.Run "python """ & pythonScript & """", 0, False

' Alternative: If you want to use pythonw.exe (no console version), uncomment below:
' WshShell.Run "pythonw """ & pythonScript & """", 0, False
