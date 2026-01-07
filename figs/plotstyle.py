import matplotlib


print("Setting font styles")

matplotlib.pyplot.rcParams['font.family'] = 'serif'
matplotlib.pyplot.rcParams['font.size'] = 14
matplotlib.pyplot.rcParams['mathtext.fontset'] = 'dejavuserif'
matplotlib.pyplot.rcParams['mathtext.rm'] = 'serif'

#matplotlib.pyplot.rcParams['text.usetex'] = True



# Specify the list of preferred serif fonts
matplotlib.pyplot.rcParams['font.serif'] = ['Dejavuserif','Palatino', 'Times New Roman', 'Times','serif']



