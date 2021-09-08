$resourceGroupName = '3DWeeds' 
$region = 'usgovvirginia' 
$vmName = 'AnnotationSystem'
$snapshotName = 'AnnotationSnapshot'
$imageName = 'AnnotationImage'
$targetSubscriptionId = 5aa49bea-93fb-4d1c-ab7e-e4549cb2b935
$imageContainerName = 'migration'
$imageBlobName = 'AnnotationImageBlob'
$targetResourceGroupName = '3DWeeds-migrate'
$targetStorageAccountName = 'weedsmedia2'
$targetRegionName = 'eastus'

# Create the name of the snapshot, using the current region in the name.
$snapshotName = $imageName + "-" + $region + "-snap"
 
# Get the source snapshot
$snap = Get-AzureRmSnapshot -ResourceGroupName $resourceGroupName -SnapshotName $snapshotName
 
# Create a Shared Access Signature (SAS) for the source snapshot
$snapSasUrl = Grant-AzureRmSnapshotAccess -ResourceGroupName $resourceGroupName -SnapshotName $snapshotName -DurationInSecond 3600 -Access Read
 
# Set up the target storage account in the other region and subscription
Select-AzureRmSubscription -SubscriptionId $targetSubscriptionId
 
$targetStorageContext = (Get-AzureRmStorageAccount -ResourceGroupName $targetResourceGroupName -Name $targetStorageAccountName).Context
New-AzureStorageContainer -Name $imageContainerName -Context $targetStorageContext -Permission Container
 
# Use the SAS URL to copy the blob to the target storage account (and thus region)
Start-AzureStorageBlobCopy -AbsoluteUri $snapSasUrl.AccessSAS -DestContainer $imageContainerName -DestContext $targetStorageContext -DestBlob $imageBlobName
Get-AzureStorageBlobCopyState -Container $imageContainerName -Blob $imageBlobName -Context $targetStorageContext -WaitForComplete
 
# Get the full URI to the blob
$osDiskVhdUri = ($targetStorageContext.BlobEndPoint + $imageContainerName + "/" + $imageBlobName)
 
# Build up the snapshot configuration, using the target storage account's resource ID
$snapshotConfig = New-AzureRmSnapshotConfig -AccountType StandardLRS `
                                            -OsType Windows `
                                            -Location $targetRegionName `
                                            -CreateOption Import `
                                            -SourceUri $osDiskVhdUri `
                                            -StorageAccountId "/subscriptions/${targetSubscriptionId}/resourceGroups/${targetResourceGroupName}/providers/Microsoft.Storage/storageAccounts/${targetStorageAccountName}"
 
# Create the new snapshot in the target region
$snapshotName = $imageName + "-" + $targetRegionName + "-snap"
$snap2 = New-AzureRmSnapshot -ResourceGroupName $resourceGroupName -SnapshotName $snapshotName -Snapshot $snapshotConfig