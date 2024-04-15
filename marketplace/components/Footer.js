import { Box, Typography } from '@mui/material';
import LinkDefault from './LinkDefault';
import Logo from './Logo';

const titleStyle = {
  color: '#fff',
  margin: '0 20px 18px 0',
  letterSpacing: '0.5px',
};

const Footer = ({ logoTitle }) => {
  return (
    <Box
      sx={{
        backgroundColor: '#000',
        padding: '32px 24px',
        justifyContent: 'space-between',
        flexDirection: 'column',
        marginTop: '80px',
        display: { xs: 'none', sm: 'flex' },
      }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          marginBottom: '36px',
        }}
      >
        <Box
          sx={{
            maxWidth: '1000px',
          }}
        >
          <Logo logoTitle={logoTitle} color='#fff' />
        </Box>
        <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              marginBottom: '30px',
            }}
          >
            <Typography variant='h6' component='h6' sx={titleStyle}>
              Need Help?
            </Typography>
            <LinkDefault title='Help Center' href='#' margin='0 46px 20px 0' />
            <LinkDefault title='Order Status' href='#' margin='0 46px 20px 0' />
            <LinkDefault title='Returns & Exchange' href='#' margin='0 46px 20px 0' />
            <LinkDefault title='Login' href='#' margin='0 46px 0 0' />
          </Box>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
              marginBottom: '30px',
            }}
          >
            <Typography variant='h6' component='h6' sx={titleStyle}>
              About
            </Typography>
            <LinkDefault title='Our Story' href='#' margin='0 46px 20px 0' />
            <LinkDefault title='Environmental impact' href='#' margin='0 46px 20px 0' />
            <LinkDefault title='Team' href='#' margin='0 46px 20px 0' />
            <LinkDefault title='Blog' href='#' margin='0 46px 0 0' />
          </Box>
          <Box
            sx={{
              display: 'flex',
              flexDirection: 'column',
            }}
          >
            <Typography variant='h6' component='h6' sx={titleStyle}>
              Follow Us
            </Typography>
            <LinkDefault title='Facebook' href='#' margin='0 0 20px 0' />
            <LinkDefault title='Twitter' href='#' margin='0 0 20px 0' />
            <LinkDefault title='Instagram' href='#' margin='0 0 0 0' />
          </Box>
        </Box>
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', flexWrap: 'wrap' }}>
        <Typography variant='body1' sx={{ color: '#fff', opacity: '0.5', marginBottom: '30px' }}>
          Copyright © 2022. On-limited. All rights reserved.
        </Typography>
        <Box>
          <LinkDefault title='Terms & Conditions' href='#' margin='0 32px 0 0' />
          <LinkDefault title='Privacy Policy' href='#' margin='0 32px 0 0' />
          <LinkDefault title='Built on Polygon' href='#' />
        </Box>
      </Box>
    </Box>
  );
};

export default Footer;
