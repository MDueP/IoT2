Connect-AzAccount

$resourcegroup = 'indeklima-rg'
$location = 'ukwest'
$Subnet1 = New-AzVirtualNetworkSubnetConfig -Name Subnet1 -AddressPrefix "10.0.0.0/24"
$Subnet2  = New-AzVirtualNetworkSubnetConfig -Name Subnet2  -AddressPrefix "10.0.1.0/24"
$cred = Get-Credential
$vmParams = @{
    ResourceGroupName = $resourcegroup
    Name = 'IndeklimaVM'
    Location = $location
    ImageName = 'Ubuntu2204'
    VirtualNetworkName = 'Vnet1'
    SubnetName = 'Subnet1'
    PublicIpAddressName = 'publicip'
    Credential = $cred
    OpenPorts = 3389, 80, 22, 1883, 5000
    Size = 'Standard_D2s_v3'
  }
  $accountname = 'blobaccountkeahold2a'

New-AzResourceGroup -Name 'indeklima-rg' -Location 'ukwest'

New-AzVirtualNetwork -Name Vnet1 -ResourceGroupName $resourcegroup -Location $location -AddressPrefix "10.0.0.0/16" -Subnet $Subnet1,$Subnet2

New-AzVm @vmParams

New-AzStorageAccount -ResourceGroupName $resourcegroup `
  -Name $accountname `
  -Location $location `
  -SkuName Standard_RAGRS `
  -Kind StorageV2 `
  -AllowBlobPublicAccess $true

$ctx = New-AzStorageContext -StorageAccountName blobwebsite -UseConnectedAccount
New-AzStorageContainer -Name "websitecontainerhold2a" -Context $ctx

$publicIp = Get-AzPublicIpAddress -Name 'publicip' -ResourceGroupName $resourcegroup

$publicIp |
  Select-Object -Property Name, IpAddress, @{label='FQDN';expression={$_.DnsSettings.Fqdn}}

$job = Remove-AzResourceGroup -Name $resourcegroup -Force -AsJob
$job
