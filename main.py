import math
import tkinter as tk
import matplotlib.pyplot as plt
import re


class Event:
    probability=0
    name=""
    """
        A class representing an event.

        Args:
            probability (float): event's probability
            name (str): event's name
     """

    def __init__(self, probability: str, name: str):
        try:
            self.probability = float(probability)
            if self.probability > 1:
                self.probability = 1
            self.name = name
            print("new event:", self.probability, self.name)
        except Exception as a:
            print("Probability wasn't a number")
            print(a)

    def __str__(self):
        return self.name


def callback_probability(inp: str):
    """
    Checks if a string is feasible to be a probability
    @param inp: String to check
    @return: Boolean feasibility of being a probability
    """
    if re.fullmatch("0\.?\d*", inp):
        return True
    elif re.fullmatch("1", inp):
        return True
    elif inp == "":
        return True
    else:
        return False


def callback_tries(inp: str):
    """
    Checks if a string is feasible to be a number of tries
    @param inp: String to check
    @return: Boolean feasibility of being a number of tries
    """
    if inp.isdigit():
        return True
    elif inp == "":
        return True
    else:
        return False


class Calculator:
    events = []
    """
    A class representing a calculator
    @param events: list of all events
    """

    def __init__(self):
        """
        Constructor which creates all widgets for UI, places them on a grid and reads updates events saved in file
        """
        self.window = tk.Tk()

        self.read_events_from_file()

        self.probability_var = tk.StringVar()
        self.name_var = tk.StringVar()
        tk.Label(self.window, text="Probability:").grid(row=0, column=0)

        e_p = tk.Entry(self.window, textvariable=self.probability_var)
        e_p.grid(row=0, column=1)
        reg = self.window.register(callback_probability)
        e_p.config(validate="key", validatecommand=(reg, '%P'))

        tk.Label(self.window, text="Name").grid(row=1, column=0)
        tk.Entry(self.window, textvariable=self.name_var).grid(row=1, column=1)
        tk.Button(self.window, text="Add event",
                  command=lambda: self.add_event(self.probability_var.get(),
                                                 self.name_var.get())).grid(row=2, column=1)

        self.first_event_str = tk.StringVar(self.window)
        self.first_event = self.events[0]
        self.first_event_str.set(self.first_event)
        self.first_option_menu = tk.OptionMenu(self.window, self.first_event_str, *self.events)

        self.second_event_str = tk.StringVar(self.window)
        self.second_event = self.events[0]
        self.second_event_str.set(self.second_event)
        self.second_option_menu = tk.OptionMenu(self.window, self.second_event_str, *self.events)

        tk.Label(self.window, text="First event").grid(row=0, column=2)
        tk.Label(self.window, text="Second event").grid(row=0, column=3)

        self.probability_calculation_result_label = tk.Label(self.window, text="Result")
        tk.Button(self.window, text="And", command=lambda: self.display_and_probability()).grid(row=2, column=2)
        tk.Button(self.window, text="Or", command=lambda: self.display_or_probability()).grid(row=2, column=3)
        tk.Button(self.window, text="Xor", command=lambda: self.display_xor_probability()).grid(row=3, column=2)
        tk.Button(self.window, text="If not", command=lambda: self.display_if_not_probability()).grid(row=3, column=3)

        self.regenerate_lists()

        self.probability_calculation_result_label.grid(row=4, column=3)

        self.number_of_tries_var = tk.StringVar(value="0")
        tk.Label(self.window, text="Plots are for first event. Tries:").grid(row=4, column=0)
        e = tk.Entry(self.window, textvariable=self.number_of_tries_var)
        e.grid(row=4, column=1)
        reg = self.window.register(callback_tries)
        e.config(validate="key", validatecommand=(reg, '%P'))

        tk.Button(self.window, text="Plot chance of not happening",
                  command=lambda: self.graph_of_first_not_happening()).grid(row=5, column=0)
        tk.Button(self.window, text="Plot probability density function",
                  command=lambda: self.graph_probability()).grid(row=5, column=1)
        tk.Button(self.window, text="Plot cumulative distribution function",
                  command=lambda: self.graph_cumulative_distribution()).grid(row=6, column=0)

        self.window.mainloop()

    def read_events_from_file(self) -> None:
        """
        Method used for updating events from the file
        @return: None
        """
        with open("events.txt") as f:
            for line in f:
                line = line.strip()
                line = line.split(";")
                if len(line) == 2:
                    self.events.append(Event(line[0], line[1]))

    def update_events(self) -> None:
        """
        Method used to update attributes related to currently chosen events
        @return: None
        """
        for event in self.events:
            if self.first_event_str.get() == event.name:
                self.first_event = event
            if self.second_event_str.get() == event.name:
                self.second_event = event

    def regenerate_lists(self) -> None:
        """
        Method used to keep lists widgets with possible events up to date
        @return: None
        """

        self.first_option_menu.grid_remove()
        self.second_option_menu.grid_remove()

        self.first_event_str = tk.StringVar(self.window)
        self.first_event = self.events[0]
        self.first_event_str.set(self.first_event)
        self.first_option_menu = tk.OptionMenu(self.window, self.first_event_str, *self.events)

        self.second_event_str = tk.StringVar(self.window)
        self.second_event = self.events[0]
        self.second_event_str.set(self.second_event)
        self.second_option_menu = tk.OptionMenu(self.window, self.second_event_str, *self.events)

        self.first_option_menu.grid(row=1, column=2)
        self.second_option_menu.grid(row=1, column=3)

    def add_event(self, probability: str, name: str) -> None:
        """
        Method used for a button. Invokes methods used for adding an event.
        @param probability: Probability of the event to add
        @param name: Name of the event to add
        @return: None
        """
        tmp = Event(probability, name)
        self.events.append(tmp)
        self.regenerate_lists()

    def calculate_and_probability(self) -> float:
        """
        Calculates probability of currently chosen events.
        @return: (float) Probability of both of independent events occurring
        """
        self.update_events()
        return self.first_event.probability * self.second_event.probability

    def display_and_probability(self) -> None:
        """
        Method used for a button. Updates widget with probability of currently chosen events.
        @return: None
        """
        self.update_events()
        self.probability_calculation_result_label.config(text=self.calculate_and_probability())

    def display_or_probability(self) -> None:
        """
        Method used for a button. Updates widget with probability of currently chosen events.
        @return: None
        """
        self.update_events()
        self.probability_calculation_result_label.config(
            text=self.first_event.probability + self.second_event.probability - self.calculate_and_probability())

    def display_xor_probability(self) -> None:
        """
        Method used for a button. Updates widget with probability of currently chosen events.
        @return: None
        """
        self.update_events()
        self.probability_calculation_result_label.config(
            text=self.first_event.probability + self.second_event.probability - 2 * self.calculate_and_probability())

    def display_if_not_probability(self) -> None:
        """
        Method used for a button. Updates widget with probability of currently chosen events.
        @return: None
        """
        self.update_events()
        self.probability_calculation_result_label.config(
            text=self.first_event.probability * (1 - self.second_event.probability))

    def graph_of_first_not_happening(self) -> None:
        """
        Method used for a button. Displays a graph.
        @return: None
        """
        self.update_events()
        x_arr = [1]
        y_arr = [1 - self.first_event.probability]

        for i in range(2, int(self.number_of_tries_var.get()) + 1):
            x_arr.append(i)
            y_arr.append((1 - self.first_event.probability) * y_arr[-1])

        plt.plot(x_arr, y_arr)
        plt.show()

    def graph_probability(self) -> None:
        """
        Method used for a button. Displays a graph
        @return: None
        """

        self.update_events()

        n = int(self.number_of_tries_var.get())
        p = self.first_event.probability

        def calc(k):
            return math.comb(n, k) * (p ** k) * (1 - p) ** (n - k)

        x_arr = []
        y_arr = []

        for i in range(n + 1):
            x_arr.append(i)
            y_arr.append(calc(i))

        plt.plot(x_arr, y_arr)
        plt.show()

    def graph_cumulative_distribution(self) -> None:
        """
        Method used for a button. Displays a graph
        @return: None
        """
        self.update_events()

        n = int(self.number_of_tries_var.get())
        p = self.first_event.probability

        def calc(k):
            return math.comb(n, k) * (p ** k) * (1 - p) ** (n - k)

        x_arr = [0]
        y_arr = [calc(0)]

        for i in range(1, n + 1):
            x_arr.append(i)
            y_arr.append(calc(i) + y_arr[-1])

        plt.plot(x_arr, y_arr)
        plt.show()


if __name__ == "__main__":
    Calculator()
