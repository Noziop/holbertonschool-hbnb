// src/components/places/PlaceForm.tsx
import { useState } from 'react';
import { 
  Box, 
  TextField, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Switch,
  FormControlLabel,
  Button 
} from '@mui/material';
import { styled } from '@mui/material/styles';

const FormContainer = styled(Box)`
  display: grid;
  gap: 1rem;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 8px;
`;

const PlaceForm = () => {
  const [placeData, setPlaceData] = useState({
    name: '',
    description: '',
    number_rooms: 1,
    number_bathrooms: 1,
    max_guest: 1,
    price_by_night: 0,
    latitude: 0,
    longitude: 0,
    owner_id: '',
    city: '',
    country: '',
    is_available: true,
    status: 'active',
    minimum_stay: 1,
    property_type: 'apartment'
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/api/v1/places', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(placeData)
      });
      const data = await response.json();
      console.log('Success:', data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <FormContainer component="form" onSubmit={handleSubmit}>
      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
        <TextField
          label="Name"
          value={placeData.name}
          onChange={(e) => setPlaceData({...placeData, name: e.target.value})}
          required
        />
        <TextField
          label="Owner ID"
          value={placeData.owner_id}
          onChange={(e) => setPlaceData({...placeData, owner_id: e.target.value})}
          required
        />
      </Box>

      <TextField
        label="Description"
        multiline
        rows={4}
        value={placeData.description}
        onChange={(e) => setPlaceData({...placeData, description: e.target.value})}
        required
      />

      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 2 }}>
        <TextField
          label="Rooms"
          type="number"
          value={placeData.number_rooms}
          onChange={(e) => setPlaceData({...placeData, number_rooms: parseInt(e.target.value)})}
          required
        />
        <TextField
          label="Bathrooms"
          type="number"
          value={placeData.number_bathrooms}
          onChange={(e) => setPlaceData({...placeData, number_bathrooms: parseInt(e.target.value)})}
          required
        />
        <TextField
          label="Max Guests"
          type="number"
          value={placeData.max_guest}
          onChange={(e) => setPlaceData({...placeData, max_guest: parseInt(e.target.value)})}
          required
        />
      </Box>

      <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
        <FormControl fullWidth>
          <InputLabel>Status</InputLabel>
          <Select
            value={placeData.status}
            onChange={(e) => setPlaceData({...placeData, status: e.target.value})}
          >
            <MenuItem value="active">Active 🟢</MenuItem>
            <MenuItem value="maintenance">Maintenance 🔧</MenuItem>
            <MenuItem value="blocked">Blocked 🔴</MenuItem>
          </Select>
        </FormControl>
        <FormControl fullWidth>
          <InputLabel>Property Type</InputLabel>
          <Select
            value={placeData.property_type}
            onChange={(e) => setPlaceData({...placeData, property_type: e.target.value})}
          >
            <MenuItem value="house">House 🏠</MenuItem>
            <MenuItem value="apartment">Apartment 🏢</MenuItem>
            <MenuItem value="villa">Villa 🏰</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <FormControlLabel
        control={
          <Switch
            checked={placeData.is_available}
            onChange={(e) => setPlaceData({...placeData, is_available: e.target.checked})}
          />
        }
        label="Available for booking 👻"
      />

      <Button 
        type="submit"
        variant="contained"
        sx={{
          background: 'linear-gradient(45deg, #ff4081 30%, #7c4dff 90%)',
          color: 'white'
        }}
      >
        Create Haunted Place 🏚️
      </Button>
    </FormContainer>
  );
};

export default PlaceForm;