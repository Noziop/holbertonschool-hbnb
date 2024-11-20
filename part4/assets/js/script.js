// Fonction utilitaire pour les cookies
function getCookie(name) {
    return document.cookie.split('; ').reduce((r, v) => {
        const parts = v.split('=');
        return parts[0] === name ? decodeURIComponent(parts[1]) : r;
    }, '');
}

// Gestion de l'authentification
function handleAuth() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) {
            logoutLink.style.display = 'block';
            logoutLink.addEventListener('click', handleLogout);
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
    }
}

function handleLogout(e) {
    e.preventDefault();
    document.cookie = 'token=; Max-Age=0; path=/';
    window.location.href = 'login.html';
}

// Gestion des places
async function handlePlaces() {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    const token = getCookie('token');
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';
    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.innerHTML = `
            <h3>${place.name}</h3>
            <p>$ ${place.price_by_night} / night</p>
            <p>${place.description}</p>
            <a href="place.html?id=${place.id}">View Details</a>
        `;
        placesList.appendChild(card);
    });
}

// Gestion des détails d'une place
async function handlePlaceDetails() {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');
    if (!placeId) return;

    const token = getCookie('token');
    try {
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            const place = await response.json();
            await displayPlaceDetails(place);
            setupReviewForm(place);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// Affichage des détails d'une place
async function displayPlaceDetails(place) {
    const placeInfo = document.querySelector('.place-info');
    const token = getCookie('token');
    
    placeInfo.innerHTML = `
        <h2>${place.name}</h2>
        <p><strong>Host:</strong> You must be logged in to see this name...</p>
        <p><strong>Price per night:</strong> $${place.price_by_night}</p>
        <p><strong>Description:</strong> ${place.description}</p>
        <p><strong>Amenities:</strong> ${place.amenities ? place.amenities.join(', ') : 'None'}</p>
    `;

    // Récupérer les infos du host
    try {
        const ownerResponse = await fetch(`http://localhost:5000/api/v1/users/${place.owner_id}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (ownerResponse.ok) {
            const owner = await ownerResponse.json();
            const hostElement = placeInfo.querySelector('p:nth-child(2)');
            hostElement.innerHTML = `<strong>Host:</strong> ${owner.first_name} ${owner.last_name}`;
        }
    } catch (error) {
        console.error('Error fetching owner details:', error);
    }

    // Récupérer les reviews séparément
    try {
        const reviewsResponse = await fetch(`http://localhost:5000/api/v1/places/${place.id}/reviews`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (reviewsResponse.ok) {
            const reviews = await reviewsResponse.json();
            displayReviews(reviews);
        }
    } catch (error) {
        console.error('Error fetching reviews:', error);
        displayReviews([]); // Afficher "No reviews yet!" en cas d'erreur
    }
}

// Affichage des reviews
async function displayReviews(reviews) {
    const reviewsSection = document.getElementById('reviews');
    if (!reviewsSection) return;

    if (reviews && reviews.length > 0) {
        const token = getCookie('token');
        const reviewsWithUserNames = await Promise.all(reviews.map(async review => {
            try {
                const userResponse = await fetch(`http://localhost:5000/api/v1/users/${review.user_id}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    }
                });
                
                if (userResponse.ok) {
                    const user = await userResponse.json();
                    return {
                        ...review,
                        userName: `${user.first_name} ${user.last_name}`
                    };
                }
                return review;
            } catch (error) {
                console.error('Error fetching user details:', error);
                return review;
            }
        }));

        const reviewsHTML = reviewsWithUserNames.map(review => `
            <div class="review-card">
                <p><strong>${token ? (review.userName || review.user_id) : 'You must be logged in to see this name'}</strong></p>
                <p>${review.text}</p>
                <p><em>Created: not implemented yet, come back in a few years if it really upsets you 👻</em></p>
                <p><strong>Rating:</strong> ${'❤️'.repeat(review.rating)}</p>
            </div>
        `).join('');

        reviewsSection.innerHTML = `
            <h2>Reviews</h2>
            ${reviewsHTML}
        `;
    } else {
        reviewsSection.innerHTML = '<h2>Reviews</h2><p>No reviews yet!</p>';
    }
}

// Configuration du formulaire de review
function setupReviewForm(place) {
    const addReviewSection = document.getElementById('add-review');
    if (!addReviewSection) return;
    
    const token = getCookie('token');
    if (!token) {
        addReviewSection.style.display = 'none';
        return;
    }

    addReviewSection.style.display = 'block';
    const reviewForm = document.getElementById('review-form');
    
    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        console.log("Formulaire soumis!");
        
        const reviewText = document.getElementById('review-text').value;
        const rating = document.querySelector('input[name="rate"]:checked')?.value || 5;
        
        console.log("Review text:", reviewText);
        console.log("Rating:", rating);
        
        // Récupérer le user_id du token
        const tokenParts = token.split('.');
        const tokenPayload = JSON.parse(atob(tokenParts[1]));
        const userId = tokenPayload.sub;
        
        console.log("Token payload:", tokenPayload);
        console.log("User ID:", userId);
        console.log("Place owner ID:", place.owner_id);
        
        const reviewData = { 
            user_id: userId,
            place_id: place.id,
            text: reviewText,
            rating: parseInt(rating)
        };
        
        console.log("Review data to send:", reviewData);

        try {
            const response = await fetch(`http://localhost:5000/api/v1/reviews`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(reviewData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.log("Error response:", errorData);
                throw new Error(JSON.stringify(errorData));
            }

            alert('Review added successfully!');
            window.location.reload();
        } catch (error) {
            console.error('Error adding review:', error);
            alert('Error adding review: ' + error.message);
        }
    });
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    handleAuth();
    handlePlaces();
    handlePlaceDetails();
    
    // Gestion du formulaire de login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://localhost:5000/api/v1/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    alert('Login failed: ' + response.statusText);
                }
            } catch (error) {
                alert('Login error: ' + error.message);
            }
        });
    }
});