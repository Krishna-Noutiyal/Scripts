$certname = "Cert Name"
$org = "Organisation name"
$country = "IN"
$yearsValid = 5

New-SelfSignedCertificate -Type Custom `
  -Subject "CN=$certname, O=$org, C=$country" `
  -KeyUsage DigitalSignature `
  -CertStoreLocation "Cert:\CurrentUser\My" `
  -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3") `
  -KeyAlgorithm RSA `
  -KeyLength 2048 `
  -FriendlyName "Self Signing Certificate" `
  -NotAfter (Get-Date).AddYears($yearsValid)


