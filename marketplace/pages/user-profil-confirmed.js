import { useState } from 'react';
import { useRouter } from 'next/router';
import { Modal, Button } from '@mui/material';
import LogIn from '../components/LogIn';
import LoginIcon from '@mui/icons-material/Login';

export const UserProfileConfirmed = () => {
  const router = useRouter('/user-profil-confirmed');
  const [open, setOpen] = useState(false);
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => setOpen(true);

  return (
    <div className='flex justify-center'>
      <div className='px-4' style={{ maxWidth: '1256px', width: '100%', margin: '63px 0' }}>
        <div
          style={{
            display: 'flex',
            flex: '1',
            height: '100%',
            width: '100%',
            justifyContent: 'center',
            alignItems: 'baseline',
            flexWrap: 'wrap',
          }}
        >
          Welcome to ON-Wallet. Your profil is confirmed now, please
          <Button onClick={handleOpen}>
            Log in <LoginIcon />
          </Button>
        </div>
      </div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby='modal-modal-title'
        aria-describedby='modal-modal-description'
      >
        <LogIn onClose={handleClose} isNewUser={false} />
      </Modal>
    </div>
  );
};

export default UserProfileConfirmed;
