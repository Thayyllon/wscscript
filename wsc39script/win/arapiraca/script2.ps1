$password = ConvertTo-SecureString "Skill39" -AsPlainText -Force
$credentials = New-Object System.Management.Automation.PSCredential("Administrator@wsc2023.al.gov",$password)
(Invoke-WebRequest -UseBasicParsing -Uri http://localhost:8080 -Credential $credentials).StatusCode