import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  CardActions,
  Button,
} from '@mui/material';

const UNLISTED_STATUS = 0;
const LISTED_STATUS = 1;
const PAID_STATUS = 2;
const WITHDRAWN_STATUS = 3;

const statusList = {
  [UNLISTED_STATUS]: 'Not listed',
  [LISTED_STATUS]: 'Listed',
  [PAID_STATUS]: 'Paid',
  [WITHDRAWN_STATUS]: 'Withdrawn',
};

const ItemCard = ({
  nft,
  cancelListing,
  withdrawItem,
  burnItem,
  handleSellClick,
  confirmReception,
  depositItem,
  cardClick,
  userAddress,
}) => {
  const { image, name, status, description, price, buyer, brand } = nft;

  return (
    <Card
      sx={{ maxWidth: 345, minWidth: 320 }}
      style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}
    >
      <div onClick={() => cardClick(nft)} style={{ cursor: 'pointer' }}>
        <CardMedia
          component='img'
          style={{ height: '250px', width: 'auto', margin: 'auto' }}
          image={image}
          alt={name}
        />
        <CardContent>
          <Typography variant='overline' display='block' gutterBottom>
            {statusList[status]}
          </Typography>
          <Typography gutterBottom variant='h5' component='div'>
            {name}
          </Typography>
          <Typography variant='body2' color='text.secondary'>
            {description}
          </Typography>
          <Typography variant='body2' color='text.secondary'>
            {brand?.toString()}
          </Typography>
          {(status === LISTED_STATUS || status === PAID_STATUS) && (
            <Typography
              variant='overline'
              display='block'
              gutterBottom
              style={{ color: '#1B5E20' }}
            >
              {price} USD
            </Typography>
          )}
        </CardContent>
      </div>
      <CardActions>
        {status === LISTED_STATUS && (
          <Button size='small' onClick={() => cancelListing(nft)}>
            Cancel Listing
          </Button>
        )}
        {status === UNLISTED_STATUS && (
          <>
            <Button size='small' onClick={() => withdrawItem(nft)}>
              Withdraw
            </Button>
            <Button size='small' onClick={() => burnItem(nft)}>
              Burn
            </Button>
            <Button size='small' onClick={handleSellClick}>
              Sell
            </Button>
          </>
        )}
        {status === PAID_STATUS && buyer === userAddress && (
          <>
            <Button size='small' onClick={() => confirmReception(nft)}>
              Confirm Reception
            </Button>
            <Button size='small'>Report Transaction</Button>
          </>
        )}
        {status === WITHDRAWN_STATUS && (
          <>
            <Button size='small' onClick={() => depositItem(nft)}>
              Deposit
            </Button>
          </>
        )}
      </CardActions>
    </Card>
  );
};

export default ItemCard;
