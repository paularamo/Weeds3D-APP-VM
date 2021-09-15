## In the Goverment Subscription

Before starting, be aware you have the VM generation, the size and type of storage.

  

![](https://lh3.googleusercontent.com/RrrVCaoLbn3BjRS6J9GQHxtN3uW-DYHmQR9M2t30afhxnp1z8_JJifzgiTta_yHCMfV4sCHSOlzV82MoqOesp0_joVU1EIPtmCzd82ZEaShvPRQjs2MlG1-DGSOTf_LchyoB7VKh=s0)

  

Also check the disk on the VM

![](https://lh4.googleusercontent.com/YsQ3lAFosQMWpC9iABRM67CvXSUsxAIQN6gQcCbo1uW3upmrbvk55W8ZKjEdNqX1Jmp0txvjADwWW5Iqqe0PUwSYOZLuIx6R0cZp9ZEZGrrCS-sj2IcyPZiYA6V2w4LOFb-otANJ=s0)

  
  

Connect the VM through ssh, over the terminal type this:

  

sudo waagent -deprovision

  

Accept the request (y)

  

![](https://lh3.googleusercontent.com/0VyjXAmbw5oGIOMysN8A5z6AIwaCSr21kGRTGJpxnuZldz7_i2kdiy-B77AxPAfu6hwGxV4Gu7KuWhIcvDFdafkQn1VqXbLfKQhCc1vQ2-avdcg9d4T4ep8IYeV_memCu-vzw3nf=s0)

  

Open powershell in the Azure GovAccount, and run these commands:

  

az vm deallocate --resource-group 3DWeeds --name AnnotationSystem

  

az vm generalize --resource-group 3DWeeds --name AnnotationSystem

  

az image create --resource-group 3DWeeds --name AnnotationImage --source AnnotationSystem

  

Change the names in red by your VMs information.

In blue the new name of your VMimage

  

Modify this script with your VM information create_snapshot.ps1

Check the region or location of your resource. If you have doubts, use this CLI in powershell to verify the string. Get-AzureRmLocation |Format-Table

  

Then, through the portal go to your new snapshot (resource)  Imagename-location-snap.

Then go to “Snap Export” option in the menu on your left.

Create the URL at least for 10000

Copy the URL on the gray text box and keep this in a text file.

  

![](https://lh4.googleusercontent.com/U1pfgoXWX46f-d1dt6uCms0pM_Mf5-nZqXzEG-jcT6LeVivQtsksz-qdSCNAOoKIiYbrkchzGI21dUCvTf90O6LcPLY-ErnVuGkFx-GtASe-s0F2hWAo_DS94iJOADu8WzQXKdwA=s0)

  

Before the next step:

Go to the CALS-PSA subscription and create a storage account, and a blob container. Let me know if you need instructions here.

  

Generate Shared Access Signature with all privileges and at least one day of access time.

Copy the complete URI, keep this in the same text file.

  

Come back to the PowerShell in this Gov account, and execute the next CLI, where in green you should paste the URL for the snapshot, and in purple you should paste the URI from the CALS-PSA blob container.

  

azcopy copy 'https://md-zlfrg422rpfr.blob.core.usgovcloudapi.net/h4c5w4m5bsj2/abcd?sv=2018-03-28&sr=b&si=3c148163-9fb5-4662-8645-6858f5f22f0b&sig=C8Hkwm9MQ%2B2WsAQyvBjE%2FmXYfw8k9oQ3LjLy8S2l0vU%3D' 'https://weedsmedia2.blob.core.windows.net/migration?sv=2019-12-12&st=2021-09-03T17%3A33%3A29Z&se=2022-09-04T17%3A33%3A00Z&sr=c&sp=racwdl&sig=%2BTtF%2BvV1OLQViAuThS0kOV1r332gY5eppWjX%2B2ZEalo%3D' --recursive

  
  
  

## In the CALS-PSA - Power shell

  

Select-AzureRmSubscription '5aa49bea-93fb-4d1c-ab7e-e4549cb2b935'

  

Modify and run this script, create_snapshot_in_new_subscription.ps1

