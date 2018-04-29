"""A simple module to give the shortest route from the starting point, passing through all the ten locations and going back to the starting point.

This module uses the Google Maps APIs to compute the shortest route.
It takes eleven values from the user, namely, the starting point and ten locations (the location can be entered as a city, a specific address, or a precise longitude latitude value).
The output is a text file, which is saved in the current working directory.
For one reason or another, it crashes when you try to give it intercontinental input.
This module currently works with Mac OS only.

MIT License

Copyright (c) 2018 Maja Gwozdz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

from tkinter import *
import json
import googlemaps
import distance_matrix
import os


gmaps = googlemaps.Client(key='AIzaSyDPvBnTO0y4tMKWrf3qtbMs27PZ6HD9vOY')


fields = 'Starting point', 'Place 1', 'Place 2', 'Place 3', 'Place 4', 'Place 5', 'Place 6', 'Place 7', 'Place 8', 'Place 9', 'Place 10'

places_list = []
distances_from_start = []
distance_from_nearest = []


file_with_results = open('results.txt', 'w')

def fetch(entries):

   global starting_point
   starting_point = entries[0][1].get()
   for entry in entries:
      field = entry[0]

      places_list.append(entry[1].get())

   del places_list[0]


def makeform(root, fields):

   entries = []
   for field in fields:
      row = Frame(root)
      lab = Label(row, width=15, text=field, anchor='w')
      ent = Entry(row)
      row.pack(side=TOP, fill=X, padx=5, pady=5)
      lab.pack(side=LEFT)
      ent.pack(side=RIGHT, expand=YES, fill=X)
      entries.append((field, ent))
   return entries


if __name__ == '__main__':
   root = Tk()
   root.title("Salesman")
   instructions = Label(root, text="This simple programme gives you the shortest route passing through the places entered. You will get the results as a text file (called 'results.txt') on your desktop. \n Enter the places (a city or a specific address), then press CALCULATE and EXIT.")
   instructions.pack()
   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: fetch(e)))
   b1 = Button(root, text='Calculate',
          command=(lambda e=ents: fetch(e)))
   b1.pack(side=LEFT, padx=5, pady=5)
   b2 = Button(root, text='Exit', command=root.quit)
   b2.pack(side=LEFT, padx=5, pady=5)

   root.mainloop()


file_with_results.write("Your starting point is: {}.\n\nThe recommended route is as follows: \n".format(starting_point))

# Using the distance_matrix module to determine the distances between the starting point and the other locations.
for place in places_list:
    result = gmaps.distance_matrix(starting_point, place)

    dist = result['rows'][0]['elements'][0]['distance']['value']

    distances_from_start.append((dist, place))


# Computing the respective distances between the locations.
while len(distances_from_start) != 0:

    closest = min(distances_from_start)

    nearest_point = closest[0]

    destination = closest[1]

    for i in distances_from_start:
        distance_from_nearest.append(int(abs(nearest_point - i[0])))

    distances_from_start.remove(closest)

    distance_from_nearest = []

    file_with_results.write("Go to {}. \n".format(destination))


file_with_results.write("\nHave a good trip!")

file_with_results.close()











