# CraiglistSearchAlert
This program sends email notifications to a user when search results appear for indicated keywords.

# To Run the Program
Install the necessary python packages:
  `pip install beautifulsoup4`
  `pip install requests`
  `pip install smtplib` (not needed for mac users)

Create a virtual environment:
  `python3 -m venv env`

Start the environment:
  `source env/bin/activate`
  TIP: When finished developing, run `deactivate` to stop the virtual environment.

Run program:
  `python3 search.py keyword1 keyword2 keyword3`
  
