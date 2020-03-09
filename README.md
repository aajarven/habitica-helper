# Helper for Running Habitica Challenges
This tool allows automating some tedious tasks that are required when running challenges and choosing their winners. Currently only picking the winner of weekly sharing challenge is supported, but more functionality might be added later.

## Installation
This helper is written using Python, so you'll need to ensure it is installed to begin with (see https://www.python.org/). You'll also need `pip`, but that's likely installed along with python. If it isn't, see e.g. https://pip.pypa.io/en/stable/installing/.

First, download the contents of this repository. Then navigate on command line to the directory you downloaded it into, and install the required packages:
```
pip install -r requirements.txt
```

Then you'll need to create a configuration file with your user ID and API key. The easiest way to do this is to copy the file `conf/secrets_template.py` to `conf/secrets.py`, and then use your favourite text editor to replace `yourUID` and `yourToken` with ones from your Habitica settings page. Never reveal that `secrets.py` file to anyone else.

Now you are ready to use the helper tool. These steps need to be done only once.

## Usage
Now you can invoke the helper tool using command line. The command
```
python hhelper.py
```
shows you help for different functionalities this helper tool has. For checking the winner of the newest Sharing Weekend challenge for our party, you can use
```
python hhelper.py sharing-winners
```
