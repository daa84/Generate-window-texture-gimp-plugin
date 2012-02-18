#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2012  Andrey Dubravin andrey.dubravin(at)gmail.com
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


from gimpfu import *
import random

class WindowGenerator:

    def __init__(self, levels_count, level_border, windows_per_level, window_border, emit_windows_percent, black_window_color, emit_window_color):
	self.levels_count = levels_count
	self.level_border = level_border
	self.black_window_color = black_window_color
	self.emit_window_color = emit_window_color
	self.windows_per_level = windows_per_level
	self.window_border = window_border
	self.emit_windows_percent = emit_windows_percent

    def draw_level(self, image, layer, y_offset):
	for i in xrange(self.windows_per_level):
	    if random.random() > self.emit_windows_percent:
		continue

	    pdb.gimp_rect_select(image, self.level_border + i * self.window_width + i * self.window_border, y_offset, 
		    self.window_width, self.level_height - 5,
		    CHANNEL_OP_REPLACE, False, 0)

	    pdb.gimp_context_set_background(self.emit_window_color)
	    pdb.gimp_edit_fill(layer, BACKGROUND_FILL)



    def draw_windows(self, image, layer):
	extreme_border_error = self.level_border / self.levels_count
	if extreme_border_error <= 0:
	    extreme_border_error = 1
	self.level_height = layer.height / self.levels_count - self.level_border - extreme_border_error
	self.window_width = (layer.width - self.level_border * 2) / self.windows_per_level - self.window_border

	if self.level_height <= 0 or self.window_width <= 0:
	    pdb.gimp_message("Windows can be generated with given parameters")
	    return
	for i in xrange(self.levels_count):
	    self.draw_level(image, layer, i * self.level_height + i * self.level_border + self.level_border)
	pdb.gimp_selection_clear(image)

def generate_window_texture(image, levels_count, level_border, windows_per_level, window_border, emit_windows_percent, black_window_color, emit_window_color):
    pdb.gimp_context_push()
    pdb.gimp_image_undo_group_start(image)

    layer = pdb.gimp_layer_new(image, image.width, image.height, RGB, "windows", 100, NORMAL_MODE)
    pdb.gimp_image_add_layer(image, layer, 0)
    pdb.gimp_context_set_background(black_window_color)
    pdb.gimp_edit_clear(layer)
    generator = WindowGenerator(levels_count, level_border, windows_per_level, window_border, emit_windows_percent, black_window_color, emit_window_color)
    generator.draw_windows(image, layer)

    pdb.gimp_displays_flush()
    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_context_pop()

register(
	"python-fu-generate-window-texture",
	"Generate window texture",
	"Generate simple image that can be used as windows texture",
	"Dubravin Andrey",
	"Dubravin Andrey (andrey.dubravin@gmail.com)",
	"18.02.2012",
	"Generate window texture", # menu
	"RGB*", # image types
	[
	    (PF_IMAGE, "image", "Исходное изображение", None),
	    (PF_INT, "levels_count", "Building levels count", 15),
	    (PF_INT, "level_border", "Border between levels", 4),
	    (PF_INT, "windows_per_level", "Windows per level", 10),
	    (PF_INT, "window_border", "Left/right window border", 2),
	    (PF_FLOAT, "emit_windows_percent", "Amount of emit windows", 0.7),
	    (PF_COLOR, "black_window_color",  "Black window color", (100, 100, 100)),
	    (PF_COLOR, "emit_window_color",  "Window with light", (255, 219, 121))
	    ],
	[], # Return
	generate_window_texture, menu="<Image>/Generate/")

main()
