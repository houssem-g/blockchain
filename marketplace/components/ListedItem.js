import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  CardActions,
  Button,
  Input,
} from '@mui/material';

const ListedItem = ({ nft, buyNft, cardClick }) => {
  const { image, name, description, price } = nft;

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
          <Typography gutterBottom variant='h5' component='div'>
            {name}
          </Typography>
          <Typography variant='body2' color='text.secondary'>
            {description}
          </Typography>
          <Typography variant='overline' display='block' gutterBottom style={{ color: '#1B5E20' }}>
            {price} USD
          </Typography>
        </CardContent>
      </div>
      <CardActions>
        <Button size='small' onClick={() => buyNft(nft)}>
          Buy
        </Button>
      </CardActions>
    </Card>
  );
};

export default ListedItem;
