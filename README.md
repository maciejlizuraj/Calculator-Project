# Calculator-Project
A GUI application used for calculations related to probability of independent events

# Dependencies
requires libraries:
math
tkinter
mathplotlib.pyplot
re


# How to run
```
py -m pip install mathplotlib
py -m main
```

# Key features
1. Adding new events for calculations by providing probability and name
2. Calculating And/Or/Xor/If not probabilities of two events. For example First event If not Second Event
3. Displaying a plot of chance of first event not occuring/first event probability density function/first event cumulative distribution function with custom number of tries
4. Loading events from txt file at startup


# Examples of use
1. Adding a new event:![image](https://github.com/maciejlizuraj/Calculator-Project/assets/130994353/60f5cee5-6f62-46f9-8c60-5cc098975dae)
2. Selecting events to calculate from![image](https://github.com/maciejlizuraj/Calculator-Project/assets/130994353/c08ecb1d-2084-4d09-bd06-2ac0e8fb30f7)
3. Calculating probability of If not, etc. of those 2 events![image](https://github.com/maciejlizuraj/Calculator-Project/assets/130994353/aa1bb884-9904-41d1-8e2d-dfa83042b284)
4. Getting a plot of probability of event not happening, etc. depending on number of tries![image](https://github.com/maciejlizuraj/Calculator-Project/assets/130994353/d0ac5bef-1b62-4f3a-b1b1-8c99ccdba5b9)


# Challanges faced
1. Using some of the widgets like optionbox seemed unintuitive at first. It feels quite different compared to Java.
2. Validation of inputs feels rather tricky.
3. Documenting. Some methods are almost similar like ones for calculating And probability and Or probability. Since their names are self-explainatory, I found it hard to find a good description.


# Lessons learned
Throughout implementing the calculator I learned how to use tkinter and matplotlib and got more familiar with implementing classes in python. I learned how important clarity of names is and how important it is to differenciate between widgets that will be further used and those, that aren't worth storing as a variable.
