import { useEffect, useState } from 'react';

export default function MyProfile() {
  const [balance, setBalance] = useState(0);

  useEffect(() => {
    getBalance();
  }, []);

  async function getBalance() {
    setBalance(0.0);
  }

  return (
    <div className='flex justify-center'>
      <h1 className='px-20 py-10 text-3xl'>Coming Soon</h1>
      <div className='px-4' style={{ maxWidth: '1256px' }}>
        <p className='px-600 text-blue-400 font-bold' style={{ textAlign: 'right' }}>
          Your Balance is: {balance} USD
        </p>
      </div>
    </div>
  );
}
