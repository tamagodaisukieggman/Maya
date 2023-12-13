''''''''''''''''''''''''''''''''''''''
' Excel ファイルのマクロを実行
''''''''''''''''''''''''''''''''''''''

' Excel
Dim excelApp : Set excelApp = CreateObject("Excel.Application")

' Excel を非表示
excelApp.Visible = False

' Excel を起動したままにするか（1つ目のコマンドライン引数）
Dim launchExcel : launchExcel = WScript.Arguments(0)

' Excel ファイル（2つ目のコマンドライン引数）
Dim targetFile : targetFile = WScript.Arguments(1)

' マクロ（3つ目のコマンドライン引数）
Dim targetMacro : targetMacro = WScript.Arguments(2)

' Excel ファイルを開く
excelApp.Workbooks.Open targetFile

' マクロの実行
excelApp.Run targetMacro

If launchExcel = 0 Then
    ' Excelの終了
    excelApp.Quit
Else
    ' Excel を表示
    excelApp.Visible = True
End If
