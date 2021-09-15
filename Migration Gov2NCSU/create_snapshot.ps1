# -- Create a snapshot of the OS (and optionally data disks) from the generalized VM -- #>
$resourceGroupName = '3DWeeds' 
$region = 'usgovvirginia' 
$vmName = 'AnnotationSystem'
$snapshotName = 'AnnotationSnapshot'
$imageName = 'AnnotationImage'  

$vm = Get-AzureRmVM -ResourceGroupName $resourceGroupName -Name $vmName
$disk = Get-AzureRmDisk -ResourceGroupName $resourceGroupName -DiskName $vm.StorageProfile.OsDisk.Name
$snapshot = New-AzureRmSnapshotConfig -SourceUri $disk.Id -CreateOption Copy -Location $region
 
$snapshotName = $imageName + "-" + $region + "-snap"
 
New-AzureRmSnapshot -ResourceGroupName $resourceGroupName -Snapshot $snapshot -SnapshotName $snapshotName 