# フォルダのパスを指定
$targetFolder = Read-Host -Prompt "Enter the path to the folder"

# 指定したフォルダ内の全ての .bat ファイルを取得し、処理
Get-ChildItem -Path $targetFolder -Filter *.bat -Recurse | ForEach-Object {
    $content = Get-Content -Path $_.FullName -Raw
    $content = $content -replace "`r?`n", "`r`n"
    [System.IO.File]::WriteAllLines($_.FullName, $content -split "`r`n", [System.Text.Encoding]::GetEncoding("shift_jis"))
}

Write-Host "Conversion complete."
