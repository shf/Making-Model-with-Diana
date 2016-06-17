from images2gif import readGif as readGif
from images2gif import writeGif as writeGif

from PIL import Image
import os

dir = os.path.dirname(__file__)+"/GeneratedModels-Modified"
#files = os.listdir(dir)
files = ["Model-em100-r8-rB14-case3"]

for i in range(len(files)):
	os.chdir(dir+"/"+files[i])
	file_names = sorted((fn for fn in os.listdir('.') if fn.endswith('.png')))
	#['animationframa.png', 'animationframb.png', 'animationframc.png', ...] "
	
	images = [Image.open(fn) for fn in file_names]
	
	print writeGif.__doc__
	# writeGif(filename, images, duration=0.1, loops=0, dither=1)
	#    Write an animated gif from the specified images.
	#    images should be a list of numpy arrays of PIL images.
	#    Numpy images of type float should have pixels between 0 and 1.
	#    Numpy images of other types are expected to have values between 0 and 255.
	
	
	#images.extend(reversed(images)) #infinit loop will go backwards and forwards.
	
	filename = files[i]+".GIF"
	writeGif(filename, images, duration=0.1)