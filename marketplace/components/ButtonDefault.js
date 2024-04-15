import { Button } from '@mui/material';

const ButtonDefault = ({ title, onClick, margin, lightMode, width, type, size='large' }) => {
  const styles = {
    borderRadius: '50px',
    fontSize: '14px',
    textTransform: 'none',
    letterSpacing: '1.25px',
    backgroundColor: lightMode ? 'transparent' : '#000',
    borderColor: lightMode ? '#000' : '#fff',
    color: lightMode ? '#000' : '#fff',
    '&:hover': {
      backgroundColor: lightMode ? 'transparent' : '#000',
      borderColor: lightMode ? '#000' : '#fff',
    },
    width,
    margin,
  };

  return (
    <Button
      fullWidth
      sx={styles}
      variant={lightMode ? 'outlined' : 'contained'}
      size={size}
      type={type}
      onClick={onClick}
    >
      {title}
    </Button>
  );
};

export default ButtonDefault;
