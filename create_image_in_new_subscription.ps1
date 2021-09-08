###Create an image in the target subscription
## -- In the second subscription, create a new Image from the copied snapshot --#

$targetSubscriptionId = '5aa49bea-93fb-4d1c-ab7e-e4549cb2b935'
$imageContainerName = 'migration'
$imageBlobName = 'AnnotationImageBlob'
$targetResourceGroupName = '3DWeeds-migrate'
$targetStorageAccountName = 'weedsmedia2'
$targetRegionName = 'eastus'
$resourceGroupName = '3DWeeds-migrate'
$imageName = 'AnnotationImage'

$snapshotName = $imageName + "-" + $targetRegionName + "-snap"
$snap = Get-AzureRmSnapshot -ResourceGroupName $resourceGroupName -SnapshotName $snapshotName 
$imageConfig = New-AzureRmImageConfig -Location $targetRegionName
 
Set-AzureRmImageOsDisk -Image $imageConfig `
                        -OsType Linux `
                        -OsState Generalized `
                        -SnapshotId $snap.Id
 
New-AzureRmImage -ResourceGroupName $resourceGroupName `
                 -ImageName $imageName `
                 -Image $imageConfig