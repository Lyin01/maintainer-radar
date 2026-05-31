param(
    [string]$Repo = "maintainer-radar",

    [string]$Org = "",

    [string]$Description = "Local-first triage, PR risk, and release-readiness CLI for open-source maintainers."
)

$ErrorActionPreference = "Stop"

if (-not $env:GITHUB_TOKEN) {
    throw "Set GITHUB_TOKEN to a token with permission to create repositories."
}

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

$body = @{
    name = $Repo
    description = $Description
    private = $false
    has_issues = $true
    has_projects = $true
    has_wiki = $false
} | ConvertTo-Json

$headers = @{
    Authorization = "Bearer $env:GITHUB_TOKEN"
    Accept = "application/vnd.github+json"
    "X-GitHub-Api-Version" = "2022-11-28"
}

$createUrl = "https://api.github.com/user/repos"
if ($Org) {
    $createUrl = "https://api.github.com/orgs/$Org/repos"
}

$repoInfo = Invoke-RestMethod -Method Post -Uri $createUrl -Headers $headers -Body $body -ContentType "application/json"

if (-not (Test-Path ".git")) {
    git init -b main
}

git remote remove origin 2>$null
git remote add origin $repoInfo.clone_url
git push -u origin main

Write-Host "Published $($repoInfo.html_url)"
