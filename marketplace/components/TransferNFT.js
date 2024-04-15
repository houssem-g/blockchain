import React, { useState } from 'react';
import { Stack, TextField, Container, Paper } from '@mui/material';
import { isEmpty } from 'lodash';
import CloseIcon from '@mui/icons-material/Close';
import ButtonDefault from './ButtonDefault';
import { useForm } from 'react-hook-form';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
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
};

const closeBtnStyle = {
  position: 'absolute',
  top: '15px',
  right: '24px',
  fontSize: '14px',
  fontWeight: '500px',
  cursor: 'pointer',
};

const TransferNFT = ({ onClose, onCloseAndBack, serialNumber, refetchItemsList }) => {
  const { storageData } = useUserData();
  const [successfullyTransferred, setSuccessfullyTransferred] = useState(false);
  const [error, setError] = useState(null);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const handleCloseModal = () => {
    if (successfullyTransferred) {
      onCloseAndBack();
    } else {
      onClose();
    }
  };

  const transferNFT = async data => {
    const auth = `Bearer ${storageData?.access_token}`;
    try {
      const payload = `serial_number=${serialNumber}&username=${data?.username}`;
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
      const response = await fetch(`${apiURI}/v1/items/transfer`, requestOptions);
      if (!response.ok) {
        throw new Error(`Error! status: ${response.status}`);
      }
      const result = await response.json();
      if (typeof result === 'string') {
        setSuccessfullyTransferred(true);
        refetchItemsList();
      }
      if (result?.detail) {
        setError(result?.detail);
      }
    } catch (error) {
      setError('An error occured');
    }
  };

  const renderContent = () => {
    return (
      <Container sx={containerStyles}>
        <form onSubmit={handleSubmit(transferNFT)}>
          {!showConfirmation ? (
            <Stack spacing={3}>
              <TextField
                label='Username'
                variant='outlined'
                InputLabelProps={{ shrink: true }}
                {...register('username', { required: true })}
                required
                fullWidth
              />
              <div style={{ width: '140px' }}>
                <ButtonDefault
                  onClick={() => setShowConfirmation(true)}
                  disabled={!isEmpty(errors)}
                  title={'Transfer'}
                />
              </div>
            </Stack>
          ) : (
            <>
              <div>
                Are you sure you want to tranfer this item? This operation cannot be undone. Would
                you like to proceed?
              </div>
              <div style={{ display: 'flex', marginTop: '30px', justifyContent: 'space-between' }}>
                <ButtonDefault
                  onClick={() => setShowConfirmation(false)}
                  title={'Cancel'}
                  width={80}
                  lightMode
                />
                <ButtonDefault type='submit' title={'Transfer'} width={100} />
              </div>
            </>
          )}
        </form>
      </Container>
    );
  };

  const renderSuccessContent = () => {
    return (
      <Container sx={containerStyles}>
        <div style={{ textAlign: 'center' }}>
          <CheckCircleIcon
            sx={{ color: '#3fb922', height: '86px', marginRight: '4px', marginBottom: '2px' }}
          />
          Item was successfully transferred.
        </div>
      </Container>
    );
  };

  const renderErrorContent = () => {
    return (
      <Container sx={containerStyles}>
        <div style={{ textAlign: 'center' }}>
          <ErrorIcon
            sx={{ color: '#dc2626', height: '86px', marginRight: '4px', marginBottom: '2px' }}
          />
          {error}
        </div>
      </Container>
    );
  };

  return (
    <Paper sx={style}>
      <div style={closeBtnStyle} onClick={handleCloseModal}>
        Close
        <CloseIcon sx={{ height: '16px', marginBottom: '2px' }} />
      </div>
      {!successfullyTransferred && !error && renderContent()}
      {!successfullyTransferred && error && renderErrorContent()}
      {successfullyTransferred && !error && renderSuccessContent()}
    </Paper>
  );
};

export default TransferNFT;
