import { useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import PersonIcon from '@mui/icons-material/Person';
import SettingsIcon from '@mui/icons-material/Settings';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import Modal from '@mui/material/Modal';
import useUserData from '../utils/useUserData';
import LoginIcon from '@mui/icons-material/Login';
import LogoutIcon from '@mui/icons-material/Logout';
import LogIn from './LogIn';
import Logo from './Logo';

const pages = ['FAQ'];
const userProfile = '/';
const settings = '/settings';
const pagesMap = {
  FAQ: '/faq',
};

const NavBar = ({ logoTitle }) => {
  const { handleLogout, storageData } = useUserData();
  const showAuthItem = storageData?.access_token;

  const [anchorElNav, setAnchorElNav] = useState(null);
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const openPage = page => {
    window.location.href = pagesMap[page];
    setAnchorElNav(null);
  };

  const handleOpenNavMenu = e => {
    setAnchorElNav(e.currentTarget);
    e.preventDefault();
  };

  const onLogout = () => {
    handleLogout();
  };

  return (
    <AppBar
      position='static'
      color='transparent'
      sx={{ height: '63px', boxShadow: 'none', borderBottom: '1px solid rgba(0, 0, 0, 0.12)' }}
    >
      <Container maxWidth='false' sx={{ height: '63px' }}>
        <Toolbar disableGutters>
          <Logo logoTitle={logoTitle} />
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size='large'
              aria-controls='menu-appbar'
              aria-haspopup='true'
              href={settings}
              onClick={e => handleOpenNavMenu(e)}
              color='inherit'
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id='menu-appbar'
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map(page => (
                <MenuItem key={page} onClick={() => openPage(page)}>
                  <Typography textAlign='center'>{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <Typography
            variant='h6'
            noWrap
            component='div'
            sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
          >
            {logoTitle}
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map(page => (
              <Button
                key={page}
                onClick={() => openPage(page)}
                href={pagesMap[page]}
                sx={{
                  my: 2,
                  color: 'black',
                  display: 'block',
                  textTransform: 'capitalize',
                  letterSpacing: '1.25px',
                }}
              >
                {page}
              </Button>
            ))}
          </Box>

          <Box sx={{ flexGrow: 0, display: 'flex', alignItems: 'center' }}>
            <Tooltip title='Settings'>
              <IconButton
                size='large'
                aria-label='settings'
                aria-controls='menu-appbar'
                aria-haspopup='true'
                color='inherit'
                href={settings}
                onClick={() => (window.location.href = settings)}
              >
                <SettingsIcon />
              </IconButton>
            </Tooltip>
            {!showAuthItem && (
              <Tooltip title='Log In'>
                <IconButton
                  size='large'
                  aria-label='login'
                  aria-controls='menu-appbar'
                  aria-haspopup='true'
                  color='inherit'
                  onClick={handleOpen}
                >
                  <LoginIcon />
                </IconButton>
              </Tooltip>
            )}
            {showAuthItem && (
              <Tooltip title='User Profile'>
                <IconButton
                  sx={{ p: 0 }}
                  href={userProfile}
                  onClick={() => (window.location.href = userProfile)}
                >
                  <Avatar alt='avatar'>
                    <PersonIcon />
                  </Avatar>
                </IconButton>
              </Tooltip>
            )}
            {showAuthItem && (
              <Tooltip title='Log Out'>
                <IconButton
                  size='large'
                  aria-label='logout'
                  aria-controls='menu-appbar'
                  aria-haspopup='true'
                  color='inherit'
                  onClick={onLogout}
                >
                  <LogoutIcon />
                </IconButton>
              </Tooltip>
            )}
          </Box>
        </Toolbar>
      </Container>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby='modal-modal-title'
        aria-describedby='modal-modal-description'
      >
        <LogIn onClose={handleClose} />
      </Modal>
    </AppBar>
  );
};
export default NavBar;
