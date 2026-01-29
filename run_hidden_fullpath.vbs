Set WshShell = CreateObject("WScript.Shell")

' ⚠️ EDIT THIS PATH to match your actual rpc.py location
pythonScript = "e:\CodingWorld\Pyhton Projects\PlayGround\DiscordBotdevelopment\rich-ptesence\rpc.py"

' Run Python script hidden (0 = hidden window, False = don't wait for completion)
WshShell.Run "python """ & pythonScript & """", 0, False

' Alternative: Use pythonw.exe for even quieter operation (uncomment below)
' WshShell.Run "pythonw """ & pythonScript & """", 0, False
