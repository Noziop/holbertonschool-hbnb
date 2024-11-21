// Fonction utilitaire pour les cookies
function getCookie(name) {
    const value = document.cookie.split('; ').reduce((r, v) => {
        const parts = v.split('=');
        return parts[0] === name ? decodeURIComponent(parts[1]) : r;
    }, '');
    return value;
}

// Gestion de l'authentification
document.addEventListener('DOMContentLoaded', () => {
    // Login form
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        // Dans la partie login
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

    // Gestion affichage login/logout
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    if (token) {
        if (loginLink) loginLink.style.display = 'none';
        if (logoutLink) {
            logoutLink.style.display = 'block';
            logoutLink.addEventListener('click', (e) => {
                e.preventDefault();
                document.cookie = 'token=; Max-Age=0; path=/';
                window.location.href = 'login.html';
            });
        }
    } else {
        if (loginLink) loginLink.style.display = 'block';
        if (logoutLink) logoutLink.style.display = 'none';
    }

    // Fetch et affichage des places
    const placesList = document.getElementById('places-list');
    if (placesList) {
        const fetchPlaces = async () => {
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
                console.error('Error fetching places:', error);
            }
        };

        const displayPlaces = (places) => {
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
        };

        // Filtrage par prix
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                const maxPrice = event.target.value;
                const cards = document.querySelectorAll('.place-card');
                cards.forEach(card => {
                    const priceText = card.querySelector('p').textContent;
                    const price = parseInt(priceText.replace(/[^0-9]/g, ''));
                    card.style.display =
                        maxPrice === 'all' || price <= parseInt(maxPrice) ? 'block' : 'none';
                });
            });
        }

        fetchPlaces();
    }

    // Gestion des reviews
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const urlParams = new URLSearchParams(window.location.search);
            const placeId = urlParams.get('id');
            const reviewText = document.getElementById('review-text').value;

            try {
                const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ text: reviewText })
                });

                if (response.ok) {
                    alert('Review added successfully!');
                    window.location.reload();
                } else {
                    alert('Failed to add review');
                }
            } catch (error) {
                alert('Error adding review: ' + error.message);
            }
        });
    }
});

// Pour la page de détails d'une place
const placeDetails = document.getElementById('place-details');
if (placeDetails) {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    const fetchPlaceDetails = async () => {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'login.html';
            return;
        }

        try {
            const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (response.ok) {
                const place = await response.json();
                displayPlaceDetails(place);
            }
        } catch (error) {
            console.error('Error fetching place details:', error);
        }
    };

    const displayPlaceDetails = async (place) => {
        const placeInfo = document.querySelector('.place-info');
        const token = getCookie('token');

        placeInfo.innerHTML = `
            <h2>${place.name}</h2>
            <p><strong>Host:</strong> Loading...</p>
            <p><strong>Price per night:</strong> $${place.price_by_night}</p>
            <p><strong>Description:</strong> ${place.description}</p>
            <p><strong>Amenities:</strong> ${place.amenities ? place.amenities.join(', ') : 'None'}</p>
        `;

        try {
            // On s'assure d'avoir exactement le même format de header que dans curl
            const ownerResponse = await fetch(`http://localhost:5000/api/v1/users/${place.owner_id}`, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });

            if (ownerResponse.ok) {
                const owner = await ownerResponse.json();
                const hostElement = placeInfo.querySelector('p:nth-child(2)');
                hostElement.innerHTML = `<strong>Host:</strong> ${owner.first_name}  ${owner.last_name}`;
            }
        } catch (error) {
            console.error('Error fetching owner details:', error);
        }

        // Afficher les reviews
        const reviewsSection = document.getElementById('reviews');
        if (place.reviews && place.reviews.length > 0) {
            const reviewsHTML = place.reviews.map(review => `
                <div class="review-card">
                    <p><strong>${review.user_id}:</strong></p>
                    <p>${review.text}</p>
                    <p><em>${review.created_at}</em></p>
                    <hr>
                    <p><strong>Rating:</strong> ${review.rating}</p>
                    <
                </div>
            `).join('');
            reviewsSection.innerHTML = `
                <h2>Reviews</h2>
                ${reviewsHTML}
            `;
        }
    };

    if (placeId) {
        fetchPlaceDetails();
    }
    // Afficher les reviews
    const reviewsSection = document.getElementById('reviews');
    if (reviewsSection) {
        if (place.reviews && place.reviews.length > 0) {
            const reviewsHTML = place.reviews.map(review => `
                <div class="review-card">
                    <p><strong>${review.user_id}:</strong></p>
                    <p>${review.text}</p>
                    <p><em>${review.created_at}</em></p>
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

    // Gérer le formulaire d'ajout de review
    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection && token) {
        addReviewSection.style.display = 'block';

        const reviewForm = document.getElementById('review-form');
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Ajoutons des logs ici
            console.log("Formulaire soumis!");

            const reviewText = document.getElementById('review-text').value;
            const rating = document.querySelector('input[name="rate"]:checked')?.value || 5;

            // Log des valeurs récupérées
            console.log("Review text:", reviewText);
            console.log("Rating:", rating);

            // Récupérer le user_id du token
            const tokenParts = token.split('.');
            const tokenPayload = JSON.parse(atob(tokenParts[1]));
            const userId = tokenPayload.sub;

            // Log du token décodé
            console.log("Token payload:", tokenPayload);
            console.log("User ID:", userId);

            const reviewData = {
                user_id: userId,
                place_id: place.id,  // On utilise place.id au lieu de placeId
                text: reviewText,
                rating: parseInt(rating)
            };

            // Log des données à envoyer
            console.log("Review data to send:", reviewData);

            try {
                const response = await fetch(`http://localhost:5000/api/v1/places/${place.id}/reviews`, {
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


    } else if (addReviewSection) {
        addReviewSection.style.display = 'none';
    }
};