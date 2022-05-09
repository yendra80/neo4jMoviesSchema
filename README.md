### **Neo4J Installation on Debian based OS**
###### Official documentation can be seen from https://neo4j.com/docs/operations-manual/current/installation/linux/debian/

### 1. Environment Setup
There are 2 items need to be checked on environment
- An OpenJDK Java 11 runtime is installed or available through your package manager.
- The repository containing the Neo4j Debian package is known to the package manager.

  ###### OpenJDK Java 11 installation
  >echo "deb http://httpredir.debian.org/debian stretch-backports main" | sudo tee -a /etc/apt/sources.list.d/stretch-backports.list 
  >
  >sudo apt-get update
  >
  >sudo apt-get install openjdk-11-jre

  ###### Add Neo4j Repository
  To use the repository for generally available versions of Neo4j, run:
  >wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add echo 'deb https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
  >
  >sudo apt-get update

### 2. Installation
There are 2 types of Neo4J: Community Edition and Enterprise Edition. When installing Neo4j Enterprise Edition, you will be prompted to accept the license agreement. Once the license agreement is accepted installation begins.

    To install Neo4j Community Edition:
    >sudo apt-get install neo4j=1:4.4.6

    To install Neo4j Enterprise Edition:
    >sudo apt-get install neo4j-enterprise=1:4.4.6

### 3. Neo4J Instance Checking
Once the installation process is complete, Neo4j should be running. However, it is not set to start on a reboot of your system. So the last setup step is to enable it as a service and then start it:
    > sudo systemctl enable neo4j.service

  Now start the service if it is not already running:
    > sudo systemctl start neo4j.service

  After completing all of these steps, examine Neo4j’s status using the systemctl command:
    > sudo systemctl status neo4j.service

  Output will similar to the following:
  ![image](https://user-images.githubusercontent.com/54164349/167444342-100d3ff8-82e4-4d51-bb50-3173e2b00c90.png)

### 4. Connecting to Neo4j through Cypher Shell
To interact with Neo4j on the command line, use the cypher-shell utility. Invoke the utility like this:
    > cypher-shell

When you first invoke the shell, you will login using the default administrative neo4j user and neo4j password combination. Once you are authenticated, Neo4j will prompt you to change the administrator password. Once you change your password you can re-login to the cypher-shell again with the new password

  ![CypherShell](https://user-images.githubusercontent.com/54164349/167445701-f122bac7-25a0-442c-b2f3-595fcd4f1421.PNG)

You can exit from cypher shell command line by type :exit

![CypherExit](https://user-images.githubusercontent.com/54164349/167446432-180268f2-0ced-49ba-af29-b6e0847e6d0b.PNG)

### 5. Configuring Neo4j for Remote Access
If you would like to incorporate Neo4j into a larger application or environment that uses multiple servers, then you will need to configure it to accept connections from other systems. In this step you will configure Neo4j to allow remote connections, and you will also add firewall rules to restrict which systems can connect to your Neo4j server.

By default Neo4j is configured to accept connections from localhost only (127.0.0.1 is the IP address for localhost). This configuration ensures that your Neo4j server is not exposed to the public Internet, and that only users with access to the local system can interact with Neo4j.

To change the network socket that Neo4j uses from localhost to one that other systems can use, you will need to edit the /etc/neo4j/neo4j.conf file. Open the configuration file in your preferred editor and find the dbms.default_listen_address setting. The following example uses nano to edit the file:
