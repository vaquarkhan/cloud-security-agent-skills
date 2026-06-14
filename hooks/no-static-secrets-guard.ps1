$patterns = 'AKIA[0-9A-Z]{16}|aws_secret_access_key|client_secret=|AccessKeySecret'
$diff = git diff --cached 2>$null
if ($diff -match $patterns) {
  Write-Error "Possible static secret in staged diff. Use IdentityManager / vault."
  exit 1
}
Write-Host "OK: no obvious static secret patterns in staged diff"
