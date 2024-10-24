// src/components/places/PlaceList.tsx
import { useState, useEffect } from 'react'
import axios from 'axios'
import { motion } from 'framer-motion'
import { styled } from '@mui/material/styles'

const HauntedCard = styled(motion.div)`
  padding: 20px;
  margin: 10px;
  border-radius: 8px;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-5px);
  }
`