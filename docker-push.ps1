# Forcefully clear proxy settings for this session
[System.Environment]::SetEnvironmentVariable("HTTP_PROXY", $null, "Process")
[System.Environment]::SetEnvironmentVariable("HTTPS_PROXY", $null, "Process")
[System.Environment]::SetEnvironmentVariable("http_proxy", $null, "Process")
[System.Environment]::SetEnvironmentVariable("https_proxy", $null, "Process")




# will auto push docke rimage to registry after its creation - container app wil auto pull this image

az acr login --name mf37registry
docker tag main-app:latest mf37registry.azurecr.io/main-app:latest
docker push mf37registry.azurecr.io/main-app:latest
