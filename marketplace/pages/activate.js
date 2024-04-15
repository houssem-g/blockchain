import { useState } from 'react';
import useUserData from '../utils/useUserData';
import { Modal, Button } from '@mui/material';
import LoginIcon from '@mui/icons-material/Login';
import LogIn from '../components/LogIn';
import { useRouter } from 'next/router';

const userProfile = '/';

export const Activate = () => {
  const { storageData } = useUserData();
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const handleClose = () => {
    setOpen(false);
  };
  const handleOpen = () => setOpen(true);

  if (storageData?.access_token && typeof window !== 'undefined') {
    const activationCode = window.location.href.split('#')[1];
    router.push({ pathname: userProfile, query: { code: activationCode } }, userProfile);
  }

  return (
    <div className='flex justify-center'>
      {!storageData?.access_token && (
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
            Congratulations on your purchase and welcome to ON-Wallet. Please
            <Button onClick={handleOpen}>
              Sign up or Log in <LoginIcon />
            </Button>
            to activate the item.
          </div>
        </div>
      )}
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby='modal-modal-title'
        aria-describedby='modal-modal-description'
      >
        <LogIn onClose={handleClose} />
      </Modal>
    </div>
  );
};

export default Activate;
