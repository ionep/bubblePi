import pygame

def playSound():
	pygame.mixer.init()
	pygame.mixer.music.load("/home/pi/Desktop/cloud/file.mp3");
	pygame.mixer.music.set_volume(1.0);
	pygame.mixer.music.play();
	
	while pygame.mixer.music.get_busy()== True:
	    pass
	
#playSound();
