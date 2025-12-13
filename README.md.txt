# News Service System – Client/Server Project

## Project Description

This project is a Python-based client–server news service system that allows users to retrieve current news headlines and news sources using real-time data from **NewsAPI.org**. The system follows a client/server architecture where the server handles API communication, data processing, and multi-client management, while the client provides an interactive, menu-driven interface for user interaction.

The server connects to NewsAPI.org to fetch up-to-date news data, processes client requests, limits results for clarity, and sends structured responses back to connected clients. It supports multiple simultaneous client connections using multithreading and logs all client requests on the server side. For evaluation and testing purposes, full API responses are saved locally in JSON files.

The client allows users to search news headlines by keyword, category, or country, list all available headlines, browse news sources by category, country, or language, and request detailed information for selected items. This project demonstrates core concepts in network programming, including socket communication, API integration, JSON handling, multithreading, and file management.

---

## Semester

**ITNE352: Network Programming**
Semester 1, Academic Year 2025–2026

---

## Group Information

**Group Name:** GC10
**Course Code:** ITNE352
**Section:** X

**Group Members:**

* Marwa Fawzi Alzubari – 202205026
* Jasmine – 2023

---

## Table of Contents

1. Project Description
2. Semester
3. Group Information
4. Requirements
5. How to Run the Project
6. The Scripts
7. Additional Concepts
8. Acknowledgments
9. Conclusion

---

## Requirements

To run this project locally, the following requirements must be met:

* Python 3.8 or later
* Internet connection (required for accessing NewsAPI.org)
* A valid NewsAPI API key

### Required Python Libraries

The following Python libraries are used in this project:

* `socket` (built-in)
* `threading` (built-in)
* `requests`
* `json` (built-in)
* `datetime` (built-in)

You can install the required external library using:

```bash
pip install requests
```

---

## How to Run the Project

1. Ensure Python is installed on your system.
2. Obtain an API key from **[https://newsapi.org](https://newsapi.org)**.
3. Open the server script and replace the `API_KEY` value with your own NewsAPI key.
4. Run the server script first:

```bash
python server.py
```

5. Run the client script in a separate terminal:

```bash
python client.py
```

6. Enter a client name when prompted.
7. Use the interactive menus to navigate between headlines, sources, and detailed views.
8. The client remains connected until the user selects the **Quit** option.

---

## The Scripts

### Server Script (`server.py`)

The server script is responsible for:

* Accepting TCP client connections
* Handling multiple clients simultaneously using threads
* Receiving client requests and menu selections
* Connecting to NewsAPI endpoints based on client options
* Limiting results to a maximum of 15 items per request
* Sending brief lists and detailed information to clients
* Logging all requests on the server screen
* Saving full API responses as JSON files using the format:
  `<client_name>_<option>_<group_ID>.json`

Key functionalities include searching headlines by keyword, category, or country, listing all headlines, browsing sources, and returning detailed information for selected items.

### Client Script (`client.py`)

The client script:

* Connects to the server via TCP sockets
* Sends the client name upon connection
* Displays structured, menu-driven options to the user
* Sends user selections and parameters to the server
* Receives and displays brief lists and detailed responses
* Allows navigation between menus until quitting

The client is designed to be user-friendly, ensuring that information is displayed clearly and in an organized manner.

---

## Additional Concepts

This project applies several important concepts beyond basic socket communication:

* **Multithreading:** Each client connection is handled in a separate thread, allowing the server to manage multiple clients concurrently.
* **API Integration:** Real-time data is retrieved from NewsAPI.org using HTTP requests.
* **JSON File Management:** API responses are saved locally for testing, evaluation, and verification.
* **Structured Client–Server Protocol:** Clearly defined message exchanges ensure reliable communication between the client and server.

---

## Acknowledgments

We would like to thank **Dr. Mohammed Almeer** for his guidance and support throughout this project, as well as the University of Bahrain for providing the learning environment and resources necessary to complete this work.

---

## Conclusion

The News Service System successfully demonstrates the implementation of a Python-based client–server application that integrates networking, APIs, and multithreading. Through this project, we gained hands-on experience in designing network protocols, managing concurrent client connections, and working with real-time data sources. The system meets the project requirements and provides a solid foundation for further enhancements such as improved error handling, security features, or a graphical user interface.


