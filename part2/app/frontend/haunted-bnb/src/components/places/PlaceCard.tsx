// src/components/places/PlaceCard.tsx
import { Card, CardContent, CardMedia, Typography, Chip, Box } from '@mui/material';
import { styled } from '@mui/material/styles';
import { motion } from 'framer-motion';
import { FaBed, FaBath, FaUsers, FaEuroSign } from 'react-icons/fa';

const StyledCard = styled(motion.div)`
  height: 100%;
  .MuiCard-root {
    height: 100%;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
    
    &:hover {
      border-color: #ff4081;
      box-shadow: 0 0 20px rgba(255, 64, 129, 0.3);
    }
  }
`;

const StatusChip = styled(Chip)<{ status: string }>`
  position: absolute;
  top: 10px;
  right: 10px;
  background: ${props => 
    props.status === 'active' ? '#4caf50' : 
    props.status === 'maintenance' ? '#ff9800' : '#f44336'};
`;

const IconText = styled(Box)`
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0;
`;

interface PlaceCardProps {
  place: {
    id: string;
    name: string;
    description: string;
    number_rooms: number;
    number_bathrooms: number;
    max_guest: number;
    price_by_night: number;
    city: string;
    country: string;
    status: 'active' | 'maintenance' | 'blocked';
    property_type: string;
  };
}

const PlaceCard = ({ place }: PlaceCardProps) => {
  return (
    <StyledCard
      whileHover={{ y: -5 }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
    >
      <Card>
        <CardMedia
          component="img"
          height="140"
          image={`https://source.unsplash.com/400x200/?haunted,house,${place.id}`}
          alt={place.name}
        />
        <CardContent>
          <StatusChip 
            label={place.status} 
            status={place.status}
          />
          <Typography variant="h5" gutterBottom>
            {place.name} 👻
          </Typography>
          <Typography variant="body2" color="text.secondary" gutterBottom>
            {place.description}
          </Typography>
          
          <Box sx={{ mt: 2 }}>
            <IconText>
              <FaBed /> {place.number_rooms} rooms
            </IconText>
            <IconText>
              <FaBath /> {place.number_bathrooms} bathrooms
            </IconText>
            <IconText>
              <FaUsers /> Up to {place.max_guest} ghosts
            </IconText>
            <IconText>
              <FaEuroSign /> {place.price_by_night}/night
            </IconText>
          </Box>

          <Typography variant="body2" sx={{ mt: 2 }}>
            📍 {place.city}, {place.country}
          </Typography>
          
          <Chip 
            label={place.property_type}
            size="small"
            sx={{ mt: 1 }}
          />
        </CardContent>
      </Card>
    </StyledCard>
  );
};

export default PlaceCard;