import { useState, useEffect } from 'react';
import { Typography, Avatar, IconButton } from '@mui/material';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';
import PersonIcon from '@mui/icons-material/Person';
import AddPhotoAlternateIcon from '@mui/icons-material/AddPhotoAlternate';
import styles from '../styles/Home.module.css';
import useUserData from '../utils/useUserData';
import ButtonDefault from './ButtonDefault';
import Modal from '@mui/material/Modal';
import AddNFT from './AddNFT';

const settings = '/settings';

const UserInfo = ({ refetchItemsList, activationCode }) => {
  const { storageData } = useUserData();
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
  };

  useEffect(() => {
    if (activationCode) {
      handleOpen();
    }
  }, [activationCode]);

  return (
    <>
      <div
        onClick={() => (window.location.href = settings)}
        alt='backgound image'
        style={{
          cursor: 'pointer',
          height: '322px',
          maxWidth: '1256px',
          width: '100%',
          display: 'flex',
          borderRadius: '4px',
          background: 'radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(189,189,189,1) 100%)',
        }}
      >
        <AddPhotoAlternateIcon
          sx={{ margin: 'auto', color: '#bdbdbd', height: '100px', width: '100px' }}
        />
      </div>
      <div style={{ marginTop: '24px', display: 'flex' }} className={styles.userInfoCard}>
        <div style={{ marginTop: '24px', display: 'flex' }} className={styles.userInfoCardContent}>
          <Avatar
            sx={{ height: '160px', width: '160px', marginRight: '40px', cursor: 'pointer' }}
            className={styles.userInfoCardAvatar}
            alt='avatar'
            onClick={() => (window.location.href = settings)}
          >
            <PersonIcon sx={{ height: '160px', width: '160px' }} />
          </Avatar>
          <div style={{ marginTop: '18px' }}>
            <Typography sx={{ textTransform: 'capitalize' }} variant='h3' component='h3'>
              {storageData?.username}
            </Typography>
            <div style={{ width: '150px', marginTop: '20px' }}>
              <ButtonDefault
                title='Edit Profile'
                onClick={() => (window.location.href = settings)}
                margin='0px !important'
                lightMode
              />
            </div>
          </div>
        </div>
        <div
          style={{
            display: 'flex',
            flex: '1',
            height: '36px',
            marginTop: '24px',
            justifyContent: 'end',
          }}
          className={styles.userInfoCardBtns}
        >
          <ButtonDefault
            title='Add Certificate'
            onClick={handleOpen}
            margin='0 8px 0 0'
            width='180px'
          />
          <IconButton size='large' aria-label='more' aria-haspopup='true' color='inherit'>
            <MoreHorizIcon />
          </IconButton>
        </div>
      </div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby='modal-title'
        aria-describedby='modal-description'
      >
        <AddNFT
          onClose={handleClose}
          refetchItemsList={refetchItemsList}
          activationCode={activationCode}
        />
      </Modal>
    </>
  );
};

export default UserInfo;
