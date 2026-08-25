param(
    [Parameter(Mandatory=$true)]
    [string]$Path
)

if (-not (Test-Path -LiteralPath $Path)) {
    Write-Host "FAIL: File not found at $Path" -ForegroundColor Red
    exit 2
}

$content = Get-Content -LiteralPath $Path -Raw
$lines = $content -split "`n"
$issues = @()
$warnings = @()
$passed = @()

# Check 1: Identity at the top
if ($content -match "(?m)^## \d+\. Identity" -or $content -match "(?m)^## Identity") {
    $passed += "Identity section found"
} else {
    $issues += "Missing Identity section"
}

# Check 2: Security and Safety section
if ($content -match "## Security") {
    $passed += "Security section found"
    if ($content -match "IMPORTANT:") {
        $passed += "IMPORTANT markers found in security section"
    } else {
        $issues += "Security section missing IMPORTANT: markers"
    }
} else {
    $issues += "Missing Security and Safety section"
}

# Check 3: Tone and Style section
if ($content -match "## Tone" -or $content -match "## Style") {
    $passed += "Tone and Style section found"
} else {
    $issues += "Missing Tone and Style section"
}

# Check 4: Core Workflow section
if ($content -match "## Core Workflow") {
    $passed += "Core Workflow section found"
} elseif ($content -match "## Doing tasks" -or $content -match "## Workflow" -or $content -match "## Doing Tasks") {
    $passed += "Core Workflow section found"
} else {
    $issues += "Missing Core Workflow section"
}

# Check 5: Tool Usage section
if ($content -match "## Tool") {
    $passed += "Tool Usage section found"
} else {
    $warnings += "Missing Tool Usage Policy section (recommended)"
}

# Check 6: Domain Knowledge section
if ($content -match "## Domain") {
    $passed += "Domain Knowledge section found"
} else {
    $warnings += "Missing Domain Knowledge section (recommended)"
}

# Check 7: Environment Info section
if ($content -match "## Environment" -or $content -match '<env>') {
    $passed += "Environment Info section found"
} else {
    $warnings += "Missing Environment Info section (recommended)"
}

# Check 8: Reminders section
if ($content -match "## Reminders") {
    $passed += "Reminders section found"
} else {
    $warnings += "Missing Reminders section (recommended)"
}

# Check 9: Safety rules repeated at end
$lastSection = $lines[-10..-1] -join "`n"
if ($lastSection -match "IMPORTANT:") {
    $passed += "Safety rules repeated at end of prompt (recency reinforcement)"
} else {
    $warnings += "Safety rules not repeated at end - U-shaped attention recommends this"
}

# Check 10: example tags
if ($content -match '<example>') {
    $passed += "Examples wrapped in example tags"
} else {
    $warnings += "No example tags found - add at least one Input/Output example"
}

# Check 11: system-reminder pre-declaration
if ($content -match 'may include.*<system-reminder>' -or $content -match '<system-reminder>.*pre-declared') {
    $passed += "system-reminder tags pre-declared"
} elseif ($content -match 'system-reminder') {
    $warnings += "system-reminder mentioned but pre-declaration pattern not found"
} else {
    $warnings += "system-reminder tags not pre-declared - mid-conversation injection won't work as expected"
}

# Check 12: bidirectional constraints
if ($content -match "instead of") {
    $passed += "Bidirectional constraints found (prefer X instead of Y)"
} else {
    $warnings += "No bidirectional constraint pattern found"
}

# Check 13: Explain WHY pattern
# Uses "Reason:" prefix which is the convention from the template, not just bare "because"
if ($content -match "(?m)^Reason:" -or $content -match "(?i)Reason: " -or $content -match "\. Reason:") {
    $passed += "WHY explanations found (Reason: pattern)"
} elseif ($content -match "because" -or $content -match "since" -or $content -match "this is why") {
    $warnings += "WHY explanations found but not using the standard 'Reason:' prefix pattern"
} else {
    $warnings += "No WHY explanations found"
}

# Check 14: No flattery
$flattery = @("extremely talented", "incredibly experienced", "world-class", "brilliant", "unparalleled", "legendary", "guru")
$foundFlattery = $false
foreach ($term in $flattery) {
    if ($content -match [regex]::Escape($term)) {
        $foundFlattery = $true
        break
    }
}
if ($foundFlattery) {
    $issues += "Flattery detected - remove superlative adjectives"
} else {
    $passed += "No flattery detected"
}

# Check 15: Token estimate
$tokenEstimate = [int]($content.Length / 4)
if ($tokenEstimate -gt 6000) {
    $warnings += "Estimated tokens (~$tokenEstimate) exceed 6000 guideline"
} else {
    $passed += "Estimated tokens (~$tokenEstimate) within 6000 guideline"
}

# Output results
Write-Host "`n=== Validation Report for $Path ===" -ForegroundColor Cyan
Write-Host "`n--- Passed Checks ---" -ForegroundColor Green
foreach ($item in $passed) {
    Write-Host "  [PASS] $item" -ForegroundColor Green
}

if ($warnings.Count -gt 0) {
    Write-Host "`n--- Warnings ---" -ForegroundColor Yellow
    foreach ($item in $warnings) {
        Write-Host "  [WARN] $item" -ForegroundColor Yellow
    }
}

if ($issues.Count -gt 0) {
    Write-Host "`n--- Issues ---" -ForegroundColor Red
    foreach ($item in $issues) {
        Write-Host "  [FAIL] $item" -ForegroundColor Red
    }
}

Write-Host "`n--- Summary ---" -ForegroundColor Cyan
Write-Host "  Passed: $($passed.Count)"
Write-Host "  Warnings: $($warnings.Count)"
Write-Host "  Issues: $($issues.Count)"

if ($issues.Count -gt 0) {
    Write-Host "  Verdict: FAIL" -ForegroundColor Red
    exit 2
} elseif ($warnings.Count -gt 0) {
    Write-Host "  Verdict: PASS with warnings" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "  Verdict: PASS" -ForegroundColor Green
    exit 0
}
