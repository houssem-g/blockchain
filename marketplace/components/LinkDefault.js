import { Link } from '@mui/material';

const LinkDefault = ({ title, href, margin }) => {
  const styles = {
    color: '#fff',
    margin,
    letterSpacing: '0.5px',
  };

  return (
    <Link sx={styles} href={href} underline='none'>
      {title}
    </Link>
  );
};

export default LinkDefault;
