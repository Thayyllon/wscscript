'SRV-CEILANDIA','SRV-TAGUATINGA','SRV-BRASILIA' | ForEach-Object { Resolve-DnsName -Type A $_ | Select Name,IPAddress }