import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Input } from '@mui/material';

import React, { useState } from 'react';

const DialogModal = ({ handleUpdatePrice, handleClose, open }) => {
  const [price, setPrice] = useState(null);
  const handleSave = () => {
    handleUpdatePrice(price);
    setPrice(null);
    handleClose();
  };

  return (
    <Dialog
      open={open}
      onClose={handleClose}
      aria-labelledby='alert-dialog-title'
      aria-describedby='alert-dialog-description'
    >
      <DialogTitle id='alert-dialog-title' sx={{ width: '300px' }}>
        Selling price
      </DialogTitle>
      <DialogContent>
        <Input
          placeholder='Selling price'
          onChange={e => setPrice(e.target.value)}
          variant='outlined'
          style={{ width: '100%' }}
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Cancel</Button>
        <Button onClick={handleSave} autoFocus>
          Sell
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DialogModal;
