from gmusicapi.api import Api
from getpass import getpass


def init():
    api = Api()

    with open("/tmp/gmusic.txt") as f:
        creds = f.read()
        email, password = creds.split(":")

    logged_in = api.login(email, password)

    return api, logged_in


def main():
    api, success = init()
    if success:
        print "Yep"
    else:
        print "NOPE"
        return

    query = raw_input("Search Query: ")
    response = api.search(query)
    search_results = response["results"]

    songs = search_results["songs"]
    if not len(songs):
        print "Nothing found :("
        return

    for i, song in enumerate(songs[:10]):
        print "%d." % i, "%(id)s: %(artist)s - %(title)s" % song

    num = raw_input("Choose song: ")
    song = songs[int(num)]

    url = api.get_stream_url(song["id"])
    print url


if __name__ == '__main__':
    main()
