import '../styles/globals.css';
import '../styles/upload_document.css';
import * as React from 'react';
import NavBar from '../components/NavBar';
import Footer from '../components/Footer';
import QrDrawer from '../components/QrDrawer';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  typography: {
    fontFamily: 'Inter-Regular',
  },
});

function MyApp({ Component, pageProps }) {
  const logoTitle = 'ON-Wallet';
  return (
    <ThemeProvider theme={theme}>
      <div
        style={{
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          fontFamily: 'Inter-Regular',
          position: 'relative',
        }}
      >
        <QrDrawer/>
        <NavBar logoTitle={logoTitle} />
        <Container maxWidth='1256px' sx={{ flex: '1' }}>
          <Component {...pageProps} />
        </Container>
        <Footer logoTitle={logoTitle} />
      </div>
    </ThemeProvider>
  );
}

export default MyApp;
