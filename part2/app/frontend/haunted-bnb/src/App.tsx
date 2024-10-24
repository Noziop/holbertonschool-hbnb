// src/App.tsx
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from '@mui/material';
import { hauntedTheme } from './theme';
import Router from './routes';
import { Container } from '@mui/material';

function App() {
  return (
    <ThemeProvider theme={hauntedTheme}>
      <BrowserRouter>
        <Container sx={{ py: 4 }}>  {/* Ajoute un peu d'espace en haut et en bas */}
          <Router />
        </Container>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;