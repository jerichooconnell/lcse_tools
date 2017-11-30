wall_player.go
==============

This is the 3-panel movie player. It launches three separate `mplayer` instances in `udp` slave mode and sends them timecode information.

Build with go

.. code:: bash

  go build wall_player.go

Run player

.. code:: bash

  wall_player <file_left> <file_right> <file_center>
