<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/SarCTutor/calendly-event-tools">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

<h2 align="center">Calendly Event Tools</h2>

  <p align="center">
    Toolset for automating interactions between Calendly, CSV event files, and SQL.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#environment-setup">Environment Setup</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a> </li>
    <li><a href="#csv-formats">CSV Formats</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<br>
<!-- ABOUT THE PROJECT -->

## About The Project

This is a script set for automating various operations involving importing events from Calendly, processing them, and uploading them to a SQL database.

### Features

* Import events from Calendly to CSV file.
* Intelligent matching of user-inputted names to unique user IDs.
* Updating SQL with session data from CSV file.
* Auto-generated SQL session info based on CSV of recurring appointments.
* Elegant menus for all operations.

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- GETTING STARTED -->
## Getting Started

As a set of Python scripts, the main thing you will need is a Python3 installation and the required prerequisite modules.  

### Prerequisites

* PyCalendly
* csv
* pandas
* python-dotenv

All libraries are available through [pip](https://pypi.org/project/pip/). 

### Installation

1. Install all listed prerequisites using `pip` (or a package manager of your choice)
   
2. Clone the repo
   ```sh
   git clone https://github.com/SarCTutor/calendly-event-tools.git
   ```

### Environment Setup

1. Create a file called `.env`
   ```sh
   touch .env
   ```
2. Get a (free) Calendly API Key ("Personal Access Token") at [https://developer.calendly.com](https://developer.calendly.com/how-to-authenticate-with-personal-access-tokens)
   
3. Enter your Calendly API key in `.env`
   ```sh
   CALENDLY_API_KEY='xxxxxxxx'
   ```
4. Find your Calendly URI using the following mini-script
   ```python
   from calendly import Calendly
   calendly = Calendly('YOUR_API_KEY')
   info = calendly.about()
   print(info['resource']['uri'])
   ```
5. Enter your Calendly URI in `.env` 
    ```sh
   CALENDLY_URI='https://api.calendly.com/users/xxxxxxx'
   ```
6. Enter your SQL Path in `.env`.  
    ```sh
    SQL_PATH='/Users/USERNAME/SQLite/Calendly.db'
    ```
    (If you don't intend to use the SQL scripts, you can skip this step.)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

By default, the program can be run by executing the file `main.py`.  This provides you with a menu to select which operations you would like to perform:
1. Retrieve from Calendly
2. Process names to IDs
3. Push new event entries to SQL
4. Generate regular appointment entries

### Retrieve from Calendly
This operation connects to Calendly and retrieves all appointment information from today's date onwards.  It is saved to `events_parsed.csv`.  

### Process names to IDs.
This operation loads the event data from `events_parsed.csv` and attempts to populate the `id` column with user IDs.  

Names are matched to IDs based on a lookup table, `id_names.csv`.

If no match is found for a user's name, a menu of possible names is shown to the user to choose from.  If there is still no match, the `id` is set to `"Unknown"`.

All data is saved back to `events_parsed.csv`.

### Push new event entries to SQL

Pushes event entries from `events_parsed.csv` to a SQL server with columns `Student_ID`, `Date_Time`, and `Length`.

Most of this logic is handled by [pandas.DataFrame.to_sql](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_sql.html).

### Generate regular appointment entries

Allows for population of SQL database with regular recurring sessions that are _not_ booked through Calendly.  Takes events from `regular_events.csv`, and a start date, and generates all appointments through that week (start date -> Sunday).

Example usage:
```ssh
[*] Generate regular appointment entries

Enter a date in YYYY-MM-DD format: 2022-03-21

Pushing events from [regular_events.csv] to SQL...

Pushed 2 recurring events to SQL database.
```
In this example, given a start date of Tuesday March 22nd, the appointments would be added on Wednesday the 23rd, and Thursday the 24th.  

<!-- CSV FILE INFO -->
## CSV Formats

### events_parsed.csv

### id_name.csv

### regular_events.csv




Example `regular_events.csv`: 
```csv
name,day,time,length
Alice,Wednesday,10:00,60
Bob,Thursday,14:30,60
```

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ROADMAP
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/SarCTutor/calendly-event-tools/issues) for a full list of proposed features (and known issues). 

<p align="right">(<a href="#top">back to top</a>)</p> -->

<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GPL-3.0 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Sar C - sarctutor@gmail.com

Project Link: [https://github.com/SarCTutor/calendly-event-tools](https://github.com/SarCTutor/calendly-event-tools)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [laxmena/PyCalendly](https://github.com/laxmena/PyCalendly)
* [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[forks-shield]: https://img.shields.io/github/forks/SarCTutor/calendly-event-tools.svg?style=for-the-badge
[forks-url]: https://github.com/SarCTutor/calendly-event-tools/network/members
[stars-shield]: https://img.shields.io/github/stars/SarCTutor/calendly-event-tools.svg?style=for-the-badge
[stars-url]: https://github.com/SarCTutor/calendly-event-tools/stargazers
[issues-shield]: https://img.shields.io/github/issues/SarCTutor/calendly-event-tools.svg?style=for-the-badge
[issues-url]: https://github.com/SarCTutor/calendly-event-tools/issues
[license-shield]: https://img.shields.io/github/license/SarCTutor/calendly-event-tools.svg?style=for-the-badge
[license-url]: https://github.com/SarCTutor/calendly-event-tools/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/sarc
[product-screenshot]: images/screenshot.png