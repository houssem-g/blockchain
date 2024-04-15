import { Link } from '@mui/material';

const ButtonLink = ({ title, onClick }) => {
  const styles = {
    color: 'black',
    textDecorationColor: 'black',
    opacity: '0.87',
    fontSize: '14px',
    letterSpacing: '0.1px',
    '&:hover': {
      cursor: 'pointer',
    },
  };

  return (
    <Link sx={styles} onClick={onClick}>
      {title}
    </Link>
  );
};

export default ButtonLink;
