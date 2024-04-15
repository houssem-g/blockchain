import { Typography, IconButton } from '@mui/material';
import FavoriteIcon from '@mui/icons-material/Favorite';
import { apiURI } from '../utils/api_path';
import Image from 'next/image';

const ItemCarousel = ({ nft, nftClick }) => {
  return (
    <div
      style={{
        cursor: 'pointer',
        width: '207px',
        marginRight: '16px',
        flexShrink: '0',
        display: 'flex',
        flexDirection: 'column',
        alignSelf: 'flex-start',
      }}
      onClick={() => nftClick(nft)}
    >
      <div
        style={{
          height: '294px',
          backgroundColor: '#ffffff',
          display: 'flex',
          alignItems: 'center',
          position: 'relative',
        }}
      >
        <Image
          src={`${apiURI}/v1/imgs/${nft?.image_hash_key}`}
          alt={nft?.item_class_name}
          layout='fill'
          objectFit='contain'
        />
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <Typography
          sx={{ letterSpacing: '0.25px', opacity: '0.87', margin: '8px', fontWeight: '400' }}
          variant='h6'
          component='h6'
        >
          {nft?.item_class_name}
        </Typography>
        <IconButton size='large' aria-label='more' aria-haspopup='true' color='inherit'>
          <FavoriteIcon />
        </IconButton>
      </div>
      <Typography
        sx={{ letterSpacing: '0.5px', opacity: '0.87', margin: '8px', fontWeight: '800' }}
        variant='h5'
        component='h5'
      >
        {nft?.status === 1 ? nft?.price : ''}
      </Typography>
    </div>
  );
};

export default ItemCarousel;
