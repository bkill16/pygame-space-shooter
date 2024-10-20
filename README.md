# Overview

Astro Assault is a classic arcade-style game where the player pilots a spaceship and defends against falling asteroids. The goal is to destroy as many asteroids as possible by shooting lasers at them. The more asteroids the player destroys, the more difficult the game becomes.

The game begins with a simple menu, giving the player the option to start the game or quit. To navigate between options, use the up and down arrow keys. To select a menu option, press enter. Upon starting the game, the player is then loaded into the game state. The player can move the spaceship from left to right by using the left and right arrow keys. To fire lasers at oncoming asteroids, press space (holding the space bar doesn't fire continuous shots. The player must hit the space bar multiple times to fire multiple shots). If the player wishes to return to the main menu from the game state, press escape.

This project was created to further my understanding of game development using Python and Pygame. By working on this project, I was able to learn and improve my skills in sprite-based game mechanics, collision detection, and object-oriented programming.

[Software Demo Video](https://www.youtube.com/watch?v=dNXPHZ-8MkI)

# Development Environment

The tools used to build this project includes Visual Studio Code (IDE) and audio and visual assets for background images, sprites, menu music, laser fire, and font.

Images

- Menu Background: https://stock.adobe.com/search?k=pixel+space&asset_id=546468718
- Game Background: https://stock.adobe.com/search?k=pixel+space&asset_id=546468872
- Spaceship: https://stock.adobe.com/search?k=8+bit+spaceship&asset_id=356255763
- Asteroid: https://wallpapers.com/png/pixel-art-asteroid-space-object-ejxo47v76y24ntmc.html#google_vignette

Sounds

- Menu Music: https://www.fesliyanstudios.com/royalty-free-music/download/8-bit-retro-funk/883
- Laser Fire: Laser gun 19 - https://www.soundfishing.eu/sound/laser-gun

Font

- https://www.dafont.com/upheaval.font

Astro Assault was built with Python and Pygame. It also utilizes sys and random.

# Useful Websites

- [Pygame Tutorial for Beginners](https://www.youtube.com/watch?v=FfWpgLFMI7w)
- [Pygame Menu - Read the Docs](https://pygame-menu.readthedocs.io/en/latest/)
- [Pygame - Creating Sprites](https://www.geeksforgeeks.org/pygame-creating-sprites/)
- [ChatGPT](https://chatgpt.com/)

# Future Work

- Display the player's score on the game screen for them to see.
- Penalize players for missing asteroids.
- Refactor and modularize code. Add some sort of unit testing.
