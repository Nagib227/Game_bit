from PIL import Image, ImageDraw, ImageFilter
from random import *


def GaussNoize(board, width, save, seed):
	im1 = Image.new("RGB", (width, width))
	draw = ImageDraw.Draw(im1)
	width = im1.size[0]
	height = im1.size[1]

	for x in range(width):
		for y in range(height):
			sr = randint(0, 255)
			draw.point((x, y), (sr, sr, sr))

	im1 = im1.filter(ImageFilter.GaussianBlur(radius=1.5))

	draw = ImageDraw.Draw(im1)
	pix = im1.load()

	for x in range(width):
		for y in range(height):
			r = pix[x, y][0]

			if r > 127:
				cell = 10
			else:
				cell = 20

			if board[x][y] == 0:
				board[x][y] = cell

			if save:
				if r > 127:
					r = 255
				else:
					r = 0

				draw.point((x, y), (r, r, r))

	if save:
		im1.save(f'E:\Лицей\Game Beat\maps\{seed}.png')

	return board

# код взят с сайта:
# https://habr.com/ru/post/647023/



