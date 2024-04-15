import { Link } from '@mui/material';

const ButtonLink = ({ title, onClick }) => {

  const styles = { 
    color: 'black',
    textDecorationColor: 'black',
    opacity: '0.87',
    fontSize: '16px',
    letterSpacing: '0.1px',
    marginTop: 'auto!important',
    "&:hover": {
      cursor: 'pointer',
    },
  };

  return (
    <Link
      sx={ styles }
      onClick={onClick}
    >
      {title}
    </Link>
    )
};

export default ButtonLink;