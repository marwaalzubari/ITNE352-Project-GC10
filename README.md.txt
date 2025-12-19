# News Service System – Client/Server Project

## Project Description
This project is a client-server application developed using Python. The system allows users to retrieve current news headlines and news sources using NewsAPI. The project focuses on basic network programming concepts such as client/server architecture, socket communication, multithreading, JSON data handling, and API usage.

The server handles multiple client connections and communicates with NewsAPI to fetch news data. The client sends requests to the server and displays the received data in an organized and user-friendly way.

## Course Information
Course Name: ITNE352 – Network Programming  
Semester: S1 2025–2026  
Instructor: Dr. Mohammed Almeer  
University: University of Bahrain  

## Group Information
Group Name: GC10  
Course Code: ITNE352  

Group Members:
- Jasmene Mohammed Mohammed – 202303420  
- Marwa Fawzi Alzubari – 202205026  

## Requirements
Python 3.x  
Internet connection  
Required libraries: socket, threading, json, requests, tkinter  

Install required library:
pip install requests

## How to Run the System
Run the server first:
python server.py

Run the client (console):
python client.py

Run the client (GUI):
python client_gui.py

## Client Menus
Main Menu:
- Search Headlines
- List of Sources
- Quit

Headlines Options:
- Search by keyword
- Search by category
- Search by country
- List all headlines

Sources Options:
- Search by category
- Search by country
- Search by language
- List all sources

Maximum results displayed: 15 items per request.

## Project Scripts
server.py: Handles client connections, communicates with NewsAPI, saves JSON files, and sends data to clients.  
client.py: Console-based client with text menus and data display.  
client_gui.py: GUI-based client using Tkinter for easier interaction.

## Additional Concept
Graphical User Interface (GUI) using Tkinter to improve usability.

## Acknowledgments
News data provided by NewsAPI.org.  
Python documentation and course materials.

## Conclusion
This project demonstrates a basic client-server system using Python. It helped us understand networking concepts, API usage, and teamwork in software development.
