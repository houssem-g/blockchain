import { Typography } from '@mui/material';
import ItemCarousel from './ItemCarousel';
import styles from '../styles/Home.module.css';

const ItemsCarousel = ({ title, nfts, nftClick }) => {
  return (
    <div style={{ margin: '68px 0 0 24px' }}>
      <Typography
        sx={{ letterSpacing: '0.5px', opacity: '0.87', marginBottom: '36px', fontWeight: '600' }}
        variant='h6'
        component='h6'
      >
        {title} ({nfts?.length})
      </Typography>
      <div
        style={{ display: 'flex', overflowX: { sx: 'none', md: 'auto' } }}
        className={styles.itemsCarousel}
      >
        {nfts?.map((nft, idx) => (
          <ItemCarousel key={idx} nft={nft} nftClick={nftClick} />
        ))}
      </div>
    </div>
  );
};

export default ItemsCarousel;
