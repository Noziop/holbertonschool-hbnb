// src/pages/Places.tsx
import { useState, useEffect } from 'react';
import { Grid, Container, Typography } from '@mui/material';
import PlaceCard from '../components/places/PlaceCard';
import { Place } from '../types/place';

const Places = () => {
  const [places, setPlaces] = useState<Place[]>([]);

  useEffect(() => {
    // TODO: Fetch places from API
    setPlaces([
      {
        id: '1',
        name: 'Haunted Manor',
        description: 'A spooky place with real ghosts!',
        number_rooms: 13,
        number_bathrooms: 3,
        max_guest: 6,
        price_by_night: 666,
        latitude: 48.8566,
        longitude: 2.3522,
        owner_id: '1',
        city: 'Paris',
        country: 'France',
        is_available: true,
        status: 'active',
        minimum_stay: 1,
        property_type: 'house',
        amenity_ids: [],
        review_ids: []
      }
    ]);
  }, []);

  return (
    <Container>
      <Typography variant="h2" gutterBottom>
        Our Haunted Places 👻
      </Typography>
      <Grid container spacing={3}>
        {places.map(place => (
          <Grid item xs={12} sm={6} md={4} key={place.id}>
            <PlaceCard place={place} />
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Places;