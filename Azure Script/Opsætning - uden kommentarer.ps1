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

ssh Hold2a@20.254.232.236

git clone https://github.com/MDueP/IoT2.git

sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt install python3-flask
sudo apt-get install -y mosquitto mosquitto-clients

sudo nano /etc/mosquitto/mosquitto.conf
indsæt:

pid_file /run/mosquitto/mosquitto.pid

user mosquitto
max_queued_messages 200
message_size_limit 0
allow_zero_length_clientid true
allow_duplicate_messages false

listener 1883
autosave_interval 900
autosave_on_changes false
persistence true
persistence_file mosquitto.db
allow_anonymous true
log_dest file /var/log/mosquitto/mosquitto.log
        
sudo systemctl restart mosquitto
sudo systemctl status mosquitto.service 
sudo pip install -r requirements.txt
nohup flask run --host=0.0.0.0 --debug & 

$job = Remove-AzResourceGroup -Name $resourcegroup -Force -AsJob
$job
