from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class LoadMovies:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_movie(self, ptitle, preleased, ptagline):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_movie, ptitle, preleased, ptagline)
            for row in result:
                print("Created movie for: {m}".format(m=row["m"]))

    @staticmethod
    def _create_and_return_movie(tx, title, released, tagline):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "MERGE (m:Movie:Movie { title: $title, released: $released, tagline: $tagline }) "
            "RETURN m"
        )
        result = tx.run(query, title=title, released=released, tagline=tagline)
        try:
            return [{"m": row["m"]["title"]} for row in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

if __name__ == "__main__":
    uri = "neo4j://3.83.97.78"
    user = "neo4j"
    password = "neo4j"
    app = LoadMovies(uri, user, password)
    app.create_movie("The Matrix", 1999, "Welcome to the Real World")
    app.create_movie("Something's Gotta Give", 1975, " Nothing to lose")
    app.create_movie("Ninja Assassin", 2009, "Prepare to enter a secret world of assassins")
    app.create_movie("The Matrix Reloaded", 2003, "Free your mind")
    app.create_movie("Stand By Me", 1995, "For some, it's the last real taste of innocence, and the first real taste of life. But for everyone, it's the time that memories are made of.")
    app.create_movie("The Birdcage", 1996, "Come as you are")
    app.create_movie("Sleepless in Seattle", 1993, "What if someone you never met, someone you never saw, someone you never knew was the only someone for you?")
    app.create_movie("Charlie Wilson's War", 2007, "A stiff drink. A little mascara. A lot of nerve. Who said they couldn't bring down the Soviet empire.")
    app.create_movie("The Polar Express", 2004, "This Holiday Seasonâ€¦ Believe")
    app.create_movie("That Thing You Do", 1996, "In every life there comes a time when that thing you dream becomes that thing you do")
    app.create_movie("Snow Falling on Cedars", 1999, "First loves last. Forever.")
    app.create_movie("A Few Good Men", 1992, "In the heart of the nation's capital, in a courthouse of the U.S. government, one man will stop at nothing to keep his honor, and one will stop at nothing to find the truth.")
    app.create_movie("Twister", 1996, "Don't Breathe. Don't Look Back.")
    app.create_movie("Apollo 13", 1995, "Houston, we have a problem.")
    app.create_movie("Unforgiven", 1992, "It's a hell of a thing, killing a man")
    app.create_movie("Johnny Mnemonic", 1995, "The hottest data on earth. In the coolest head in town")
    app.create_movie("Cast Away", 2000, "At the edge of the world, his journey begins.")
    app.create_movie("Jerry Maguire", 2000, "The rest of his life begins now.")
    app.create_movie("When Harry Met Sally", 1998, "At odds in life... in love on-line.")
    app.create_movie("V for Vendetta", 2006, "Freedom! Forever!")
    app.create_movie("The Replacements", 2000, "Pain heals, Chicks dig scars... Glory lasts forever")
    app.create_movie("The Da Vinci Code", 2006, "Break The Codes")
    app.create_movie("Top Gun", 1986, "I feel the need, the need for speed.")
    app.create_movie("Joe Versus the Volcano", 1990, "A story of love, lava and burning desire.")
    app.create_movie("RescueDawn", 2006, "Based on the extraordinary true story of one man's fight for freedom")
    app.create_movie("What Dreams May Come", 1998, "After life there is more. The end is just the beginning.")
    app.create_movie("Speed Racer", 2008, "Speed has no limits")
    app.create_movie("One Flew Over the Cuckoo's Nest", 1975, "If he's crazy, what does that make you?")
    app.create_movie("The Green Mile", 1999, "Walk a mile you'll never forget.")
    app.create_movie("Frost/Nixon", 2008, "400 million people were waiting for the truth.")
    app.create_movie("The Matrix Revolutions", 2003, "Everything that has a beginning has an end")
    app.create_movie("The Devil's Advocate", 1997, "Evil has its winning ways")
    app.create_movie("A League of Their Own", 1992, "Once in a lifetime you get a chance to do something different.")
    app.create_movie("Cloud Atlas", 2012, "Everything is connected")
    app.create_movie("As Good as It Gets", 1997, "A comedy from the heart that goes for the throat.")
    app.create_movie("Bicentennial Man", 1999, "One robot's 200 year journey to become an ordinary man.")
    app.create_movie("You've Got Mail", 1998, "At odds in life... in love on-line.")
    app.create_movie("Hoffa", 1992, "He didn't want law. He wanted justice.")

    app.close()
