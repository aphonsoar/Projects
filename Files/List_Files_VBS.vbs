Option Explicit
	CONST PASTA = "C:\Users\dir"
	Dim FSO
	Dim FIL
	Dim FOL
	Dim TXT
	Dim LOGF
	Dim CSV
	Dim XLSX
	
	
	TXT = replace(Wscript.ScriptFullName, ".vbs", ".txt")
	Set FSO = CreateObject("Scripting.FileSystemObject")
	Set	LOGF = FSO.OpenTextFile(txt, 2, true)
	
	if FSO.FolderExists(PASTA) = false then
		wscript.echo "Pasta " & pasta & " nao existe !"
		wscript.quit(0)
	end if
	
	call ListarPasta(PASTA)
	
	Sub ListarPasta(p)
		Dim SFOL
		Dim SFIL

		for each SFOL in FSO.GetFolder(p).SubFolders
			ListarPasta(SFOL.PATH)
		next
		
		for each SFIL in FSO.GetFolder(p).Files
			LOGF.WriteLine sFIL.Path	
		next 
		
	End Sub