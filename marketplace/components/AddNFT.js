import React, { useEffect, useState } from 'react';
import { Stack, TextField, Container, Paper, Snackbar, IconButton, Box } from '@mui/material';
import { isEmpty } from 'lodash';
import { QrReader } from 'react-qr-reader';
import QrCodeScannerIcon from '@mui/icons-material/QrCodeScanner';
import CloseIcon from '@mui/icons-material/Close';
import ButtonDefault from './ButtonDefault';
import { useForm } from 'react-hook-form';
import useUserData from '../utils/useUserData';
import { apiURI } from '../utils/api_path';

const style = {
  display: 'flex',
  width: { xs: '100%', md: '500px' },
  height: { xs: '100%', md: '200px' },
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  bgcolor: 'background.paper',
  boxShadow: 24,
};

const containerStyles = {
  paddingTop: '30px',
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  fontSize: '14px',
  textAlign: 'center',
};

const closeBtnStyle = {
  position: 'absolute',
  top: '15px',
  right: '24px',
  fontSize: '14px',
  fontWeight: '500px',
  cursor: 'pointer',
};

const AddNFT = ({ onClose, refetchItemsList, activationCode }) => {
  const { storageData } = useUserData();
  const [open, setOpen] = useState(false);
  const [showQrReader, setShowQrReader] = useState(false);
  const [message, setMessage] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
  } = useForm();

  useEffect(() => {
    if (activationCode) {
      setValue('activation_key', activationCode);
    }
  }, [activationCode]);

  const addNFT = data => {
    const auth = `Bearer ${storageData?.access_token}`;
    try {
      const payload = `activation_key=${data?.activation_key}`;
      const requestOptions = {
        mode: 'cors',
        method: 'POST',
        headers: {
          Authorization: `${auth}`,
          accept: 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: payload,
      };
      fetch(`${apiURI}/v1/items/activate`, requestOptions)
        .then(response => {
          return response?.json();
        })
        .then(data => {
          if (data?.status === 'activated') {
            setMessage('Item successfully activated');
            refetchItemsList();
            setOpen(true);
          }
          if (data?.detail) {
            setMessage(data?.detail);
            setOpen(true);
          }
        });
    } catch (error) {
      setMessage('An error occured');
      setOpen(true);
    }
  };

  const handleClose = () => {
    setOpen(false);
    setMessage('');
  };

  return (
    <Paper sx={style}>
      <div style={closeBtnStyle} onClick={onClose}>
        Close
        <CloseIcon sx={{ height: '16px', marginBottom: '2px' }} />
      </div>
      <Container sx={containerStyles}>
        <form onSubmit={handleSubmit(addNFT)}>
          <Stack spacing={3}>
            <Box sx={{ display: { xs: 'inline-block', md: 'none' } }}>
              <>
                <div>Click here to scan QR code</div>
                <IconButton color='inherit' onClick={() => setShowQrReader(!showQrReader)}>
                  <QrCodeScannerIcon sx={{ height: '150px', width: '150px' }} />
                </IconButton>
              </>
              {showQrReader && (
                <QrReader
                  key='environment'
                  onResult={(result, error) => {
                    if (!!result && result !== 'No result') {
                      setValue('activation_key', result?.text?.split('#')[1]);
                    }

                    if (!!error) {
                      // console.info(error);
                    }
                  }}
                  style={{ width: '100%' }}
                  constraints={{
                    facingMode: 'environment',
                  }}
                />
              )}
              <div style={{ margin: '30px 0 30px 0' }}>or add activation key manually</div>
            </Box>
            <TextField
              label='Activation key'
              variant='outlined'
              InputLabelProps={{ shrink: true }}
              {...register('activation_key', { required: true })}
              required
              fullWidth
            />
            <div style={{ width: '180px' }}>
              <ButtonDefault type='submit' disabled={!isEmpty(errors)} title={'Add Certificate'} />
            </div>
          </Stack>
        </form>
      </Container>
      <Snackbar open={open} autoHideDuration={2000} onClose={handleClose} message={message} />
    </Paper>
  );
};

export default AddNFT;
