#!/usr/bin/env python

"""
A simple pygtk dialog box application for launching the 3-panel movie player on the Power Wall
"""

import pygtk
pygtk.require('2.0')
import gtk

from subprocess import call

# Init our movie data
path_1 = "/home/user/converted-movies"
path_2 = "/mnt/scratch/low-z/1536/movies/new"

font_size = 25000
wall_player_path='/home/user/converted-movies/wall_player'

movies = [
dict(name='ICF-10K-FV-dump25-27-fly27', path=path_1, files=['ICF-10K-FV-dump25-27-fly27-panel-1.avi', 'ICF-10K-FV-dump25-27-fly27-panel-3.avi', 'ICF-10K-FV-dump25-27-fly27-panel-2.avi']),
dict(name='ICF-10K-FV-dump27_fly', path=path_1, files=['ICF-10K-FV-dump27_fly_panel-1.avi', 'ICF-10K-FV-dump27_fly_panel-3.avi', 'ICF-10K-FV-dump27_fly_panel-2.avi']),
dict(name='ICF-10K-FV-dump27', path=path_1, files=['ICF-10K-FV-dump27-panel-1.avi', 'ICF-10K-FV-dump27-panel-3.avi', 'ICF-10K-FV-dump27-panel-2.avi']),
dict(name='icfv2-12fps', path=path_1, files=['icfv2-12fps-panel-1.avi', 'icfv2-12fps-panel-2.avi', 'icfv2-12fps-pane-3.avi']),
dict(name='icfv2-18fps', path=path_1, files=['icfv2-18fps-panel-1.avi', 'icfv2-18fps-panel-3.avi', 'icfv2-18fps-panel-2.avi']),
dict(name='phlin5pw', path=path_1, files=['phlin5pw-panel-1.avi', 'phlin5pw-panel-3.avi', 'phlin5pw-panel-2.avi']),
dict(name='rgb16', path=path_1, files=['rgb16-DT-3-SCmovie-PW-panel-1.avi', 'rgb16-DT-3-SCmovie-PW-panel-3.avi', 'rgb16-DT-3-SCmovie-PW-panel-2.avi']),
dict(name='Sakurai-1536', path=path_1, files=['Sakurai-1536-Lg10Vort-part1-panel-1_0000-1359_18.avi', 'Sakurai-1536-TanhUY-part1-panel-1_0000-1358_18.avi', 'Sakurai-1536-FV-part1-panel-1_0000-1359_18.avi']),
dict(name='tp2-2d', path=path_1, files=['tp2-2d-panel-1.avi', 'tp2-2d-panel-3.avi', 'tp2-2d-panel-2.avi']),
dict(name='u05PWall1-Lvort', path=path_1, files=['u05PWall1-Lvort-panel-1.avi', 'u05PWall1-Lvort-panel-3.avi', 'u05PWall1-Lvort-panel-2.avi']),
dict(name='low-z-1536 Vort', path=path_2, files=['low-z-1536_Lg10Vort-01-slice_1_0001-1960_4k_18.avi', 'low-z-1536_Lg10Vort-01-slice_3_0001-1960_4k_18.avi', 'low-z-1536_Lg10Vort-01-back_0001-1960_4k_18.avi']),
dict(name='low-z-1536 FV', path=path_2, files=['low-z-1536_FV-hires-01-slice_1_0001-1960_4k_18.avi', 'low-z-1536_FV-hires-01-slice_3_0001-1960_4k_18.avi', 'low-z-1536_FV-hires-01-back_0001-1960_4k_18.avi']),
dict(name='low-z-1536 Vort FV TanhUY', path=path_2, files=['low-z-1536_Lg10Vort-01-back_0001-1960_4k_18.avi', 'low-z-1536_TanhUY--001-back_0001-1960_4k_18.avi', 'low-z-1536_FV-hires-01-back_0001-1960_4k_18.avi']),
dict(name='low-z-1536 Vort FV Enuc', path=path_2, files=['low-z-1536_Lg10Vort-01-back_0001-1960_4k_18.avi', 'low-z-1536_Lg10ENUCbyP-back_0001-1960_4k_18.avi', 'low-z-1536_FV-hires-01-back_0001-1960_4k_18.avi']),
]

class MoviesMenu:

    def play_movie_callback(self, widget, data):
        print "Playing movie" % data
        
        cli = [wall_player_path] + data.get('files')
        print "Executing ", cli
        call(cli)

    # another callback
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.resize(800, 1024)

        self.window.set_title("LCSE Demo Movies")

        self.window.connect("delete_event", self.delete_event)

        # Sets the border width of the window.
        self.window.set_border_width(10)

        self.box = gtk.VBox(True, 10)
        self.window.add(self.box)
        
        for movie in movies:
        
          #label = gtk.Label()
          #label.set_markup('<span size="38000">%s</span>' % movie.get('name'))
          #label.show()          
          
          button = gtk.Button(movie.get('name'))
          label = button.get_child()
          label.set_markup('<span size="%i">%s</span>' % (font_size, movie.get('name')))
        
          #button.get_label().set_use_markup(gtk.TRUE)
          
          button.connect("clicked", self.play_movie_callback, movie)
          button.show()
          
          self.box.pack_start(button, True, True, 0)

        self.box.show()
        self.window.show()

def main():
    gtk.main()

if __name__ == "__main__":
    hello = MoviesMenu()
    main()
