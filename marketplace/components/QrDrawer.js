import * as React from 'react';
import { Global } from '@emotion/react';
import { styled } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { grey } from '@mui/material/colors';
import { Box} from '@mui/material';
import QrScanner from './QrScanner';
import QrCodeScannerIcon from '@mui/icons-material/QrCodeScanner';
import SwipeableDrawer from '@mui/material/SwipeableDrawer';

const drawerBleeding = 96;

const Root = styled('div')(({ theme }) => ({
  height: '100%',
  backgroundColor:
    theme.palette.mode === 'light' ? grey[100] : theme.palette.background.default,
}));

const StyledBox = styled(Box)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'light' ? '#fff' : grey[800],
}));

const Puller = styled(Box)(({ theme }) => ({
  width: 44,
  height: 6,
  backgroundColor: '#BDBDBD',
  borderRadius: 3,
  position: 'absolute',
  bottom: 8,
  left: 'calc(50% - 22px)',
}));

const QrDrawer = (props) => {
  const { window } = props;
  const [open, setOpen] = React.useState(false);

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

  const container = window !== undefined ? () => window().document.body : undefined;

  return (
    <Root>
      <CssBaseline />
      <Global
        styles={{
          '.MuiDrawer-root > .MuiPaper-root': {
            height: `calc(90% - ${drawerBleeding}px)`,
            overflow: 'visible',
          },
        }}
      />
      <SwipeableDrawer
        container={container}
        anchor="top"
        open={open}
        onClose={toggleDrawer(false)}
        onOpen={toggleDrawer(true)}
        swipeAreaWidth={drawerBleeding}
        disableSwipeToOpen={false}
        ModalProps={{
          keepMounted: true,
        }}
      >
        <StyledBox
          sx={{
            position: 'absolute',
            display: { xs: 'flex', sm: 'none' },
            height: 96,
            bottom: -drawerBleeding,
            borderBottomLeftRadius: 13,
            borderBottomRightRadius: 13,
            visibility: 'visible',
            boxShadow: '0 4px 2px -2px rgba(0, 0, 0, 0.12)',
            right: 0,
            left: 0,
          }}
        >
          <QrCodeScannerIcon
            sx={{ fontSize: '50px', margin: 'auto', color: '#BDBDBD', padding: '0 0 5px 0px' }}
          />
          <Puller />
        </StyledBox>
        <StyledBox
          sx={{
            height: '100%',
            overflow: 'auto',
          }}
        >
          <QrScanner open={open} />
        </StyledBox>
      </SwipeableDrawer>
    </Root>
  );
}

export default QrDrawer;
