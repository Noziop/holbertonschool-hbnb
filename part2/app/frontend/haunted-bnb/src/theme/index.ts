import { createTheme } from '@mui/material/styles';

export const hauntedTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#ff4081',  // Rose fantôme
      light: '#ff79b0',
      dark: '#c60055',
    },
    secondary: {
      main: '#b388ff',  // Violet spectral
      light: '#e7b9ff',
      dark: '#805acb',
    },
    background: {
      default: '#1a1a1a',  // Noir hanté
      paper: '#2d2d2d',
    },
    error: {
      main: '#ff1744',  // Rouge sang
    },
  },
  typography: {
    fontFamily: '"Creepster", "Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#2d2d2d',
          borderRadius: 8,
          transition: 'all 0.3s ease-in-out',
          '&:hover': {
            transform: 'translateY(-5px)',
            boxShadow: '0 10px 20px rgba(0,0,0,0.2)',
          },
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
        },
      },
    },
  },
});

export default hauntedTheme;