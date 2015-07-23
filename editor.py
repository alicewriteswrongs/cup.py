import curses
from curses.textpad import Textbox, rectangle

def gather(textbox):
    """
    collect and return the contents of the window.
    modified from the gather provided by the standard library
    (cause that one doesn't work!)
    """
    result = ""
    for y in range(textbox.maxy+1):
        textbox.win.move(y, 0)
        stop = textbox._end_of_line(y)
        for x in range(textbox.maxx+1):
            if x > stop:
                break
            result = result + chr(curses.ascii.ascii(textbox.win.inch(y, x)))
        if textbox.maxy > 0:
            result = result + "\n"
    return result.strip()


class Editor():
    def __init__(self, filename=''):
        self.screen = curses.initscr()
        self.buffers = {}
        self.current_buffer = ''
        curses.cbreak()
        self.screen.keypad(1)
        curses.noecho()
        curses.start_color()
        self.screen.refresh()

    def listen(self):
        while True:
            c = self.screen.getch()
            if c == ord('q'):
                self.close()
                break
            elif c == ord('e'):
                self.switch_buffer(self.current_buffer)
            # elif c == ord('b'):
            #     //switch buffers
            else:
                print("umm some sort of error")


    def editstatus(self):
        status = curses.newwin(1, curses.COLS-1, curses.LINES - 1, 0)
        status.addstr("EDIT MODE")
        status.refresh()

    def commandstatus(self):
        status = curses.newwin(1, curses.COLS-1, curses.LINES -1, 0)
        status.addstr("COMMAND MODE")
        status.refresh()

    def buffer_list(self, active=''):
        """
        puts a list of open buffers at the top
        """
        rectangle(self.screen, 0,0, 2, curses.COLS -1)
        self.screen.refresh()
        buflist = curses.newwin(1, curses.COLS-1, 1,1)
        buflist.refresh()
        bufferlist = []
        if (active == ''):
            bufferlist = ["new file"]
        bufferlist += list(self.buffers.keys())
        buflist.addstr("buffers:" + " | ".join(bufferlist))
        buflist.refresh()

    def add_buffer(self, filename, text):
        self.buffers[filename] = Buffer(filename, text)

    def close(self):
        """
        saves current buffer
        unsets things to make curses friendly
        """
        self.buffers[self.current_buffer].save_buffer()
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

    def switch_buffer(self, target):
        """
        saves current buffer, switches to a new one
        """
        self.editstatus()
        if self.current_buffer == '':
            self.buffers[target].edit_buffer()
            self.current_buffer = target
        else:
            self.buffers[self.current_buffer].save_buffer()
            self.buffers[target].edit_buffer()
            self.current_buffer = target
        self.commandstatus()


class Buffer():
    def __init__(self, filename, text=''):
        self.filename = filename
        self.text = text

    def edit_buffer(self):
        bufscreen = curses.newwin(curses.LINES-5, curses.COLS-1, 3,0)
        bufscreen.addstr(self.text)
        textbox = Textbox(bufscreen)
        textbox.edit()
        self.text = gather(textbox)
        bufscreen.clear()

    def save_buffer(self):
        with open(self.filename, "w") as myfile:
            myfile.write(self.text)




