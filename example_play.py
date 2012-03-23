import sys
import signal
from getpass import getpass
from gmusicapi.api import Api

try:
    from PyQt4.QtGui import QApplication
    from PyQt4.phonon import Phonon
    PLAYER = "phonon"
except ImportError:
    try:
        import glib
        import pygst
        pygst.require("0.10")
        import gst
        PLAYER = "gst"
    except ImportError:
        PLAYER = None


def init():
    api = Api()

    logged_in = False
    attempts = 0

    while not logged_in and attempts < 3:
        email = raw_input("Email: ")
        password = getpass()

        logged_in = api.login(email, password)
        attempts += 1

    return api, logged_in


def play(url):
    if PLAYER == "phonon":
        app = QApplication(sys.argv)
        app.setApplicationName("Google Music playing test")
        output = Phonon.AudioOutput(Phonon.MusicCategory)
        media = Phonon.MediaObject()
        Phonon.createPath(media, output)
        media.setCurrentSource(Phonon.MediaSource(url))
        media.play()
        # Trick to allow Ctrl+C to exit.
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        sys.exit(app.exec_())

    elif PLAYER == "gst":
        player = gst.element_factory_make("playbin2", "player")
        player.set_property("uri", url)
        player.set_state(gst.STATE_PLAYING)
        glib.MainLoop().run()
    else:
        print "Cannot play the media :("
        return


def main():
    api, success = init()
    if success:
        print "Success: logged in."
    else:
        print "Couldn't log in :("
        return

    query = raw_input("Search Query: ")
    response = api.search(query)
    search_results = response["results"]

    songs = search_results["songs"]
    if not len(songs):
        print "Nothing found :("
        return

    for i, song in enumerate(songs[:10]):
        print "%d." % i, "%(artist)s - %(title)s" % song

    num = None
    while num is None:
        num = raw_input("Choose song: ")
        try:
            num = int(num)
        except ValueError:
            num = None
        else:
            try:
                song = songs[num]
            except IndexError:
                num = None

    url = api.get_stream_url(song["id"])
    play(url)


if __name__ == '__main__':
    main()
