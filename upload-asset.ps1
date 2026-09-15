param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath,

    [Parameter(Mandatory=$true)]
    [string]$RemoteName
)

$Repo = "Allebox/bavaria-video-assets"
$RemotePath = "generated/$RemoteName"

if (!(Test-Path $FilePath)) {
    Write-Host "ERROR: File not found: $FilePath"
    exit 1
}

$bytes = [System.IO.File]::ReadAllBytes($FilePath)
$base64 = [Convert]::ToBase64String($bytes)

$payloadObject = @{
    message = "Add Bavaria generated asset: $RemoteName"
    content = $base64
}

$payload = $payloadObject | ConvertTo-Json -Compress

$tempJson = Join-Path $env:TEMP "bavaria-gh-upload.json"

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

[System.IO.File]::WriteAllText(
    $tempJson,
    $payload,
    $utf8NoBom
)

Write-Host "Uploading $RemoteName..."

gh api `
  --method PUT `
  -H "Accept: application/vnd.github+json" `
  -H "X-GitHub-Api-Version: 2022-11-28" `
  "/repos/$Repo/contents/$RemotePath" `
  --input $tempJson

$exitCode = $LASTEXITCODE

Remove-Item $tempJson -Force -ErrorAction SilentlyContinue

if ($exitCode -ne 0) {
    Write-Host ""
    Write-Host "UPLOAD FAILED - local file preserved."
    exit 1
}

Remove-Item $FilePath -Force

Write-Host ""
Write-Host "UPLOAD OK"
Write-Host "Local temporary file deleted."
Write-Host ""
Write-Host "RAW URL:"
Write-Host "https://raw.githubusercontent.com/$Repo/main/$RemotePath"