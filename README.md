# Orange Chat

Finally, a custom chatting application that doesn't suck, built by a person that loves :tangerine:oranges.

# Installation

:warning: Orange Chat is currently work in progress. Once it's finished it will deployed on the website ```orangechat.tech```. There may be bugs or security vulernabilities in the program running it on your computer. Orange is not liable for any damage commited to your computer if there are any issues during installation.

### Prerequisites:

* Python 3.8 or higher installed(tested and developed using Python 3.11.2)
* A Mac, Windows, or Linux system
* Admin access on your system

If you don't have python installed, you can install it from their official website [here](https://python.org), or use other alternatives such as [anaconda](https://www.anaconda.com/products/distribution), [homebrew](https://formulae.brew.sh/formula/python@3.11), e.t.c. However, we recommend installing it directly from python's official website as it reduces a lot of complications.

## Step 1
Clone the repository in your local system. You can do so using the following command line code or just click the green button and then click 'Download ZIP':

If you want to run the command line code, go to your terminal(mac/linux) or command prompt(windows) and copy/paste the following code:
```bash
git clone https://github.com/rrcoder0167/Orange-Chat
```

## Step 2
Now, unzip the folder(if you downloaded it using github.com, if you used command line you don't need to do anything). Then, go to your terminal/command prompt and type in `cd` followed by a space. After that, drag the folder that says 'Orange-Chat' from your downloads in your file explorer(windows)/finder(mac) and drop it into your terminal. Then, click enter.

The end result will probably look something like this:
```bash
cd /path/to/folder/Orange-Chat
```

## Step 3

Create a virtual environment for python by running this line in your terminal:
```bash
python3 -m pip install venv
```
Then, activate the virtual environment(or venv for short) by running(MacOS and Linux) 
```bash
source .venv/bin/activate
```
or for Windows do
```bash
.venv\bin\activate
```

## Step 4

Now that the virtual environment is activated, install the requirements by doing `pip install -r requirements.txt` or if that doesn't work, run `pip3 install -r requirements.txt`

## Step 5
After that, set the environment variables by running the following code. These are just temperorary and get removed after restarting or shutting down your computer:

To set the `MONGO_URI` variable, for MacOS or Linux run:
```bash
export MONGO_URI=mongodb+srv://rrcoder0167:1F4iy9NBl7LJjcUs@orange-chat.xb2revk.mongodb.net/chat_db
```
For Windows, you can do 
```bash
set MONGO_URI=mongodb+srv://rrcoder0167:1F4iy9NBl7LJjcUs@orange-chat.xb2revk.mongodb.net/chat_db
```

Lastly, set the `SECRET_KEY` environment variable for the flask authentication cookies. You can do any value you want although we recommend a secure string like this `36024aafe2dbe4b763921f96244aa393`. You can also generate a random secure password from here. To set the SECRET KEY, for Mac/Linux do 
```bash
export SECRET_KEY=put_your_random_string_here
``` 
or for windows do 
```bash
set SECRET_KEY=put_your_random_string_here
```

## Step 6

That's it! You're all done! Now, just run `flask run` in your terminal. When you type that in, you should get something like this in your terminal:
```bash
  * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
  * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

The last thing you have to do is go to your web browser and type in the link `http://127.0.0.1:5000` or whatever url shows up when you run `flask run`. You should see the current progress of the Orange Chat application. At times, it may not work if there is a certain error that I'm trying to fix on my local copy, not commited to github. If there are any issues or features you would like to suggest, add a bug or issue in this github repo.

# Current Development Progress

- [x] Starting the Project and Creating the initial landing page
- [x] Creating the Login/Signup Page
- [x] Adding the User basic html and css template
- [x] Adding accept/decline/cancel friend requests feature
- [x] Adding Friends to program
- [x] Converting from SQL Alchemy to MongoDB
- [x] Creating new UI Profile Button
- [ ] Creating the Landing Page
- [ ] Creating the new Chatting UI(Home Button, Status, Conversations, About, e.t.c]


What I'm working on now: Working on the New UI for the application


# About the Project

Project started on Jan. 10, 2023

Hey there! I'm Riddhiman, the sole developer of Orange Chat. I created Orange Chat to be an open-source alternative application to google chat/discord with fun perks and all the features that I felt other alternatives lacked on. Some of these features include, lack of support for my favorite fruit, fun easter eggs and perks, and something that I feel I can own, to create something that felt customized for me, my friends, and everyone that uses it.

If you want to collaborate or reach out to me for anything, you can dm me on discord here:

[![Discord Presence](https://lanyard.cnrad.dev/api/870936028108705803)](https://discord.com/users/870936028108705803)

or on my google chat which is [riddhiman.rana@gmail.com](mailto:riddhiman.rana@gmail.com)

You can also join my discord server [here](https://discord.gg/NFsWcXfz).

Thanks for checking this project out!

# Credits

* Aarnav Anand: Orange company name creator
* Shankara Mohan: UI Design Ideas
* Abhinav Venkat: Minor Development Help
* Toshit Chawda: Minor Development Help
* My friends: Support during project creation