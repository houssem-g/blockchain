import { useEffect, useState } from 'react';
import UserInfo from '../components/UserInfo';
import { Modal, Button } from '@mui/material';
import LogIn from '../components/LogIn';
import LoginIcon from '@mui/icons-material/Login';
import ItemCardFull from '../components/ItemCardFull';
import ItemsCarousel from '../components/ItemsCarousel';
import useUserData from '../utils/useUserData';
import { apiURI } from '../utils/api_path';
import { withRouter } from 'next/router';

export const UserProfile = props => {
  const { storageData } = useUserData();
  const [userItems, setUserItems] = useState([]);
  const [open, setOpen] = useState(false);
  const [activationCode, setActivationCode] = useState();
  const handleClose = () => {
    setOpen(false);
  };
  useEffect(() => {
    setActivationCode(props?.router?.query?.code);
  }, [props]);
  const handleOpen = () => setOpen(true);
  const [selectedItem, setSelectedItem] = useState(null);

  const getUserItems = () => {
    const auth = `Bearer ${storageData?.access_token}`;
    try {
      const requestOptions = {
        method: 'GET',
        mode: 'cors',
        headers: {
          accept: 'application/json',
          Authorization: `${auth}`,
        },
      };

      fetch(`${apiURI}/v1/users/${storageData?.username}/items`, requestOptions)
        .then(response => response.json())
        .then(data => setUserItems(data));
    } catch (error) {
      console.log('error');
    }
  };

  useEffect(() => {
    if (storageData?.username) {
      getUserItems();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [storageData]);

  const renderContent = () => {
    return (
      <>
        {selectedItem ? (
          <ItemCardFull
            nft={selectedItem}
            userAddress={null}
            key={selectedItem.itemId}
            cancelListing={null}
            withdrawItem={null}
            burnItem={null}
            listItem={null}
            confirmReception={null}
            depositItem={null}
            updatePrice={null}
            backClick={() => setSelectedItem(null)}
            refetchItemsList={getUserItems}
          />
        ) : (
          <>
            <UserInfo refetchItemsList={getUserItems} activationCode={activationCode} />
            {userItems?.length > 0 && (
              <ItemsCarousel
                title='My items'
                nfts={userItems}
                nftClick={nft => setSelectedItem(nft)}
              />
            )}
          </>
        )}
      </>
    );
  };
  return (
    <div className='flex justify-center'>
      <div className='px-4' style={{ maxWidth: '1256px', width: '100%', margin: '63px 0' }}>
        {storageData?.access_token ? (
          renderContent()
        ) : (
          <div
            style={{
              display: 'flex',
              flex: '1',
              height: '100%',
              width: '100%',
              justifyContent: 'center',
              alignItems: 'baseline',
              flexWrap: 'wrap',
            }}
          >
            Welcome to ON-Wallet. Please
            <Button onClick={handleOpen}>
              Sign up or Log in <LoginIcon />
            </Button>
          </div>
        )}
      </div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby='modal-modal-title'
        aria-describedby='modal-modal-description'
      >
        <LogIn onClose={handleClose} />
      </Modal>
    </div>
  );
};

export default withRouter(UserProfile);
