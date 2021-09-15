$targetSubscriptionId = '5aa49bea-93fb-4d1c-ab7e-e4549cb2b935'
$imageContainerName = 'migration'
$imageBlobName = 'AnnotationImageBlob'
$targetResourceGroupName = '3DWeeds-migrate'
$targetStorageAccountName = 'weedsmedia2'
$targetRegionName = 'eastus'

$imageName = 'AnnotationImage'

# Get the full URI to the blob
$osDiskVhdUri = 'https://weedsmedia2.blob.core.windows.net/migration/abcd'
 
# Build up the snapshot configuration, using the target storage account's resource ID
$snapshotConfig = New-AzureRmSnapshotConfig -AccountType StandardLRS `
                                            -OsType Linux `
                                            -Location $targetRegionName `
                                            -CreateOption Import `
                                            -SourceUri $osDiskVhdUri `
                                            -StorageAccountId "/subscriptions/${targetSubscriptionId}/resourceGroups/${targetResourceGroupName}/providers/Microsoft.Storage/storageAccounts/${targetStorageAccountName}"
 
# Create the new snapshot in the target region
$snapshotName = $imageName + "-" + $targetRegionName + "-snap"
$snap2 = New-AzureRmSnapshot -ResourceGroupName $resourceGroupName -SnapshotName $snapshotName -Snapshot $snapshotConfig