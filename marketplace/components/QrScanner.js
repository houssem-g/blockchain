import React, { useState, useEffect } from 'react';
import { QrReader } from 'react-qr-reader';
import { apiURI } from '../utils/api_path';
import { Box, Typography } from '@mui/material';
import useUserData from '../utils/useUserData';

export const QrScanner = (open) => {
  const { storageData } = useUserData();
  const [data, setData] = useState('No result');
  const [info, setInfo] = useState();
  const addNFT = () => {
    const auth = `Bearer ${storageData?.access_token}`;
    try {
      const payload = `activation_key=${data}`;
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
            setInfo('Item successfully activated');
          }
          if (data?.detail) {
            setInfo(data?.detail);
          }
        });
    } catch (error) {
      setInfo('An error occured');
    }
  };

  useEffect(() => {
    if (data !== 'No result' && storageData?.access_token) {
      addNFT();
    }
  }, [data, storageData?.access_token]);

  return (
    <Box sx={{ height: '100%' }}>
        <QrReader
          key='environment'
          onResult={(result, error) => {
            if (!!result) {
              setData(result?.text?.split('#')[1]);
            }

            if (!!error) {
              // console.info(error);
            }
          }}
          style={{ width: '100%', height: '100%', display: 'flex', justifyContent: 'center' }}
          videoStyle={{ width: '100%', height: '100%', objectFit: 'cover'}}
          videoContainerStyle={{ width: '100%', height: '100%'}}
          containerStyle={{ width: '100%', height: '100%'}}
          ViewFinder={() =>
            <Box sx={{ position: 'absolute', top: 'calc(50% - 170px)', left: 'calc(50% - 154px)', zIndex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <Typography variant='h6' component='h6' sx={{ color: '#fff', marginBottom: '24px' }}>
                Point the camera to the QR code
              </Typography>
              <Box sx={{ height: '250px', width: '250px', color: '#fff', border: '4px solid #FFFFFF', borderRadius: '13px' }}/>
            </Box>
          }
          constraints={{
            facingMode: 'environment',
          }}
          videoId={'QRVideo'}
        />
      {data !== 'No result' && <p>Activation key: {data}</p>}
      {info && <p>{info}</p>}
    </Box>
  );
}

export default QrScanner;
