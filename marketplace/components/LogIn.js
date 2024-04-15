import { useState } from 'react';
import { Stack, TextField, Typography, Container, Paper, Snackbar, Box } from '@mui/material';
import { isEmpty } from 'lodash';
import CloseIcon from '@mui/icons-material/Close';
import ButtonDefault from './ButtonDefault';
import ButtonLink from './ButtonLink';
import { useForm } from 'react-hook-form';
import useUserData from '../utils/useUserData';
import React from 'react';
import { apiURI } from '../utils/api_path';
import Image from 'next/image';
import loginImage from '../public/loginImg.jpg';
import { useRouter } from 'next/router';

const userProfile = '/';

const style = {
  display: 'flex',
  maxWidth: '1160px',
  maxHeight: '773px',
  width: '100%',
  height: '100%',
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  bgcolor: 'background.paper',
  boxShadow: 24,
  p: 4,
};

const containerStyles = {
  display: 'flex',
  flexDirection: 'column',
  justifyContent: 'center',
  flex: 1,
};

const closeBtnStyle = {
  position: 'absolute',
  top: '15px',
  right: '24px',
  fontSize: '14px',
  fontWeight: '500px',
  cursor: 'pointer',
};

const LogIn = ({ onClose, isNewUser }) => {
  const router = useRouter();
  const { handleLogin, handleUserData } = useUserData();
  const [newUser, setNewUser] = useState(isNewUser === false ? false : true);
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const getUserData = data => {
    const auth = `Bearer ${data?.access_token}`;
    try {
      const requestOptions = {
        method: 'GET',
        mode: 'cors',
        headers: {
          accept: 'application/json',
          Authorization: `${auth}`,
        },
      };

      fetch(`${apiURI}/v1/users/me`, requestOptions)
        .then(response => response.json())
        .then(data => {
          if (Object.keys(data).includes('detail')) {
            alert(data['detail']);
          }
          handleUserData(data);
        });
    } catch (error) {
      console.log('error');
    }
  };

  const signUp = data => {
    try {
      const payload = JSON.stringify({
        email: data?.email,
        username: data?.name,
        password: data?.password,
      });
      const requestOptions = {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
        },
        body: payload,
      };

      fetch(`${apiURI}/v1/users/signup`, requestOptions)
        .then(response => {
          if (response?.ok) {
            setOpen(true);
          }
          return response.json();
        })
        .then(res => {
          if (res.email)
            alert(
              'To finalize your subscrition, please click on the activation link sent to your email address.',
            );
          else alert(res.detail);
        });
    } catch (error) {
      setMessage('An error occured');
      setOpen(true);
    }
  };

  const logIn = data => {
    try {
      const payload = `grant_type=&username=${data?.email}&password=${data?.password}&scope=&client_id=&client_secret=`;
      const requestOptions = {
        mode: 'cors',
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          Accept: 'application/json',
        },
        body: payload,
      };
      fetch(`${apiURI}/v1/users/login`, requestOptions)
        .then(response => {
          if (response?.ok) {
            setMessage('User successfully logged in');
            router.push(userProfile).then(res => {
              if (res) {
                setOpen(true);
                onClose();
              }
            });
          }
          return response?.json();
        })
        .then(data => {
          handleLogin(data);
          getUserData(data);
        });
    } catch (error) {
      setMessage('An error occured');
      setOpen(true);
    }
  };

  const onForgotPassword = () => {};

  const onRedirectToLogin = () => {
    setNewUser(!newUser);
  };

  const handleClose = () => {
    setOpen(false);
    setMessage('');
  };

  return (
    <Paper style={style}>
      <div style={closeBtnStyle} onClick={onClose}>
        <Box sx={{ display: { xs: 'none', md: 'inline-flex' } }}>Close</Box>
        <CloseIcon sx={{ height: '16px', marginBottom: '2px' }} />
      </div>
      <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
        <Image src={loginImage} alt='login image' layout='intrinsic' />
      </Box>
      <Container sx={containerStyles}>
        <Stack spacing={3} sx={{ alignItems: 'center', marginBottom: '24px' }}>
          <Typography
            sx={{ letterSpacing: '0.25px', opacity: '0.87', margin: '8px', fontWeight: '500' }}
            variant='h6'
            component='h6'
          >
            {newUser ? 'Sign up for Marketplace' : 'Welcome to Marketplace'}
          </Typography>
          <Typography
            sx={{ letterSpacing: '0.25px', opacity: '0.87', margin: '8px', fontWeight: '500' }}
            variant='subtitle2'
            component='subtitle2'
          >
            Buy, sell and unlock experinces. Save favourite items, track prices & much more!
          </Typography>
          <ButtonDefault title={newUser ? 'Sign up With Google' : 'Log in With Google'} />
          <span>or</span>
        </Stack>
        <form onSubmit={newUser ? handleSubmit(signUp) : handleSubmit(logIn)}>
          <Stack spacing={3}>
            {newUser && (
              <TextField
                label='Name'
                variant='outlined'
                type='name'
                InputLabelProps={{ shrink: true }}
                {...register('name', { required: true })}
                required
                fullWidth
              />
            )}
            <TextField
              label='Email'
              variant='outlined'
              type='email'
              InputLabelProps={{ shrink: true }}
              {...register('email', {
                required: true,
                pattern: /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/i,
              })}
              required
              fullWidth
            />
            <TextField
              label={newUser ? 'Create Password' : 'Password'}
              variant='outlined'
              type='password'
              InputLabelProps={{ shrink: true }}
              {...register('password', { required: true })}
              required
              fullWidth
            />
            <ButtonLink onClick={onForgotPassword} title='Forgot password?' />
            <div style={{ width: '105px' }}>
              <ButtonDefault
                type='submit'
                disabled={!isEmpty(errors)}
                title={newUser ? 'Sign Up' : 'Log In'}
              />
            </div>
            {errors.email && errors.email.type === 'pattern' && (
              <span style={{ color: 'red', fontSize: '14px' }}>Email format is not valid</span>
            )}
            <ButtonLink
              onClick={onRedirectToLogin}
              title={
                newUser ? 'Already have an account? Log in' : 'Don’t have an account? Register here'
              }
            />
          </Stack>
        </form>
      </Container>
      <Snackbar open={open} autoHideDuration={6000} onClose={handleClose} message={message} />
    </Paper>
  );
};

export default LogIn;
