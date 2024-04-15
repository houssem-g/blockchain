import SettingsCard from '../components/settings/SettingsCard';
import useUserData from '../utils/useUserData';
import { apiURI } from '../utils/api_path';
import { useState, useEffect } from 'react';

export default function Settings() {
  const { storageData } = useUserData();

  const [data, setData] = useState({});
  const [username, setUsername] = useState('');

  useEffect(() => {
    if (typeof window !== 'undefined' && storageData?.username) {
      setUsername(storageData?.username);
    }
  }, [storageData?.username]);

  const getUsersDetails = async () => {
    const auth = `Bearer ${storageData?.access_token}`;
    await fetch(`${apiURI}/v1/users/${username}`, {
      headers: {
        Accept: 'application/json',
        Authorization: `${auth}`,
      },
      redirect: 'follow',
      method: 'POST',
      mode: 'cors',
    })
      .then(res => res.json())
      .then(response => {
        setData(response);
      });
  };

  useEffect(() => {
    if (username) {
      getUsersDetails();
    }
  }, [username]);

  return (
    <div className='flex justify-center'>
      <div
        className='px-4'
        style={{
          maxWidth: '866px',
          margin: '39px 0 63px 0',
          display: 'flex',
          flex: '1',
          flexDirection: 'column',
        }}
      >
        <SettingsCard title='Upload a new cover photo' type='cover' />
        <SettingsCard title='Upload a new profile photo' type='avatar' />
        <SettingsCard title='Update description' description={data.description} />
        <SettingsCard
          title='Update username'
          description={data.username}
          updateUser={username => setUsername(username)}
        />
        <SettingsCard title='Change account privacy' type='privacy' />
      </div>
    </div>
  );
}
