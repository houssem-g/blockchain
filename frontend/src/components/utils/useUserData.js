import { decodeJwt } from './jwts';

export default function useUserData() {
  const getJWToken = () => {
    if (typeof window !== 'undefined') {
      const user = JSON.parse(localStorage?.getItem('@USER'));
      console.log("we are returning the token");
      return user?.access_token;
    }
    console.log("we failed returning the token");
  };

  const handleLogin = token => {
    const decodedToken = decodeJwt(token?.access_token);
    const data = JSON.stringify({access_token: token?.access_token, ...decodedToken});
    if (typeof window !== 'undefined') {
      localStorage.setItem("@USER", data);
      window.dispatchEvent(new Event("storage"));
    }
  };

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.setItem("@USER", null);
      window.dispatchEvent(new Event("storage"));
    }
  };

  const handleUserData = userData => {
    const data = JSON.stringify({...userData})
    if (typeof window !== 'undefined') {
      localStorage.setItem("@USER_DETAILS", data);
      window.dispatchEvent(new Event("storage"));
    }
  }

  return { handleLogin, handleLogout, getJWToken, handleUserData };
}
