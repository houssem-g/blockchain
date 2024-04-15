import {
  Box,
  Table,
  TableHead,
  TableCell,
  TableRow,
  TableBody,
  ListItem,
  ListItemText,
  List,
  CardContent,
  Typography,
  CardActions,
  Button,
  Paper,
  Accordion,
  AccordionDetails,
  AccordionSummary,
} from '@mui/material';
import KeyboardBackspaceIcon from '@mui/icons-material/KeyboardBackspace';
import VerifiedUserIcon from '@mui/icons-material/VerifiedUser';
import VerifiedIcon from '@mui/icons-material/Verified';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import DialogModal from './DialogModal';
import PositiveImpact from './PositiveImpact';
import React, { useState } from 'react';
import ButtonDefault from './ButtonDefault';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import Modal from '@mui/material/Modal';
import TransferNFT from './TransferNFT';
import BurnNFT from './BurnNFT';
import styles from '../styles/Home.module.css';
import { apiURI } from '../utils/api_path';
import Image from 'next/image';

const data = [
  {
    name: '1 Jun',
    price: 4000,
    amt: 2400,
  },
  {
    name: '2 Jul',
    price: 3000,
    amt: 2210,
  },
  {
    name: '5 Aug',
    price: 2000,
    amt: 2290,
  },
  {
    name: '27 Aug',
    price: 2780,
    amt: 2000,
  },
  {
    name: '12 Sep',
    price: 1890,
    amt: 2181,
  },
  {
    name: '29 Sep',
    price: 2390,
    amt: 2500,
  },
];

const historyItems = [
  {
    buyer: 'Name Surname',
    price: '12 USD',
    serial: '#1234',
    series: 'Summer 2021',
    date: 'Jan 22, 22 8:11 PM',
  },
  {
    buyer: 'Name1 Surname1',
    price: '12 USD',
    serial: '#1234',
    series: 'Summer 2021',
    date: 'Jan 22, 22 8:11 PM',
  },
  {
    buyer: 'Name2 Surname2',
    price: '12 USD',
    serial: '#1234',
    series: 'Summer 2021',
    date: 'Jan 22, 22 8:11 PM',
  },
];

const ACTIONS = {
  TRANSFER: 'transfer',
  BURN: 'burn',
};

const UNLISTED_STATUS = 'activated';
const LISTED_STATUS = 1;
const PAID_STATUS = 2;
const WITHDRAWN_STATUS = 3;

const ItemCardFull = ({
  nft,
  cancelListing,
  withdrawItem,
  burnItem,
  listItem,
  confirmReception,
  depositItem,
  updatePrice,
  backClick,
  userAddress,
  refetchItemsList,
}) => {
  const {
    brand_name,
    category_name,
    image_hash_key,
    item_class_description,
    item_class_name,
    item_config_description,
    product_number,
    serial_number,
    status,
  } = nft;
  const [openSellDialog, setOpenSellDialog] = useState(false);
  const [open, setOpen] = useState(false);
  const [action, setAction] = useState(null);

  const handleOpen = action => {
    setOpen(true);
    setAction(action);
  };
  const handleClose = (_, reason) => {
    if (reason && reason == 'backdropClick') {
      return;
    }

    setOpen(false);
  };

  const handleCloseAndBack = () => {
    backClick();
  };

  const renderTransferContent = () => {
    return (
      <TransferNFT
        onClose={handleClose}
        onCloseAndBack={handleCloseAndBack}
        serialNumber={serial_number}
        refetchItemsList={refetchItemsList}
      />
    );
  };

  const renderBurnContent = () => {
    return (
      <BurnNFT
        onClose={handleClose}
        serialNumber={serial_number}
        onCloseAndBack={handleCloseAndBack}
        refetchItemsList={refetchItemsList}
      />
    );
  };

  return (
    <>
      <div>
        <Button
          size='small'
          startIcon={<KeyboardBackspaceIcon />}
          style={{ marginBottom: '10px', display: 'flex' }}
          onClick={backClick}
        >
          Back
        </Button>
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
          <Paper
            variant='outlined'
            sx={{ height: '500px', width: '520px', display: 'flex', position: 'relative' }}
            className={styles.itemFullCardImg}
          >
            <Image
              src={`${apiURI}/v1/imgs/${image_hash_key}`}
              alt={name}
              style={{ borderRadius: '4px', maxHeight: '500px', maxWidth: '520px', margin: 'auto' }}
              layout='fill'
              objectFit='contain'
            />
          </Paper>
          <CardContent style={{ marginLeft: '30px' }} className={styles.itemFullCardContent}>
            <Typography sx={{ textTransform: 'capitalize' }} variant='h4' component='h4'>
              {item_class_name}
            </Typography>
            <div style={{ display: 'flex', marginTop: '16px' }}>
              {status === LISTED_STATUS && (
                <div>
                  <Typography
                    sx={{ color: 'rgba(0, 0, 0, 0.6)', marginRight: '30px' }}
                    variant='body2'
                    component='body2'
                  >
                    SOLD BY
                  </Typography>
                  <div style={{ lineHeight: '36px' }}>
                    DimitarI
                    <VerifiedUserIcon
                      sx={{
                        color: '#0077FF',
                        height: '16px',
                        marginLeft: '4px',
                        marginBottom: '4px',
                      }}
                    />
                  </div>
                </div>
              )}
              <div>
                <Typography sx={{ color: 'rgba(0, 0, 0, 0.6)' }} variant='body2' component='body2'>
                  CERTIFIED BY
                </Typography>
                <div style={{ lineHeight: '36px' }}>
                  {brand_name || 'Test Brand'}
                  <VerifiedIcon
                    sx={{
                      color: '#0077FF',
                      height: '16px',
                      marginLeft: '4px',
                      marginBottom: '4px',
                    }}
                  />
                </div>
                <Typography sx={{ color: 'rgba(0, 0, 0, 0.6)' }} variant='body2' component='body2'>
                  SERIAL NUMBER
                </Typography>
                <div style={{ lineHeight: '36px' }}>
                  {serial_number}
                  <VerifiedIcon
                    sx={{
                      color: '#0077FF',
                      height: '16px',
                      marginLeft: '4px',
                      marginBottom: '4px',
                    }}
                  />
                </div>
              </div>
            </div>
            {(status === LISTED_STATUS || status === PAID_STATUS) && (
              <Typography
                variant='overline'
                display='block'
                gutterBottom
                sx={{ fontSize: '34px', letterSpacing: '0.25px', fontWeight: '800' }}
              >
                {price} USD
              </Typography>
            )}
            <CardActions sx={{ flexDirection: 'column' }}>
              {status === LISTED_STATUS && (
                <ButtonDefault
                  title='Cancel Listing'
                  onClick={() => cancelListing(nft)}
                  margin='0px !important'
                />
              )}
              {status === UNLISTED_STATUS && (
                <>
                  <ButtonDefault
                    title='Transfer'
                    onClick={() => handleOpen(ACTIONS.TRANSFER)}
                    margin='0px 0px 14px 0px !important'
                  />
                  <ButtonDefault
                    title='Burn'
                    onClick={() => handleOpen(ACTIONS.BURN)}
                    margin='0px !important'
                    lightMode
                  />
                </>
              )}
              {status === PAID_STATUS && buyer === userAddress && (
                <>
                  <ButtonDefault
                    title='Confirm Reception'
                    onClick={() => confirmReception(nft)}
                    margin='0px 0px 14px 0px !important'
                  />
                  <ButtonDefault
                    title='Report Transaction'
                    onClick={null}
                    margin='0px !important'
                  />
                </>
              )}
              {status === WITHDRAWN_STATUS && (
                <>
                  <ButtonDefault
                    title='Deposit'
                    onClick={() => depositItem(nft)}
                    margin='0px !important'
                  />
                </>
              )}
            </CardActions>
            <div style={{ width: '600px' }} className={styles.accordion}>
              <List>
                {item_config_description?.map(i => (
                  <ListItem
                    key={i?.key}
                    disablePadding
                    divider
                    sx={{ '&:last-child': { borderBottom: 'none' }, padding: '26px 16px' }}
                  >
                    <ListItemText
                      disableTypography
                      primary={
                        <Typography variant='h6' component='h6'>
                          {i?.key}
                        </Typography>
                      }
                    />
                    <div style={{ fontSize: '18px', paddingRight: '10px' }}>{i?.value}</div>
                  </ListItem>
                ))}
              </List>
            </div>
          </CardContent>
        </div>
        <Accordion sx={{ boxShadow: 'none', '&:before': { height: '0' } }} defaultExpanded>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls='panel3a-content'
            id='panel3a-header'
          >
            <Typography variant='h6' component='h6'>
              Description
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant='body1' component='body1'>
              {item_class_description}
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion sx={{ boxShadow: 'none', '&:before': { height: '0' } }} defaultExpanded>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls='panel3a-content'
            id='panel3a-header'
          >
            <Typography variant='h6' component='h6'>
              Price History
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <div style={{ height: '300px' }}>
              <ResponsiveContainer width='100%' height='100%'>
                <LineChart
                  width={500}
                  height={300}
                  data={data}
                  margin={{
                    top: 50,
                    right: 30,
                    left: 10,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray='3 3' />
                  <XAxis dataKey='name' />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type='monotone' dataKey='price' stroke='#82ca9d' />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </AccordionDetails>
        </Accordion>
        <Accordion sx={{ boxShadow: 'none', '&:before': { height: '0' } }} defaultExpanded>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls='panel3a-content'
            id='panel3a-header'
          >
            <Typography variant='h6' component='h6'>
              Travel History of Item
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant='body1' component='body1'>
              Track the journey of your item
            </Typography>
            <Box sx={{ overflowX: 'auto' }}>
              <Table aria-label='caption table'>
                <TableHead>
                  <TableRow>
                    <TableCell>Buyer</TableCell>
                    <TableCell>Sales price</TableCell>
                    <TableCell>Serial</TableCell>
                    <TableCell>Series</TableCell>
                    <TableCell>Date / Time</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {historyItems.map(row => (
                    <TableRow key={row.buyer}>
                      <TableCell>{row.buyer}</TableCell>
                      <TableCell>{row.price}</TableCell>
                      <TableCell>{row.serial}</TableCell>
                      <TableCell>{row.series}</TableCell>
                      <TableCell>{row.date}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </AccordionDetails>
        </Accordion>
        <Accordion sx={{ boxShadow: 'none', '&:before': { height: '0' } }} defaultExpanded>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls='panel3a-content'
            id='panel3a-header'
          >
            <Typography variant='h6' component='h6'>
              Positive Impact
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <PositiveImpact />
          </AccordionDetails>
        </Accordion>
        <DialogModal
          handleUpdatePrice={price => {
            updatePrice(itemId, price);
            listItem(nft);
          }}
          handleClose={() => setOpenSellDialog(false)}
          open={openSellDialog}
        />
      </div>
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby='modal-title'
        aria-describedby='modal-description'
      >
        <>
          {action === ACTIONS.TRANSFER && renderTransferContent()}
          {action === ACTIONS.BURN && renderBurnContent()}
        </>
      </Modal>
    </>
  );
};

export default ItemCardFull;
