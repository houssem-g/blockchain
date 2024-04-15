import React, { useState } from 'react';
import { Container, Paper } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import ButtonDefault from './ButtonDefault';
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

const BurnNFT = ({ onClose, serialNumber, refetchItemsList, onCloseAndBack }) => {
  const { storageData } = useUserData();
  const [successfullyBurned, setSuccessfullyBurned] = useState(false);
  const [error, setError] = useState(false);

  const handleCloseModal = () => {
    if (successfullyBurned) {
      onCloseAndBack();
      refetchItemsList();
    } else {
      onClose();
    }
  };

  const burnNFT = async () => {
    const auth = `Bearer ${storageData?.access_token}`;
    try {
      const payload = `serial_number=${serialNumber}`;
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
      const response = await fetch(`${apiURI}/v1/items/burn`, requestOptions);
      if (!response.ok) {
        throw new Error(`Error! status: ${response.status}`);
      }
      const result = await response.json();
      if (result?.includes('burned item with')) {
        setSuccessfullyBurned(true);
      }
      if (result?.details) {
        setError(true);
      }
    } catch (error) {
      console.log('error');
    }
  };

  const renderContent = () => {
    return (
      <Container sx={containerStyles}>
        <div>
          Are you sure you want to burn this item? This operation cannot be undone. Would you like
          to proceed?
        </div>
        <div style={{ display: 'flex', marginTop: '30px', justifyContent: 'space-between' }}>
          <ButtonDefault onClick={handleCloseModal} title={'Cancel'} width={80} lightMode />
          <ButtonDefault onClick={burnNFT} title={'Burn'} width={80} />
        </div>
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
          Item was successfully burned.
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
          An error occured
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
      {!successfullyBurned && !error && renderContent()}
      {!successfullyBurned && error && renderErrorContent()}
      {successfullyBurned && !error && renderSuccessContent()}
    </Paper>
  );
};

export default BurnNFT;
