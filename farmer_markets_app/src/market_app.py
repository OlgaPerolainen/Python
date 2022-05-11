"""
This is a file to start a program that shows US farmer markets.
It allows to search for markets by name, city, state or zip;
order results by name from A to Z or Z to A, by city, state, ranks and votes;
read and add comments and ranks and change and delete them if you log in using password;
search for markets situated in the radius of N miles.
"""


from source import app

if __name__ == "__main__":
    app.run()
