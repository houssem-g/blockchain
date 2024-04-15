import { decodeJwt } from './jwts';
import { useState, useEffect } from 'react';

export default function useUserData() {
  const [storageData, setStorageData] = useState();

  const setData = () =>
    setStorageData(
      typeof window !== 'undefined'
        ? {
            ...JSON.parse(localStorage?.getItem('@USER')),
            ...JSON.parse(localStorage?.getItem('@USER_DETAILS')),
          }
        : null(),
    );

  useEffect(() => {
    setData();
    if (typeof window !== 'undefined') {
      window?.addEventListener('storage', () => {
        setData();
      });
    }
  }, []);

  const handleLogin = token => {
    const decodedToken = decodeJwt(token?.access_token);
    const data = JSON.stringify({ access_token: token?.access_token, ...decodedToken });
    if (typeof window !== 'undefined') {
      localStorage.setItem('@USER', data);
      window.dispatchEvent(new Event('storage'));
    }
  };

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('@USER', null);
      localStorage.setItem('@USER_DETAILS', null);
      setStorageData(null);
      window.dispatchEvent(new Event('storage'));
    }
  };

  const handleUserData = userData => {
    const data = JSON.stringify({ ...userData });
    if (typeof window !== 'undefined') {
      localStorage.setItem('@USER_DETAILS', data);
      window.dispatchEvent(new Event('storage'));
    }
  };

  return { handleLogin, handleLogout, handleUserData, storageData };
}
