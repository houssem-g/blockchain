import { useState } from 'react';
import { Stack, TextField, Typography, Container, Paper, Snackbar } from '@mui/material';
import { isEmpty } from 'lodash';
import CloseIcon from '@mui/icons-material/Close';
import ButtonDefault from './ButtonDefault';
import ButtonLink from './ButtonLink';
import { useForm } from "react-hook-form";
import useUserData from './utils/useUserData';
import React from 'react';



const LogIn = ({ onClose, onSuccess, styleModule }) => {
  const { handleLogin, handleUserData, getJWToken } = useUserData();
  const [newUser, setNewUser] = useState(true);
  const [open, setOpen] = useState(false);
  const [message, setMessage] = useState('');
  const { register, handleSubmit, formState: { errors } } = useForm();

  const getUserData = () => {
    const auth = `Bearer ${getJWToken()}`;
    try {
      const requestOptions = {
        method: 'GET',
        mode: 'cors',
        headers: {
          'accept': 'application/json',
          'Authorization': `${auth}`,
          'Access-Control-Allow-Origin':'*'
        },
      };
      
      fetch('http://127.0.0.1:8000/v1/users/me', requestOptions)
        .then(response => response.json())
        .then(data => handleUserData(data));
    } catch (error) {
      console.log('error')
    }
  };

  const signUp = data => {
    try {
      const payload = JSON.stringify(
        {
          "email": data?.email,
          "username": data?.name,
          "password": data?.password
        }
      );
      const requestOptions = {
        method: 'POST',
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin':'*'
        },
        body: payload,
      };
      
      fetch('http://127.0.0.1:8000/v1/users/signup', requestOptions)
        .then(response => {
          if (response?.ok) {
            setMessage('User successfully created')
            setOpen(true);
          }
        })
    } catch (error) {
      setMessage('An error occured')
      setOpen(true);
    }
  };

  const logIn = data => {
    try {
      const payload = `grant_type=&username=${data?.email}&password=${data?.password}&scope=&client_id=&client_secret=`;
      const requestOptionsLogin = {
        mode: 'cors',
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          Accept: 'application/json',
        },
        body: payload
      };
      fetch('http://127.0.0.1:8000/v1/users/login', requestOptionsLogin)
      .then(response => {
        if (response?.ok) {
          setMessage('User successfully logged in')
          setOpen(true);
          onClose();
          onSuccess();
        }
        return response?.json();
      })
      .then(data => {
        handleLogin(data);
        getUserData();
      });
    } catch (error) {
      setMessage('An error occured')
      setOpen(true);
    }
  }

  const onForgotPassword = () => {
  }

  const onRedirectToLogin = () => {
    setNewUser(!newUser);
  }

  const handleClose = () => {
    setOpen(false);
    setMessage('');
  }

  return (
    <Paper style={styleModule.paperStyles}>
 
        <div style={styleModule.imageForm} >
          <img src='http://localhost:3000/loginImg.jpg' />          
        </div>

        <Container style={styleModule.form}>
          <div style={styleModule.contentBtnClose} onClick={onClose}>
            <button style = {styleModule.btnClose}>
              <span style= {styleModule.textClose}>Close</span>
              <CloseIcon sx={styleModule.closeIconStyle} />
            </button>
          </div>
          
            <Stack spacing={3} sx={styleModule.contentTitle}>
              <Typography
                sx={styleModule.titleStyles}
              >
                {newUser ? 'Sign up for Marketplace' : 'Welcome to Marketplace'}
              </Typography>
              <div style={styleModule.contentSubtitle2}>
                <Typography
                  sx={styleModule.subtitle2}
                >
                  Buy, sell and unlock experinces. Save favourite items, track prices & much more!
                </Typography>
              </div>
              <div style={styleModule.contentButtonGoogle}>
              <ButtonDefault
                title={newUser ? 'Sign up With Google' : 'Log in With Google'}
              />
              </div>
              <div style={styleModule.contentTextOr}>
                <span style={styleModule.textOr}>or</span>
              </div>
            </Stack>
            <form onSubmit={newUser ? handleSubmit(signUp) : handleSubmit(logIn)}>
              <Stack spacing={3} style={styleModule.contentBody}>
                <div style={styleModule.inputTextContent}>
                  {newUser && (
                    <div style={styleModule.contentName}>
                    <TextField
                      label="Name"
                      variant="outlined"
                      type='name'
                      style={styleModule.inputSignInName}
                      InputLabelProps={{ shrink: true }}
                      {...register("name", { required: true })}
                      required
                      fullWidth
                    />
                    </div>
                  )}
                  
                  <div style={styleModule.contentEmail}>
                    <TextField
                      label="Email"
                      variant="outlined"
                      type='email'
                
                      style={styleModule.inputSignInEmail}
                      InputLabelProps={{ shrink: true }}
                      {...register("email", { required: true, pattern: /^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/i })}
                      required
                      fullWidth
                    />
                  </div>
                  <div style={styleModule.contentPwd}>
                    <TextField
                      label={newUser ? 'Create Password' : 'Password'}
                      variant="outlined"
                      type="password"
                      style={styleModule.inputSignInPwd}
                      InputLabelProps={{ shrink: true }}
                      {...register("password", { required: true })}
                      required
                      fullWidth
                    />
                    {!newUser &&(<u ><a style={styleModule.forgetPwd} href="#linkToForgetPwd" onClick={onForgotPassword}>Forgot password?</a></u>)}
                    {errors.email && errors.email.type === "pattern" && <span style={styleModule.emailError}>Email format is not valid</span>}
                    {/* <ButtonLink onClick={onForgotPassword} title="Forgot password?" /> */}
                  </div>
                </div>
                
                
                <div style={styleModule.contentButtonLogin}>
                  <div style={styleModule.buttonLogin}>
                    <ButtonDefault
                      type='submit'
                      disabled={!isEmpty(errors)}
                      title={newUser ? 'Sign Up' : 'Log In'}
                    />
                  </div>
                  <div style={styleModule.texthaveAccount}>
                    <ButtonLink onClick={onRedirectToLogin} title={newUser ? 'Already have an account? Log in' : 'Don’t have an account? Register here'} />
                  </div>
                </div>

              </Stack>
            </form>
        </Container>
      {/* </div> */}
      <Snackbar
        open={open}
        autoHideDuration={6000}
        onClose={handleClose}
        message={message}
       
      />
    </Paper>
      
  );
}

export default LogIn;