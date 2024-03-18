#Script til opsætning af en flask website på Azure med brug af Powershell 7 og Az-module
#Lavet af Mikkel Due-Pedersen d.14/03-2024

#Login på din Azure konto
Connect-AzAccount
#####################################
#Variabler
$resourcegroup = 'indeklima-rg'
$location = 'ukwest'
$Subnet1 = New-AzVirtualNetworkSubnetConfig -Name Subnet1 -AddressPrefix "10.0.0.0/24"
$Subnet2  = New-AzVirtualNetworkSubnetConfig -Name Subnet2  -AddressPrefix "10.0.1.0/24"
$cred = Get-Credential #Username: Hold2a Password: Kea2024hold2a
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
#########################
#Lav en Resourcegroup
New-AzResourceGroup -Name 'indeklima-rg' -Location 'ukwest'
############################################################
#vnet og subnet

New-AzVirtualNetwork -Name Vnet1 -ResourceGroupName $resourcegroup -Location $location -AddressPrefix "10.0.0.0/16" -Subnet $Subnet1,$Subnet2
###########################################################
#Lav VM
New-AzVm @vmParams

############################################################
#Storage & Blob
New-AzStorageAccount -ResourceGroupName $resourcegroup `
  -Name $accountname `
  -Location $location `
  -SkuName Standard_RAGRS `
  -Kind StorageV2 `
  -AllowBlobPublicAccess $true

$ctx = New-AzStorageContext -StorageAccountName blobwebsite -UseConnectedAccount
New-AzStorageContainer -Name "websitecontainerhold2a" -Context $ctx
# Når det er lavet, upload github filerne ind i container

#############################################################################################
#Tjek PublicIP og forbind til VM
$publicIp = Get-AzPublicIpAddress -Name 'publicip' -ResourceGroupName $resourcegroup

$publicIp |
  Select-Object -Property Name, IpAddress, @{label='FQDN';expression={$_.DnsSettings.Fqdn}}
#############################################################################################
#ssh ind i den
ssh Hold2a@20.162.122.217 #ændre det sidste alt efter hvad for en publicip man får

#############################################################################################
#bash til setup af hjemmeside
git clone https://github.com/MDueP/IoT2.git
sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt install python3-flask
sudo apt-get install -y mosquitto mosquitto-clients
########################################################
#Få mosquitto op at køre:
sudo nano /etc/mosquitto/mosquitto.conf
indsæt: listener 1883
        allow_anonymous true
        #I bunden af filen
sudo reboot
#Når vm er genstartet tjek med:
sudo systemctl status mosquitto.service #om programmet kører
sudo lsof -i -P -n | grep LISTEN #om porten er åben
#########################################################
#Installer modulerne med de her cmd:
#pip install -r requirements.txt
#cd ind i mappen med filerne og kør flask run:
nohup flask run --host=0.0.0.0 --debug & #--host 0.0.0.0, gør at den kører på alle åbne IP-Adresser
#nohup gør at den kører efter man lukker for SSH forbindelsen
#########################
#fjern det hele igen
$job = Remove-AzResourceGroup -Name $resourcegroup -Force -AsJob
$job
