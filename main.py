# reference - https://github.com/beenje/tkinter-logging-text-widget

import logging
import queue
import signal
import tkinter as tk
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
from tkinter.scrolledtext import ScrolledText

import homework01

logger = logging.getLogger(__name__)


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads
    The ConsoleUi class polls this queue to display records in a ScrolledText widget
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


class ConsoleUi:
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame):
        self.frame = frame
        # Create a ScrolledText widget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=12)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        self.scrolled_text.tag_config('DEBUG', foreground='gray')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(tk.END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')

        # Auto scroll to the bottom
        self.scrolled_text.yview(tk.END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


class FormUi:
    def __init__(self, frame):
        self.frame = frame

        # Create a combo box to select the logging level
        values = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        self.level = tk.StringVar()
        ttk.Label(self.frame, text='Level:').grid(column=0, row=0, sticky=W)
        self.combobox = ttk.Combobox(
            self.frame,
            textvariable=self.level,
            width=25,
            state='readonly',
            values=values
        )
        self.combobox.current(0)
        self.combobox.grid(column=1, row=0, sticky=(W, E))
        # Create a text field to enter a message
        self.message = tk.StringVar()
        ttk.Label(self.frame, text='Message:').grid(column=0, row=1, sticky=W)
        ttk.Entry(self.frame, textvariable=self.message, width=25).grid(column=1, row=1, sticky=(W, E))

        # Add a button to log the message
        self.button = ttk.Button(self.frame, text='Submit', command=self.submit_message)
        self.button.grid(column=1, row=2, sticky=W)

        self.button = ttk.Button(self.frame, text='Problem 01',
                                 command=lambda: self.submit_message_with_callback(homework01.problema1))
        self.button.grid(column=1, row=3, sticky=W)

        self.button = ttk.Button(self.frame, text='Problem 02',
                                 command=lambda: self.submit_message_with_callback(homework01.problema2))
        self.button.grid(column=1, row=4, sticky=W)

    def submit_message(self):
        # Get the logging level numeric value
        lvl = getattr(logging, self.level.get())
        logger.log(lvl, self.message.get())

    def submit_message_with_callback(self, callback):
        # Get the logging level numeric value
        lvl = getattr(logging, self.level.get())
        result = callback()
        logger.log(lvl, '{}'.format(result))


class ThirdUi:

    def __init__(self, frame):
        self.frame = frame
        ttk.Label(self.frame, text='This is just an example of a third frame').grid(column=0, row=1, sticky=W)
        ttk.Label(self.frame, text='With another line here!').grid(column=0, row=4, sticky=W)


class App:

    def __init__(self, root):
        self.root = root
        root.title('Logging Handler')
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create the panes and frames
        vertical_pane = ttk.PanedWindow(self.root, orient=VERTICAL)
        vertical_pane.grid(row=0, column=0, sticky="nsew")
        horizontal_pane = ttk.PanedWindow(vertical_pane, orient=HORIZONTAL)
        vertical_pane.add(horizontal_pane)
        form_frame = ttk.Labelframe(horizontal_pane, text="Problems")
        form_frame.columnconfigure(1, weight=1)
        horizontal_pane.add(form_frame, weight=1)
        console_frame = ttk.Labelframe(horizontal_pane, text="Output")
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        horizontal_pane.add(console_frame, weight=1)
        third_frame = ttk.Labelframe(vertical_pane, text="Third Frame")
        vertical_pane.add(third_frame, weight=1)

        # Initialize all frames
        self.form = FormUi(form_frame)
        self.console = ConsoleUi(console_frame)
        self.third = ThirdUi(third_frame)
        self.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.root.bind('<Control-q>', self.quit)
        signal.signal(signal.SIGINT, self.quit)

    def quit(self, *args):
        self.root.destroy()


def main():
    logging.basicConfig(level=logging.DEBUG)
    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
