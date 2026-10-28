#Requires -Version 5.1
<#
.SYNOPSIS
    Render all PlantUML diagrams to SVG and PNG.

.DESCRIPTION
    Downloads plantuml.jar into %TEMP%\opencode if it is missing and renders
    every .puml file from diagrams/ into diagrams/rendered/.

.EXAMPLE
    .\scripts\build-diagrams.ps1
#>

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$diagrams = Join-Path $root "diagrams"
$rendered = Join-Path $diagrams "rendered"
$jar = Join-Path $env:TEMP "opencode\plantuml.jar"
$jarUrl = "https://repo1.maven.org/maven2/net/sourceforge/plantuml/plantuml/1.2024.7/plantuml-1.2024.7.jar"

Write-Host "Project: $root"

if (-not (Get-Command java -ErrorAction SilentlyContinue)) {
    throw "Java not found. Install Java 11+ and try again."
}

if (-not (Test-Path $jar)) {
    Write-Host "Downloading PlantUML..."
    $dir = Split-Path -Parent $jar
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
    Invoke-WebRequest -Uri $jarUrl -OutFile $jar -UseBasicParsing
}

New-Item -ItemType Directory -Force -Path $rendered | Out-Null

$files = Get-ChildItem -Path $diagrams -Filter "*.puml" -File
if ($files.Count -eq 0) {
    throw "No .puml files found in $diagrams"
}

Write-Host "Rendering $($files.Count) diagram(s)..."

& java -jar $jar -charset UTF-8 -tsvg -o $rendered $files.FullName
if ($LASTEXITCODE -ne 0) { throw "SVG rendering failed with exit code $LASTEXITCODE" }

& java -jar $jar -charset UTF-8 -tpng -Sdpi=200 -o $rendered $files.FullName
if ($LASTEXITCODE -ne 0) { throw "PNG rendering failed with exit code $LASTEXITCODE" }

$out = Get-ChildItem -Path $rendered -File
Write-Host "Done. Generated $($out.Count) file(s) in $rendered"
$out | Select-Object Name, Length | Format-Table -AutoSize
