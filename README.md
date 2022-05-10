## **Instructions:**
- Set up Neo4j Enterprise (Docker / VM). 
- Model any of the below datasets from Tabular to Graph using arrows.app and share the JSON export or URL of the data model.
- Write a graph-enabled application using JavaScript / Python / Go / .Net / Java to ingest data based on the data model.
- Write some exploratory Cypher queries to look at some patterns. You may use Neo4j Browser to execute your queries. You are also encouraged to look into other Neo4j - tools available such as Bloom, Graph Data Science and NeoDash, however primarily the focus must be on Cypher.
- Document all of the above in a README.md file with the code base and share it through a public GitHub repository.

## Data:
- Social Network Graph (https://gist.github.com/maruthiprithivi/10b456c74ba99a35a52caaffafb9d3dc)
- North Wind (https://gist.github.com/maruthiprithivi/f11bf40b558879aca0c30ce76e7dec98)
- Movies (https://gist.github.com/maruthiprithivi/23a210f5c0dc7ba53ac986dfe6f38943)

## Useful Resources:
- Neo4j Graph Academy
- Neo4j YouTube Channel
- Neo4j Developer Blog
- Neo4j Developer Docs


## **Set up Neo4j Enterprise on VM**

I set up cloud environment under AWS EC2 with Ubuntu OS to install Neo4j Enterprise Edition with the following major key steps
###### Official documentation can be seen from https://neo4j.com/docs/operations-manual/current/installation/linux/debian/

#### 1. Environment Setup
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

#### 2. Installation
There are 2 types of Neo4J: Community Edition and Enterprise Edition. When installing Neo4j Enterprise Edition, you will be prompted to accept the license agreement. Once the license agreement is accepted installation begins. For this exercise i choose Neo4j Enterprise Edition

    To install Neo4j Community Edition:
    >sudo apt-get install neo4j=1:4.4.6

    To install Neo4j Enterprise Edition:
    >sudo apt-get install neo4j-enterprise=1:4.4.6

#### 3. Neo4J Instance Checking
Once the installation process is complete, Neo4j should be running. However, it is not set to start on a reboot of your system. So the last setup step is to enable it as a service and then start it:
    
    > sudo systemctl enable neo4j.service

  Now start the service if it is not already running:
    
    > sudo systemctl start neo4j.service

  After completing all of these steps, examine Neo4j’s status using the systemctl command:
    
    > sudo systemctl status neo4j.service

  Output will similar to the following:
  ![image](https://user-images.githubusercontent.com/54164349/167444342-100d3ff8-82e4-4d51-bb50-3173e2b00c90.png)

#### 4. Connecting to Neo4j through Cypher Shell
To interact with Neo4j on the command line, use the cypher-shell utility. Invoke the utility like this:
    > cypher-shell

When you first invoke the shell, you will login using the default administrative neo4j user and neo4j password combination. Once you are authenticated, Neo4j will prompt you to change the administrator password. Once you change your password you can re-login to the cypher-shell again with the new password

  ![CypherShell](https://user-images.githubusercontent.com/54164349/167445701-f122bac7-25a0-442c-b2f3-595fcd4f1421.PNG)

You can exit from cypher shell command line by type :exit

![CypherExit](https://user-images.githubusercontent.com/54164349/167446432-180268f2-0ced-49ba-af29-b6e0847e6d0b.PNG)

#### 5. Configuring Neo4j for Remote Access
If you would like to incorporate Neo4j into a larger application or environment that uses multiple servers, then you will need to configure it to accept connections from other systems. In this step you will configure Neo4j to allow remote connections, and you will also add firewall rules to restrict which systems can connect to your Neo4j server.

By default Neo4j is configured to accept connections from localhost only (127.0.0.1 is the IP address for localhost). This configuration ensures that your Neo4j server is not exposed to the public Internet, and that only users with access to the local system can interact with Neo4j.

To change the network socket that Neo4j uses from localhost to one that other systems can use, you will need to edit the /etc/neo4j/neo4j.conf file. Open the configuration file in your preferred editor and find the dbms.default_listen_address setting. The following example uses nano to edit the file:

  > sudo nano /etc/neo4j/neo4j.conf

Locate the commented out #dbms.default_listen_address=0.0.0.0 line and uncomment it by removing the leading # comment character.

![NetworkConfiguration](https://user-images.githubusercontent.com/54164349/167447442-c58a3936-9e82-47ce-8ddd-22e85d8df9d9.PNG)

By default, the value 0.0.0.0 will bind Neo4j to all available IPv4 interfaces on your system, including localhost. If you would like to limit Neo4j to a particular IP address, for example a private network IP that your servers use for a datapath, specify the IP address that is assigned to your server’s private network interface here.

When you are finished configuring the default IP address that Neo4j will use for connections, save and close neo4j.conf. You might need to restart neo4j instance so  the configuration take effect by execute sudo systemctl restart neo4j.service

#### 6. Connecting to Neo4j through browser

Neo4j equipped with browser to query graph data and cypher. Connect to Neo4j browser by execute http request on your IP and port 7474 (make sure the port is opened) and enter your neo4j username and password that created previously

![image](https://user-images.githubusercontent.com/54164349/167448353-5a6f9f2b-19c6-486c-876e-366390ae8349.png)

Once login the browser will display similar with bellow and we can play along with the data - create node, create relationship, query graph data and others

![image](https://user-images.githubusercontent.com/54164349/167449198-11c6eecc-f4ed-41a3-886a-abdc2b1bbf96.png)


#### Conclusion
You have now installed, configured, and added data to Neo4j on your server. You also optionally configured Neo4j to accept connections from remote systems including browser. Next part would be design the graph schema using arrows.app



## **Design Graph Model using arrows.app**

For this assignment, i choose the movies dataset that can be obtain from (https://gist.github.com/maruthiprithivi/23a210f5c0dc7ba53ac986dfe6f38943) or from official Neo4j blog & academy. I stored in my github as well for data upload and other reference (/datasets/movies)

For movies design, there are 2 nodes that will be implemented
  > - Person
  > - Movie 

Person node will have 2 labels to distinguish their characters Actors and Producer

Concept of Graph Database is data are connected so data need to have relationship. Person and Movie have 2 relationship based on the data that we used and we can name it by use standardize verb
  > - ACTED_IN
  > - DIRECTED

Person will have 2 properties to store additional information of each person
  > - name
  > - born

While movie have 3 properies for this case
  > - title
  > - released
  > - tagline

Even relationship can have property as well. In this case the individual person will have the role in the movie that they played. So we need to add property name roles in the relationship.

Arrows.app designated is only for drawing pictures of graphs and get the feel on how the graph data should connected each other. The complete view in arrows.app will similar to bellow:

![image](https://user-images.githubusercontent.com/54164349/167526229-ab99ca0d-de18-48c8-a800-236eeac35993.png)

## **Ingest data based on the data model using Python**
Neo4j provides drivers which allow you to make a connection to the database and develop applications which create, read, update, and delete information from the graph

#### Neo4j Python Driver
Initially we need to install Neo4j driver for Python. The Neo4j Python driver is officially supported by Neo4j and connects to the database using the binary protocol. It aims to be minimal, while being idiomatic to Python.

Install the Neo4j Driver using pip:
  > pip install neo4j

#### Run python program to load 3 datasets - Actor, Director and Movie
3 python code was setup with the following purposes: LoadMovies.py will load and create the node for movie data set, LoadActors.py will create the Person node, Actors label and create relationship between Person, Actors & Movie node. 

Use the following command to run code:
  > python LoadMovies.py
  > 
  > python LoadActors.py
  > 
  > python LoadDirectors.py

Python code will open connection to neo4j database through neo4j protocol with user and password setup previously. URL might need to be changed to adapt with new environment by changed the following connection string:

  > uri = "neo4j://3.83.97.78"
  > 
  > user = "neo4j"
  > 
  > password = "<password provided>"
  > 

  Once python code successfuly executed we can start explore the node and their relationship in the graph
  
## **Graph Exploration using cypher queries use Neo4j Browser**
  
  #### Schema checking and monitor the data loaded in the Neo4j database
  Let's get back to Neo4j browswer and do schema checking by execute _call db.schema.visualization()_
  We can see there are Person node who contain 2 labels: Actor & Director, and Movie node that connected to Person by 2 relationship (ACTED_IN and DIRECTED). 
  
  ![db schema visualization](https://user-images.githubusercontent.com/54164349/167576301-ef20e77b-3794-49be-9a3e-56e986a2c0ae.PNG)
  
  Let see the total data loaded to Neo4j to reconcile the data with the source
  
  ![image](https://user-images.githubusercontent.com/54164349/167578826-1a07d606-d1df-49fc-b8e4-8b2878c71528.png)


  #### Which movies that Keanue Reeves played  
  We can retrieve all his movies by starting from the Keanue Reeves node and following the ACTED_IN relationships. The results should look like a graph.

  ![image](https://user-images.githubusercontent.com/54164349/167583287-b8abbf4c-1290-4401-8f61-a94cfb9494ec.png)

  #### Who are the colleagues (co-actors) played with Keanue Reeves in his movies
  > MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:ACTED_IN]-(coActor:Person)
  > RETURN m, coActor, p

  ![image](https://user-images.githubusercontent.com/54164349/167587728-83643b86-3d77-48e2-a23e-bcd5ffb7c6d9.png)

  ![image](https://user-images.githubusercontent.com/54164349/167585623-8863cce0-de08-41e9-82f7-0e381b2bda2a.png)
  
  
  #### Who are the actors may not worked with Keanu but connected through his co Actor so have possibility to collaborate in the future -  Collaborative Filtering
  > MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(movie1:Movie)<-[:ACTED_IN]-(coActor:Person)-[:ACTED_IN]->(movie2:Movie)<-[:ACTED_IN]-(coCoActor:Person)
  > WHERE p <> coCoActor
  >
  > AND NOT (p)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(coCoActor)
  >
  > RETURN coCoActor.name, count(coCoActor) as Freq
  > 
  > ORDER BY Freq desc
  > 
  > LIMIT 5

  ![image](https://user-images.githubusercontent.com/54164349/167595395-2ee624da-f2bf-40ee-840b-43a4af60847d.png)
  
  Alternatively we can see through the graph to see overall relationship
  
  ![image](https://user-images.githubusercontent.com/54164349/167595574-e775607d-c38b-483d-b7b6-56be3a569185.png)


  #### Exploring the Paths between Keanu Reeves and Tom Cruise
  
  Throught the table, we can see Tom Cruise have the heighest frequency of occurences become co-co-actor between Keanue Reeves and his co Actor. Now we need to see which movies and actors between Keanue Reeves and Tom Cruise so h/she can introduce them
  
  > MATCH (p:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(movie1:Movie)<-[:ACTED_IN]-(coActor:Person)-[:ACTED_IN]->(movie2:Movie)<-[:ACTED_IN]-(p2:Person {name: 'Tom Cruise'})
  > 
  > WHERE NOT (p)-[:ACTED_IN]->(:Movie)<-[:ACTED_IN]-(p2)
  > 
  > RETURN p, movie1, coActor, movie2, p2
  
  ![image](https://user-images.githubusercontent.com/54164349/167597303-48907113-afd4-4d4a-a968-40c777e29bef.png)
