
Function New-Notification
{
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$False)][string]$Url = "http://192.168.0.148:8000/notify",
        [Parameter(Mandatory=$True)][string]$description,
        [Parameter(Mandatory=$True)][string]$customer_guid,
        [Parameter(Mandatory=$True)][string]$system,
        [Parameter(Mandatory=$False)][string]$attachment_path = ""
    )

    $fileEnc = "";
    if ($attachment_path -ne "") {
        $fileBytes = [System.IO.File]::ReadAllBytes($attachment_path);
        $fileEnc = [System.Text.Encoding]::GetEncoding('UTF-8').GetString($fileBytes);
    }

    $boundary = [System.Guid]::NewGuid().ToString(); 
    $CRLF = "`r`n";
    $body = (
        "--$boundary",
        "Content-Disposition: form-data; name=`"description`"",
        "",
        "$description",
        "--$boundary",
        "Content-Disposition: form-data; name=`"customer`"",
        "",
        "$customer_guid",
        "--$boundary",
        "Content-Disposition: form-data; name=`"system`"",
        "",
        "$system",
        "--$boundary",
        "Content-Disposition: form-data; name=`"attachment`"; filename=`"$attachment_path`"",
        "Content-Type: application/octet-stream",
        "",
        "$fileEnc",
        "--$boundary--"
    ) -join $CRLF

    Invoke-RestMethod -Uri $Url -Method POST -ContentType "multipart/form-data; boundary=`"$boundary`"" -Body $body -Verbose
}

##### Use this module to notify with a file upload
# Import-Module ./CreateNotification.ps1
# New-Notification -description "something went wrong" -system "the mainframe" -customer_guid "a2ccb709-c8f3-4df7-b5f5-f8492bb65de8" -url "http://192.168.0.148:8000/notify" -attachment_path "/mnt/Create-Notification.ps1"

##### Standalone notification without file upload
# Invoke-WebRequest -Uri "http://192.168.0.148:8000/notify" -Method POST -Body @{description='Detected suspicious activity in the log';customer='a2ccb709-c8f3-4df7-b5f5-f8492bb65de8';system="cisco router"}

