from editor import Editor
from curses import textpad
import curses


cup = Editor()
cup.add_buffer("blah")
cup.buffer_list()
cup.buffers["blah"].edit_buffer()
cup.test_echo()
cup.close()


