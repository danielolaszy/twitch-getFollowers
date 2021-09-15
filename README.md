<!-- ABOUT THE PROJECT -->

## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/danielolaszy/twitch-getFollowers)

This project allows the user to input a list of channels into a `channels.csv` file and get all the users that follow the channels in the file.

## Getting Started

In order to get started with the code you'll need to have Python 3.9.6+. To get the project running locally, follow these simple steps.

### Prerequisites

- Python
- API credentials from [dev.twitch.tv](https://dev.twitch.tv/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/danielolaszy/twitch-getFollowers.git
   ```
2. Install python packages via pip
   ```sh
   pip install python-dotenv requests
   ```
3. Enter the Client ID and Client Secret into the `.env` file
   ```JS
   CLIENT_ID=
   CLIENT_SECRET=
   ```

<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

- [Twitch API](https://dev.twitch.tv/docs/api/)
- [Requests](https://docs.python-requests.org/en/master/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[product-screenshot]: images/screenshot.png
