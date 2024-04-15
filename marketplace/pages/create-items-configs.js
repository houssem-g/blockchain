import { useState } from 'react';
import * as XLSX from 'xlsx';
import Button from '@mui/material/Button';
import React from 'react';
import OpenInBrowserIcon from '@mui/icons-material/OpenInBrowser';
import useUserData from '../utils/useUserData';
import { apiURI } from '../utils/api_path';

export default function CreateItemConfigs() {
  const { storageData } = useUserData();
  const [columns, setColumns] = useState([]);
  const [data, setData] = useState([]);
  const [file, setFile] = useState({});
  const [allImages, setAllImage] = useState([]);
  const [allImagesNames, setAllImageNames] = useState([]);
  const [listOfh3, setListOfh3] = useState([]);
  const [displayHideButton, setDisplayHideButton] = useState('none');

  const processData = dataString => {
    const dataStringLines = dataString.split(/\r\n|\n/);
    const headers = dataStringLines[0].split(/,(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)/);

    const list = [];
    for (let i = 1; i < dataStringLines.length; i++) {
      const row = dataStringLines[i].split(/,(?![^"]*"(?:(?:[^"]*"){2})*[^"]*$)/);
      if (headers && row.length == headers.length) {
        const obj = {};
        for (let j = 0; j < headers.length; j++) {
          let d = row[j];
          if (d.length > 0) {
            if (d[0] == '"') d = d.substring(1, d.length - 1);
            if (d[d.length - 1] == '"') d = d.substring(d.length - 2, 1);
          }
          if (headers[j]) {
            obj[headers[j]] = d;
          }
        }

        // remove the blank rows
        if (Object.values(obj).filter(x => x).length > 0) {
          list.push(obj);
        }
      }
    }
    setData(list);
    const imagesNames = [];
    for (let obj of list) {
      if (!Object.keys(obj).includes('image')) {
        alert('Please add column image with images names to upload');
        setDisplayHideButton('none');
        setListOfh3([]);
        break;
      } else {
        imagesNames.push(obj['image']);
      }
    }
    setAllImageNames(imagesNames);

    setColumns(columns);
  };

  //   // handle file upload
  const handleFileUpload = e => {
    let fileList = e.target.files;
    const file = fileList[0];
    setFile(file);
    const reader = new FileReader();
    const listOfNewElement = [];
    for (let el of fileList) {
      const element = (
        <div className='textAndIconToUpload'>
          <h1 className='circle'>CSV</h1>
          <h3 className='csvAndImages'>{el['name']}</h3>
        </div>
      );
      listOfNewElement.push(element);
    }
    setListOfh3([...listOfh3, listOfNewElement]);

    // setListOfh3(...listOfh3, listOfNewElement)
    if (fileList.length > 0) setDisplayHideButton('block');

    // setNameFiles(listOfName)
    reader.onload = evt => {
      /* Parse data */
      const bstr = evt.target.result;
      const wb = XLSX.read(bstr, { type: 'binary' });
      /* Get first worksheet */
      const wsname = wb.SheetNames[0];
      const ws = wb.Sheets[wsname];

      /* Convert array of arrays */
      const raw_data = XLSX.utils.sheet_to_csv(ws, { header: 1 });
      processData(raw_data);
    };
    reader.readAsBinaryString(file);
  };

  const handleImageUpload = e => {
    let fileList = e.target.files;
    for (let i = 0; i < fileList.length; i++) {
      let reader = new FileReader();

      reader.onload = function () {
        setAllImage(allImages => [...allImages, fileList[i]]);
      };
      reader.readAsBinaryString(file);
    }
    // const imageFile = fileList[0];

    // const reader = new FileReader();
    let listOfNewElement = [];
    let listImages = [];
    for (let el of fileList) {
      if (!allImagesNames.includes(el['name'])) {
        alert('the image ' + el['name'] + ' has not been added to the csv');
        listOfNewElement = [];
        break;
      }
      const element = (
        <div className='textAndIconToUpload'>
          <h1 className='circle'>IMG</h1>
          <h3 className='csvAndImages'>{el['name']}</h3>
        </div>
      );
      listImages.push(el);

      listOfNewElement.push(element);
    }
    setListOfh3([...listOfh3, listOfNewElement]);

    // reader.readAsBinaryString(imageFile);
  };
  const sendImageUploaded = async () => {
    const formData = new FormData();
    formData.append('item_configs_csv', file);
    for (let i = 0; i < allImages.length; i++) {
      formData.append('images', allImages[i]);
    }
    const auth = `Bearer ${storageData?.access_token}`;
    await fetch(`${apiURI}/v1/items_configs/list`, {
      headers: {
        Accept: 'application/json',
        // 'enctype':"multipart/form-data",
        Authorization: `${auth}`,
      },
      redirect: 'follow',
      method: 'POST',

      mode: 'cors',
      body: formData,
    })
      .then(res => res.json())
      .then(response => {
        if (response['detail'] == undefined) {
          alert('file sent Successfully !');
        } else {
          alert('Seomething went wrong, error :' + response['detail']);
          return response['detail'];
        }
      });
  };
  const resetFiles = () => {
    setListOfh3([]);
    setAllImage([]);
  };
  return (
    <container
      style={{ display: `${storageData?.access_token}` != 'undefined' ? 'block' : 'none' }}
    >
      <div className='totContentUploadFile'>
        <div className='contentUploadFile'>
          <div className='buttonsUpload'>
            <OpenInBrowserIcon className='iconBrowse'></OpenInBrowserIcon>
            <Button variant='contained' component='label' className='upload'>
              Upload CSV
              <input type='file' accept='.csv,.xlsx,.xls' hidden onChange={handleFileUpload} />
            </Button>
            <Button
              variant='contained'
              component='label'
              className='upload'
              sx={{ textAlign: 'center', display: displayHideButton }}
            >
              Upload Image
              <input
                type='file'
                accept='.jpg, .jpeg'
                hidden
                onChange={handleImageUpload}
                multiple
              />
            </Button>
          </div>
          <div className='fileName'>{listOfh3}</div>
        </div>
        <div className='buttonConfirmAndCancel'>
          <Button variant='contained' component='label' color='error' onClick={resetFiles}>
            Cancel
          </Button>
          <Button
            variant='contained'
            component='label'
            color='success'
            sx={{ marginRight: '25px !important' }}
            onClick={sendImageUploaded}
          >
            Confirm
          </Button>
        </div>
      </div>
    </container>
  );
}
