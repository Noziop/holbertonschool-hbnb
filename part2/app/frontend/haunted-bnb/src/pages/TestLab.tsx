// src/pages/TestLab.tsx
import { useState } from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { styled } from '@mui/material/styles';
import PlaceForm from '../components/places/PlaceForm';

const TestContainer = styled(Box)`
  background: linear-gradient(to bottom, #1a1a1a, #2d2d2d);
  min-height: 100dvh;
  min-width: 99.98dvw;
  margin: -2.1rem -1.5rem;
`;

const NavButton = styled(Button)`
  margin-right: 1rem;
  background: ${props => props.active ? 
    'linear-gradient(45deg, #ff4081 30%, #7c4dff 90%)' : 
    'transparent'};
  border: 1px solid #ff4081;
  
  &:hover {
    background: linear-gradient(45deg, #ff4081 30%, #7c4dff 90%);
  }
`;

const TestSection = styled(Paper)`
  maw-width: 800px;
  padding: 1rem;
  margin-top: 2rem;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid #ff4081;
`;

const TestLab = () => {
  const [activeSection, setActiveSection] = useState('places');

  return (
    <TestContainer>
      <Typography variant="h2" sx={{ color: '#ff4081', mb: 4 }}>
        🧪 Haunted Testing Lab 👻
      </Typography>

      {/* Navigation */}
      <Box>
        <NavButton 
          active={activeSection === 'places'} 
          onClick={() => setActiveSection('places')}
        >
          Places 🏚️
        </NavButton>
        <NavButton 
          active={activeSection === 'amenities'} 
          onClick={() => setActiveSection('amenities')}
        >
          Amenities ✨
        </NavButton>
        <NavButton 
          active={activeSection === 'reviews'} 
          onClick={() => setActiveSection('reviews')}
        >
          Reviews 📝
        </NavButton>
      </Box>

      {/* Content */}
      <TestSection>
      {activeSection === 'places' && (
  <Box>
    <Typography variant="h4" sx={{ mb: 3 }}>Create New Place 🏚️</Typography>
    <PlaceForm />
  </Box>
)}
        {activeSection === 'amenities' && (
          <Typography>Amenities testing coming soon... ✨</Typography>
        )}
        {activeSection === 'reviews' && (
          <Typography>Reviews testing coming soon... 📝</Typography>
        )}
      </TestSection>
    </TestContainer>
  );
};

export default TestLab;