# WN_LN_classifier
@author: Tibor Teske

# What this is:

This Pipeline classifies, tags and annotates Web and Light novels. It uses https://www.wlnupdates.com/  API to tag and supply each and every title with informations.
Afterwards it aggregates them and loads them into a BI dashboard, where you can then gather various information about favourit tags, genres, missing chapters etc.


# How to use this:
Unless you are an avid fan of Web or Light novels, i suggest you dont. And if you are, then great, let us continue.
Curently its still very manual and handmade for my personal usage, but you can modify it if you take your time


1) write down every WN/LN you have read in "Reading list einträge.xlsx"
2) Insert the path to your files inside the script
3) Run the script
4) now supply the generated "List of Books" with as many extra information as you want (rating, if you want to reread it etc.)
5) Now open the powerBI
6) click Data transformation
7) navigate to "Reading list_generiert.xlsx" for every tab
8) Save and Apply
9) Now you have your finished evaluation


# Future plans?

Automize it, make it a dialogue, generally use a better API for better classifying.

Example picture of the finished report, the first page:
![grafik](https://user-images.githubusercontent.com/44898627/150655885-5b157419-977c-453b-a4f8-0c586547ef5a.png)
