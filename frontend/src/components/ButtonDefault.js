import { Button } from '@mui/material';

const ButtonDefault = ({ title, onClick, margin, lightMode, width, type }) => {

  const styles = {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center',
    padding: '0px 16px',
    gap: '16px',

    height: '44px',

    /* custom/primary */

    background: '#111111',
    borderRadius: '50px',

    /* Inside auto layout */

    flex: 'none',
    order: 0,
    alignSelf: 'stretch',
    flexGrow: 0,
    fontFamily: 'Inter',
    fontStyle: 'normal',
    fontWeight: '500',
    fontSize: '14px',
    lineHeight: '36px',
    textTransform: 'none',
    letterSpacing: '1.25px',
    backgroundColor: lightMode ? 'transparent' : '#000',
    borderColor: lightMode ? '#000' : '#fff',
    color: lightMode ? '#000' : '#fff',
    "&:hover": {
      backgroundColor: lightMode ? 'transparent' : '#000',
      borderColor: lightMode ? '#000' : '#fff',
    },
    width,
    margin
  };

  return (
    <Button
      fullWidth
      sx={ styles }
      variant={lightMode ? 'outlined' : 'contained'}
      size="large"
      type={type}
      onClick={onClick}
    >
      {title}
    </Button>
    )
};

export default ButtonDefault;