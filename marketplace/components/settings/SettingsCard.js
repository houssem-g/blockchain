import { useState, useRef, useEffect } from 'react';
import { Paper, Typography, TextField, Avatar, Select, MenuItem } from '@mui/material';
import LockIcon from '@mui/icons-material/Lock';
import PersonIcon from '@mui/icons-material/Person';
import AddPhotoAlternateIcon from '@mui/icons-material/AddPhotoAlternate';
import PublicIcon from '@mui/icons-material/Public';
import ButtonDefault from '../ButtonDefault';
import styles from '../../styles/Home.module.css';
import Image from 'next/image';
import { apiURI } from '../../utils/api_path';
import useUserData from '../../utils/useUserData';

const coverImg = {
  img: '',
  name: 'cover.png',
};

const avatarImg = {
  img: '',
  name: 'profile_pic.png',
};

const privacy = {
  private: 'Profile: private',
  public: 'Profile: public',
};

const SettingsCard = ({ title, description, type = 'text', updateUser }) => {
  const uploadInputRef = useRef(null);
  const [editMode, setEditMode] = useState(false);
  const [profilePrivacy, setProfilePrivacy] = useState('private_profile');
  const [displayedValue, setDisplayedValue] = useState();
  const { handleUserData } = useUserData();
  const [newDescription, setNewDescription] = useState({
    textArea: '',
    textAreaValue: '',
  });

  const { storageData } = useUserData();
  useEffect(() => {
    if (description) {
      setDisplayedValue(description);
    }
  }, [description]);

  const onSave = async () => {
    setEditMode(false);
    const auth = `Bearer ${storageData?.access_token}`;
    const formData = new FormData();
    formData.append('username', storageData?.username);

    let ressource = '';

    if (newDescription.textArea == 'Update username') {
      ressource = 'username_update';
      formData.append('new_username', newDescription.textAreaValue);
    } else {
      ressource = 'description_update';
      formData.append('description', newDescription.textAreaValue);
    }

    await fetch(`${apiURI}/v1/users/${ressource}`, {
      headers: {
        Accept: 'application/json',
        Authorization: `${auth}`,
      },
      redirect: 'follow',
      method: 'PUT',

      mode: 'cors',
      body: formData,
    })
      .then(res => res.json())
      .then(response => {
        if (
          (response == 'User updated with success !') &
          (newDescription.textArea == 'Update username')
        ) {
          setDisplayedValue(newDescription.textAreaValue);
          updateUser(newDescription.textAreaValue);
          let get_data = JSON.parse(localStorage.getItem('@USER_DETAILS'));
          get_data['username'] = newDescription.textAreaValue;
          localStorage.setItem('username', newDescription.textAreaValue);
          handleUserData(get_data);
        } else if (response != 'User updated with success !') {
          alert(response['detail']);
        } else {
          setDisplayedValue(newDescription.textAreaValue);
        }
      });
  };

  const onEdit = () => {
    setEditMode(true);
    if (type === 'avatar' || type === 'cover') {
      uploadInputRef.current && uploadInputRef.current.click();
    }
  };

  const privacyContent = () => {
    return (
      <div style={{ marginTop: '16px' }}>
        <Typography variant='h5' component='div' sx={{ opacity: '0.87' }}>
          {title}
        </Typography>
        {editMode ? (
          <Select
            value={profilePrivacy}
            variant='standard'
            onChange={event => setProfilePrivacy(event.target.value)}
            sx={{ marginTop: '4px' }}
          >
            <MenuItem value='private_profile'>
              <LockIcon sx={{ color: '#0077FF', fontSize: '16px', marginRight: '8px' }} />
              {privacy.private}
            </MenuItem>
            <MenuItem value='public_profile'>
              <PublicIcon sx={{ color: '#0077FF', fontSize: '16px', marginRight: '8px' }} />
              {privacy.public}
            </MenuItem>
          </Select>
        ) : (
          <Typography
            variant='body2'
            component='div'
            sx={{
              opacity: '0.87',
              letterSpacing: '0.1px',
              marginTop: '10px',
              fontSize: '16px',
              display: 'flex',
              alignItems: 'center',
            }}
          >
            {profilePrivacy === 'privateProfile' ? (
              <LockIcon sx={{ color: '#0077FF', fontSize: '16px', marginRight: '8px' }} />
            ) : (
              <PublicIcon sx={{ color: '#0077FF', fontSize: '16px', marginRight: '8px' }} />
            )}
            {profilePrivacy}
          </Typography>
        )}
      </div>
    );
  };

  const imgContent = () => {
    return (
      <div style={{ display: 'flex' }} className={styles.settingCardContent}>
        {type === 'avatar' ? (
          <Avatar sx={{ height: '70px', width: '70px', marginRight: '40px' }} alt='avatar'>
            <PersonIcon sx={{ height: '70px', width: '70px' }} />
          </Avatar>
        ) : (
          <div
            alt='backgound image'
            style={{
              borderRadius: '3px',
              height: '93px',
              width: '160px',
              display: 'flex',
              marginRight: '40px',
              background:
                'radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(189,189,189,1) 100%)',
            }}
          >
            <AddPhotoAlternateIcon
              sx={{ maxHeight: '93px', maxWidth: '160px', margin: 'auto', color: '#bdbdbd' }}
            />
          </div>
        )}
        <div style={{ alignSelf: 'center' }} className={styles.settingCardText}>
          <Typography variant='h5' component='div' sx={{ opacity: '0.87' }}>
            {title}
          </Typography>
          {editMode ? (
            <input
              sx={{ opacity: '0.87', letterSpacing: '0.1px', width: '100%', marginTop: '4px' }}
              ref={uploadInputRef}
              type='file'
              accept='image/*'
            />
          ) : (
            <Typography
              variant='body2'
              component='div'
              sx={{ opacity: '0.87', letterSpacing: '0.1px', marginTop: '10px', fontSize: '16px' }}
            >
              {type === 'avatar' ? avatarImg?.name : coverImg?.name}
            </Typography>
          )}
        </div>
      </div>
    );
  };

  const textContent = () => {
    return (
      <div style={{ marginTop: '16px' }}>
        <Typography variant='h5' component='div' sx={{ opacity: '0.87' }}>
          {title}
        </Typography>
        {editMode ? (
          <TextField
            id='standard-basic'
            variant='standard'
            sx={{ opacity: '0.87', letterSpacing: '0.1px', width: '100%', marginTop: '4px' }}
            defaultValue={displayedValue}
            onChange={event =>
              setNewDescription({
                ...newDescription,
                textAreaValue: event.target.value,
                textArea: Object.values({ title })[0],
              })
            }
            multiline
          />
        ) : (
          <Typography
            variant='body2'
            component='div'
            sx={{ opacity: '0.87', letterSpacing: '0.1px', marginTop: '10px', fontSize: '16px' }}
          >
            {displayedValue}
          </Typography>
        )}
      </div>
    );
  };

  const getContent = () => {
    switch (type) {
      case 'avatar':
        return imgContent();
      case 'cover':
        return imgContent();
      case 'privacy':
        return privacyContent();
      default:
        return textContent();
    }
  };

  return (
    <Paper
      elevation={0}
      className={styles.settingCard}
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginTop: '24px',
        backgroundColor: '#F5F5F5',
        borderRadius: '13px',
        padding: '24px',
        width: '100%',
      }}
    >
      <div style={{ flex: '1' }}>{getContent()}</div>
      <div style={{ alignSelf: 'center', marginLeft: '20px' }} className={styles.settingCardBtn}>
        {editMode ? (
          <ButtonDefault title='Save' onClick={() => onSave()} margin='0px !important' />
        ) : (
          <ButtonDefault title='Edit' onClick={() => onEdit()} margin='0px !important' lightMode />
        )}
      </div>
    </Paper>
  );
};

export default SettingsCard;
