# I dont know how to explain this lmao

from PIL import Image, ImageSequence, ImageOps
import numpy as np
from io import BytesIO

class AmongUs:
	def __init__(self, gif_width=16, gif_height=16):
		amogus_gif = Image.open("./assets/amogus.gif")
		self.amogus = []
		self.gif_width = gif_width
		self.gif_height = gif_height
		for frame in ImageSequence.Iterator(amogus_gif):
			self.amogus.append(frame.resize((self.gif_width, self.gif_height), Image.LANCZOS).convert("RGBA"))



	def convert_image(self, background):
		background = Image.open(background).convert("RGB")

		background = background.resize((512, 512), Image.LANCZOS)
		width, height = background.size

		width -= background.width % self.gif_width
		height -= background.height % self.gif_height

		amogus_horizontal_count = width // self.gif_width
		amogus_vertical_count = height // self.gif_height

		background = background.resize((amogus_horizontal_count, amogus_vertical_count), Image.LANCZOS)

		empty_image = Image.new("RGBA", size=(width, height))
		background = np.array(background)

		images = []
		frame_count = len(self.amogus)

		for i in range(frame_count):
			empty_image = Image.new("RGBA", size=(width, height))
			for y in range(len(background)):
				for x in range(len(background[0])):
					frame_offset = (y + x + i) % frame_count
					amogus_frame = self.amogus[frame_offset]
					image_offset = ((x * self.gif_width), (y * self.gif_height)) 
					alpha = amogus_frame.split()[3]
					amogus_frame = ImageOps.grayscale(self.amogus[frame_offset])
					img = ImageOps.colorize(amogus_frame, black=(0,0,0,0), white=background[y][x])
					img.putalpha(alpha)
					empty_image.paste(img, image_offset)
			images.append(empty_image)

		output_file = BytesIO()
		images[0].save(output_file, "GIF", save_all=True, append_images=images[1:], duration=50, loop=0)
		output_file.seek(0)
		return output_file

