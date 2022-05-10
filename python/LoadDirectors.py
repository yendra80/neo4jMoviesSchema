from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class LoadDirectors:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_director(self, pperson, ptitle, pborn):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_director, pperson, ptitle, pborn)
            for row in result:
                print("Created / merged person and label director from Movie: " ,ptitle, "= {p}".format(p=row["p"]))


    @staticmethod
    def _create_and_return_director(tx, person, title, born):
        query = (
            "MERGE (p:Person:Director { name: $name, born: $born})" 
            " RETURN p"
        )
        #print(query)

        result = tx.run(query, name=person, born=born)

        try:
            return [{"p": row["p"]["name"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_relationship(self, pperson, ptitle):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_rel, pperson, ptitle)

            for row in result:
                print("Created / merged relationship movie and director from: ", ptitle, "and {p}".format(p=row["p"]))

    @staticmethod
    def _create_and_return_rel(tx, person, title):
        query2 = (
            "MATCH (m:Movie) where m.title = $title  "
            "MATCH (p:Person {name: $name}) "
            "MERGE (p)-[:DIRECTED]->(m)" 
            " RETURN p"
        )

        #print (query2)
        result = tx.run(query2, title=title, name=person)
        
        try:
            return [{"p": row["p"]["name"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

if __name__ == "__main__":
    uri = "neo4j://3.83.97.78"
    user = "neo4j"
    password = "neo4j"
    app = LoadDirectors(uri, user, password)

    ######################################################################################################
    ## Create Person& Directors
    ######################################################################################################
    app.create_director("Lilly Wachowski", "The Matrix", 1970)
    app.create_director("Lana Wachowski", "The Matrix", 1970)
    app.create_director("Lana Wachowski", "The Matrix Reloaded", 1970)
    app.create_director("Lilly Wachowski", "The Matrix Reloaded", 1970)
    app.create_director("Lana Wachowski", "The Matrix Revolutions", 1970)
    app.create_director("Lilly Wachowski", "The Matrix Revolutions", 1970)
    app.create_director("Taylor Hackford", "The Devil's Advocate", 1970)
    app.create_director("Rob Reiner", "A Few Good Men", 1970)
    app.create_director("Tony Scott", "Top Gun", 1970)
    app.create_director("Cameron Crowe", "Jerry Maguire", 1970)
    app.create_director("Rob Reiner", "Stand By Me", 1970)
    app.create_director("James L. Brooks", "As Good as It Gets", 1970)
    app.create_director("Vincent Ward", "What Dreams May Come", 1970)
    app.create_director("Scott Hicks", "Snow Falling on Cedars", 1970)
    app.create_director("Nora Ephron", "You've Got Mail", 1970)
    app.create_director("Nora Ephron", "Sleepless in Seattle", 1970)
    app.create_director("John Patrick Stanley", "Joe Versus the Volcano", 1970)
    app.create_director("Rob Reiner", "When Harry Met Sally", 1970)
    app.create_director("Tom Hanks", "That Thing You Do", 1970)
    app.create_director("Howard Deutch", "The Replacements", 1970)
    app.create_director("Werner Herzog", "RescueDawn", 1970)
    app.create_director("Mike Nichols", "The Birdcage", 1970)
    app.create_director("Clint Eastwood", "Unforgiven", 1970)
    app.create_director("Robert Longo", "Johnny Mnemonic", 1970)
    app.create_director("Tom Tykwer", "Cloud Atlas", 1970)
    app.create_director("Lilly Wachowski", "Cloud Atlas", 1970)
    app.create_director("Lana Wachowski", "Cloud Atlas", 1970)
    app.create_director("Ron Howard", "The Da Vinci Code", 1970)
    app.create_director("James Marshall", "V for Vendetta", 1970)
    app.create_director("Lana Wachowski", "Speed Racer", 1970)
    app.create_director("Lilly Wachowski", "Speed Racer", 1970)
    app.create_director("James Marshall", "Ninja Assassin", 1970)
    app.create_director("Frank Darabont", "The Green Mile", 1970)
    app.create_director("Ron Howard", "Frost/Nixon", 1970)
    app.create_director("Danny DeVito", "Hoffa", 1970)
    app.create_director("Ron Howard", "Apollo 13", 1970)
    app.create_director("Jan de Bont", "Twister", 1970)
    app.create_director("Robert Zemeckis", "Cast Away", 1970)
    app.create_director("Milos Forman", "One Flew Over the Cuckoo's Nest", 1970)
    app.create_director("Nancy Meyers", "Something's Gotta Give", 1970)
    app.create_director("Chris Columbus", "Bicentennial Man", 1970)
    app.create_director("Mike Nichols", "Charlie Wilson's War", 1970)
    app.create_director("Robert Zemeckis", "The Polar Express", 1970)
    app.create_director("Penny Marshall", "A League of Their Own", 1970)
    ######################################################################################################
    ## Create Relationship between Directors & Movie through DIRECTED
    ######################################################################################################
    app.create_relationship("Lilly Wachowski", "The Matrix")
    app.create_relationship("Lana Wachowski", "The Matrix")
    app.create_relationship("Lana Wachowski", "The Matrix Reloaded")
    app.create_relationship("Lilly Wachowski", "The Matrix Reloaded")
    app.create_relationship("Lana Wachowski", "The Matrix Revolutions")
    app.create_relationship("Lilly Wachowski", "The Matrix Revolutions")
    app.create_relationship("Taylor Hackford", "The Devil's Advocate")
    app.create_relationship("Rob Reiner", "A Few Good Men")
    app.create_relationship("Tony Scott", "Top Gun")
    app.create_relationship("Cameron Crowe", "Jerry Maguire")
    app.create_relationship("Rob Reiner", "Stand By Me")
    app.create_relationship("James L. Brooks", "As Good as It Gets")
    app.create_relationship("Vincent Ward", "What Dreams May Come")
    app.create_relationship("Scott Hicks", "Snow Falling on Cedars")
    app.create_relationship("Nora Ephron", "You've Got Mail")
    app.create_relationship("Nora Ephron", "Sleepless in Seattle")
    app.create_relationship("John Patrick Stanley", "Joe Versus the Volcano")
    app.create_relationship("Rob Reiner", "When Harry Met Sally")
    app.create_relationship("Tom Hanks", "That Thing You Do")
    app.create_relationship("Howard Deutch", "The Replacements")
    app.create_relationship("Werner Herzog", "RescueDawn")
    app.create_relationship("Mike Nichols", "The Birdcage")
    app.create_relationship("Clint Eastwood", "Unforgiven")
    app.create_relationship("Robert Longo", "Johnny Mnemonic")
    app.create_relationship("Tom Tykwer", "Cloud Atlas")
    app.create_relationship("Lilly Wachowski", "Cloud Atlas")
    app.create_relationship("Lana Wachowski", "Cloud Atlas")
    app.create_relationship("Ron Howard", "The Da Vinci Code")
    app.create_relationship("James Marshall", "V for Vendetta")
    app.create_relationship("Lana Wachowski", "Speed Racer")
    app.create_relationship("Lilly Wachowski", "Speed Racer")
    app.create_relationship("James Marshall", "Ninja Assassin")
    app.create_relationship("Frank Darabont", "The Green Mile")
    app.create_relationship("Ron Howard", "Frost/Nixon")
    app.create_relationship("Danny DeVito", "Hoffa")
    app.create_relationship("Ron Howard", "Apollo 13")
    app.create_relationship("Jan de Bont", "Twister")
    app.create_relationship("Robert Zemeckis", "Cast Away")
    app.create_relationship("Milos Forman", "One Flew Over the Cuckoo's Nest")
    app.create_relationship("Nancy Meyers", "Something's Gotta Give")
    app.create_relationship("Chris Columbus", "Bicentennial Man")
    app.create_relationship("Mike Nichols", "Charlie Wilson's War")
    app.create_relationship("Robert Zemeckis", "The Polar Express")
    app.create_relationship("Penny Marshall", "A League of Their Own")
    app.close()
