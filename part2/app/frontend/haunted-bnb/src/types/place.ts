// src/types/place.ts
export interface Place {
    id: string;
    name: string;
    description: string;
    number_rooms: number;
    number_bathrooms: number;
    max_guest: number;
    price_by_night: number;
    latitude: number;
    longitude: number;
    owner_id: string;
    city: string;
    country: string;
    is_available: boolean;
    status: 'active' | 'maintenance' | 'blocked';
    minimum_stay: number;
    property_type: 'house' | 'apartment' | 'villa';
    amenity_ids: string[];
    review_ids: string[];
  }
  
  // src/components/places/PlaceCard.tsx
  import { styled } from '@mui/material/styles';
  import { Card, CardContent, Typography, Chip } from '@mui/material';
  import { motion } from 'framer-motion';
  
  const HauntedCard = styled(motion.div)`
    cursor: pointer;
    position: relative;
    &:before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      opacity: 0;
      transition: opacity 0.3s;
    }
    &:hover:before {
      opacity: 1;
    }
  `;
  
  const PlaceCard = ({ place }: { place: Place }) => {
    return (
      <HauntedCard
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        <Card>
          <CardContent>
            <Typography variant="h5" component="div">
              {place.name} 👻
            </Typography>
            <Typography color="text.secondary">
              {place.description}
            </Typography>
            <Typography variant="body2">
              💰 ${place.price_by_night}/night
            </Typography>
            <Typography variant="body2">
              👥 Up to {place.max_guest} ghosts
            </Typography>
            <Chip 
              label={place.status} 
              color={place.status === 'active' ? 'success' : 'error'}
            />
          </CardContent>
        </Card>
      </HauntedCard>
    );
  };
  
  export default PlaceCard;