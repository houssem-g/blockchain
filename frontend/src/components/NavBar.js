import { useEffect, useState } from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import SettingsIcon from '@mui/icons-material/Settings';
import { styled } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import Avatar from '@mui/material/Avatar';
import InputBase from '@mui/material/InputBase';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import Modal from '@mui/material/Modal';
import useUserData from './utils/useUserData';
import LoginIcon from '@mui/icons-material/Login';
import LogoutIcon from '@mui/icons-material/Logout';
import LogIn from './LogIn';
import Logo from './Logo';
import {styleFormSignInDesktop} from "../styles/form_sign_in/desktop";

const pagesBrandAdmin = ['Create Items', 'Brand Dashboard'];
const pagesSimpleUser = ['Listed Items', 'My Profile'];
const userProfile = '/user-profile';
const settings = '/settings';
const pagesMap = {
  'Listed Items': '/',
  'Create Items': '/create-item',
  'Create Items Configs': '/create-items-configs',
  'My Profile': '/my-profile',
  'Brand Dashboard': '/brand-dashboard',
};

const Search = styled('div')(({ theme }) => ({
  position: 'relative',
  borderRadius: '20px',
  backgroundColor: '#F5F5F5',
  '&:hover': {
    opacity: '0.8',
  },
  marginLeft: 0,
  height: '40px',
  width: '295px !important',
  [theme.breakpoints.up('sm')]: {
    marginLeft: theme.spacing(3),
    width: 'auto',
  },
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
  color: 'inherit',
  '& .MuiInputBase-input': {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `12px`,
    transition: theme.transitions.create('width'),
    width: '100%',
    [theme.breakpoints.up('md')]: {
      width: '20ch',
    },
  },
}));

const NavBar = ({logoTitle}) => {
  const { handleLogout, getJWToken } = useUserData();
  const [userLoggedIn, setUserLoggedIn] = useState();
  const [userData, setUserData] = useState();
  const showAuthItem = getJWToken() || userLoggedIn;

  const updateToken = () => {
    setUserLoggedIn(typeof window !== 'undefined' ? getJWToken() : null);
  }
  const [anchorElNav, setAnchorElNav] = useState(null);
  const [open, setOpen] = useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => {
    setOpen(false);
    updateToken();
  };
  useEffect(() => {
    if (typeof window !== 'undefined') {
      setUserData(JSON.parse(localStorage?.getItem("@USER_DETAILS")));
      window.dispatchEvent(new Event("storage"));
    }
  }, []);

  const isBrandAdmin = userData?.user_type === "simple_user" ? false : true;
  console.log(userData?.user_type);
  const pages = isBrandAdmin ? pagesBrandAdmin : pagesSimpleUser;

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const openPage = page => {
    window.location.href = pagesMap[page];
    setAnchorElNav(null);
  };

  const handleOpenNavMenu = (e) => {
    setAnchorElNav(e.currentTarget);
    e.preventDefault();
  };

  const onLogout = () => {
    handleLogout();
    updateToken();
  };

  return (
    <AppBar position="static" color="transparent" sx={{boxShadow: 'none', borderBottom: '1px solid rgba(0, 0, 0, 0.12)'}}>
      <Container maxWidth="false">
        <Toolbar disableGutters>
          <Logo logoTitle={logoTitle} />
          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              href={settings}
              onClick={e => handleOpenNavMenu(e)}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
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
              {pages.map((page) => (
                <MenuItem key={page} onClick={() => openPage(page)}>
                  <Typography textAlign="center">{page}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
          >
            {logoTitle}
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={() => openPage(page)}
                href={pagesMap[page]}
                sx={{ my: 2, color: 'black', display: 'block', textTransform: 'capitalize', letterSpacing: '1.25px' }}
              >
                {page}
              </Button>
            ))}
          </Box>

          <Box sx={{ flexGrow: 0, display: 'flex', alignItems: 'center' }}>
            <Search sx={{ display: { xs: 'none', md: 'block'  } }}>
              <StyledInputBase
                placeholder="Search"
                inputProps={{ 'aria-label': 'search' }}
              />
            </Search>
            <Tooltip title="Settings">
              <IconButton
                size="large"
                aria-label="settings"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                color="inherit"
                href={settings}
                onClick={() => window.location.href = settings}
              >
                <SettingsIcon />
              </IconButton>
            </Tooltip>
            {!showAuthItem && (
              <Tooltip title="Log In">
                <IconButton
                  size="large"
                  aria-label="login"
                  aria-controls="menu-appbar"
                  aria-haspopup="true"
                  color="inherit"
                  onClick={handleOpen}
                >
                  <LoginIcon />
                </IconButton>
              </Tooltip>
            )}
            {showAuthItem && (
            <Tooltip title="User Profile">
              <IconButton
                sx={{ p: 0 }} 
                href={userProfile}
                onClick={() => window.location.href = userProfile}
              >
                <Avatar alt="John Smith" src="https://images.unsplash.com/photo-1570295999919-56ceb5ecca61" />
              </IconButton>
            </Tooltip>
            )}
            {showAuthItem && (
              <Tooltip title="Log Out">
                <IconButton
                  size="large"
                  aria-label="logout"
                  aria-controls="menu-appbar"
                  aria-haspopup="true"
                  color="inherit"
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
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <LogIn
          onClose={handleClose}
          onSuccess={() => setUserLoggedIn(true)}
          styleModule={styleFormSignInDesktop}
        />
      </Modal>
    </AppBar>
  );
};
export default NavBar;
