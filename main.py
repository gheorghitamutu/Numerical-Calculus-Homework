# reference - https://github.com/beenje/tkinter-logging-text-widget

import logging
import queue
import threading
import tkinter as tk
from functools import partial
from tkinter import ttk, VERTICAL, HORIZONTAL, N, S, E, W
from tkinter.scrolledtext import ScrolledText

# HOMEWORK IMPORTS
import homework01
import homework02
import homework03
import homework04

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
        self.scrolled_text = ScrolledText(frame, state='disabled', height=30, width=110)
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
        self.level = 'INFO'

        ttk.Label(self.frame, text='Homework 01', width=50, anchor='center').grid(column=0, row=0)
        ttk.Separator(frame, orient=HORIZONTAL).grid(row=1, column=0, sticky="ew")

        self.button_list = list()
        for i in range(0, homework01.PROBLEMS_COUNT):
            self.button_list.append(ttk.Button(self.frame, text='Problem 0{}'.format(i + 1), width=50))
            self.button_list[-1].config(command=partial(
                self.submit_message_with_callback_threaded, homework01.get_function_by_index(i)))
            self.button_list[-1].grid(column=0, row=i + 2, sticky=E)  # offset of 2 for row index (0 - label, 1 - sep)

        ttk.Label(self.frame, text='Homework 02', width=50, anchor='center').grid(column=0, row=5)
        ttk.Separator(frame, orient=HORIZONTAL).grid(row=6, column=0, sticky="ew")
        for i in range(0, homework02.PROBLEMS_COUNT):
            self.button_list.append(ttk.Button(self.frame, text='Problem 0{}'.format(i + 1), width=50))
            self.button_list[-1].config(command=partial(
                self.submit_message_with_callback_threaded, partial(homework02.get_function_by_index(i), logger.info)))
            # offset of 2 for row index (0 - label, 1 - sep) + homework label + sep + previous homework problem count
            self.button_list[-1].grid(column=0, row=i + 2 + 1 + 1 + homework01.PROBLEMS_COUNT, sticky=E)

        ttk.Label(self.frame, text='Homework 03', width=50, anchor='center').grid(column=0, row=8)
        ttk.Separator(frame, orient=HORIZONTAL).grid(row=9, column=0, sticky="ew")
        for i in range(0, homework03.PROBLEMS_COUNT):
            self.button_list.append(ttk.Button(self.frame, text='Problem 0{}'.format(i + 1), width=50))
            self.button_list[-1].config(command=partial(
                self.submit_message_with_callback_threaded, partial(homework03.get_function_by_index(i), logger.info)))
            # offset of 2 for row index (0 - label, 1 - sep) + homework label + sep + previous homework problem count
            self.button_list[-1].grid(
                column=0, row=i + 2 + 1 + homework01.PROBLEMS_COUNT + 2 + 1 + 1 + homework02.PROBLEMS_COUNT, sticky=E)

        ttk.Label(self.frame, text='Homework 04', width=50, anchor='center').grid(column=0, row=13)
        ttk.Separator(frame, orient=HORIZONTAL).grid(row=14, column=0, sticky="ew")
        for i in range(0, homework04.PROBLEMS_COUNT):
            self.button_list.append(ttk.Button(self.frame, text='Problem 0{}'.format(i + 1), width=50))
            self.button_list[-1].config(command=partial(
                self.submit_message_with_callback_threaded, partial(homework04.get_function_by_index(i), logger.info)))
            self.button_list[-1].grid(
                column=0,
                row=i + 2 + 1 + homework01.PROBLEMS_COUNT +
                    2 + 1 + 1 + homework02.PROBLEMS_COUNT +
                    2 + 1 + 1 + homework03.PROBLEMS_COUNT,
                sticky=E)

        # ... ADD NEXT HOMEWORK AND ITS BUTTONS

    def submit_message_with_callback(self, callback):
        result = callback()

        if result is not None:
            lvl = getattr(logging, self.level)
            logger.log(lvl, '{}'.format(result))

    def submit_message_with_callback_threaded(self, callback):
        # don't block the GUI main thread while computing!
        thread = threading.Thread(target=self.submit_message_with_callback, args=(callback,))
        thread.start()
        # no need to join the thread


class App:
    def __init__(self, root):
        self.root = root
        root.title('Numeric Calculus')
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

        # Initialize all frames
        self.form = FormUi(form_frame)
        self.console = ConsoleUi(console_frame)


def main():
    logging.basicConfig(level=logging.INFO)

    root = tk.Tk()
    app = App(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
