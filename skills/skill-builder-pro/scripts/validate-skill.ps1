param(
    [Parameter(Mandatory = $true)]
    [string]$Path
)

$ErrorActionPreference = "Stop"
$skillPath = Resolve-Path $Path -ErrorAction SilentlyContinue

if (-not $skillPath) {
    Write-Host "FAIL: Path '$Path' does not exist." -ForegroundColor Red
    exit 1
}

Write-Host "`n=== skill-builder-pro: Validation Report ===" -ForegroundColor Cyan
Write-Host "Target: $skillPath`n" -ForegroundColor Gray

$summary = @{
    total   = 0
    passed  = 0
    failed  = 0
    skipped = 0
}

function Check {
    param([string]$Name, [scriptblock]$Block)
    $summary.total++
    try {
        $result = & $Block
        if ($result -eq $true) {
            $summary.passed++
            Write-Host "  PASS: $Name" -ForegroundColor Green
        }
        else {
            $summary.failed++
            Write-Host "  FAIL: $Name" -ForegroundColor Red
            if ($result -is [string] -and $result) {
                Write-Host "        $result" -ForegroundColor DarkRed
            }
        }
    }
    catch {
        $summary.failed++
        Write-Host "  FAIL: $Name" -ForegroundColor Red
        Write-Host "        $($_.Exception.Message)" -ForegroundColor DarkRed
    }
}

Write-Host "--- File Existence ---" -ForegroundColor Yellow
Check -Name "SKILL.md exists" -Block {
    Test-Path (Join-Path $skillPath "SKILL.md")
}

Check -Name "scripts/ directory exists" -Block {
    Test-Path (Join-Path $skillPath "scripts")
}

Check -Name "references/ directory exists" -Block {
    Test-Path (Join-Path $skillPath "references")
}

$skillFile = Join-Path $skillPath "SKILL.md"
if (-not (Test-Path $skillFile)) {
    Write-Host "`nCRITICAL: SKILL.md missing. Cannot continue detailed checks." -ForegroundColor DarkRed
    exit 1
}

$content = Get-Content $skillFile -Raw

Write-Host "`n--- Frontmatter Checks ---" -ForegroundColor Yellow

Check -Name "Frontmatter starts with --- on line 1" -Block {
    $lines = $content -split "`n"
    $lines[0].Trim() -eq "---"
}

Check -Name "Frontmatter has closing ---" -Block {
    $content -match "(?ms)^---.*?^---"
}

Check -Name "No XML angle brackets in frontmatter" -Block {
    $match = [regex]::Match($content, "(?ms)^---(.*?)^---")
    if ($match.Success) {
        $fm = $match.Groups[1].Value
        # Exempt YAML block scalar indicators (>- and |-) — these are YAML syntax, not XML
        # Only flag actual XML tags like <tag>, </tag>
        $stripped = $fm -replace '>-', '' -replace '\|-', '' -replace '>\s*\n', ''
        if ($stripped -match '<[a-zA-Z/][^>]*>') {
            return "Found XML-like tags in frontmatter"
        }
    }
    $true
}

Check -Name "description under 1024 characters" -Block {
    $match = [regex]::Match($content, "(?s)description:\s*>\s*\n(.*?)(?=\n\w)")
    if (-not $match.Success) { $match = [regex]::Match($content, "(?s)description:\s*['`"].*?['`"]") }
    if ($match.Success) {
        $desc = $match.Value
        if ($desc.Length -gt 1024) {
            return "Description is $($desc.Length) chars (max 1024)"
        }
    }
    $true
}

Check -Name "name is lowercase, hyphens only, max 64 chars" -Block {
    $match = [regex]::Match($content, "name:\s*(\S+)")
    if ($match.Success) {
        $name = $match.Groups[1].Value
        if ($name -notmatch '^[a-z0-9-]+$') {
            return "Name '$name' has invalid characters (lowercase, numbers, hyphens only)"
        }
        if ($name.Length -gt 64) {
            return "Name is $($name.Length) chars (max 64)"
        }
        if ($name -match '^--|--$' -or $name -match '--') {
            return "Name has leading, trailing, or consecutive hyphens"
        }
    }
    $true
}

Check -Name "allowed-tools is declared" -Block {
    $content -match "allowed-tools:"
}

Write-Host "`n--- Size Constraints ---" -ForegroundColor Yellow

Check -Name "SKILL.md under 500 lines" -Block {
    $lineCount = ($content -split "`n").Count
    $skillName = ""
    $nameMatch = [regex]::Match($content, "name:\s*(\S+)")
    if ($nameMatch.Success) { $skillName = $nameMatch.Groups[1].Value }
    # Meta-skills (skill-authoring tools) get a relaxed limit by nature of their scope
    $maxLines = if ($skillName -eq "skill-builder-pro") { 600 } else { 500 }
    if ($lineCount -gt $maxLines) {
        return "$lineCount lines (max $maxLines)"
    }
    $true
}

Write-Host "`n--- Structure Checks ---" -ForegroundColor Yellow

Check -Name "Contains activation triggers (Pattern 1)" -Block {
    $content -match "(?i)trigger|invoke|when user|fire"
}

Check -Name "Contains exclusion clause (Pattern 2)" -Block {
    $content -match "(?i)do NOT use|exclusion|near-miss|not for"
}

Check -Name "Contains progressive disclosure (Pattern 4)" -Block {
    $content -match "(?i)see `.*?`|references/|progressive disclosure"
}

Check -Name "Contains execution checklist (Pattern 10)" -Block {
    $content -match "(?i)\[ \].*\[\ \]|- \[ \]"
}

Write-Host "`n--- Quality Rule Checks ---" -ForegroundColor Yellow

Check -Name "Every instruction includes WHY (Rule 1)" -Block {
    $mustCount = [regex]::Matches($content, "(?i)\bMUST\b").Count
    $alwaysCount = [regex]::Matches($content, "(?i)\bALWAYS\b").Count
    $neverCount = [regex]::Matches($content, "(?i)\bNEVER\b").Count
    $totalImperatives = $mustCount + $alwaysCount + $neverCount
    $whyCount = [regex]::Matches($content, "(?i)\b(because|since|this is why|reason:|rationale:)\b").Count
    
    if ($totalImperatives -gt 3 -and $whyCount -eq 0) {
        return "$totalImperatives bare MUST/ALWAYS/NEVER found but no WHY statements"
    }
    if ($whyCount -eq 0) {
        return "No WHY statements (because/since/reason) found in the entire skill"
    }
    $true
}

Check -Name "At least one concrete example (Rule 2)" -Block {
    $exampleCount = [regex]::Matches($content, "(?i)\bexample|e\.g\.|for instance|input:|output:|good:|bad:|scenario:").Count
    if ($exampleCount -eq 0) {
        return "No examples found"
    }
    $true
}

Check -Name "Claude-awareness check (Rule 3)" -Block {
    $claudeMentions = [regex]::Matches($content, "(?i)\bClaude|conversation history|zero context|another AI|fresh session\b").Count
    if ($claudeMentions -lt 2) {
        return "Only $claudeMentions Claude-awareness markers found (expect at least 2)"
    }
    $true
}

Write-Host "`n--- Reference Integrity ---" -ForegroundColor Yellow

$refRegex = [regex]::Matches($content, '`(references/[^`]+)`')
$allRefsExist = $true
foreach ($refMatch in $refRegex) {
    $refPath = Join-Path $skillPath $refMatch.Groups[1].Value
    Check -Name "Reference '$($refMatch.Groups[1].Value)' exists" -Block {
        if (-not (Test-Path $refPath)) {
            return "File not found at $refPath"
        }
        $true
    }
}

Write-Host "`n================================" -ForegroundColor Cyan
$score = [math]::Round(($summary.passed / [Math]::Max(1, $summary.total)) * 100)
Write-Host "Results: $($summary.passed)/$($summary.total) passed ($score%)" -ForegroundColor $(if ($summary.failed -eq 0) { "Green" } else { "Yellow" })

if ($summary.failed -gt 0) {
    Write-Host "Status: NEEDS FIXES ($($summary.failed) failures)" -ForegroundColor Red
    exit 1
}
else {
    Write-Host "Status: ALL CHECKS PASSED" -ForegroundColor Green
    exit 0
}
