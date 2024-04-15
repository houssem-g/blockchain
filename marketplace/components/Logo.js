import { Typography, Chip } from '@mui/material';

const Logo = ({ logoTitle, color = '#000' }) => {
  const styles = {
    color,
    mr: 2,
    display: {
      xs: 'none',
      md: 'flex',
      fontSize: '27px',
      fontWeight: '700',
      letterSpacing: '0.5px',
    },
    fontFamily: 'Gilroy-ExtraBold',
    marginBottom: '5px',
  };

  return (
    <Typography variant='h6' noWrap component='div' sx={styles}>
      {logoTitle}
      <Chip
        label='BETA'
        color='primary'
        size='small'
        sx={{
          fontSize: '10px',
          marginLeft: '5px',
          marginTop: '10px',
          fontFamily: 'Gilroy-ExtraBold',
        }}
      />
    </Typography>
  );
};

export default Logo;
