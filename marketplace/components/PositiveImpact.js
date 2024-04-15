import { Card, CardContent, Typography, CardMedia, Link, CardActions } from '@mui/material';
import CommuteIcon from '@mui/icons-material/Commute';
import LocalDrinkIcon from '@mui/icons-material/LocalDrink';
import NatureIcon from '@mui/icons-material/Nature';
import styles from '../styles/Home.module.css';

const PositiveImpact = () => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center' }} className={styles.positiveImpact}>
      <Card
        className={styles.positiveImpactCard}
        sx={{
          backgroundColor: '#F5F5F5',
          border: 'none',
          height: '590px',
          width: '290px',
          borderRadius: '13px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          marginBottom: '15px',
          marginRight: { xs: '0p', md: '10px' },
        }}
        variant='outlined'
      >
        <CardContent>
          <Typography sx={{ marginBottom: '16px' }} variant='h5' component='div'>
            Footprint
          </Typography>
          <Typography
            variant='body2'
            component='div'
            style={{ opacity: '0.87', lineHeight: '22px' }}
          >
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Semper ut quam et faucibus id.
            Sed eget cursus mattis faucibus lacus. Consequat elementum risus.
          </Typography>
          <div style={{ display: 'flex', marginTop: '32px', alignItems: 'center' }}>
            <CommuteIcon sx={{ color: '#FFD740', fontSize: '40px', marginRight: '28px' }} />
            <div>
              <Typography sx={{ fontWeight: '600' }} variant='subtitle1' component='div'>
                12.3
              </Typography>
              <Typography
                variant='body1'
                component='div'
                style={{ opacity: '0.87', lineHeight: '24px', letterSpacing: '0.5' }}
              >
                km of driving emissions avoided
              </Typography>
            </div>
          </div>

          <div style={{ display: 'flex', marginTop: '32px', alignItems: 'center' }}>
            <LocalDrinkIcon sx={{ color: '#40C4FF', fontSize: '40px', marginRight: '28px' }} />
            <div>
              <Typography sx={{ fontWeight: '600' }} variant='subtitle1' component='div'>
                876.0
              </Typography>
              <Typography
                variant='body1'
                component='div'
                style={{ opacity: '0.87', lineHeight: '24px', letterSpacing: '0.5' }}
              >
                days of drinking water saved
              </Typography>
            </div>
          </div>

          <div style={{ display: 'flex', marginTop: '32px', alignItems: 'center' }}>
            <NatureIcon sx={{ color: '#9CCC65', fontSize: '40px', marginRight: '28px' }} />
            <div>
              <Typography sx={{ fontWeight: '600' }} variant='subtitle1' component='div'>
                5.0
              </Typography>
              <Typography
                variant='body1'
                component='div'
                style={{ opacity: '0.87', lineHeight: '24px', letterSpacing: '0.5' }}
              >
                m2 of land saved from pesticides
              </Typography>
            </div>
          </div>
        </CardContent>
        <CardActions sx={{ margin: '0 0 16px 8px' }}>
          <div>
            Powered by{' '}
            <Link href='#' color='inherit'>
              GreenStory
            </Link>
          </div>
        </CardActions>
      </Card>

      <Card
        className={styles.positiveImpactCard}
        sx={{
          backgroundColor: '#F5F5F5',
          border: 'none',
          height: '590px',
          width: '290px',
          borderRadius: '13px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          marginBottom: '15px',
          marginRight: { xs: '0p', md: '10px' },
        }}
        variant='outlined'
      >
        <CardContent>
          <Typography sx={{ marginBottom: '16px' }} variant='h5' component='div'>
            Sustainable
          </Typography>
          <Typography
            variant='body2'
            component='div'
            style={{ opacity: '0.87', lineHeight: '22px' }}
          >
            Want to reduce your carbon footprint when shopping? Here are some quick tips!
          </Typography>
          <div style={{ marginTop: '32px' }}>
            <Typography sx={{ fontWeight: '600' }} variant='subtitle1' component='div'>
              Duty-Free
            </Typography>
            <Typography
              variant='body1'
              component='div'
              style={{ opacity: '0.87', lineHeight: '24px', letterSpacing: '0.5' }}
            >
              This only shows items in your region, so your orders will have shorter distances to
              travel to reach your wardrobe!
            </Typography>
          </div>

          <div style={{ marginTop: '32px' }}>
            <Typography sx={{ fontWeight: '600' }} variant='subtitle1' component='div'>
              Direct Shipping
            </Typography>
            <Typography
              variant='body1'
              component='div'
              style={{ opacity: '0.87', lineHeight: '24px', letterSpacing: '0.5' }}
            >
              Your item will be delivered directly to you (last year our community eliminated over
              300,000 shipments through our hubs)
            </Typography>
          </div>
        </CardContent>
        <CardActions sx={{ margin: '0 0 16px 8px' }}>
          <Link href='#' color='inherit'>
            Learn more
          </Link>
        </CardActions>
      </Card>

      <Card
        className={styles.positiveImpactCard}
        sx={{
          backgroundColor: '#F5F5F5',
          border: 'none',
          height: '590px',
          width: '290px',
          borderRadius: '13px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          marginBottom: '15px',
          marginRight: { xs: '0p', md: '10px' },
        }}
        variant='outlined'
      >
        <CardContent>
          <Typography sx={{ marginBottom: '16px' }} variant='h5' component='div'>
            How it’s made
          </Typography>
          <Typography
            variant='body2'
            component='div'
            style={{ opacity: '0.87', lineHeight: '22px' }}
          >
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Semper ut quam et faucibus id.
            Sed eget cursus mattis faucibus lacus. Consequat elementum.
          </Typography>
          <CardMedia
            component='img'
            style={{ height: '296px', width: 'auto', margin: '16px auto' }}
            image='https://images.unsplash.com/photo-1513828583688-c52646db42da'
            alt='production'
          />
        </CardContent>
        <CardActions sx={{ margin: '0 0 16px 8px' }}>
          <Link href='#' color='inherit'>
            Learn more
          </Link>
        </CardActions>
      </Card>

      <Card
        className={styles.positiveImpactCard}
        sx={{
          backgroundColor: '#F5F5F5',
          border: 'none',
          height: '590px',
          width: '290px',
          borderRadius: '13px',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          marginBottom: '15px',
          marginRight: { xs: '0p', md: '10px' },
        }}
        variant='outlined'
      >
        <CardContent>
          <Typography sx={{ marginBottom: '16px' }} variant='h5' component='div'>
            Where it’s made
          </Typography>
          <Typography
            variant='body2'
            component='div'
            style={{ opacity: '0.87', lineHeight: '22px' }}
          >
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sagittis porta sit et cras
            volutpat. Nunc, orci amet, feugiat quis commodo nibh. Mus gravida cras.
          </Typography>
          <CardMedia
            component='img'
            style={{ height: '296px', width: 'auto', margin: '16px auto' }}
            image='https://images.unsplash.com/photo-1461183479101-6c14cd5299c4'
            alt='map'
          />
        </CardContent>
        <CardActions sx={{ margin: '0 0 16px 8px' }}>
          <Link href='#' color='inherit'>
            Learn more
          </Link>
        </CardActions>
      </Card>
    </div>
  );
};

export default PositiveImpact;
