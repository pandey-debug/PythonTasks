import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "cinebook-production-high-fidelity-key-92842")

# FastAPI Backend URL (Can be customized via environment variable)
FASTAPI_URL = os.environ.get("FASTAPI_BACKEND_URL", "http://localhost:8000")

# ─────────────────────────────────────────────────────────────────────────────
# 🏠 HOME & BROWSE
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    """Home page with available movies"""
    try:
        response = requests.get(f"{FASTAPI_URL}/movies/available/")
        if response.status_code == 200:
            movies = response.json()
        else:
            movies = []
    except Exception as e:
        print("Backend communication error in index:", e)
        movies = []
    
    return render_template('index.html', movies=movies)


@app.route('/api/search')
def search_movies():
    """Search movies by title"""
    title = request.args.get('title', '')
    if not title:
        return jsonify([])
    
    try:
        response = requests.get(f"{FASTAPI_URL}/movies/search/", params={'title': title})
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify([])
    except Exception as e:
        print("Backend search API error:", e)
        return jsonify([])


# ─────────────────────────────────────────────────────────────────────────────
# 👤 USER MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json() or {}
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        role = data.get('role', 'user').strip()
        password = data.get('password', '').strip()

        if not name or not phone or not password:
            return jsonify({'success': False, 'message': 'Name, phone and password are required'}), 400

        try:
            response = requests.post(
                f"{FASTAPI_URL}/users/",
                json={'name': name, 'phone': phone, 'role': role, 'password': password}
            )

            if response.status_code == 200:
                user = response.json()
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_role'] = user.get('role', 'user')

                redirect_url = url_for('admin_dashboard') if user['role'] == 'admin' else url_for('index')
                return jsonify({'success': True, 'message': 'Registration successful!', 'redirect': redirect_url})
            else:
                error = response.json().get('detail', 'Registration failed')
                return jsonify({'success': False, 'message': error}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json() or {}
        user_name = data.get('name', '').strip()
        password = data.get('password', '').strip()

        if not user_name or not password:
            return jsonify({'success': False, 'message': 'Username and password are required'}), 400

        try:
            response = requests.post(f"{FASTAPI_URL}/login/", json={'name': user_name, 'password': password})

            if response.status_code == 200:
                user = response.json()
                session['user_id'] = user['id']
                session['user_name'] = user['name']
                session['user_role'] = user['role']

                # Redirect based on role
                redirect_url = url_for('admin_dashboard') if user['role'] == 'admin' else url_for('index')
                return jsonify({'success': True, 'message': 'Login successful!', 'redirect': redirect_url})
            else:
                error = response.json().get('detail', 'Invalid credentials')
                return jsonify({'success': False, 'message': error}), 401
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    return render_template('login.html')


@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))


# ─────────────────────────────────────────────────────────────────────────────
# 🎬 MOVIE DETAILS
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    """Movie details page"""
    try:
        response = requests.get(f"{FASTAPI_URL}/movies/{movie_id}")
        if response.status_code == 200:
            movie = response.json()
            return render_template('movie_detail.html', movie=movie)
        else:
            return render_template('error.html', message='Movie was not found in our scheduled databases.'), 404
    except Exception as e:
        return render_template('error.html', message=str(e)), 500


# ─────────────────────────────────────────────────────────────────────────────
# 🎟️ BOOKING
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/booking/<int:movie_id>', methods=['GET', 'POST'])
def booking(movie_id):
    """Movie booking page"""
    # Check if user is logged in
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        data = request.get_json() or {}
        seats = int(data.get('seats', 1))
        
        try:
            # Get movie details first to verify availability
            movie_response = requests.get(f"{FASTAPI_URL}/movies/{movie_id}")
            if movie_response.status_code != 200:
                return jsonify({'success': False, 'message': 'Movie not found'}), 404
            
            # Create booking
            booking_data = {
                'user_id': session['user_id'],
                'movie_id': movie_id,
                'seats_booked': seats,
                'booking_date': datetime.now().strftime('%Y-%m-%d'),
                'booking_time': datetime.now().strftime('%H:%M:%S')
            }
            
            response = requests.post(f"{FASTAPI_URL}/bookings/", json=booking_data)
            
            if response.status_code == 200:
                booking_res = response.json()
                return jsonify({
                    'success': True,
                    'message': 'Booking successful!',
                    'booking_reference': booking_res['booking_reference'],
                    'booking_id': booking_res['id']
                })
            else:
                error = response.json().get('detail', 'Booking parameters invalid')
                return jsonify({'success': False, 'message': error}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
    
    # GET request - show booking page
    try:
        response = requests.get(f"{FASTAPI_URL}/movies/{movie_id}")
        if response.status_code == 200:
            movie = response.json()
            return render_template('booking.html', movie=movie)
        else:
            return render_template('error.html', message='Movie details were not found.'), 404
    except Exception as e:
        return render_template('error.html', message=str(e)), 500


@app.route('/confirmation/<booking_reference>')
def confirmation(booking_reference):
    """Booking confirmation page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        response = requests.get(f"{FASTAPI_URL}/bookings/ref/{booking_reference}")
        if response.status_code == 200:
            booking_obj = response.json()
            # Get movie details
            movie_response = requests.get(f"{FASTAPI_URL}/movies/{booking_obj['movie_id']}")
            movie = movie_response.json() if movie_response.status_code == 200 else {}
            return render_template('confirmation.html', booking=booking_obj, movie=movie)
        else:
            return render_template('error.html', message='Your booking reference voucher does not exist.'), 404
    except Exception as e:
        return render_template('error.html', message=str(e)), 500


# ─────────────────────────────────────────────────────────────────────────────
# 📋 USER BOOKINGS
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/my-bookings')
def my_bookings():
    """View user's booking history"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    try:
        response = requests.get(f"{FASTAPI_URL}/bookings/user/{session['user_id']}")
        bookings = []
        if response.status_code == 200:
            bookings = response.json()
            # Get movie details for each booking
            for b in bookings:
                movie_response = requests.get(f"{FASTAPI_URL}/movies/{b['movie_id']}")
                if movie_response.status_code == 200:
                    b['movie'] = movie_response.json()
        
        return render_template('my_bookings.html', bookings=bookings)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500


@app.route('/api/cancel-booking/<int:booking_id>', methods=['DELETE'])
def cancel_booking(booking_id):
    """Cancel a booking"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    try:
        response = requests.delete(f"{FASTAPI_URL}/bookings/{booking_id}")
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({'success': True, 'message': result.get('message', 'Booking successfully cancelled.')})
        else:
            error = response.json().get('detail', 'Cancellation rejected by ticketing server')
            return jsonify({'success': False, 'message': error}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ─────────────────────────────────────────────────────────────────────────────
# 🔧 ADMIN DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    if 'user_id' not in session or session.get('user_role') != 'admin':
        return render_template('error.html', message="Access Denied: You do not have Super Administrator privileges. Please register/login with an Administrator role to access this dashboard!"), 403

    try:
        movies = []
        bookings = []
        users = []
        
        # Get all movies
        movies_response = requests.get(f"{FASTAPI_URL}/movies/all/")
        if movies_response.status_code == 200:
            movies = movies_response.json()
        
        # Get all bookings
        bookings_response = requests.get(f"{FASTAPI_URL}/bookings/")
        if bookings_response.status_code == 200:
            bookings = bookings_response.json()
        
        # Get all users
        users_response = requests.get(f"{FASTAPI_URL}/users/")
        if users_response.status_code == 200:
            users = users_response.json()
        
        return render_template('admin.html', movies=movies, bookings=bookings, users=users)
    except Exception as e:
        return render_template('error.html', message=str(e)), 500


@app.route('/api/admin/add-movie', methods=['POST'])
def add_movie():
    """Add a new movie (admin)"""
    try:
        data = request.get_json() or {}
        
        response = requests.post(f"{FASTAPI_URL}/movies/", json=data)
        
        if response.status_code == 200:
            movie = response.json()
            return jsonify({'success': True, 'message': 'Movie added successfully!', 'movie': movie})
        else:
            error = response.json().get('detail', 'Failed to add movie show')
            return jsonify({'success': False, 'message': error}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/admin/complete-show/<int:movie_id>', methods=['PUT'])
def complete_show(movie_id):
    """Mark show as completed (admin)"""
    try:
        response = requests.put(f"{FASTAPI_URL}/movies/{movie_id}/complete")
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({'success': True, 'message': result.get('message', 'Show marked as completed.')})
        else:
            error = response.json().get('detail', 'Failed to update show state')
            return jsonify({'success': False, 'message': error}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# ─────────────────────────────────────────────────────────────────────────────
# ⚠️ ERROR HANDLERS
# ─────────────────────────────────────────────────────────────────────────────
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', message='Page or endpoint not found on the virtual cinema dashboard.'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('error.html', message='Internal dashboard handler error occurred.'), 500


if __name__ == '__main__':
    port = int(os.environ.get("FLASK_PORT", 3000))
    app.run(debug=True, host='0.0.0.0', port=port)
