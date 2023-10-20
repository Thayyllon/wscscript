#WSC 2023 #39

import paramiko
import time
import os 

maquinas = [
    "SOROCABA","CAMPINAS","APARECIDA","JAPARATINGA","ARAPIRACA","MARAGOGI","MACEIO","CEILANDIA","TAGUATINGA","GAMA","GUARA","SRV-DC-SHARE","SRV-HA-01","SRV-HA-02","FZ-WEB-01","FZ-WEB-02"
]

SOROCABA = "192.168.0.1"
CAMPINAS = "192.168.0.2"

APARECIDA = "192.168.0.254"

JAPARINGA = "172.18.0.12"

ARAPIRACA = "172.17.0.11"
MARAGOGI = "172.17.0.21"
MACEIO = "172.17.0.22"

CEILANDIA = "192.168.17.1"
TAGUATINGA = "192.168.17.2"

GAMA = "192.168.17.250"
GUARA = "192.168.17.249"

DC_SHARE = "10.0.0.2"
HA_01 = "10.0.0.251"
HA_02 = "10.0.0.252"
FZ_WEB_01 = "10.0.0.21"
FZ_WEB_02 = "10.0.0.22"

port = 22
username = "root"
password = "Skill39"

username1 = "Administrator"
password1 = "Skill39"

pontuação = 0 

pontos = [0.10, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55 ]
# 0.1 - pontos[0]
# 0.2 - pontos[1]
# 0.25 - pontos[2]
# 0.3 - pontos[3]
# 0.35 - pontos[4]
# 0.4 - pontos[5]
# 0.45 - pontos[6]
# 0.50 - pontos[7]
# 0.55 - pontos[8]


#----------------------------------------Função para conectar nos servidores e executar comandos-------------------------------------------- 

def con_serv(servidor, comando):

    ssh = paramiko.SSHClient()

    try:
    
    #Conecta nos servidores
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passa as credenciais 
        ssh.connect(servidor, port, username, password,timeout=120,banner_timeout=120,auth_timeout=120)

    #Executa os comandos passados na função 
        commands = [
            comando
        ]

        for command in commands:
         #   print(f"Executing command: {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            # t = 10
            # time.sleep(t)
            output = stdout.read().decode()
            
        ssh.close()

    #Tratamento de erro 
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your credentials.")
    except paramiko.SSHException as e:
        print(f"SSH error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
    
        if ssh is not None:
            ssh.close()

    return output


#----------------------------------------Função para conectar nos servidores e executar comandos no windows-------------------------------------------- 

def con_win(servidor, comando):

    ssh = paramiko.SSHClient()

    try:
    
    #Conecta nos servidores
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    #Passa as credenciais 
        ssh.connect(servidor, port, username1, password1,timeout=120,banner_timeout=120,auth_timeout=120)

    #Executa os comandos passados na função 
        commands = [
            comando
        ]

        for command in commands:
         #   print(f"Executing command: {command}")
            stdin, stdout, stderr = ssh.exec_command(command)
            t = 10
            time.sleep(t)
            output = stdout.read().decode()
            
        ssh.close()

    #Tratamento de erro 
    except paramiko.AuthenticationException:
        print("Authentication failed, please check your credentials.")
    except paramiko.SSHException as e:
        print(f"SSH error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
    
        if ssh is not None:
            ssh.close()

    return output

#-------------------------------------Função e auditoria para registrar o que está sendo corrigido pelo script------------------------------

def auditoria(maquina, pontuação, comando, audit):

    texto = f"-------------------------------------------------------------------------- \n \n \n MAQUINA CORRIGIDA: {maquina} \n \n  COMANDO REALIZADO: '{comando}' \n \n  OUTPUT DO COMANDO:\n\n{audit} \n PONTUACAO: {pontuação} \n \n \n"
    file = "/var/wsc39script/maquinas"

    with open(file,'a') as anexo:
            anexo.write(texto)

    return print(f"Correção da máquina {maquina} realizada com sucesso.")


#Função de anexo de mensagem no arquivo maquinas
def anexo(texto):
    file = "/var/wsc39script/maquinas"
    with open(file, 'a') as anexo:
            anexo.write(texto)
    

#Correções 

case = input("DIGITE O NÚMERO PARA CORREÇÃO DE PARTES DA PROVA \n 1 - wsc2023.sp.gov \n 2 - Máquina JAPARATINGA \n 3 - wsc2023.df.gov \n 4 - wsc2023.datacenter \n 5 - wsc2023.al.gov \n\n") 
def switch_case(case):
    if case == "1":

        #CORREÇÃO MAQUINA SRV-CAMPINAS EMAIL ----------------------

        comando = 'echo ""'
        con_serv(CAMPINAS,comando)

        cmd = 'sshpass -p "Skill39" scp /var/wsc39script/lin/email root@192.168.0.2:/opt/'
        os.system(cmd)

        comando = 'bash /opt/email | telnet localhost 25'
        con_serv(CAMPINAS,comando)
        time.sleep(2)
        comando1 = 'bash /opt/email | telnet localhost 25'
        audit = con_serv(CAMPINAS,comando1)
        #print(audit)

        auditoria(maquinas[1],pontos[7],comando, audit) #0.5


        #CORREÇÃO MAQUINA SRV-SOROCABA DNS 01 ----------------------


        comando = "for x in SRV-CAMPINAS SRV-SOROCABA SRV-APARECIDA; do host $x.wsc2023.sp.gov; done "

        audit = con_serv(SOROCABA,comando)
        #print(audit)
        auditoria(maquinas[0],pontos[7],comando,audit) #0.5
            

        #CORREÇÃO MAQUINA SRV-SOROCABA DNS 02 ----------------------


        comando = "host -t mx wsc2023.sp.gov"

        audit = con_serv(SOROCABA,comando)
        #print(audit)

        auditoria(maquinas[0],pontos[7],comando,audit) #0.5

        
        #CORREÇÃO MAQUINA SRV-SOROCABA LDAP 01 ----------------------


        comando = 'slapcat -a "(&(objectClass=dcObject)(objectClass=organization))" | head -n1 > /var/ldap1'
       
        con_serv(SOROCABA,comando)

        time.sleep(10)

        comando1 = 'cat /var/ldap1'

        audit = con_serv(SOROCABA,comando1)

        auditoria(maquinas[0],pontos[7],comando,audit) #0.5


        #CORREÇÃO MAQUINA SRV-SOROCABA LDAP 02 ----------------------


        comando = 'slapcat -a "(&(objectClass=inetOrgPerson)(uid=donald))" > /var/ldap2'
        
        con_serv(SOROCABA,comando)
        
        time.sleep(10)
        
        comando1 = 'cat /var/ldap2'
        
        audit = con_serv(SOROCABA,comando1)
        #print(audit)

        auditoria(maquinas[0],pontos[7],comando,audit) #0.5


    elif case == "2":

        #Correção com tgtadm -------------------------------------------------------------------------------------

        texto = "\n \n ----------------------- Correção com tgtadm ----------------------- \n\n "
        anexo(texto)

        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 01 ----------------------


        comando = 'tgtadm -m target --op show | grep Target'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 02 ----------------------


        comando = 'tgtadm -m target --op show'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 03 ----------------------


        comando = 'tgtadm -m target --op show | grep Initiator'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 04 ----------------------


        comando = 'fdisk -l /var/lib/iscsi_disks/web-disk.img | grep web-disk | cut -d" " -f3,4'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 05 ----------------------


        comando = ' fdisk -l /var/lib/iscsi_disks/maragogi-disk.img | grep maragogi-disk | cut -d" " -f3,4'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 06 ----------------------


        comando = 'tgtadm --lld iscsi --op show --mode account'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)


        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 07 ----------------------


        comando = 'grep incominguser /etc/tgt/targets.conf'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)


        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #Correção com targetcli ------------------------------------------------------------------------------------------------------------------------------
        
        texto = "\n \n ----------------------- Correção com targetcli ----------------------- \n\n "
        anexo(texto)

        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 01 ----------------------


        comando = 'targetcli cd /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-web &> /dev/null ; echo $? && targetcli cd /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maragogi &> /dev/null ; echo $? &&  targetcli cd /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maceio &> /dev/null ; echo $?'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 02 ----------------------


        comando = ' targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-web/tpg1 get attribute authentication &&  targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maragogi/tpg1 get attribute authentication &&  targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maceio/tpg1 get attribute authentication'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 03 ----------------------


        comando = ' targetcli cd /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-web/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-arapiraca &> /dev/null ; echo $? &&  targetcli cd /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maragogi/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-maragogi &> /dev/null ; echo $? && targetcli cd /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maceio/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-maceio &> /dev/null ; echo $?'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 04 ----------------------


        comando = 'fdisk -l /var/lib/iscsi_disks/web-disk.img | grep web-disk | cut -d" " -f3,4'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 05 ----------------------


        comando = ' fdisk -l /var/lib/iscsi_disks/maragogi-disk.img | grep maragogi-disk | cut -d" " -f3,4'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)

        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 06 ----------------------


        comando = 'targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-web/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-arapiraca get auth userid &&  targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maceio/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-maceio get auth userid &&  targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maragogi/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-maragogi get auth userid'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)


        auditoria(maquinas[3],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-JAPARATINGA ISCSI 07 ----------------------


        comando = ' targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-web/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-arapiraca get auth password &&  targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maragogi/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-maragogi get auth password &&  targetcli /iscsi/iqn.2023-08.farmzone.gov.al.wsc2023:target-maceio/tpg1/acls/iqn.2023-08.farmzone.gov.al.wsc2023:initiator-maceio get auth password'

        audit = con_serv(JAPARINGA,comando)
        #print(audit)


        auditoria(maquinas[3],pontos[2],comando,audit) #0.25

    elif case == "3":

        #CORREÇÃO MAQUINA SRV-CEILANDIA AD DC----------------------


        comando = 'powershell Get-ADDomainController -Discover'

        audit = con_win(CEILANDIA,comando)
        #print(audit)

        auditoria(maquinas[7],pontos[7],comando,audit) #0.5


        #CORREÇÃO MAQUINA SRV-CEILANDIA DNS----------------------

        cmd = 'sshpass -p "Skill39" scp -r /var/wsc39script/win/ceilandia Administrator@192.168.17.1:C:/wsc39'
        os.system(cmd)

        comando = 'powershell "C:\\wsc39\\.\\dns.ps1" '

        audit = con_win(CEILANDIA,comando)
        #print(audit)


        auditoria(maquinas[7],pontos[7],comando,audit) #0.5


        #CORREÇÃO MAQUINA SRV-TAGUATINGA DHCP ----------------------


        comando = 'journalctl -x | grep DHCP &> /dev/null ; echo $?'

        audit = con_serv(TAGUATINGA,comando)
        #print(audit)


        auditoria(maquinas[8],pontos[5],comando,audit) #0.4


        #CORREÇÃO MAQUINA SRV-TAGUATINGA CA01 ----------------------


        comando = 'ls -l /data/CA &> /dev/null ; echo $?'

        audit = con_serv(TAGUATINGA,comando)
        #print(audit)

        auditoria(maquinas[8],pontos[5],comando,audit) #0.45


        #CORREÇÃO MAQUINA SRV-TAGUATINGA CA02 ----------------------


        comando = 'ls -l /data/CA/private/cakey.pem /data/CA/cacert.pem &> /dev/null ; echo $?'

        audit = con_serv(TAGUATINGA,comando)
        #print(audit)

        auditoria(maquinas[8],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-TAGUATINGA CA03 ----------------------


        comando = 'openssl x509 -text -noout -in /data/CA/cacert.pem -subject | tail -n1'

        audit = con_serv(TAGUATINGA,comando)
        #print(audit)

        auditoria(maquinas[8],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-TAGUATINGA CA04 ----------------------


        comando = 'curl -s http://ca.seletivaredes.wsc2023.df.gov/CA/DF-ROOT-CA.crt'

        audit = con_serv(TAGUATINGA,comando)
        #print(audit)

        auditoria(maquinas[8],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-TAGUATINGA CA05 ----------------------


        comando = 'openssl x509 -in /etc/ssl/CA/cacert.pem -text -noout -ext crlDistributionPoints,authorityInfoAccess'

        audit = con_serv(TAGUATINGA,comando)
        #print(audit)

        auditoria(maquinas[8],pontos[4],comando,audit) #0.35


    elif case == "4":

       #CORREÇÃO MAQUINA SRV-DC-SHARE DFS ----------------------


        comando = 'powershell ls C:\share\web'

        audit = con_win(DC_SHARE,comando)
        #more print(audit)

        auditoria(maquinas[11],pontos[7],comando,audit) #0.5


        #CORREÇÃO MAQUINA SRV-HA-01 Proxy1 ----------------------


        comando = 'curl -I -s http://localhost:8080/stats | grep 200'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-01 Proxy2 ----------------------


        comando = 'curl localhost:8080 > assert.txt ; curl localhost:8080 >> assert.txt ; clear ; cat assert.txt'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-01 Proxy3 ----------------------


        comando = 'curl -s -I localhost:8080 | grep server ; curl -s -I localhost:8080 | grep server'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-01 Proxy4 ----------------------


        comando = 'openssl s_client localhost:443 | grep issuer'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-HA-01 VRRP1 ----------------------


        comando = ' grep "virtual_router_id 10" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-HA-01 VRRP2 ----------------------


        comando = 'awk "/authentication \{/,/\}/" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-01 VRRP3 ----------------------


        comando = 'grep "state" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-01 VRRP4 ----------------------


        comando = 'awk "/virtual_ipaddress \{/,/\}/" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-01 VRRP5 ----------------------


        comando = 'grep "interface" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_01,comando)
        #print(audit)

        auditoria(maquinas[12],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-02 Proxy1 ----------------------


        comando = 'curl -I -s http://localhost:8080/stats | grep 200'

        audit = con_serv(HA_02,comando)
        #print(audit)

        auditoria(maquinas[13],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-02 Proxy2 ----------------------


        comando = 'curl localhost:8080 > assert.txt ; curl localhost:8080 >> assert.txt ; clear ; cat assert.txt'

        audit = con_serv(HA_02,comando)
        #print(audit)

        auditoria(maquinas[13],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-02 Proxy3 ----------------------


        comando =  'curl -s -I localhost:8080 | grep server ; curl -s -I localhost:8080 | grep server'

        audit = con_serv(HA_02,comando)
        #print(audit)

        auditoria(maquinas[13],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-HA-02 Proxy4 ----------------------


        comando =  'openssl s_client localhost:443 | grep issuer'

        audit = con_serv(HA_02,comando)
        #print(audit)

        auditoria(maquinas[13],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-HA-02 vrrp1 ----------------------


        comando =  'grep "virtual_router_id 10" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_02,comando)
        #print(audit)

        auditoria(maquinas[13],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-HA-02 vrrp2 ----------------------


        comando =  'awk "/authentication \{/,/\}/" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_02,comando)
        #print(audit)

        auditoria(maquinas[13],pontos[4],comando,audit) #0.35

        
        #CORREÇÃO MAQUINA SRV-HA-02 vrrp3 ----------------------


        comando =  'grep "state" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_02,comando)
        #print(audit)


        auditoria(maquinas[13],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-HA-02 vrrp4 ----------------------


        comando =  'awk "/virtual_ipaddress \{/,/\}/" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_02,comando)
        #print(audit)

        auditoria(maquinas[13],pontos[1],comando,audit) #0.20


        #CORREÇÃO MAQUINA SRV-HA-02 vrrp4 ----------------------


        comando =  'grep "interface" /etc/keepalived/keepalived.conf'

        audit = con_serv(HA_02,comando)
        #print(audit)

        auditoria(maquinas[13],pontos[1],comando,audit) #0.20


        #CORREÇÃO MAQUINA SRV-WEB-01 NFS ----------------------


        comando =  'mount | grep proto=tcp ; echo $?'

        audit = con_serv(FZ_WEB_01,comando)
        #print(audit)

        auditoria(maquinas[14],pontos[1],comando,audit) #0.20


        #CORREÇÃO MAQUINA SRV-WEB-01 Nginx 01 ----------------------


        comando =  'grep "listen 8081" /etc/nginx/sites-enabled/default ; echo $?'

        audit = con_serv(FZ_WEB_01,comando)
        #print(audit)

        auditoria(maquinas[14],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-WEB-01 Nginx 02 ----------------------


        comando =  'grep "root \/var\/www\/html\/web" /etc/nginx/sites-enabled/default ; echo $?'

        audit = con_serv(FZ_WEB_01,comando)
        #print(audit)

        auditoria(maquinas[14],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-WEB-01 Nginx 03 ----------------------


        comando =  'grep "listen 80" /etc/nginx/sites-enabled/default ; echo $?'

        audit = con_serv(FZ_WEB_01,comando)
        #print(audit)

        auditoria(maquinas[14],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-WEB-01 Nginx 04 ----------------------


        comando =  'grep "root \/var\/www\/html\/default" /etc/nginx/sites-enabled/default ; echo $?'

        audit = con_serv(FZ_WEB_01,comando)
        #print(audit)

        auditoria(maquinas[14],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-WEB-02 NFS ----------------------


        comando =  'mount | grep proto=tcp ; echo $?'

        audit = con_serv(FZ_WEB_02,comando)
        #print(audit)

        auditoria(maquinas[15],pontos[1],comando,audit) #0.20


        #CORREÇÃO MAQUINA SRV-WEB-02 Nginx 01 ----------------------


        comando =  'grep "\<VirtualHost \*:8082\>" /etc/apache2/sites-enabled/000-default.conf ; echo $?'

        audit = con_serv(FZ_WEB_02,comando)
        #print(audit)

        auditoria(maquinas[15],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-WEB-02 Nginx 02 ----------------------


        comando =  'grep "DocumentRoot \/var\/www\/html\/web" /etc/apache2/sites-enabled/000-default.conf ; echo $?'

        audit = con_serv(FZ_WEB_02,comando)
        #print(audit)

        auditoria(maquinas[15],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-WEB-02 Nginx 03 ----------------------


        comando =  'grep "\<VirtualHost \*:80\>" /etc/apache2/sites-enabled/000-default.conf ; echo $?'

        audit = con_serv(FZ_WEB_02,comando)
        #print(audit)

        auditoria(maquinas[15],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-WEB-02 Nginx 04 ----------------------


        comando =  'grep "DocumentRoot \/var\/www\/html\/default" /etc/apache2/sites-enabled/000-default.conf; echo $?'

        audit = con_serv(FZ_WEB_02,comando)
        #print(audit)

        auditoria(maquinas[15],pontos[2],comando,audit) #0.25
    
    elif case == "5":

        comando = 'echo ""'
        audit = con_win(ARAPIRACA,comando)
        audit = con_win(MARAGOGI,comando)
        audit = con_win(MACEIO,comando)

        cmd = 'sshpass -p "Skill39" scp -r /var/wsc39script/win/arapiraca Administrator@172.17.0.11:C:/wsc39'
        os.system(cmd)
        cmd2 = 'sshpass -p "Skill39" scp -r /var/wsc39script/win/maragogi Administrator@172.17.0.21:C:/wsc39'
        os.system(cmd2)
        cmd3 = 'sshpass -p "Skill39" scp -r /var/wsc39script/win/maceio Administrator@172.17.0.22:C:/wsc39'
        os.system(cmd3)

       #CORREÇÃO MAQUINA SRV-ARAPIRACA ISCSI INITIATOR ----------------------


        comando = 'powershell C:\\wsc39\\.\\script1.ps1'

        audit = con_win(ARAPIRACA,comando)
        #print(audit)

        auditoria(maquinas[4],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-ARAPIRACA ISS ----------------------


        comando = 'powershell C:\\wsc39\\.\\script2.ps1'

        audit = con_win(ARAPIRACA,comando)
        #print(audit)

        auditoria(maquinas[4],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-ARAPIRACA ISS2 ----------------------


        comando = 'powershell C:\\wsc39\\.\\script3.ps1'

        audit = con_win(ARAPIRACA,comando)
        #print(audit)

        auditoria(maquinas[4],pontos[7],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-MARAGOGI ISCSI INITIATOR ----------------------


        comando = 'powershell C:\\wsc39\\.\\script1.ps1'

        audit = con_win(MARAGOGI,comando)
        #print(audit)

        auditoria(maquinas[5],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-MARAGOGI DFS ----------------------


        comando = 'powershell C:\\wsc39\\.\\script2.ps1'

        audit = con_win(MARAGOGI,comando)
        #print(audit)

        auditoria(maquinas[5],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-MARAGOGI DFS ----------------------


        comando = 'powershell C:\\wsc39\\.\\script3.ps1'

        audit = con_win(MARAGOGI,comando)
        #print(audit)

        auditoria(maquinas[5],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-MARAGOGI DFS ----------------------


        comando = 'powershell C:\\wsc39\\.\\script4.ps1'

        audit = con_win(MARAGOGI,comando)
        #print(audit)

        auditoria(maquinas[5],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-MARAGOGI DFS ----------------------


        comando = 'powershell C:\\wsc39\\.\\script5.ps1'

        audit = con_win(MARAGOGI,comando)
        #print(audit)

        auditoria(maquinas[5],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-MARAGOGI DFS ----------------------


        comando = 'powershell C:\\wsc39\\.\\script7.ps1'

        audit = con_win(MARAGOGI,comando)
        #print(audit)

        auditoria(maquinas[5],pontos[1],comando,audit) #0.20


        #CORREÇÃO MAQUINA SRV-MARAGOGI DFS ----------------------


        comando = 'powershell C:\\wsc39\\.\\script6.ps1'

        audit = con_win(MARAGOGI,comando)
        #print(audit)

        auditoria(maquinas[5],pontos[1],comando,audit) #0.20


        #CORREÇÃO MAQUINA SRV-MACEIO ISCSI ----------------------


        comando = 'powershell C:\\wsc39\\.\\script1.ps1'

        audit = con_win(MACEIO,comando)
        #print(audit)

        auditoria(maquinas[6],pontos[2],comando,audit) #0.25


        #CORREÇÃO MAQUINA SRV-MACEIO ----------------------


        comando = 'powershell C:\\wsc39\\.\\script2.ps1'

        audit = con_win(MACEIO,comando)
        #print(audit)

        auditoria(maquinas[6],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-MACEIO ----------------------


        comando = 'powershell C:\\wsc39\\.\\script3.ps1'

        audit = con_win(MACEIO,comando)
        #print(audit)

        auditoria(maquinas[6],pontos[4],comando,audit) #0.35


        #CORREÇÃO MAQUINA SRV-MACEIO ----------------------


        comando = 'powershell C:\\wsc39\\.\\script4.ps1'

        audit = con_win(MACEIO,comando)
        #print(audit)

        auditoria(maquinas[6],pontos[1],comando,audit) #0.35

         #CORREÇÃO MAQUINA SRV-MACEIO ----------------------


        comando = 'powershell C:\\wsc39\\.\\script5.ps1'

        audit = con_win(MACEIO,comando)
        #print(audit)

        auditoria(maquinas[6],pontos[1],comando,audit) #0.35

    else:
            
            print("Opção Invalida, escolha entre 1 a 4")    

          
switch_case(case)
   
