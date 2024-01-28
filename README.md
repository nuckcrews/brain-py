# Brain - Python Library

## Setup

If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

1. Clone this repository

2. Navigate into the project directory

   ```bash
   $ cd brain-py
   ```

3. Create a new virtual environment

   ```bash
   $ virtualenv virt
   $ source virt/bin/activate
   ```

4. Install the requirements

   ```bash
   $ pip install -r requirements.txt
   ```

5. Make a copy of the example environment variables file

   ```bash
   $ cp .env.example .env
   ```

## CLI

1. Run the application

    ```bash
    $ ./cli.sh
    ```
## Server

1. Generate a secret key

   ```bash
   $ python -c 'import secrets; print(secrets.token_hex())'
   ```
   Once generated, set the `FLASK_APP_SECRET_KEY` in your `.env` as the new value.

2. Run the application

   ```bash
   $ python server.py
   ```

## Contributing

All contributions are welcome! Reach out for more information.