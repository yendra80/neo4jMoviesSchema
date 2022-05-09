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
There are 2 types of Neo4J: Community Edition and Enterprise Edition

To install Neo4j Community Edition:
>sudo apt-get install neo4j=1:4.4.6

To install Neo4j Enterprise Edition:
>sudo apt-get install neo4j-enterprise=1:4.4.6
