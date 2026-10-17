$ErrorActionPreference = 'Stop'
$workspaceRoot = [IO.Path]::GetFullPath((Split-Path $PSScriptRoot -Parent))
$reportDir = Join-Path $workspaceRoot 'reports\reorganization_20261013'
New-Item -ItemType Directory -Path $reportDir -Force | Out-Null
if (Test-Path -LiteralPath (Join-Path $reportDir 'moves.json')) { throw 'Migration already started; inspect the move log before continuing.' }
function SafePath([string]$relative) {
    $resolved = [IO.Path]::GetFullPath((Join-Path $workspaceRoot $relative))
    if (-not $resolved.StartsWith($workspaceRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw "Path escapes workspace: $resolved" }
    return $resolved
}
$mapping = @(
    @('video_work\models','shared\models'),
    @('couple_samples','shared\characters'),
    @('facebook_brand','shared\branding'),
    @('reference_samples','shared\kinetic_reference\samples'),
    @('text_kinetic_motion.mp4','shared\kinetic_reference\text_kinetic_motion.mp4'),
    @('video_work\reference_frames','shared\kinetic_reference\reference_frames'),
    @('video_work\reference_sheets','shared\kinetic_reference\reference_sheets'),
    @('video_work\reference_frames.json','shared\kinetic_reference\reference_frames.json'),
    @('video_work\reference_analysis.md','shared\kinetic_reference\reference_analysis.md'),
    @('video_work\inspect_reference.py','tools\inspect_reference.py'),
    @('video_work\download_whisper.py','tools\download_whisper.py'),
    @('package_reusable.py','tools\package_reusable.py'),
    @('Hansi_Ki_Dhun_Reusable_Song_Kit.zip','archives\Hansi_Ki_Dhun_Reusable_Song_Kit_pre_20261013.zip'),
    @('breakup_roast','songs\breakup_roast'),
    @('mann_mera_reels','songs\mann_mera_reels'),
    @('meetha_bhi_khana_hai','songs\meetha_bhi_khana_hai'),
    @('nahana_chahiye','songs\nahana_chahiye'),
    @('neend_ka_jadoo','songs\neend_ka_jadoo'),
    @('palang_ke_andar_yoddha','songs\palang_ke_andar_yoddha'),
    @('final_video','songs\hoodie_breakup\final_video'),
    @('portrait_images','songs\hoodie_breakup\portrait_images'),
    @('portrait_images_32.zip','songs\hoodie_breakup\portrait_images_32.zip'),
    @('lyrics.txt','songs\hoodie_breakup\lyrics.txt'),
    @('scene_prompts.json','songs\hoodie_breakup\scene_prompts.json'),
    @('song.mp3','songs\hoodie_breakup\song.mp3'),
    @('video_work','songs\hoodie_breakup\video_work')
)
# Validate every recursive move's fully resolved source and destination first.
foreach ($pair in $mapping) {
    $src=SafePath $pair[0]; $dst=SafePath $pair[1]
    if (-not (Test-Path -LiteralPath $src)) { throw "Missing source $src" }
    if (Test-Path -LiteralPath $dst) { throw "Destination already exists $dst" }
}
Write-Output 'Recording original file sizes and SHA-256 checksums...'
$inventory = @(Get-ChildItem -LiteralPath $workspaceRoot -File -Recurse | Where-Object { -not $_.FullName.StartsWith($reportDir + '\') } | ForEach-Object {
    [PSCustomObject]@{path=$_.FullName.Substring($workspaceRoot.Length+1).Replace('\','/');bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()}
})
$inventory | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $reportDir 'before.json') -Encoding utf8
$records = @()
foreach ($pair in $mapping) {
    $src=SafePath $pair[0]; $dst=SafePath $pair[1]
    New-Item -ItemType Directory -Path (Split-Path $dst -Parent) -Force | Out-Null
    Move-Item -LiteralPath $src -Destination $dst
    $records += [PSCustomObject]@{from=$pair[0].Replace('\','/');to=$pair[1].Replace('\','/')}
    $records | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $reportDir 'moves.json') -Encoding utf8
}
# Download fragments are disposable only when their concatenation exactly equals model.bin.
$partsDir=SafePath 'shared\models\whisper-small\parts'
$modelPath=SafePath 'shared\models\whisper-small\model.bin'
$parts=@(Get-ChildItem -LiteralPath $partsDir -File | Sort-Object Name)
$hasher=[Security.Cryptography.IncrementalHash]::CreateHash([Security.Cryptography.HashAlgorithmName]::SHA256)
$totalBytes=0L
for($i=0;$i -lt $parts.Count;$i++) {
    if($parts[$i].Name -ne ('{0:D4}.part' -f $i)){throw 'Non-contiguous download fragments; no cleanup performed.'}
    $chunk=[IO.File]::ReadAllBytes($parts[$i].FullName)
    $hasher.AppendData($chunk); $totalBytes += $chunk.Length
}
$partsHash=[Convert]::ToHexString($hasher.GetHashAndReset()).ToLowerInvariant();$hasher.Dispose()
$modelHash=(Get-FileHash -LiteralPath $modelPath -Algorithm SHA256).Hash.ToLowerInvariant()
if($partsHash -ne $modelHash -or $totalBytes -ne (Get-Item -LiteralPath $modelPath).Length){throw 'Fragments do not match model; preserved for inspection.'}
$cleanup=@()
foreach($part in $parts){
    $checked=SafePath $part.FullName.Substring($workspaceRoot.Length+1)
    $cleanup += [PSCustomObject]@{path=$checked.Substring($workspaceRoot.Length+1).Replace('\','/');bytes=$part.Length;reason='Verified byte-identical download fragment of retained model.bin'}
    Remove-Item -LiteralPath $checked
}
Remove-Item -LiteralPath $partsDir
@{model_sha256=$modelHash;fragment_sha256=$partsHash;removed_bytes=$totalBytes;files=$cleanup} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $reportDir 'cleanup.json') -Encoding utf8
Write-Output "Moved $($records.Count) items. Removed only verified duplicate fragments: $totalBytes bytes."
