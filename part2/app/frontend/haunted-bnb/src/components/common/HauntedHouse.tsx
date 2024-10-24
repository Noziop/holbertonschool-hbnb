// src/components/common/HauntedHouse.tsx
import { motion } from 'framer-motion';
import { styled } from '@mui/material/styles';

interface HauntedHouseProps {
  type: 'house' | 'apartment' | 'villa';
  status: 'active' | 'maintenance' | 'blocked';
}

const StyledHouse = styled(motion.div)<HauntedHouseProps>`
  width: 400px;
  height: 400px;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background: ${props => props.status === 'active' ? 
      'radial-gradient(circle at center, #ff4081 0%, transparent 70%)' : 
      'radial-gradient(circle at center, #666 0%, transparent 70%)'};
    opacity: 0.2;
    animation: glow 2s infinite alternate;
  }

  @keyframes glow {
    from {
      opacity: 0.1;
    }
    to {
      opacity: 0.3;
    }
  }
`;

const House = styled.div<HauntedHouseProps>`
  width: 100%;
  height: 100%;
  background: ${props => {
    switch(props.type) {
      case 'villa':
        return `url("data:image/svg+xml,%3Csvg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M10,80 L50,20 L90,80 Z' fill='%23322'/%3E%3Cpath d='M20,80 L20,40 L50,20 L80,40 L80,80 Z' fill='%23211'/%3E%3Crect x='45' y='60' width='10' height='20' fill='%23700'/%3E%3C/svg%3E")`;
      case 'apartment':
        return `url("data:image/svg+xml,%3Csvg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Crect x='20' y='20' width='60' height='60' fill='%23322'/%3E%3C/svg%3E")`;
      default:
        return `url("data:image/svg+xml,%3Csvg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M20,80 L50,20 L80,80 Z' fill='%23322'/%3E%3C/svg%3E")`;
    }
  }};
  background-repeat: no-repeat;
  background-position: center;
`;

const Windows = styled(motion.div)`
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
`;

const Window = styled(motion.div)`
  position: absolute;
  width: 20px;
  height: 20px;
  background: #700;
  border-radius: 2px;
`;

export const HauntedHouse: React.FC<HauntedHouseProps> = ({ type, status }) => {
  return (
    <StyledHouse
      type={type}
      status={status}
      initial={{ scale: 0.8, y: 100, opacity: 0 }}
      animate={{ 
        scale: 1, 
        y: 0, 
        opacity: 1,
        rotate: [0, 1, -1, 0]
      }}
      transition={{
        duration: 2,
        rotate: {
          duration: 4,
          repeat: Infinity,
          ease: "easeInOut"
        }
      }}
    >
      <House type={type} status={status} />
      <Windows>
        {[...Array(6)].map((_, i) => (
          <Window
            key={i}
            style={{
              top: `${30 + (i % 2) * 20}%`,
              left: `${30 + Math.floor(i / 2) * 20}%`
            }}
            animate={{
              opacity: [0.3, 0.8, 0.3],
              backgroundColor: ['#700', '#f00', '#700']
            }}
            transition={{
              duration: 2,
              delay: i * 0.2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        ))}
      </Windows>
    </StyledHouse>
  );
};

export default HauntedHouse;