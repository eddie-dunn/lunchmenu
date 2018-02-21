# lunchmenu
Webapp for showing the lunch menus of restaurants

## Get the backend running locally

Install pipenv

    pip install --user pipenv

Make sure that ~/.local/bin is in your `$PATH`. If you use bash, you can run:

    echo 'export PATH="~/.local/bin:$PATH"' >> ~/.bashrc

Then run the following commands in the root of this project:

    pipenv install
    pipenv shell
    ./main.sh

If you want the server to be reachable from other hosts on your network replace
the last command with:

    ./main.sh -h 0.0.0.0
