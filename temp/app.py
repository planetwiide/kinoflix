# kinoflix - v1.0.1
# Author: Planetwide
# Description:
# This script sets up a Flask-based web application named "kinoflix" for 
# watching, storing, and streaming video files. it features a clean html ui along with yml user database.

# Import required modules
from flask import Flask, request, send_file, redirect, url_for, session, send_from_directory, Response, render_template
from pystyle import Colorate, Colors, System, Center, Write, Anime
from webbrowser import open_new as open_browser
from socket import gethostname, gethostbyname
import os
import yaml
import bcrypt
import secrets
from os import listdir, chdir
from os.path import isfile as file_exists


# ASCII banner for kinoflix
kinoflix_banner = """
 _    _             
| | _(_)_ __   ___  
| |/ / | '_ \ / _ \ 
|   <| | | | | (_) |
|_|\_\_|_| |_|\___/ 

 / _| (_)_  __      
| |_| | \ \/ /      
|  _| | |>  <       
|_| |_|_/_/\_\ 
"""

# ASCII banner with image
banner_image = '''

⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣴⣶⣶⣶⣶⣦⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⠏⠁⠀⢶⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀
⠀⠀⢀⣾⣿⣿⣿⣿⣿⣿⡿⠿⣿⠀⠀⠀⠀⣿⠿⢿⣿⣿⣿⣿⣿⣿⣷⡀⠀⠀
⠀⢠⣾⣿⣿⣿⣿⣿⡿⠋⣠⣴⣿⣷⣤⣤⣾⣿⣦⣄⠙⢿⣿⣿⣿⣿⣿⣷⡄⠀
⠀⣼⣿⣿⣿⣿⣿⡏⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⢹⣿⣿⣿⣿⣿⣧⠀
⢰⣿⣿⣿⣿⣿⡿⠀⣾⣿⣿⣿⣿⠟⠉⠉⠻⣿⣿⣿⣿⣷⠀⢿⣿⣿⣿⣿⣿⡆
⢸⣿⣿⣿⣿⣿⣇⣰⣿⣿⣿⣿⡇⠀⠀⠀⠀⢸⣿⣿⣿⣿⣆⣸⣿⣿⣿⣿⣿⡇
⠸⣿⣿⣿⡿⣿⠟⠋⠙⠻⣿⣿⣿⣦⣀⣀⣴⣿⣿⣿⣿⠛⠙⠻⣿⣿⣿⣿⣿⠇
⠀⢻⣿⣿⣧⠉⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠈⣿⣿⣿⡟⠀
⠀⠘⢿⣿⣿⣷⣦⣤⣴⣾⠛⠻⢿⣿⣿⣿⣿⡿⠟⠋⣿⣦⣤⠀⣰⣿⣿⡿⠃⠀
⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣄⣈⣁⣠⣤⣶⣾⣿⣿⣷⣾⣿⣿⡿⠁⠀⠀
⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠋⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠛⠻⠿⠿⠿⠿⠟⠛⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀

'''

# Flask application initialization
app = Flask("kinoflix", static_url_path='/static', static_folder='img', template_folder='web')
app.secret_key = secrets.token_urlsafe(16)

# Function to read the content of a file and return it
def read_file_contents(filename: str):
    """Read the contents of a file and return it as a string."""
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()



# Function to hash passwords using SHA-256
def hash_password(password):
    """Hashes a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Function to load users
def load_users(filename='users.yml'):
    """Loads users from the YAML file and hashes passwords if needed."""
    with open(filename, 'r') as file:
        users = yaml.safe_load(file)

    for user in users['users']:
        if user['password'] and not user.get('hashed_password'):
            user['hashed_password'] = hash_password(user['password'])

    with open(filename, 'w') as file:
        yaml.dump(users, file, default_flow_style=False)

    return users['users']


# Function for authenticating a user by checking username and password in users.yml
def auth(username, pwd):
    """Authenticate a user by verifying credentials in users.yml."""
    with open('users.yml', 'r') as file:
        users = yaml.safe_load(file)
    
    for user in users['users']:
        if user['username'] == username and bcrypt.checkpw(pwd.encode('utf-8'), user['hashed_password'].encode('utf-8')):
            print("Authenticated:", username)
            return True
            
    print("Failed to Authenticate:", username)
    return False


# Route for login page and authentication handling
@app.route('/login', methods=['GET', 'POST'])
def login_route():
    """Handle user login and authentication."""
    next_url = request.args.get('next', '/')  # Set default next URL to root
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # If user is authenticated, store the session and redirect to next URL
        if auth(username, password):
            session['authenticated'] = True
            session.modified = True  # Mark session as changed
            return redirect(next_url)
        
        # Redirect back to the login page if authentication fails
        return redirect(url_for('login_route'))
    
    # Display the login HTML page
    return read_file_contents('web/login.html')

# Main index route
@app.route('/', methods=['GET'])
def index_route():
    """Serve the index page if the user is authenticated."""
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('login_route'))
    
    # Get a list of movie info YAML files
    media_infos = [f for f in listdir('media_infos') if f.endswith('.yml')]
    
    # Create a list to store the movie info dictionaries
    movies = []
    
    # Read the movie info from each YAML file and add it to the list
    for movie_info in media_infos:
        with open(f'media_infos/{movie_info}', 'r', encoding='utf-8') as file:
            movie = yaml.safe_load(file)
            movie['filename'] = movie_info.split('.')[0]  # Add the filename to the movie info dictionary
            
            # Check if a cover image exists for the movie
            cover_image = f'{movie["name"]}.png'
            if os.path.exists(f'media_infos/{cover_image}'):
                movie['cover_image'] = f'/static/media_infos/{cover_image}'
            else:
                movie['cover_image'] = '/static/img/kinoflix.png'  # Use a default cover image if none exists
            
            # Check if a movie file exists for the movie
            movie_file = f'{movie["filename"]}.mp4'
            if not os.path.exists(f'media/{movie_file}'):
                movie_file = f'{movie["filename"]}.mkv'
                if not os.path.exists(f'media/{movie_file}'):
                    movie_file = f'{movie["filename"]}.avi'
                    if not os.path.exists(f'media/{movie_file}'):
                        movie_file = None
            
            movie['movie_file'] = movie_file
            
            movies.append(movie)
    
    # Read the dashboard HTML file and replace the placeholder with the movie cards
    dashboard_html = read_file_contents('web/dashboard.html')
    movie_cards = ''
    
    # Create the HTML code for each movie card
    for movie in movies:
        if movie['movie_file']:
            movie_cards += '''
                <div class="card">
                    <div class="card-header" style="background-image: url('{}');">
                    <h2 class="card-title">{}</h2>
                    </div>
                    <div class="card-body">
                    <p class="sub-text">{} • {}</p>
                    <h4 class="mt-0 mb-1">Description</h4>
                    <p class="description">
                        {}
                    </p>
                    </div>
                    <a class="card-link-footer" href="/player/{}">Watch movie</a>
                </div>
            '''.format(movie['cover_image'], movie['name'], movie['category'], movie['year'], movie['description'], movie['filename'])
    
    # Replace the placeholder with the movie cards
    dashboard_html = dashboard_html.replace('{{ movie_cards }}', movie_cards)
    
    return dashboard_html
@app.route('/player/<filename>')
def player(filename):
    return render_template('player.html', filename='/get/' + filename)

@app.route('/static/media_infos/<image>')
def serve_media_infos_image(image):
    return send_from_directory('media_infos', image)

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_handler():
    """Handle file uploads from the user."""
    try:
        filename = request.args.get('filename', '').strip()
        if not filename:
            return response_with_status('error, invalid filename provided.')
        
        uploaded_file = request.files.get('file')
        if uploaded_file:
            uploaded_file.save(f'media/{filename}')
            return redirect('/')
        
        return response_with_status('error, no file uploaded.')
        
    except Exception as error:
        return response_with_status(f'error: {str(error)}')

@app.route('/get/<filename>', methods=['GET'])
def file_retrieval_route(filename):
    """Retrieve a file by its filename, or return a default image if not found."""
    file_path = f'media/{filename}'
    
    if file_exists(file_path):
        return send_file(file_path, as_attachment=True)
    
    # Attempt to match filename without extension
    for file in listdir('media'):
        if filename == ''.join(file.split('.')[:-1]):
            return send_file(f'media/{file}', as_attachment=True)
    
    # Attempt to match filename with different extensions
    for extension in ['.mp4', '.mkv', '.avi']:
        file_path = f'media/{filename}{extension}'
        if file_exists(file_path):
            return send_file(file_path, as_attachment=True)
    
    return send_file('img/kinoflix.png', as_attachment=True)

# Route to retrieve images from the static/img folder
@app.route('/images/<image>', methods=['GET'])
def image_retrieval_route(image):
    """Retrieve images from the img folder."""
    return send_from_directory('img', image)

# Function to return a response with a status code
def response_with_status(text: str, status_code: int = 200) -> tuple:
    """Return a response text with a specified status code."""
    print(f"Response: {text} | Status Code: {status_code}")
    return text, status_code

# System configuration with Pystyle
System.Clear()
System.Size(160, 50)
System.Title("⛩️ kinoflix ⛩️")
login = os.getlogin()

# Function to display the UI
def display_ui():
    """Display the kinoflix user interface."""
    System.Clear()
    print("\n" * 2)
    print(Colorate.Diagonal(Colors.blue_to_cyan, Center.XCenter(kinoflix_banner)))
    print(" ")
    print(Colorate.Diagonal(Colors.blue_to_cyan, Center.XCenter("v1.0.1 - github.com/planetwiide/kinoflix")))
    print("\n" * 5)

# Banner animation display
Anime.Fade(Center.Center(banner_image), Colors.blue_to_cyan,
           Colorate.Diagonal, enter=True)

# Start the Flask application
def start_flask_app(host: str, port: int):
    """Start the Flask application on the specified host and port."""
    return app.run(host, port)

# Main function to initialize the server
def main():
    """Main function to initialize and run the kinoflix server."""
    display_ui()

    users = load_users()
    # Retrieve hostname and local IP address
    hostname, local_ip = gethostname(), gethostbyname(gethostname())
    print(" ")

    # Get user input for IP address and port, with default values
    host = Write.Input(login + " ┃ input IP address (0.0.0.0 for all devices, press enter to automate): ",
                       Colors.blue_to_cyan, interval=0.000001) or local_ip
    print(" ")
    port = Write.Input(login + " ┃ input port (press enter to automate 8080): ",
                       Colors.blue_to_cyan, interval=0.000001) or "8080"
    
    try:
        port = int(port)
    except ValueError:
        Colorate.Error(login + " ┃ invalid port; port should be an integer.")
        return

    print(" ")
    Write.Input(login + " ┃ press enter to run the server ", Colors.blue_to_cyan, interval=0.000001)

    # Generate the URL and start the Flask server
    url = f"http://{host}:{port}/"
    
    display_ui()
    print(Colorate.Vertical(Colors.blue_to_cyan, f"{login} ┃ running on: {url}"))
    print(Colors.green, end='')

    start_flask_app(host=host, port=port)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '').lower()

    # Load movie data directly into the card generation function
    def generate_movie_cards():
        cards = ''
        for filename in os.listdir('media_infos'):
            if filename.endswith('.yml'):
                with open(os.path.join('media_infos', filename), 'r', encoding='utf-8') as file:
                    movie_info = yaml.safe_load(file)
                    movie_name = movie_info['name'].lower()
                    movie_category = movie_info['category'].lower()
                    movie_year = str(movie_info['year'])

                    # Check if the query is in the movie name, genre, or year
                    if query in movie_name or query in movie_category or query in movie_year:
                        cover_image = f'{movie_info["name"]}.png'
                        if not os.path.exists(f'media_infos/{cover_image}'):
                            cover_image = 'img/kinoflix.png'  # Default cover image

                        movie_file = movie_info.get('filename', '').replace(" ", "_")

                        # Generate the movie card HTML using the same layout as the dashboard
                        cards += f'''
                        <div class="card">
                            <div class="card-header" style="background-image: url('/static/media_infos/{cover_image}');">
                                <h2 class="card-title">{movie_info["name"]}</h2>
                            </div>
                            <div class="card-body">
                                <p class="sub-text">{movie_info["category"]} • {movie_info["year"]}</p>
                                <h4 class="mt-0 mb-1">Description</h4>
                                <p class="description">{movie_info["description"]}</p>
                            </div>
                            <a class="card-link-footer" href="/player/{movie_info["name"]}">Watch movie</a>
                        </div>
                        '''
        return cards

    return render_template('search.html', movie_cards=generate_movie_cards())

# Entry point to run the application
if __name__ == '__main__':
    while True:
        main()
