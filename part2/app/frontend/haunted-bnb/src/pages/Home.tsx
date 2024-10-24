// src/pages/Home.tsx
import { motion } from 'framer-motion';
import { styled } from '@mui/material/styles';
import { Typography, Box, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const HauntedContainer = styled(Box)`
  min-height: 100vh;
  min-width: 100vw;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  background: linear-gradient(to bottom, #000000, #1a0f0a);
  position: relative;
  overflow: hidden;
  margin: -2rem;
`;

const FogLayer = styled(motion.div)`
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.05),
    transparent
  );
  pointer-events: none;
`;

const HauntedMansion = styled(motion.div)`
  width: 300px;
  height: 300px;
  margin-bottom: 2rem;
  background: #1a0f0a;
  clip-path: polygon(50% 0, 100% 50%, 100% 100%, 0 100%, 0 50%);
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 20px;
    height: 30px;
    background: #ff4081;
    transform: translate(-50%, -50%);
    box-shadow: 0 0 20px #ff4081;
  }
`;

const Home = () => {
    const navigate = useNavigate();
  
    return (
      <HauntedContainer>
        {/* Le brouillard en premier, HORS du motion.div du titre */}
        {[...Array(3)].map((_, i) => (
          <FogLayer
            key={i}
            initial={{ x: "-100%" }}
            animate={{ x: "100%" }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear",
              delay: i * 3
            }}
            style={{
              top: `${30 + (i * 20)}%`,  // Différentes hauteurs pour chaque couche
              opacity: 0.1 - (i * 0.02)   // Différentes opacités
            }}
          />
        ))}
  
        {/* La maison hantée */}
        <motion.div
          initial={{ scale: 0.1, y: 100 }}
          animate={{ scale: 1, y: 0 }}
          transition={{ duration: 2 }}
        >
          <HauntedMansion />
        </motion.div>
  
        {/* Le titre */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1 }}
        >
          <Typography variant="h1" sx={{
            fontFamily: 'Creepster',
            fontSize: '5rem',
            color: '#fff',
            textShadow: '0 0 10px #ff4081',
            position: 'relative',  // Pour être au-dessus du brouillard
            zIndex: 1             // Pour être au-dessus du brouillard
          }}>
            Haunted BnB
          </Typography>
        </motion.div>
  
        {/* Le bouton */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 2 }}
        >
          <Button 
            variant="contained"
            onClick={() => navigate('/places')}
            sx={{
              mt: 4,
              fontSize: '1.2rem',
              background: 'linear-gradient(45deg, #ff4081 30%, #7c4dff 90%)',
              position: 'relative',  // Pour être au-dessus du brouillard
              zIndex: 1             // Pour être au-dessus du brouillard
            }}
          >
            Enter If You Dare 💀
          </Button>
        </motion.div>
      </HauntedContainer>
    );
  };

export default Home;